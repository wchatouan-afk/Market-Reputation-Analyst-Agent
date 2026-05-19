# Auto-Doc Agent

## Project Journal - Step 1 (24.04)

The Auto-Doc Agent is a specialized CLI-based assistant designed for Python developers and DevOps engineers. Its primary goal is to solve the problem of "documentation drift"—where source code evolves faster than its documentation.
Input: A local directory path pointing to a Python repository.
Output: A standardized DOCUMENTATION.md file featuring an architectural overview, class-level summaries, dependency mapping, and a functional API reference.


2. AI / Agent Approach

The Auto-Doc Agent is implemented as a ReAct-based LLM system inside a CLI application, directly supporting the system goal defined in Step 1. The system receives a local directory path pointing to a Python repository and must transform it into a structured DOCUMENTATION.md file containing architecture, class-level summaries, dependency mapping, and API references.

The AI component is the core mechanism that enables this transformation. It is responsible for interpreting the repository structure, coordinating analysis, and deciding how to extract the required information from the codebase. Without the AI agent, the system would behave as a simple file-processing script and would not be able to understand code semantics or architectural relevance.

A simple script is not sufficient because it cannot interpret the relationship between files, identify which components contain meaningful business logic, or decide what information is required to generate documentation aligned with the required output format (architecture overview, class summaries, dependency mapping, API reference). It would only execute fixed operations without understanding the structure or meaning of the repository.

The LLM acts as a controller that bridges the input (repository directory) and the output (DOCUMENTATION.md). It ensures that the final documentation is not manually written, but reconstructed from the actual state of the codebase.

The agent operates in a continuous loop aligned with the system input and output definition:

1. Input Alignment (Step 1 connection):
The system starts from a local directory path representing a Python repository. This input is identical to the one defined in the system goal and is the starting point of all reasoning.

2. Thought (Repository interpretation aligned with output requirements):
The LLM analyzes the repository structure in relation to the expected output of the system:
- class-level summaries → detection of classes and methods
- dependency mapping → detection of imports and requirements
- API reference → detection of functional and executable logic

This ensures that reasoning is always aligned with the final DOCUMENTATION.md structure defined in Step 1.

3. Action (Tool orchestration):
The LLM selects tools based on what is required to build the final documentation output:
- FileTree Explorer → to map repository structure
- SourceCode Reader → to extract classes, functions, and docstrings for class-level summaries and API reference
- Dependency Parser → to build dependency mapping

4. Observation (Structured transformation of repository state):
Each tool returns structured JSON data representing a part of the repository. This structured data is progressively accumulated into an internal representation of the project used to construct the final documentation output.

5. Output Alignment:
The iterative loop continues until all required components defined in Step 1 (architecture overview, class summaries, dependency mapping, API reference) are fully extracted. The final result is then used to generate the DOCUMENTATION.md file.

This ensures full traceability between:
Input (directory path) → AI reasoning → tool outputs → final DOCUMENTATION.md output.


3. Tools

The Auto-Doc Agent relies on a fixed set of execution tools that are directly controlled by the LLM described in Step 2. These tools are used to transform the input defined in Step 1 (a local Python repository directory path) into the final DOCUMENTATION.md output.

Each tool produces structured data that is progressively combined into a single internal Project Manifest. This manifest is the only source used to generate the final documentation output defined in Step 1.

FileTree Explorer

Input:
A local directory path (Step 1 input)

Output:
A list of all files and folders in the Python repository (excluding .gitignore paths)

Function in pipeline:
This tool is always executed first when the LLM (Step 2) starts analyzing a repository. It converts the raw directory input into a structured project map used for navigation and file selection.

SourceCode Reader

Input:
A single Python file path selected by the LLM

Output:
{
  "file_path": "str",
  "classes": [],
  "functions": [],
  "docstrings": "str"
}

Function in pipeline:
This tool is executed when the LLM identifies a file containing functional or structural code. The extracted data is used to generate:
- class-level summaries (required in Step 1 output)
- functional API reference (required in Step 1 output)

