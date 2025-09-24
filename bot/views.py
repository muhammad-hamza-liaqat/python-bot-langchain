import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedDocument
from .serializers import DocumentSerializer

from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

# ChromaDB path
CHROMA_DB_DIR = os.path.join(settings.BASE_DIR, "chroma_db")

# Upload file API
class UploadDocumentView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save file
        doc = UploadedDocument.objects.create(file=file)
        
        # Load file content
        file_path = doc.file.path
        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        documents = loader.load()
        
        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(documents)
        
        # Store in ChromaDB
        db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
        db.add_documents(docs)
        db.persist()
        
        return Response({"message": "File uploaded and processed successfully."}, status=status.HTTP_201_CREATED)

# Query API
class QueryDocumentView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Load ChromaDB
        db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
        # Get relevant docs
        results = retriever.get_relevant_documents(query)
        answers = [doc.page_content for doc in results]
        
        return Response({"query": query, "answers": answers}, status=status.HTTP_200_OK)
