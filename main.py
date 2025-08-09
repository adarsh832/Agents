import os
import sys
import time
from datetime import datetime
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools
from pydantic import SecretStr
from langsmith import Client
from langchain.callbacks import LangChainTracer
import uuid

# ANSI color codes for beautiful terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Additional colors for enhanced UI
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

def setup_langsmith_tracing():
    """Initialize LangSmith tracing for monitoring and debugging"""
    try:
        # Set up LangSmith environment variables
        langsmith_api_key = "your-api-key"
        langsmith_project = "AI-Assistant-CLI"  # You can customize this project name
        
        # Set environment variables for LangSmith
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
        os.environ["LANGCHAIN_PROJECT"] = langsmith_project
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        
        # Initialize LangSmith client
        client = Client(api_key=langsmith_api_key)
        
        # Create tracer
        tracer = LangChainTracer(project_name=langsmith_project)
        
        print_status("LangSmith tracing initialized successfully", "success")
        print_status(f"Project: {langsmith_project}", "info")
        
        return tracer, client
        
    except Exception as e:
        print_status(f"Warning: Could not initialize LangSmith tracing: {str(e)}", "warning")
        print_status("Continuing without tracing...", "info")
        return None, None
    """Display a beautiful welcome banner"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  {Colors.BOLD}{Colors.WHITE}🤖 AI ASSISTANT COMMAND CENTER 🤖{Colors.ENDC}{Colors.CYAN}                        ║
║                                                              ║
║  {Colors.OKGREEN}Powered by Google Gemini 2.5 Flash{Colors.ENDC}{Colors.CYAN}                           ║
║  {Colors.GRAY}LangChain Agent Framework{Colors.ENDC}{Colors.CYAN}                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def print_separator(char="─", length=62):
    """Print a stylish separator line"""
    print(f"{Colors.GRAY}{char * length}{Colors.ENDC}")

def print_status(message, status="info"):
    """Print status messages with appropriate colors"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if status == "success":
        print(f"{Colors.OKGREEN}✓{Colors.ENDC} {Colors.GRAY}[{timestamp}]{Colors.ENDC} {message}")
    elif status == "error":
        print(f"{Colors.FAIL}✗{Colors.ENDC} {Colors.GRAY}[{timestamp}]{Colors.ENDC} {Colors.FAIL}{message}{Colors.ENDC}")
    elif status == "warning":
        print(f"{Colors.WARNING}⚠{Colors.ENDC} {Colors.GRAY}[{timestamp}]{Colors.ENDC} {Colors.WARNING}{message}{Colors.ENDC}")
    elif status == "processing":
        print(f"{Colors.OKCYAN}⟳{Colors.ENDC} {Colors.GRAY}[{timestamp}]{Colors.ENDC} {Colors.OKCYAN}{message}{Colors.ENDC}")
    else:
        print(f"{Colors.OKBLUE}ℹ{Colors.ENDC} {Colors.GRAY}[{timestamp}]{Colors.ENDC} {message}")

def print_loading_animation(message, duration=2):
    """Display a loading animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for frame in frames:
            if time.time() >= end_time:
                break
            sys.stdout.write(f"\r{Colors.OKCYAN}{frame}{Colors.ENDC} {message}")
            sys.stdout.flush()
            time.sleep(0.1)
    
    sys.stdout.write(f"\r{Colors.OKGREEN}✓{Colors.ENDC} {message} - Complete!\n")

def print_welcome_info():
    """Display welcome information and instructions"""
    info = f"""
{Colors.BOLD}{Colors.WHITE}Welcome to your AI Assistant!{Colors.ENDC}

{Colors.OKGREEN}Available Commands:{Colors.ENDC}
  • Ask questions or give commands in natural language
  • Type {Colors.BOLD}'help'{Colors.ENDC} for assistance
  • Type {Colors.BOLD}'trace'{Colors.ENDC} to view LangSmith dashboard link
  • Type {Colors.BOLD}'exit'{Colors.ENDC} or {Colors.BOLD}'quit'{Colors.ENDC} to leave

