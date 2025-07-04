# ingest_documents.py

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# 1. Load PDF
loader = PyPDFLoader(r"C:\Users\DIVYA\Desktop\LANGCHAIN\Case In Point- CaseBook.pdf")
pages = loader.load()

# 2. Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# 3. Manual section tagging based on page numbers
PART_PAGE_RANGES = {
    "prepare_yourself": range(10, 69),
    "learning": range(69, 130),
    "case_prep": range(130, 325),
}

structured_docs = []

for i, page in enumerate(pages):
    text = page.page_content
    part = "general"
    
    for tag, page_range in PART_PAGE_RANGES.items():
        if i in page_range:
            part = tag
            break

    chunks = splitter.split_text(text)

    for j, chunk in enumerate(chunks):
        structured_docs.append(Document(
            page_content=chunk,
            metadata={
                "page_number": i + 1,
                "part": part,
                "source": "Case in Point",
                "chunk_id": f"page_{i+1}_chunk_{j}"
            }
        ))

print("✅ Structured docs created:", len(structured_docs))

# 4. Create vectorstore
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(structured_docs, embedding)

# 5. Save to disk
vectorstore.save_local("faiss_index")
print("✅ FAISS vector store saved to 'faiss_index'")
