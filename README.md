# 📚 RAG Document Chatbot

A beginner-friendly **Retrieval-Augmented Generation (RAG)** project that allows users to upload a PDF document and ask questions about its content.

The chatbot first searches the uploaded document for relevant information and then gives that information to an LLM (Gemini) to generate a natural-language answer.

This project is designed to help beginners understand how a RAG system works internally instead of using a single high-level RAG library.

---

# 🤖 What is RAG?

RAG stands for:

**R**etrieval  
**A**ugmented  
**G**eneration

RAG is a technique that allows an AI model to answer questions using information from external documents.

For example, suppose we have a PDF containing a college student handbook.

The PDF says:

> The college library is open from 8:00 AM to 8:00 PM from Monday to Saturday.

The user asks:

> What time does the library close?

Instead of asking the LLM to answer only from its existing knowledge, the RAG system first searches the PDF and finds the relevant information.

Then it gives that information to the LLM.

The LLM generates:

> The college library closes at 8:00 PM.

---

# 🎯 Project Goal

The main goal of this project is to understand how a basic RAG pipeline works.

The project demonstrates:

- PDF text extraction
- Text chunking
- Text embeddings
- Vector storage
- Similarity search
- Retrieval of relevant information
- Sending retrieved information to an LLM
- Generating an answer
- Building a simple chatbot UI

---

# 🔄 RAG Pipeline

The complete pipeline is:

