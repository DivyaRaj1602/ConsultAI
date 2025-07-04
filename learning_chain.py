# learning_chain.py

from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from retriever_setup import learning_retriever  # ← Your retriever setup
from llm_file import llm  # ← Your LLM (e.g., from ChatGroq or OpenAI)

def load_learning_chain(llm, learning_retriever):
    combine_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a consulting tutor helping a candidate understand core consulting concepts.

Use the following context to answer the user's question.
Context:
{context}

Question: {question}
Answer:"""
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=learning_retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": combine_prompt},
        verbose=True
    )
print("SUCESSSSSS")

# ✅ Export
__all__ = ["learning_chain"]
