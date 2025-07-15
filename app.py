from flask import Flask, render_template, request, jsonify
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

# Try to import Ollama, with fallback if not available
try:
    from langchain_community.llms import Ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    print("⚠️ Ollama not available. Install with: pip install langchain-community")
    OLLAMA_AVAILABLE = False

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "genai-medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name,
)

retriver = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Number of documents to retrieve
)

# Initialize Ollama model with error handling
if OLLAMA_AVAILABLE:
    try:
        llm = Ollama(model="llama3")
        print("✅ Ollama model loaded successfully")
    except Exception as e:
        print(f"⚠️ Warning: Ollama not available ({e})")
        print("💡 Install Ollama from https://ollama.ai/ and run 'ollama pull llama3'")
        llm = None
else:
    print("⚠️ Ollama package not installed")
    print("💡 Install with: pip install langchain-community")
    llm = None 

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Create chain only if LLM is available
if llm:
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriver, question_answer_chain)
    print("✅ RAG chain created successfully")
else:
    rag_chain = None
    print("⚠️ Running in document retrieval mode only")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET','POST'])
def chat():
    try:
        msg = request.form['msg']
        print(f"User input: {msg}")
        
        # Check if full RAG chain is available
        if rag_chain:
            try:
                response = rag_chain.invoke({"input": msg})
                answer = response['answer']
            except Exception as llm_error:
                print(f"LLM Error: {llm_error}")
                # Fallback to document retrieval only
                docs = retriver.invoke(msg)
                if docs:
                    answer = f"Based on the medical literature, here's relevant information:\n\n{docs[0].page_content[:400]}..."
                    if len(docs) > 1:
                        answer += f"\n\nAdditional information: {docs[1].page_content[:200]}..."
                else:
                    answer = "I couldn't find relevant information in the medical documents for your query."
        else:
            # Document retrieval mode only
            docs = retriver.invoke(msg)
            if docs:
                answer = "🔍 **Information from Medical Literature:**\n\n"
                for i, doc in enumerate(docs[:2], 1):
                    answer += f"**Source {i}:** {doc.page_content[:300]}...\n\n"
                answer += "💡 *Note: For personalized medical advice, please consult a healthcare professional.*"
            else:
                answer = "I couldn't find relevant information in the medical documents for your query. Please try rephrasing your question or ask about common medical topics."
        
        print(f"Response: {answer}")
        return str(answer)
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I encountered an error processing your request. Please try again."

@app.route('/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        msg = data.get('message', '')
        print(f"User input: {msg}")
        
        # Check if full RAG chain is available
        if rag_chain:
            try:
                response = rag_chain.invoke({"input": msg})
                answer = response['answer']
            except Exception as llm_error:
                print(f"LLM Error: {llm_error}")
                docs = retriver.invoke(msg)
                if docs:
                    answer = f"Based on medical literature: {docs[0].page_content[:300]}..."
                else:
                    answer = "I couldn't find relevant information in the medical documents."
        else:
            # Document retrieval mode only
            docs = retriver.invoke(msg)
            if docs:
                answer = f"📚 From medical literature: {docs[0].page_content[:250]}..."
            else:
                answer = "I couldn't find relevant information in the medical documents."
        
        print(f"Response: {answer}")
        return jsonify({"response": answer})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, I encountered an error processing your request."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
