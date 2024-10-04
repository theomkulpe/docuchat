# IMPORTING LIBRARIES

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
from uuid import uuid4
from groq import Groq


# DEFINING FUNCTIONS

def extract_pdf_text(pdf_path):
    '''You need to pass the path to the PDF (as a string) as the parameter.'''
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs

def extract_webpage_text(webpage_url):
    '''You need to pass the URL of the webpage (as a string) as the parameter.'''
    loader = WebBaseLoader(webpage_url)
    docs = loader.load()
    return docs

def split_text(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 150)
    splitted_docs = text_splitter.split_documents(docs)
    return splitted_docs

def create_vector_store():
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    index = faiss.IndexFlatL2(384)
    vector_store = FAISS(
        embedding_function=embeddings_model,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    return vector_store

def add_documents_to_vector_store(vector_store, docs):
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents = docs, ids = uuids)

def chat(vector_store, query):
    results = vector_store.similarity_search(
        query,
        k=5,
    )
    context = ""
    for res in results:
        context = context + res.page_content
    client = Groq(
        api_key="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",
    )
    LLM_prompt = context + "\n\nBased on the above context, generate a response to the following:\n" + query
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": LLM_prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    response = chat_completion.choices[0].message.content

    return response