```text
                 PDF DOCUMENT
                      │
                      ↓
              TEXT EXTRACTION
                      │
                      ↓
                 CHUNKING
                      │
                      ↓
                EMBEDDINGS
                      │
                      ↓
            FAISS VECTOR DATABASE
                      │
                      │
              User asks question
                      │
                      ↓
             Question Embedding
                      │
                      ↓
              SIMILARITY SEARCH
                      │
                      ↓
             RELEVANT CHUNKS
                      │
                      ↓
                GEMINI LLM
                      │
                      ↓
               FINAL ANSWER

🧠 How Does This Project Work?

The RAG system mainly has two stages:

1. Indexing

This happens when we process the document.

PDF
 ↓
Extract text
 ↓
Split text into chunks
 ↓
Convert chunks into embeddings
 ↓
Store embeddings in FAISS

The system prepares the document so that it can be searched later.

2. Retrieval + Generation

This happens when the user asks a question.

User Question
      ↓
Convert question into embedding
      ↓
Search FAISS
      ↓
Find similar document chunks
      ↓
Send chunks + question to Gemini
      ↓
Generate answer
📄 Step 1 — PDF Text Extraction

The first step is reading the PDF.

Example:

PDF:

The college library is open from
8:00 AM to 8:00 PM.

The PDF loader extracts this information as normal text.

We use:

PyPDF

PyPDF allows Python to read text from PDF files.

✂️ Step 2 — Text Chunking

A large document cannot always be given to the LLM as one huge piece of text.

Therefore, we divide the document into smaller pieces.

These pieces are called:

Chunks

For example:

Original Document
       ↓
────────────────────────

Chunk 1
"The college library is open
from 8:00 AM to 8:00 PM."

Chunk 2
"Students can borrow up to
three books at a time."

Chunk 3
"Books are issued for
14 days."

────────────────────────

Chunking makes searching easier.

🔢 Step 3 — Embeddings

Computers cannot directly understand the meaning of text in the same way humans do.

An embedding model converts text into numbers called a:

Vector

For example:

"Library closes at 8 PM"

        ↓

[0.12, -0.45, 0.78, 0.23, ...]

We use:

Sentence Transformers

with the model:

all-MiniLM-L6-v2

The important idea is:

Text
 ↓
Embedding Model
 ↓
Vector

Similar meanings tend to have similar vector representations.

🗄️ Step 4 — FAISS Vector Database

After converting all document chunks into vectors, we need a way to search them efficiently.

For this project we use:

FAISS

FAISS stands for:

Facebook AI Similarity Search

It allows us to search for vectors that are similar to a given query vector.

For example:

Document chunks:

Chunk 1 → Library
Chunk 2 → Attendance
Chunk 3 → Examination
Chunk 4 → Placement
Chunk 5 → Computer Lab

User asks:

"What are the library timings?"

The question is converted into an embedding.

FAISS searches for the most similar chunks.

It may retrieve:

Chunk 1 → Library
Chunk 7 → Library Rules
Chunk 9 → Library Services

These are called:

Relevant Chunks

🔎 Step 5 — Similarity Search

The system compares:

User Question
        ↓
Question Embedding

with:

Document Chunk Embeddings

Then it finds the closest vectors.

This is called:

Similarity Search

The project retrieves the top relevant chunks.

For example:

Question:
"What time does the library close?"

             ↓

FAISS Search

             ↓

Relevant Chunk:
"The college library is open from
8:00 AM to 8:00 PM."
🧩 Step 6 — Relevant Context

The retrieved chunks are collected together.

For example:

Context:

The college library is open from
8:00 AM to 8:00 PM from Monday to Saturday.

Students can borrow up to three books
at one time.

This context is then given to the LLM.

🧠 Step 7 — Gemini LLM

The project uses:

Google Gemini

The LLM receives:

Question
+
Retrieved Context

For example:

Context:
The college library is open from
8:00 AM to 8:00 PM.

Question:
What time does the library close?

Gemini generates:

The library closes at 8:00 PM.
💬 Step 8 — Chatbot

Finally, Streamlit provides a simple user interface.

The user can:

Upload a PDF
Process the document
Enter a question
Get an answer

The application also shows the retrieved chunks so that the user can understand what information was used.

🏗️ Project Structure
RAG-DOCUMENT-CHATBOT/
│
├── data/
│   └── handbook.pdf
│
├── store/
│   └── vector database files
│
├── src/
│   ├── __init__.py
│   ├── load_document.py
│   ├── chunk_text.py
│   ├── embeddings.py
│   ├── retrieve.py
│   └── chatbot.py
│
├── scripts/
│   └── build_index.py
│
├── app.py
│
├── .env
│
├── requirements.txt
│
├── pyproject.toml
│
└── README.md
📁 Folder and File Explanation
data/

This folder contains the documents used by the RAG system.

Example:

data/
└── handbook.pdf

You can place your PDF document here.

store/

This folder is used to store the vector database/index.

After processing the document, the document embeddings can be stored here.

store/

Think of it as:

PDF
 ↓
Embeddings
 ↓
FAISS
 ↓
store/
src/

This folder contains the main RAG components.

load_document.py

Responsible for reading the PDF.

PDF
 ↓
Text
chunk_text.py

Responsible for splitting the extracted text into smaller chunks.

Large Text
 ↓
Chunk 1
Chunk 2
Chunk 3
...
embeddings.py

Responsible for converting text chunks into numerical vectors.

Chunk
 ↓
Embedding Model
 ↓
Vector
retrieve.py

Responsible for searching the vector database and finding relevant chunks.

Question
 ↓
Similarity Search
 ↓
Relevant Chunks
chatbot.py

Responsible for sending the question and retrieved context to Gemini.

Question
+
Context
 ↓
Gemini
 ↓
Answer
scripts/build_index.py

This script can be used to process the document and create the vector index.

PDF
 ↓
Text
 ↓
Chunks
 ↓
Embeddings
 ↓
FAISS Index
app.py

This is the main Streamlit application.

It provides the user interface.

Upload PDF
     ↓
Process
     ↓
Ask Question
     ↓
Get Answer
🛠️ Technologies Used
Python

Python is used to build the complete RAG pipeline.

Streamlit

Streamlit is used to create the chatbot web interface.

It allows us to build the application without writing HTML, CSS, and JavaScript.

PyPDF

PyPDF is used to extract text from PDF documents.

Sentence Transformers

Sentence Transformers is used to generate embeddings.

The project uses:

all-MiniLM-L6-v2
FAISS

FAISS is used for vector similarity search.

It helps us find document chunks that are semantically similar to the user's question.

Gemini API

Gemini is used as the Large Language Model.

It receives:

Question + Retrieved Context

and generates the final answer.

📦 Installation
Step 1 — Clone the repository
git clone <your-github-repository-url>

Move into the project:

cd RAG-DOCUMENT-CHATBOT
🐍 Step 2 — Create Virtual Environment

Create a Python virtual environment:

python -m venv .venv
▶️ Step 3 — Activate Virtual Environment
Windows PowerShell
.venv\Scripts\Activate.ps1

After activation, you should see something similar to:

(.venv)

in the terminal.

📥 Step 4 — Install Dependencies

Run:

pip install -r requirements.txt

The main libraries are:

streamlit
pypdf
sentence-transformers
faiss-cpu
numpy
google-generativeai
python-dotenv
🔑 Step 5 — Gemini API Key

The chatbot uses a Gemini API key.

Create a .env file:

GEMINI_API_KEY=your_api_key_here

Do not upload your real API key to GitHub.

Add .env to .gitignore.

Example:

.venv/
.env
__pycache__/
*.pyc
store/
🚀 Step 6 — Run the Application

Run:

streamlit run app.py

Streamlit will start the application.

Usually it will open in the browser automatically.

🧪 How to Test the RAG Chatbot

Use a PDF document as the knowledge source.

For example:

College Student Handbook.pdf

Upload the document.

Then ask questions such as:

What are the library timings?
How many books can a student borrow?
What is the minimum attendance requirement?
Are mobile phones allowed in the examination hall?
Who should I contact for a computer laboratory problem?

The chatbot should answer using information from the document.

🔍 Testing Retrieval

One important feature of this project is that we can inspect the retrieved chunks.

For example:

Question:

What are the library timings?

The retriever may find:

Retrieved Chunk 1:

The college library is open from
8:00 AM to 8:00 PM from Monday to Saturday.

Then Gemini uses this context to answer:

The library is open from 8:00 AM
to 8:00 PM, Monday to Saturday.

This helps us understand whether the retrieval part of RAG is working correctly.

🧠 RAG vs Normal Chatbot
Normal LLM Chatbot
User Question
      ↓
     LLM
      ↓
   Answer

The model mainly relies on its existing knowledge and the conversation context.

RAG Chatbot
User Question
      ↓
Vector Search
      ↓
Relevant Document Chunks
      ↓
Question + Context
      ↓
     LLM
      ↓
   Answer

The important difference is that RAG provides the LLM with relevant information retrieved from an external knowledge source.

🌟 Advantages of RAG

RAG can be useful when information comes from private or changing documents.

Examples include:

College handbooks
Company documents
Product manuals
Research papers
Policies
Technical documentation
Project reports
User guides
Internal knowledge bases
⚠️ Limitations

This is a beginner-level RAG implementation, so it has some limitations.

1. PDF quality

If a PDF contains scanned images instead of selectable text, normal PDF text extraction may not work properly.

OCR would be needed for such documents.

2. Chunk size

Very small chunks may lose context.

Very large chunks may retrieve unnecessary information.

Therefore, chunk size needs to be chosen carefully.

3. Retrieval quality

If the correct chunk is not retrieved, the LLM may not have the information needed to answer correctly.

4. LLM limitations

The LLM can still generate an incorrect answer if the prompt or retrieved context is insufficient.

For this reason, the system should instruct the model to answer only from the retrieved context.