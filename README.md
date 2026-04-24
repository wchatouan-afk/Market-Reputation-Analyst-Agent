# Auto-Doc Agent

## Project Journal - Step 1 (24.04)

### 1. Description of the planned system and its goal
The **Auto-Doc Agent** is a Python-based tool designed to automate technical documentation. The goal is to provide a system that can scan a local codebase, understand its structure and logic, and generate a comprehensive `README.md` or technical guide automatically. It targets developers who want to maintain up-to-date documentation with minimal effort.

### 2. AI or Agent-based approach
The system uses a **single-agent architecture** based on the **ReAct (Reasoning and Acting)** pattern. 
* The agent acts as a "Technical Writer". 
* It will use a LLM (Large Language Model) to reason about which files are important and how they interact. 
* It follows a loop: Observe the file structure -> Read relevant code -> Analyze logic -> Synthesize documentation.

### 3. List of tools to be used
The agent will be equipped with the following functional tools:
* **FileTree Explorer**: To list and map the project directory structure.
* **SourceCode Reader**: To read the content of specific Python files.
* **Dependency Parser**: To identify external libraries used in the project (via `requirements.txt` or imports).
* **DocFormatter**: To convert the AI's analysis into a structured Markdown file.

### 4. Preliminary list of programming concepts required
* **File I/O & OS Module**: For navigating and reading local directories (`os`, `pathlib`).
* **Environment Management**: Using `python-dotenv` for secure API key handling.
* **LLM Integration**: Using `LangChain` or `OpenAI SDK` to power the agent's logic.
* **Modular Programming**: Organizing the system into separate modules for the agent, tools, and main execution.
* **Unit Testing**: Implementing `pytest` to ensure tools handle edge cases (e.g., empty files, restricted permissions).