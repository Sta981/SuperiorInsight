from flask import Flask, render_template, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print("Loading Superior AI Brain...")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vector_db.as_retriever(search_kwargs={"k": 4})

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

system_prompt = (
    "You are 'Superior Insight', the official AI Oracle for Superior University. "
    "Use the following pieces of retrieved context to answer the student's question accurately. "
    "Always reply in professional English, regardless of the language the user types in. "
    "If you don't know the answer based on the context, say that you don't know and advise them to contact the Student Office. "
    "Do not hallucinate external information."
    "\n\nContext:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
print("System Ready!")

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"answer": "Please ask a question.", "sources": []})
    
    try:
        response = rag_chain.invoke({"input": user_input})
        
        sources = list(set([doc.metadata.get('source', 'Official Superior Document') for doc in response['context']]))
        
        return jsonify({
            "answer": response["answer"],
            "sources": sources
        })
    except Exception as e:
        print(f"Server Error: {e}") 
        return jsonify({
            "answer": "My AI brain is experiencing high traffic or a slight network delay. Please wait 15 seconds and ask again!", 
            "sources": []
        })

if __name__ == "__main__":
    app.run(debug=True, port=5000)