Dependency Parser

Input:
Python file or requirements.txt selected by the LLM

Output:
{
  "internal_imports": [],
  "external_libs": []
}

Function in pipeline:
This tool is executed when the LLM detects import statements or dependency-related files. The output is used to construct the dependency mapping section required in Step 1.

DocFormatter

Input:
Complete Project Manifest generated from all previous tools

Output:
Final DOCUMENTATION.md file

Function in pipeline:
This is the final step of the system. It takes all structured outputs produced by previous tools and formats them into the exact structure defined in Step 1:
- architecture overview
- class-level summaries
- dependency mapping
- API reference

System constraint:
Tools do not operate independently. Every tool execution is triggered and controlled by the LLM reasoning process defined in Step 2. The tools only exist to convert repository data into structured representations that match the final DOCUMENTATION.md specification.

4. Programming Concepts

The implementation of the Auto-Doc Agent is based on a set of Python programming concepts that directly support the system defined in Step 1, orchestrated by the LLM described in Step 2, and executed through the tools defined in Step 3.

Each concept is strictly used to transform a local Python repository (input) into a structured DOCUMENTATION.md file (output).

File System Handling (pathlib, os)

Used to process the input defined in Step 1, which is a local directory path pointing to a Python repository. These modules allow the system to safely navigate the filesystem, list files, and validate project structure before any LLM-driven analysis begins.

This is the foundation that enables the FileTree Explorer tool (Step 3) to operate correctly.

Agent Orchestration (OpenAI SDK / LangChain)

Used to implement the ReAct-based LLM workflow described in Step 2. This layer controls how the LLM:
- analyzes repository structure,
- decides which tool to execute,
- and maintains context across iterations.

It directly connects the input (Step 1) to the tool execution pipeline (Step 3).

Structured Data Validation (Pydantic)

Used to enforce strict schemas for all outputs generated by tools defined in Step 3. Every tool response (classes, functions, dependencies) must follow a validated structure before being added to the internal Project Manifest.

This ensures that the final DOCUMENTATION.md output defined in Step 1 is always consistent and correctly formatted.

Environment Management (python-dotenv)

Used to securely manage configuration data such as API keys required for the LLM (Step 2). This allows the CLI system to run independently across different environments while maintaining secure access to the AI model.

Testing Framework (pytest)

Used to validate the full pipeline from Step 1 input (directory path) to Step 1 output (DOCUMENTATION.md). Testing ensures that:
- the LLM correctly orchestrates tools (Step 2),
- tools return valid structured outputs (Step 3),
- and the final documentation matches the expected format (Step 1).


---

## Project Journal - Step 2 (08.05)
The system has transitioned from a theoretical model to a modular implementation. 
- **Refined Concepts**: We integrated AST (Abstract Syntax Tree) parsing for semantic code analysis and Pydantic models for strict data validation between tools.
- **Application**: The `SourceCodeReader` now uses AST parsing to extract function and class signatures without executing code, ensuring the AI receives clean, relevant metadata. 
- **Integration**: Tools are orchestrated via a centralized registry. The `main.py` controller manages the ReAct loop, where the agent’s reasoning drives tool selection, and tool outputs are validated against Pydantic schemas before being committed to the Project Manifest.

## Step 3 & Final (15.05 - 22.05)
- **Testing Process**: A `pytest` suite was implemented to perform unit tests on individual tools and integration tests on the full "Code-to-Doc" pipeline. 
- **Deployment**: Packaged as a CLI application with a `requirements.txt` manifest.
- **Data Porting**: Raw code files are transformed into standardized JSON schemas to ensure consistency across the toolchain.
- **Deployment Strategy**: A staged release approach is proposed, starting with local CLI execution to verify output quality before CI/CD integration.
- **Conclusion**: The Auto-Doc Agent successfully automates technical documentation, reducing documentation debt while maintaining a direct, traceable link between source code and generated reference guides.
