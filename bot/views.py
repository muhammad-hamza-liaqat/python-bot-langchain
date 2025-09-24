import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .serializers import UploadFileSerializer, QuerySerializer

CHROMA_DB_DIR = "chroma_store"

embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)


def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )


class UploadFileView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UploadFileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]
            file_path = f"uploads/{file.name}"

            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            if file.name.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path)

            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)

            vectorstore = get_vectorstore()
            vectorstore.add_documents(texts)

            return Response({"message": "File uploaded and processed successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AskQuestionView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data["query"]

            vectorstore = get_vectorstore()
            retriever = vectorstore.as_retriever()

            llm = ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model="gpt-4o-mini",
                temperature=0
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant. Only answer using the provided context."),
                ("human", "{question}")
            ])

            docs = retriever.get_relevant_documents(query)
            context = "\n\n".join([doc.page_content for doc in docs])

            chain = prompt | llm
            response = chain.invoke({"question": query + "\n\nContext:\n" + context})

            return Response({"answer": response.content}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
