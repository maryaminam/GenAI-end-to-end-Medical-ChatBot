from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf_file(data):
    loader = DirectoryLoader(data, glob="*pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents



def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


def download_hugging_face_embeddings():
    # Use the new import to avoid deprecation warning
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        # Fallback to the old import if the new package is not available
        from langchain.embeddings import HuggingFaceEmbeddings
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings