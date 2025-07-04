from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory

def load_prepare_chain(llm, prepare_retriever):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a consulting coach. Use the following context to help answer the user's question."),
        HumanMessagePromptTemplate.from_template("Context:\n{context}\n\nQuestion: {question}")
    ])

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=prepare_retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        verbose=True
    )
