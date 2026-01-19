import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import MessagesPlaceholder
from tool import StoriesTool

st.set_page_config(
    page_title="HackerBot",
    page_icon="🤖",
)
st.title("HackerBot")

openai_api_key = st.secrets["OPENAI_API_KEY"]

msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(
    chat_memory=msgs, 
    return_messages=True,
    memory_key="chat_history"
)

if len(msgs.messages) == 0:
    msgs.add_ai_message("Hello! I'm HackerBot, your friendly AI assistant. How can I help you today?")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=openai_api_key)
open_ai_agent = initialize_agent(
    llm=llm,
    tools=[StoriesTool()],
    agent=AgentType.OPENAI_FUNCTIONS,
    agent_kwargs={
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]
    },
    verbose=True,
    memory=memory
)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input(disabled=not openai_api_key):
    st.chat_message("human").write(prompt)
    with st.spinner("Thinking..."):
        response = open_ai_agent.run(input=prompt)
        st.chat_message("ai").write(response)