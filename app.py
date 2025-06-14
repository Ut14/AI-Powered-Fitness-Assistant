import os
import json
import uuid
from datetime import datetime
from typing import List
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv()

PROFILE_PATH = "user_profile.json"
ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def initialize_profile():
    if not os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "w") as f:
            json.dump({"age": None, "height": None, "weight": None, "goal": None}, f, indent=4)


def update_user_profile(profile_data):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile_data, f, indent=4)


def load_user_profile():
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)


initialize_profile()

import cassio
from langchain_community.vectorstores.cassandra import Cassandra
from langchain_huggingface import HuggingFaceEmbeddings

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

astra_vector_store = Cassandra(
    embedding=embedding_model,
    table_name="fitness_notes",
    session=None,
    keyspace=None
)

retriever = astra_vector_store.as_retriever()

from langchain.schema import Document

def add_note_to_vectorstore(note: str):
    profile = load_user_profile()
    note_id = str(uuid.uuid4())
    profile["timestamp"] = str(datetime.now())
    profile["note_id"] = note_id
    doc = Document(page_content=note, metadata=profile)
    astra_vector_store.add_documents([doc])
    return "Note added."


def fetch_notes(query: str):
    documents = retriever.invoke(query)
    return [doc.page_content for doc in documents]


def get_all_notes():
    results = astra_vector_store.similarity_search("", k=100)
    return [(doc.page_content, doc.metadata.get("timestamp", ""), doc.metadata.get("note_id", "")) for doc in results]


def get_notes_display_list():
    all_notes = get_all_notes()
    display = [f"{i+1}. {n[0][:80]}... (added on {n[1]})" for i, n in enumerate(all_notes)]
    note_ids = [n[2] for n in all_notes]
    return display, note_ids


def delete_selected_notes(selected_notes_display):
    if not selected_notes_display:
        return "No notes selected."

    display_list, note_ids = get_notes_display_list()
    to_delete_indices = [display_list.index(sn) for sn in selected_notes_display]
    ids_to_delete = [note_ids[i] for i in to_delete_indices]
    astra_vector_store.delete(ids_to_delete)
    return f"Deleted {len(ids_to_delete)} note(s)."


from langchain_community.utilities import SerpAPIWrapper
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")

router_prompt = PromptTemplate.from_template("""
You are an expert decision maker.

You are given:
- The user's profile
- Their personal fitness notes
- Their current question

Decide whether you have enough information to answer **without web search**.

If insufficient, say: **"USE_WEB"**, else say: **"NO_WEB"**

{context}
""")

def should_use_web(context: str) -> bool:
    router_decision = llm.invoke(router_prompt.format(context=context)).content.strip()
    return router_decision == "USE_WEB"


from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
    question: str
    profile: dict
    notes: List[str]
    web_result: str
    final_answer: str


def create_context(state):
    profile = state["profile"]
    notes = state["notes"]
    profile_str = "\n".join([f"{k}: {v}" for k, v in profile.items()])
    notes_str = "\n".join(notes) or "None"
    return f"User Profile:\n{profile_str}\n\nNotes:\n{notes_str}\n\nQuestion:\n{state['question']}"


def load_context(state):
    return {
        "question": state["question"],
        "profile": load_user_profile(),
        "notes": fetch_notes(state["question"])
    }


def route_to_web(state):
    context = create_context(state)
    return "web_search" if should_use_web(context) else "no_web"


def perform_web_search(state):
    return {"web_result": search.results(state["question"])}


def generate_answer(state):
    profile_str = "\n".join([f"{k}: {v}" for k, v in state["profile"].items()])
    notes_str = "\n".join(state["notes"])
    web_result = state.get("web_result", "")
    prompt = f"""
You are a helpful fitness coach. Answer the user query in under 120 words.

Profile:
{profile_str}

Notes:
{notes_str}

Web Info:
{web_result}

Question:
{state['question']}
"""
    response = llm.invoke(prompt)
    return {"final_answer": response.content.strip()}


workflow = StateGraph(GraphState)
workflow.add_node("load_context", load_context)
workflow.add_node("web_search", perform_web_search)
workflow.add_node("generate_answer", generate_answer)

workflow.set_entry_point("load_context")
workflow.add_conditional_edges("load_context", route_to_web, {
    "web_search": "web_search",
    "no_web": "generate_answer"
})
workflow.add_edge("web_search", "generate_answer")
workflow.add_edge("generate_answer", END)

fitness_app = workflow.compile()


import gradio as gr

def update_profile_ui(age, height, weight, goal):
    update_user_profile({"age": age, "height": height, "weight": weight, "goal": goal})
    return "Profile updated."


def submit_question(user_question):
    state = {"question": user_question}
    for step in fitness_app.stream(state):
        if "generate_answer" in step:
            return step["generate_answer"]["final_answer"]
    return "Unable to generate answer."


def refresh_notes():
    choices, _ = get_notes_display_list()
    return gr.update(choices=choices)


with gr.Blocks() as demo:
    gr.Markdown("## Fitness Assistant")

    with gr.Tab("Profile Setup"):
        age = gr.Number(label="Age")
        height = gr.Number(label="Height (cm)")
        weight = gr.Number(label="Weight (kg)")
        goal = gr.Textbox(label="Fitness Goal")
        profile_btn = gr.Button("Update Profile")
        profile_output = gr.Textbox(label="Status")
        profile_btn.click(update_profile_ui, inputs=[age, height, weight, goal], outputs=profile_output)

    with gr.Tab("Add Notes"):
        note_input = gr.Textbox(label="Note")
        note_btn = gr.Button("Submit Note")
        note_output = gr.Textbox(label="Status")
        note_btn.click(add_note_to_vectorstore, inputs=note_input, outputs=note_output)

    with gr.Tab("Ask Questions"):
        question = gr.Textbox(label="Ask a fitness question")
        answer = gr.Textbox(label="Answer")
        question_btn = gr.Button("Submit")
        question_btn.click(submit_question, inputs=question, outputs=answer)

    with gr.Tab("View & Delete Notes"):
        notes_list = gr.CheckboxGroup(choices=[], label="Select Notes to Delete")
        refresh_btn = gr.Button("Refresh Notes")
        delete_btn = gr.Button("Delete Selected Notes")
        delete_output = gr.Textbox(label="Status")
        refresh_btn.click(fn=refresh_notes, outputs=[notes_list])
        delete_btn.click(fn=delete_selected_notes, inputs=[notes_list], outputs=[delete_output])

demo.launch(debug=True)
