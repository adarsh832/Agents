Conversational AI Agent for PC Control
A powerful and intuitive AI agent that allows you to control your Windows PC using natural language. This agent can understand simple commands, execute complex multi-step tasks with conditional logic, and manage various system settings, all through a simple command-line interface.

✨ Features
Natural Language Understanding: Powered by Google's Gemini 2.5 Flash, the agent can understand and process commands given in plain English.

System Control: Adjust system volume and screen brightness.

System Actions: Lock, shut down, or restart your computer.

File Management: Create, read, append to, and delete files.

Web Browsing: Open websites and perform web searches.

Complex Task Execution: Chain multiple commands together with conditional logic. The agent can reason and decide which tools to use in what order to accomplish a complex goal.

Extensible Toolkit: Easily add new Python functions to expand the agent's capabilities.

🛠️ Tech Stack
Core Language: Python 3.10+

LLM Framework: LangChain & LangGraph for building stateful, multi-actor applications.

Large Language Model: Google Gemini 2.5 Flash

Observability: LangSmith for tracing, monitoring, and debugging the agent's reasoning process.

📂 Project Structure
.
├── System_Control/
│   ├── browser.py         # Tools for web browsing
│   ├── file_management.py # Tools for file operations
│   └── system_cmd.py      # Tools for system commands (volume, brightness, etc.)
├── .gitignore
├── main.py                # Main entry point to run the agent
├── requirements.txt       # Project dependencies
├── tools.py               # Aggregates all tools for the agent
└── ...

🚀 Getting Started
Follow these steps to get the agent up and running on your local machine.

1. Prerequisites
Python 3.10 or higher

A Google AI Studio API key for the Gemini model.

2. Clone the Repository
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME

3. Set Up a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

# Create the virtual environment
python -m venv .venv

# Activate it
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

4. Install Dependencies
Install all the required Python packages.

pip install -r requirements.txt

5. Configure Environment Variables
You need to set up your API keys for Google Gemini and LangSmith. Create a .env file in the root of the project directory and add the following:

# .env file
GOOGLE_API_KEY="YOUR_GOOGLE_AI_STUDIO_API_KEY"

# Optional: For tracing with LangSmith
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="YOUR_LANGSMITH_API_KEY"
LANGCHAIN_PROJECT="YOUR_PROJECT_NAME" # e.g., "AI-Assistant-CLI"

💡 How to Use
Run the main script to start the interactive command-line interface.

python main.py

Once the agent is initialized, you can start giving it commands.

Example Commands
Simple Tasks:

What can you do for me?

Set the volume to 50

Set the brightness to 75

Lock the screen

Create a file named "hello.txt" with the content "Hello, World!"

Complex Task:

Check my brightness and if it is 100 then set it to 45. Then, if the brightness is under 70 then set the volume to 10. If the volume is above 1 then lock the screen.

🧠 How It Works
This agent is built using the LangGraph library, which allows for the creation of cyclical graphs that are essential for agentic behavior.

Input: The user provides a prompt in natural language.

LLM Reasoning: The Gemini model, acting as the "brain," decides which tool (or sequence of tools) is needed to address the user's request.

Tool Execution: The agent executes the chosen Python function(s) from the toolkit (e.g., set_volume, get_brightness).

Observation: The result (observation) from the tool is passed back to the LLM.

Response: The LLM processes the observation and either decides the task is complete and generates a final answer, or continues the cycle by choosing another tool.

This entire process is stateful, meaning the agent remembers previous steps in the conversation to handle complex, multi-step tasks.

🙌 Contributing
Contributions are welcome! If you have ideas for new tools or improvements, feel free to fork the repository, make your changes, and submit a pull request.

How to Add a New Tool
Create the function: Write a new Python function in the appropriate file within the System_Control/ directory.

Add Pydantic Model: Define a Pydantic model for the function's arguments to ensure type safety.

Register the tool: Import your new function into tools.py and add it to the tools list.

Re-run the agent: The agent will automatically recognize the new tool and its capabilities.

