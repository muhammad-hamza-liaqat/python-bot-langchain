# 🧠 AI Bot with Django + DRF + LangChain

This project is an **AI-powered Q&A bot** built using **Django**, **Django REST Framework (DRF)**, and **LangChain**.  
It lets you **upload PDFs or text files**, stores embeddings in **ChromaDB**, and allows you to **ask questions** which are answered using **OpenAI’s LLMs**.

---

## 🚀 Features
- Upload PDF/Text documents
- Extract embeddings with **LangChain**
- Store embeddings in **ChromaDB**
- Ask questions and get **AI-generated answers**
- RESTful API endpoints via **Django REST Framework**
- Modular and extensible project structure

---

## 📂 Project Structure
```
python-bot/
│── bot/
│   ├── views.py          # API views (upload, query)
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # API routes
│── server/
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main project URLs
│── env/                  # Virtual environment
│── manage.py             # Django entry point
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

---

## 🛠️ Installation

### 1️⃣ Clone the repository
```bash
git clone git@github.com:muhammad-hamza-liaqat/python-bot-langchain.git
```

### 2️⃣ Create & activate virtual environment
```bash
python3.11 -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your_openai_api_key
DJANGO_SECRET_KEY=your_django_secret_key_here
```

---

## ▶️ Run the Project

Start Django server:
```bash
python manage.py runserver
```

---

## 📡 API Endpoints

### Upload File
**POST** `/api/bot/upload/`  
Upload a PDF or text file and generate embeddings.

```bash
curl -X POST http://127.0.0.1:8000/api/bot/upload/   -F "file=@yourfile.pdf"
```

### Ask a Question
**POST** `/api/bot/query/`  
Ask a question based on uploaded documents.

```bash
curl -X POST http://127.0.0.1:8000/api/bot/query/   -H "Content-Type: application/json"   -d '{"query": "What is the fees of Meezan VISA Debit Card?"}'
```

Response:
```json
{
  "status": 200,
  "message": "Success",
  "data": {
    "answer": "The fees of Meezan VISA Debit Card is ..."
  }
}
```

---

## 📦 Dependencies
- Django
- Django REST Framework
- python-dotenv
- langchain
- langchain-community
- langchain-openai
- langchain-chroma
- chromadb
- PyPDF2 / pypdf

Install everything via:
```bash
pip install -r requirements.txt
```

---

## ✅ To-Do / Improvements
- [ ] Add authentication for APIs
- [ ] Support multiple vectorstore backends
- [ ] UI with React or Next.js frontend
- [ ] Dockerize the project

---

## 🤝 Contributing
Pull requests are welcome.  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License
This project is licensed under the MIT License.
