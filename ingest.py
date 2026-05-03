import json
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def run_ingestion():
    # 1. Load the Scraped JSON Data
    with open('superior.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    

    json_docs = []
    for program in json_data:
        # 1. Smart Title Extraction (Fixes the "Unknown Program" bug)
        actual_title = program.get('headings', [program['title']])[0]
        
        content = f"Program Name: {actual_title}\n"
        
        # 2. Smart Labeling for the raw numbers
        paras = program.get('paragraphs', [])
        if len(paras) >= 4:
            content += f"Total Credit Hours: {paras[0]}\n"
            content += f"Total Duration: {paras[1]}\n"
            content += f"Total Semesters: {paras[2]}\n"
            content += f"Study Mode: {paras[3]}\n"
            content += f"Details: {' '.join(paras[4:])}\n"
        else:
            content += f"Details: {' '.join(paras)}\n"
        
        # 3. Add tables (Course Roadmaps)
        for table in program.get('tables', []):
            content += f"\nCourses: {str(table)}"
            
        json_docs.append(Document(page_content=content, metadata={"source": program['url']}))
    # 2. Load the PDFs from the /data folder
    pdf_loader = DirectoryLoader('./data/', glob="./*.pdf", loader_cls=PyPDFLoader)
    pdf_docs = pdf_loader.load()
    pdf_docs = [doc for doc in pdf_docs if len(doc.page_content.strip()) > 200]
    # 3. Combine and Split into Chunks
    all_docs = json_docs + pdf_docs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    final_chunks = text_splitter.split_documents(all_docs)

    # 4. Create Vector Embeddings (The Brain)
    print("Creating Vector Database... this might take a minute.")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Store locally in a folder called 'faiss_index'
    vector_db = FAISS.from_documents(final_chunks, embeddings)
    vector_db.save_local("faiss_index")
    print("Success! The AI 'Brain' is now saved in the 'faiss_index' folder.")

if __name__ == "__main__":
    run_ingestion()