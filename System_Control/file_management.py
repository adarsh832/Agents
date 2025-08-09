import os

def create_file(path: str) -> str:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write("")  # empty file
        return f"✅ File created at: {path}"
    except Exception as e:
        return f"❌ Failed to create file: {e}"
def read_file(path: str) -> str:
    try:
        with open(path, 'r') as f:
            content = f.read()
        return f"📄 Contents of {path}:\n" + content
    except Exception as e:
        return f"❌ Failed to read file: {e}"
import ast

def write_file(input: str) -> str:
    try:
        data = ast.literal_eval(input)
        path = data["path"]
        content = data["content"]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return f"✅ Written to file at {path}"
    except Exception as e:
        return f"❌ Failed to write to file: {e}"

def append_file(input: str) -> str:
    try:
        data = ast.literal_eval(input)
        path = data["path"]
        content = data["content"]
        with open(path, 'a') as f:
            f.write(content)
        return f"✅ Appended to file at {path}"
    except Exception as e:
        return f"❌ Failed to append to file: {e}"
def delete_file(path: str) -> str:
    try:
        os.remove(path)
        return f"✅ File deleted: {path}"
    except Exception as e:
        return f"❌ Failed to delete file: {e}"
import subprocess

def execute_file(path: str) -> str:
    try:
        if not os.path.exists(path):
            return f"❌ File does not exist: {path}"
        subprocess.run([path], check=True)
        return f"✅ Executed file: {path}"
    except Exception as e:
        return f"❌ Failed to execute file: {e}"
