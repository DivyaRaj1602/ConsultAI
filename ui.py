# ui.py

import streamlit as st
from ConsultBot.prepare_chain import load_prepare_chain
from ConsultBot.case_prep_chain import load_case_prep_chain, case_prompts

from ConsultBot.learning_chain import load_learning_chain
from ConsultBot.case_example import load_case_examples_chain
from ConsultBot.llm_file import llm
from ConsultBot.retriever_setup import prepare_retriever, learning_retriever, case_prep_retriever

# Set background image
import base64

def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/avif;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    .block-container {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }}
    .markdown-text-container,
    .stTextInput input,
    .stTextArea textarea,
    .stButton > button {{
        color: white;
    }}

    .stTextInput input,
    .stTextArea textarea {{
        background-color: rgba(30, 30, 30, 0.8);
        border: 1px solid #ccc;
    }}

    .stButton > button {{
        background-color: #1f1f1f;
        border: 1px solid #ccc;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Call this with your image path
set_bg(r"C:\Users\DIVYA\Desktop\LANGCHAIN\ConsultBot\modern-boardroom-ready-meeting_1286777-1867.avif")

st.set_page_config(page_title="ConsultBot", layout="wide")
st.title("🤖 ConsultBot – Your Case Interview Coach")





# Load chains
prepare_chain = load_prepare_chain(llm, prepare_retriever)
case_prep_chain = load_case_prep_chain(llm)
learning_chain = load_learning_chain(llm, learning_retriever)
case_example_chain = load_case_examples_chain(llm, case_prep_retriever)

# App Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💼 Prepare Yourself", "🎯 Case Prep", "📘 Learning", "🧠 Case Examples"])

# --- Tab 1: Prepare Yourself ---
with tab1:
    st.subheader("💼 Interview Preparation Help")

    st.markdown("💡 **Try asking:**")
    st.markdown("""
    - How do I answer 'Why consulting?'
    - What do top firms look for in candidates?
    - How do I structure my personal pitch?
    - What should I wear for a consulting interview?
    - How do I show leadership in an interview?
    """)

    # Use dedicated history for this module
    if "chat_history_prepare" not in st.session_state:
        st.session_state.chat_history_prepare = []

    user_q1 = st.text_input("Ask a preparation question:", key="prep_input")

    # Submit logic
    if st.button("Ask", key="prep_submit") and user_q1:
        with st.spinner("Thinking..."):
            result = prepare_chain.invoke({"question": user_q1})
            st.session_state.chat_history_prepare.append(("You", user_q1))
            st.session_state.chat_history_prepare.append(("Coach", result["answer"]))

    # Optional Reset button
    if st.button("Reset Chat", key="reset_prepare"):
        st.session_state.chat_history_prepare = []

    # Display chat history
    for role, msg in st.session_state.chat_history_prepare:
        st.chat_message(role).write(msg)


# --- Tab 2: Case Prep Simulation ---
with tab2:
    st.subheader("🎯 Mock Case Interview")
    case_types = {
        "Profitability": "A retail chain has seen a 15% drop in net profits...",
        "Market Entry": "A European beverage company wants to enter the Indian market...",
        "M&A": "Your client is considering acquiring a smaller competitor...",
        "Growth Strategy": "A SaaS company wants to increase revenue by 30% in 2 years..."
    }

    if "case_started" not in st.session_state:
        st.session_state.case_started = False
    if "interview_history" not in st.session_state:
        st.session_state.interview_history = []

    case_choice = st.selectbox("Choose a case type:", list(case_types.keys()))
    
    if not st.session_state.case_started:
        if st.button("Start Interview"):
            intro = case_prep_chain.invoke({
                "input": f"Start the case interview. Case type: {case_choice}. Prompt: {case_types[case_choice]}"
            })
            st.session_state.case_started = True
            st.session_state.interview_history.append(("🤖", intro["response"]))

    if st.session_state.case_started:
        for speaker, msg in st.session_state.interview_history:
            st.markdown(f"**{speaker}**: {msg}")

        user_input = st.text_input("🧑 You:", key="case_input_tab2")
        if st.button("Send Response", key="send_response_tab2"):
            st.session_state.interview_history.append(("🧑", user_input))
            result = case_prep_chain.invoke({"input": user_input})
            st.session_state.interview_history.append(("🤖", result["response"]))

        if st.button("End Interview"):
            feedback = case_prep_chain.invoke({
                "input": "Please evaluate my case interview performance."
            })
            st.markdown("### 🧠 Interviewer Feedback")
            st.write(feedback["response"])
            st.session_state.case_started = False
            st.session_state.interview_history.clear()

# --- Tab 3: Learning Module ---
with tab3:
    st.subheader("📘 Learn Consulting Concepts")

    st.markdown("💡 **Try asking:**")
    st.markdown("""
    - What is the Ivy Case System?
    - Explain a profitability framework.
    - How do I estimate market size?
    - What are common types of business problems?
    - How do consulting firms approach analysis?
    """)

    # Initialize session state for learning history
    if "chat_history_learning" not in st.session_state:
        st.session_state.chat_history_learning = []

    user_q3 = st.text_input("Ask a consulting theory question:", key="learn_input")

    if st.button("Ask", key="learn_submit") and user_q3:
        with st.spinner("Thinking..."):
            result = learning_chain.invoke({"question": user_q3})
            st.session_state.chat_history_learning.append(("You", user_q3))
            st.session_state.chat_history_learning.append(("Tutor", result["answer"]))

    if st.button("Reset Chat", key="reset_learning"):
        st.session_state.chat_history_learning = []

    # Display chat
    for role, msg in st.session_state.chat_history_learning:
        st.chat_message(role).write(msg)


# --- Tab 4: Case Examples ---
with tab4:
    st.subheader("🧾 Real Case Examples")
    st.markdown("💡 **Try asking:**")
    st.markdown("""
        - Give me an example of a Market Entry case.
        - Can you show me a Partner Case from the book?
        - I want a PE Acquisition example.
        - Share a luxury brand expansion case.
        - What's a good profitability case to review?
    """)

    # Initialize session state for case example chat history
    if "chat_history_case_examples" not in st.session_state:
        st.session_state.chat_history_case_examples = []

    user_q4 = st.text_input("Ask for a case example or related insight:", key="case_input_tab4")

    if st.button("Fetch Example", key="case_submit_tab4"):
        with st.spinner("Retrieving relevant case..."):
            result = case_example_chain.invoke({"question": user_q4})
            st.session_state.chat_history_case_examples.append(("You", user_q4))
            st.session_state.chat_history_case_examples.append(("Trainer", result["answer"]))

    if st.button("Reset Chat", key="reset_case"):
        st.session_state.chat_history_case_examples = []

    # Display chat history
    for role, msg in st.session_state.chat_history_case_examples:
        st.chat_message(role).write(msg)

