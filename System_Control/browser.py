from langchain_hyperbrowser import HyperbrowserBrowserUseTool

# Pre-defined API key
browser = HyperbrowserBrowserUseTool(api_key="hb_adf3d2056c9ca93a480c6cf4027d")

def browse_web(task: str) -> str:
    """
    Use Hyperbrowser to perform a web browsing task.

    Args:
        task (str): The browsing instruction (e.g., "search X", "get link Y")

    Returns:
        str: Result from the browser tool
    """
    try:
        result = browser.run({"task": task})
        return result
    except Exception as e:
        return f"❌ Failed to browse: {e}"
