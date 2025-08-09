from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools

apii_key = "AIzaSyBYNKINGZ5OtgYRm6GG7FNdC7iHzL9xWPQ"

llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        api_key= "AIzaSyBYNKINGZ5OtgYRm6GG7FNdC7iHzL9xWPQ"
    )
agent = initialize_agent(
        tools,
        llm,
        verbose=True,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        max_iterations=10,
    )