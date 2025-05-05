import sqlite3
import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
##from langchain.callbacks import streamlit_callback_handler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine


st.set_page_config(page_title="SQL Agent with Groq", page_icon=":guardsman:")
st.title("SQL Agent with Groq")
user_query = st.chat_input("Ask a question about the database:")
mysql_host = st.sidebar.text_input("MySQL Host", "localhost:")
mysql_user = st.sidebar.text_input("MySQL User", "root")
mysql_password = st.sidebar.text_input("MySQL Password",type="password")
mysql_db = st.sidebar.text_input("MySQL Database")


api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not mysql_host or not mysql_user or not mysql_password or not mysql_db:
    st.warning("Please enter MySQL connection details.")
if not api_key:
    st.warning("Please enter Groq API Key.")
    st.stop()

llm=ChatGroq(groq_api_key=api_key, model="Llama3-8b-8192", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(mysql_host, mysql_user, mysql_password, mysql_db):
    connection_string = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
    engine = create_engine(connection_string)
    return SQLDatabase(engine)


db = configure_db(mysql_host, mysql_user, mysql_password, mysql_db)

toolkit= SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)


if user_query:
    with st.spinner("Thinking..."):
        #streamlit_callback_handler.StreamlitCallbackHandler.set_streamlit_info(st)
        response = agent.run(user_query)
        st.write(response)
        ###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