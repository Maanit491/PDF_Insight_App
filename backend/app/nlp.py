import os
from dotenv import load_dotenv
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.indices.postprocessor import SimilarityPostprocessor
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

def initialize_query_engine():
    folder = 'uploaded_files'
    
    if not os.listdir(folder):
        print("No files found in the uploaded_files directory for NLP model initialization")
        return None

    try:
        documents = SimpleDirectoryReader(folder).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        
        retriever = VectorIndexRetriever(index=index, similarity_top_k=4)
        postprocessor = SimilarityPostprocessor(similarity_cutoff=0.70)
        
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[postprocessor]
        )
        print("NLP model initialized successfully")
        return query_engine
    except Exception as e:
        print(f"Error initializing NLP model: {e}")
        return None


# print(response)
# print(type  (response))
# a=str(response)
# print(a)
# print(type(a))
