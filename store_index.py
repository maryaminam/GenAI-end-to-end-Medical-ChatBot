from src.helper import load_pdf_file,text_split,download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
import os
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data = load_pdf_file(data="Data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

pc= Pinecone(api_key=PINECONE_API_KEY)

index_name = "genai-medical-chatbot"

pc.create_index(
            name=index_name,
            dimension=384,  # Dimension of the embeddings (sentence-transformers/all-MiniLM-L6-v2)
            metric="cosine",  # Similarity metric
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",  # Try us-east-1 instead of us-east-2
            )
)

#embed each chunk and store in Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name,
)