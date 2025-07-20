
---

# **BotifyNow – AI Chat & RAG APIs**


A simple yet powerful FastAPI + React-based application that integrates **OpenAI GPT chat** and **RAG (Retrieval-Augmented Generation)** using **Qdrant** for semantic document search. Users can chat with the bot, upload PDFs or text files, and get **context-aware answers** and **summaries** from their uploaded documents.

---

## **📌 Features**

✅ **Chat with GPT (general Q\&A)**
✅ **Upload PDF/TXT files**
✅ **RAG-powered contextual answers using Qdrant**
✅ **Auto-summarize document after upload**
✅ **Typing indicator & WhatsApp-like chat UI** (frontend)
✅ **Full-screen, mobile-responsive React frontend**

---

## **🛠 Tech Stack**

### **Backend**

* **Python 3.12+**
* **FastAPI (REST APIs)**
* **OpenAI API (GPT & Embeddings)**
* **Qdrant (Vector DB for document search)**
* **Uvicorn (ASGI server)**

### **Frontend**

* **React + Vite** (modern, fast frontend setup)
* **CSS (minimal, professional design)**

---

## **📂 Project Architecture**

```
botifynow/
├── botifynow_backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── models.py               # Pydantic request models
│   │   ├── services/
│   │   │   ├── openai_service.py   # Chat & RAG logic
│   │   │   └── qdrant_service.py   # Embedding & vector search
│   │   └── utils/
│   │       └── pdf_extractor.py    # Extract text from PDFs
│   ├── requirements.txt            # Python dependencies
│   └── .env                        # API keys (not committed to Git)
│
└── botifynow_frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── App.jsx                  # Chat UI logic
        ├── App.css                  # Styling
        └── main.jsx                 # React entry
```

---

## **⚙ Requirements**

### **1️⃣ Backend**

* Python **3.9+** (tested on 3.12)
* OpenAI account + API key
* Install requirements:

```bash
cd botifynow_backend
pip install -r requirements.txt
```

### **2️⃣ Frontend**

* Node.js **16+** and npm

---

## **🚀 Setup Instructions**

### **1️⃣ Configure Environment**

Create a `.env` file in `botifynow_backend/`:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

*(Make sure your key has access to `gpt-3.5-turbo` and `text-embedding-3-small`)*

---

### **2️⃣ Run Backend**

```bash
cd botifynow_backend
uvicorn app.main:app --reload
```

API will be available at:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Swagger Docs: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

### **3️⃣ Run Frontend**

```bash
cd botifynow_frontend
npm install
npm run dev
```

Frontend will run at:
**[http://localhost:5173](http://localhost:5173)**

*(Vite proxy forwards API calls to `/api` → backend automatically)*

---

## **🔗 API Endpoints**

### **POST /chat**

* **Request:**

```json
{ "message": "Hello, bot!" }
```

* **Response:**

```json
{ "response": "Hello! How can I assist you today?" }
```

### **POST /upload**

* **Request:** Upload a PDF/TXT file
* **Response:**

```json
{ "message": "Document uploaded successfully", "document_id": "1234-5678" }
```

### **POST /rag-chat**

* **Request:**

```json
{ "message": "Summarize this document", "document_id": "1234-5678" }
```

* **Response:**

```json
{ "response": "This document is about..." }
```

---

## **📸 UI Preview**

<img width="491" height="862" alt="Screenshot 2025-07-20 230246" src="https://github.com/user-attachments/assets/55b5e724-bcc8-4a27-8235-999b985824d4" />


---

## **🧩 Known Issues**

* If you get **403 model\_not\_found**: Ensure you have access to `gpt-3.5-turbo` and `text-embedding-3-small`.
* Timeout errors can occur for **very large PDFs** (>10 MB).

---

## **📜 License**

MIT License – feel free to modify and use.

---
