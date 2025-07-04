# case_prep_chain.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from llm_file import llm  # ✅ Import your LLM
case_prompts = {
    "Profitability": "A retail chain has seen a 15% drop in net profits...",
    "Market Entry": "A European beverage company wants to enter the Indian market...",
    "M&A": "Your client is considering acquiring a smaller competitor...",
    "Growth Strategy": "A SaaS company wants to increase revenue by 30% in 2 years..."
}

def load_case_prep_chain(llm):
    system_prompt = """
    You are a consulting case interviewer for a top-tier firm (e.g., McKinsey, BCG, Bain). 
    Your job is to simulate a real case interview with a candidate.

    During the interview:
    - Start with a well-defined business case prompt.
    - Ask relevant follow-up questions based on the candidate's responses.
    - Keep questions concise and professional.
    - Use a logical, structured flow: clarifying questions → framework → analysis → recommendations.
    - Maintain the tone and behavior of an actual interviewer.

    If the candidate asks for clarifications or data (e.g., about the company, market, products, competitors, or financials), provide concise, realistic answers — just like in a real case interview.

    Do not give away answers or help structure the case unless explicitly requested — the goal is to assess their thinking.

    Once the user types 'end' or 'done', switch to evaluation mode.

    In evaluation mode:
    - Provide structured feedback under these 4 categories:
        1. Structure
        2. Problem Solving
        3. Communication
        4. Business Acumen
    - Give a score out of 10 for each category.
    - Then give a final verdict: Pass / Needs Improvement.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    return ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

# Export objects
__all__ = ["interview_chain", "case_prompts"]
