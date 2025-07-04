from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from retriever_setup import case_prep_retriever  # ← Your retriever setup
from llm_file import llm 

# 🧠 Prompt template for extracting useful examples
example_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a consulting trainer. A candidate has asked for real case examples to understand how business cases are structured and handled.

Use the following context extracted from a consulting casebook (primarily real case examples) to:
- Provide relevant cases.
- Highlight the type of business issue tackled.
- Mention industries if applicable.
- Give concise summaries with key lessons or approach.

Context:
{context}

User Question:
{question}

Answer:"""
)

# 🧠 Memory for maintaining chat flow
def load_case_examples_chain(llm, case_example_retriever):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=case_example_retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": example_prompt},
        verbose=True
    )