{Colors.OKCYAN}Features:{Colors.ENDC}
  • Intelligent conversation with Gemini 2.5 Flash
  • Access to various tools and utilities
  • Real-time response processing
  • LangSmith tracing for debugging and monitoring
  • Verbose agent debugging (when enabled)

{Colors.WARNING}Tips:{Colors.ENDC}
  • Be specific with your requests for better results
  • Use natural language - no special syntax required
  • The assistant can handle complex multi-step tasks
  • All conversations are traced in LangSmith for analysis
"""
    print(info)
    print_separator("═")

def get_user_input():
    """Get user input with a styled prompt"""
    prompt = f"\n{Colors.BOLD}{Colors.PURPLE}You{Colors.ENDC} {Colors.GRAY}»{Colors.ENDC} "
    return input(prompt).strip()

def display_response(response):
    """Display the agent's response in a formatted way"""
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}🤖 Assistant{Colors.ENDC} {Colors.GRAY}»{Colors.ENDC}")
    print_separator("─", 50)
    print(f"{Colors.WHITE}{response}{Colors.ENDC}")
    print_separator("─", 50)

def handle_special_commands(command, langsmith_client=None):
    """Handle special commands like help, clear, etc."""
    command_lower = command.lower().strip()
    
    if command_lower in ['help', '/help', '?']:
        help_text = f"""
{Colors.BOLD}{Colors.OKCYAN}Help & Commands{Colors.ENDC}

{Colors.OKGREEN}Basic Usage:{Colors.ENDC}
  Just type your question or command in natural language!

{Colors.OKGREEN}Special Commands:{Colors.ENDC}
  • {Colors.BOLD}help{Colors.ENDC} - Show this help message
  • {Colors.BOLD}clear{Colors.ENDC} - Clear the screen
  • {Colors.BOLD}status{Colors.ENDC} - Show system status
  • {Colors.BOLD}trace{Colors.ENDC} - Show LangSmith dashboard link
  • {Colors.BOLD}sessions{Colors.ENDC} - Show recent trace sessions
  • {Colors.BOLD}exit/quit{Colors.ENDC} - Exit the application

{Colors.OKGREEN}Examples:{Colors.ENDC}
  • "What's the weather like today?"
  • "Help me write a Python function"
  • "Search for information about machine learning"
  • "Summarize this text: [your text here]"

{Colors.OKGREEN}LangSmith Features:{Colors.ENDC}
  • All conversations are automatically traced
  • View detailed execution logs in LangSmith dashboard
  • Monitor agent performance and tool usage
  • Debug complex multi-step reasoning
"""
        print(help_text)
        return True
    
    elif command_lower in ['clear', '/clear', 'cls']:
        os.system('clear' if os.name == 'posix' else 'cls')
   
        return True
    
    elif command_lower in ['status', '/status']:
        print_status("System operational", "success")
        print_status("Gemini 2.5 Flash model loaded", "success")
        print_status("All tools initialized", "success")
        if langsmith_client:
            print_status("LangSmith tracing active", "success")
        else:
            print_status("LangSmith tracing unavailable", "warning")
        return True
    
    elif command_lower in ['trace', '/trace', 'langsmith']:
        if langsmith_client:
            dashboard_url = "https://smith.langchain.com"
            print(f"""
{Colors.BOLD}{Colors.OKCYAN}LangSmith Dashboard{Colors.ENDC}

{Colors.OKGREEN}Dashboard URL:{Colors.ENDC} {dashboard_url}
{Colors.OKGREEN}Project:{Colors.ENDC} AI-Assistant-CLI

{Colors.GRAY}Visit the dashboard to view:
• Conversation traces and logs
• Agent reasoning steps
• Tool usage statistics
• Performance metrics
• Error analysis{Colors.ENDC}
""")
        else:
            print_status("LangSmith tracing is not available", "warning")
        return True
    
    elif command_lower in ['sessions', '/sessions']:
        if langsmith_client:
            try:
                print_status("Fetching recent sessions...", "processing")
                # This would require additional LangSmith API calls
                print(f"""
{Colors.BOLD}{Colors.OKCYAN}Recent Trace Sessions{Colors.ENDC}

{Colors.GRAY}To view detailed session information, visit:
https://smith.langchain.com/projects

All your conversations are automatically traced and
organized by session for easy debugging and analysis.{Colors.ENDC}
""")
            except Exception as e:
                print_status(f"Could not fetch sessions: {str(e)}", "error")
        else:
            print_status("LangSmith tracing is not available", "warning")
        return True
    
    return False

