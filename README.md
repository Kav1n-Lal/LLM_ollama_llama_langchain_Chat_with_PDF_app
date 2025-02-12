# LLM_ollama_llama_langchain_Chat_with_PDF_app
## LLM Used-🦙 llama3.2:1b 🤖

## Overview
The **Chat_with_PDF_app** is a chat app powered by a fine-tuned large language model (LLM) known as *Llama3.2:1b* pulled from *OLLAMA*. This app takes a pdf file from the user and the user can CHAT to obtain information from the PDF file. Chat history feature is also provided.

## Process Flowchart
- The uploaded pdf is split into chunks , converted to embeddings using the *nomic-embed-text* embedding pulled from OLLAMA and stored to the **FAISS DB**(Vector database) for semantic search.
![data_ingestion](https://github.com/user-attachments/assets/45f4d42b-74ae-4ee1-847d-eeb07fbb5fac)
- **RAG-Retrieval Augmented Generation**: The question or topic from the user is converted into embeddings, fed to the vectorstore for semantic search, after that relevant chunks of documents are retrieved and fed to the LLM along with the user question generate response.
![retrieval_and_generation](https://github.com/user-attachments/assets/783ce298-1f05-4126-b91d-417931dbda10)

## 🚀 Features

- **Response Generation:** Runs locally and allows users to generate RESPONSE based on PDF data with user query.
- **Chat History:** The app generates current response based on the previous response and user query.
- **Clear conversation history:** To clear previous conversations and start a new chat.

## Development Specs
- Utilizes [llama3.2:1b](https://ollama.com/library/llama3.2:1b) and [embeddings](https://ollama.com/library/nomic-embed-text) for robust functionality.
- Developed using [Langchain](https://github.com/langchain-ai/langchain) and [Streamlit](https://github.com/streamlit/streamlit) technologies for enhanced performance.


## 🛠️ Installation
1. **Clone This Repository:**
 ```bash
   git clone [https://github.com/Kav1n-Lal/LLM_ollama_llama_langchain_Chat_with_PDF_app.git]
   ```
2. **Create a conda environment and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Download the Ollama and llama3.2:1b Model:

- Download Ollama for Windows and install it-[https://ollama.com/download]
- **On the command prompt type**:
- **ollama** to see whether it is running.
- Then type **ollama serve**, to view the localhost id.
- Now type **ollama run llama3.2:1b** to pull the LLM. You can use it like **chatGPT** on the terminal itself. To quit type **/bye**.
- Then type **ollama pull nomic-embed-text** to pull the embeddings respectively.
- **ollama list** to check whether the LLM and the embedding is pulled successfully. It displays the information.

## 📝 Usage

1. **Run the Application:**
   ```bash
   streamlit run final_pdf_chat_app.py
   ```
2. **Access the Application:**
   - Once the application is running, access it through the provided URL.
     
## System Requirements
- **CPU:** Intel® Core™ i5 or equivalent.
- **RAM:** 8 GB.
- **Disk Space:** 7 GB.
- **Hardware:** Operates on CPU; no GPU required.

## 🤖 How to Use
- Copy the cloned repository path and on lines 31 and 83 in final_pdf_chat_app.py enter the **file paths of the cloned folder and the vectorstore**  before running the code.
- Upon running the application, you'll be presented with a box to upload your pdf file, upload the file and after successfull storing of the text into the vector database, enter the relevant query to generate response from the pdf file.
- Make sure your queries are structured well with reference to the information contained in the uploaded PDF file.

## 📷 Screenshots
