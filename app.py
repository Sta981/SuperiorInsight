from flask import Flask, render_template, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

print("Loading Superior AI Brain with Custom Memory Engine...")

# 1. Load Embeddings and Database
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vector_db.as_retriever(search_kwargs={"k": 10})

# 2. Setup LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

# 3. Setup the Strict QA Prompt (Formatting fixed!)
system_prompt = (
    "You are 'Superior Insight', the official AI Oracle for Superior University. "
    "Your ONLY purpose is to assist students with information related to Superior University based strictly on the provided Context. "
    "\n\nSTRICT RULES YOU MUST FOLLOW:\n"
    "1. BOUNDARY CONTROL: Never answer out-of-domain questions. Politely refuse and say your knowledge is limited to Superior University.\n"
    "2. NO HALLUCINATION: Only use the retrieved context below. Do not guess.\n"
    "3. LANGUAGE STYLE: Reply in natural Pakistani Roman Urdu. STRICTLY AVOID formal Hindi words like 'khed', 'suvidhayein', 'yadi'. Use words like 'maazrat', 'facilities', 'agar' instead.\n"
    "4. NO WEIRD PREFIXES: Do not start your answer with labels like 'Roman Urdu:' or talk to yourself. Answer the user directly and professionally.\n"
    "\n\nContext:\n{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

print("System Ready!")

# Global Custom Memory
chat_history = []

@app.route("/")
def home():
    global chat_history
    chat_history = []  # Reset memory on refresh
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    global chat_history
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"answer": "Please ask a question.", "sources": []})
    
    try:
        # STEP 1: Format History for the AI to read
        history_text = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}" for msg in chat_history])
        
        # STEP 2: The Custom Search Formulator
        reformulate_prompt = f"""You are an expert database search query generator.
        Here is the recent chat history:
        {history_text}
        
        Latest User Question: {user_input}
        
        Task: 
        1. If the latest question uses pronouns like 'usk', 'uski', 'isko', 'isk' (its, it), figure out which specific program/topic the user is referring to from the chat history (e.g. BS Artificial Intelligence) and replace the pronoun with the actual name.
        2. Translate the final standalone question into pure English optimized for a vector database search.
        3. If the topic is entirely NEW, ignore the history and just translate the new question.
        
        CRITICAL RULE: OUTPUT NOTHING BUT THE RAW SEARCH QUERY STRING. NO INTRODUCTORY TEXT. NO QUOTES. NO CHIT-CHAT.
        """
        
        # Call LLM to get the perfectly translated and context-aware search query
        standalone_query = llm.invoke(reformulate_prompt).content.strip()
        
        print(f"\n[DEBUG] Original User Input: {user_input}")
        print(f"[DEBUG] FAISS Search Query:  {standalone_query}")
        
        # STEP 3: Fetch exact documents using the pure query
        docs = retriever.invoke(standalone_query)
        
        # STEP 4: Generate the final answer using the exact chunks
        response_text = question_answer_chain.invoke({
            "input": user_input, 
            "context": docs
        })
        
        # Save to memory (keep last 4 interactions to save tokens)
        chat_history.append({"user": user_input, "ai": response_text})
        if len(chat_history) > 4:
            chat_history = chat_history[-4:]
            
        sources = list(set([doc.metadata.get('source', 'Official Superior Document') for doc in docs]))
        
        return jsonify({
            "answer": response_text,
            "sources": sources
        })
        
    except Exception as e:
        print(f"Server Error: {e}") 
        return jsonify({
            "answer": "My AI brain is experiencing high traffic. Please wait 15 seconds and ask again!", 
            "sources": []
        })

if __name__ == "__main__":
    app.run(debug=True, port=5000)