def main():
    try:
        # Clear screen and show banner
        os.system('clear' if os.name == 'posix' else 'cls')
    
        
        # Initialize LangSmith tracing
        print_status("Setting up LangSmith tracing...", "processing")
        tracer, langsmith_client = setup_langsmith_tracing()
        
        # Check for API key
        print_status("Checking API configuration...", "processing")
        api_key = "your-google-api-key"  # Replace with your actual API key
        
        if not api_key:
            print_status("GOOGLE_API_KEY environment variable not set", "error")
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        print_status("API key found", "success")
        
        # Initialize LLM with loading animation
        print_loading_animation("Initializing Gemini 2.5 Flash model...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            api_key=SecretStr(api_key)
        )
        
        # Initialize agent with loading animation and tracing
        print_loading_animation("Setting up AI agent and tools...")
        
        # Prepare callbacks list
        callbacks = []
        if tracer:
            callbacks.append(tracer)
        
        agent = initialize_agent(
            tools,
            llm,
            verbose=True,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            max_iterations=10,
            callbacks=callbacks if callbacks else None,
        )
        
        print_status("System initialization complete!", "success")
        if tracer:
            print_status("All conversations will be traced in LangSmith", "info")
        
        print_welcome_info()
        
        # Generate a unique session ID for this CLI session
        session_id = str(uuid.uuid4())[:8]
        print_status(f"Session ID: {session_id}", "info")
        
        # Main interaction loop
        while True:
            try:
                command = get_user_input()
                
                if not command:
                    continue
                
                # Check for exit commands
                if command.lower() in ['exit', 'quit', 'bye', '/exit', '/quit']:
                    print(f"\n{Colors.OKCYAN}👋 Thank you for using AI Assistant!{Colors.ENDC}")
                    if langsmith_client:
                        print(f"{Colors.GRAY}Check LangSmith dashboard for conversation traces{Colors.ENDC}")
                    print(f"{Colors.GRAY}Goodbye!{Colors.ENDC}\n")
                    break
                
                # Handle special commands
                if handle_special_commands(command, langsmith_client):
                    continue
                
                # Process the command with the agent
                print_status(f"Processing: {command}", "processing")
                print()  # Add some space
                
                # Add session metadata for tracing
                if tracer:
                    # You can add metadata to traces
                    metadata = {
                        "session_id": session_id,
                        "user_command": command,
                        "timestamp": datetime.now().isoformat()
                    }
                
                response = agent.run(command)
                display_response(response)
                
                # Optional: Log successful completion
                if tracer:
                    print_status("Trace logged to LangSmith", "info")
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.WARNING}⚠ Interrupted by user{Colors.ENDC}")
                print(f"{Colors.GRAY}Type 'exit' to quit gracefully{Colors.ENDC}")
                continue
                
            except Exception as e:
                print_status(f"Error occurred: {str(e)}", "error")
                print(f"{Colors.GRAY}Please try again or type 'help' for assistance{Colors.ENDC}")
                if tracer:
                    print_status("Error details captured in LangSmith trace", "info")
    
    except Exception as e:
        print_status(f"Fatal error: {str(e)}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()