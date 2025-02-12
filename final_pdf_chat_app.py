import streamlit as st
import os

from langchain_text_splitters import  RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS 
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore

from langchain_ollama import ChatOllama 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader


# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chat with your file App")

def load_pdf_and_create_vector_store(pdf_file):
    
    #Reading the uoloaded pdf file
    with open(f"{pdf_file.name}", "wb") as f:
        f.write(pdf_file.getbuffer())
    
        
    pdfs = []
    for root, dirs, files in os.walk(r"C:\Users\Kavin\Desktop\final_MCQ"):# On the desktop, create a folder named 'final_MCQ' place the "final_pdf_chat_app.py"
        # print(root, dirs, files)                                          inside it and  and specify its path
        for file in files:
            if file.endswith(".pdf"):
                pdfs.append(os.path.join(root, file))

    
    #Extracting the text from the pdf file 
    docs = []
    for pdf in pdfs:
        loader = PyMuPDFLoader(pdf)
        temp = loader.load()
        docs.extend(temp)

    #Splitting the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    # Using the "nomic-embed-text" from Ollama to create embeddings
    embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url='http://localhost:11434')


    vector = embeddings.embed_query("Hello World")
    
    index = faiss.IndexFlatL2(len(vector))
    
    vector_store = FAISS(
    embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},)

    # Adding the document chunks to the vector store
    ids=vector_store.add_documents(chunks)
    
    # vectorestore folder path
    DB_FAISS_PATH = "vectorstore/faiss_pdf_text_db"
    vector_store.save_local(DB_FAISS_PATH)
    st.success('documents added to vector store')

    st.session_state['vector_store'] = vector_store  # Store the vector store in session state



with st.sidebar:
    st.title('🦙💬 Llama 2 Chat with your file App')

    pdf_file = st.file_uploader("Upload a PDF", type="pdf")

    if pdf_file:
        # If a PDF is uploaded, process it and create the vector store
        load_pdf_and_create_vector_store(pdf_file)

    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Make sure your answer is relevant to the question and it is answered from the context only.
    
    Context: {context} 
    prompt_input: {prompt_input} 
    Answer:
"""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
    
    prompt = ChatPromptTemplate.from_template(string_dialogue)

    llm = ChatOllama(model='llama3.2:1b', base_url='http://localhost:11434')

    #Loading the saved embeddings from the vectorstore
    embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url='http://localhost:11434')
    db_name = r"C:\Users\Kavin\Desktop\final_MCQ\vectorstore\faiss_pdf_text_db"                # Specify the path of the vectorstore db
    vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)

    #Retrieving the relevant documents from the vector database based on user question
    retriever = vector_store.as_retriever(search_type = 'mmr', # maximum marginal relevance
                                            search_kwargs = {'k': 5, # no of documents to be returned
                                                            'fetch_k': 20, #no of documents to be used for the mmr algorithm to find the relevant documents 
                                                            'lambda_mult': 1}) #0-max diversity,1-minimum diversity(factual)
    #print(retriever)
    docs = retriever.invoke(prompt_input)
    #print(docs)
    
    def format_docs(docs):
        return '\n\n'.join([doc.page_content for doc in docs])

    context = format_docs(docs)
    #print(context)

    rag_chain = (
        {"context": retriever|format_docs, "prompt_input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser())

    response = rag_chain.invoke(prompt_input)
    #st.write(response)
    return response


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)