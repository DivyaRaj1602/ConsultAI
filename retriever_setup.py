# retriever_setup.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Reload the vectorstore from disk
embedding_model = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# Prepare retrievers by filtering on metadata["part"]
prepare_retriever = vectorstore.as_retriever(
    search_kwargs={"filter": lambda metadata: metadata.get("part") == "prepare_yourself"}
)

learning_retriever = vectorstore.as_retriever(
    search_kwargs={"filter": lambda metadata: metadata.get("part") == "learning"}
)

case_prep_retriever = vectorstore.as_retriever(
    search_kwargs={"filter": lambda metadata: metadata.get("part") == "case_prep"}
)

print("✅ Retrievers loaded and filtered by part.")

# 👇 Export all retrievers
__all__ = ["prepare_retriever", "learning_retriever", "case_prep_retriever"]
