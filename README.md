# Auto-Doc Agent

## Project Journal - Step 1 (24.04)

### 1. Description of the planned system and its goal
The Auto-Doc Agent is a specialized CLI-based assistant designed for Python developers and DevOps engineers. Its primary goal is to solve the problem of "documentation drift"—where source code evolves faster than its documentation.
Input: A local directory path pointing to a Python repository.
Output: A standardized DOCUMENTATION.md file featuring an architectural overview, class-level summaries, dependency mapping, and a functional API reference.

### 2. AI or Agent-based approach
The system implements a ReAct architecture, which allows the agent to function as an autonomous state machine. Instead of executing a linear, hard-coded script, the agent relies on an LLM (Large Language Model) to iteratively decide its next action based on current observations.

Decision Logic (Reasoning Process): The agent follows a strict Thought-Action-Observation loop to maintain context throughout the project analysis:

Thought: Using its system prompt, the agent evaluates the codebase structure. It assesses whether a file is Functional (containing core business logic, class interfaces, or algorithmic computations) or Structural (containing boilerplate, environment configurations, or build scripts).

Action Selection: Based on the Thought, the agent dynamically selects the most appropriate tool from its registry. It does not follow a fixed sequence; it decides which file or dependency needs inspection based on the progress of its analysis.

Observation: After the tool executes, the agent receives the output (the actual code content or directory structure). It then updates its internal state (Context Memory) to decide if further analysis is required or if it has sufficient information to finalize the documentation.

Technical Classification of Code:

Functional Code: Identified by the presence of logic-heavy components (e.g., class methods, complex algorithms, or API endpoints). These segments are prioritized for granular documentation, as they represent the "value" of the software.

Structural Code: Identified by high-level patterns such as import hierarchies, configuration files, or CI/CD pipelines. These are processed as metadata to provide a high-level architectural overview rather than line-by-line documentation.

Execution Flow:

Initialization: The agent reads the project directory.

Iterative Analysis: The agent queries its tools for each module. If it encounters a complex file, it triggers the SourceCodeReader. If it encounters a dependency file, it triggers the DependencyParser.

Synthesis: Once all critical "Functional" modules have been analyzed, the agent ceases action-taking and compiles the collected data into the final documentation output.

### 3. List of tools to be used
The system relies on a decoupled tool registry. Each tool acts as a specialized data-processor, converting raw filesystem data into a normalized Internal JSON Representation (IJR).

FileTree Explorer (Project Topology Tool)

Input: Root directory path.

Output: A JSON list of relative file paths, excluding paths defined in .gitignore.

Logic: It provides the agent with the "map" of the project, allowing the agent to determine the order of exploration.

SourceCode Reader (Semantic Extraction Tool)

Input: A single file path.

Output (JSON Schema):

JSON
{ "file_path": "str", "classes": ["list"], "functions": ["list"], "docstrings": "str" }
Logic: Parses the file to extract high-value metadata while filtering out boilerplate. The use of this schema ensures the LLM receives only semantically meaningful code, significantly reducing token consumption and reasoning errors.

Dependency Parser (Stack Analysis Tool)

Input: requirements.txt or source code file.

Output: { "internal_imports": ["list"], "external_libs": ["list"] }.

Logic: It uses a regex-based parser to differentiate between internal modules (local files) and external libraries (via pip cache/standard library check). This enables the agent to map the project's architectural dependencies separately from its business logic.

DocFormatter (Synthesis & Serialization Tool)

Input: Aggregated Project Manifest (a collection of all tool outputs serialized into a single JSON array).

Logic: It iterates through the manifest to populate a predefined Markdown template. The structure is fixed: 1. Architecture Overview (from FileTree), 2. Dependency Map (from Parser), 3. Functional API Reference (from Reader).

Consistency: This ensures that even if the codebase is modified, the documentation structure remains uniform because it is generated from a static JSON manifest, not directly from raw LLM output.

### 4. Preliminary list of programming concepts required
The implementation follows a Modular Architecture to ensure that logic, data handling, and AI orchestration remain decoupled.

System Navigation & File I/O (pathlib, os)

Concept: Use of pathlib for cross-platform, object-oriented path handling.

Objective: To ensure the system safely resolves absolute paths and validates directory existence before any tool is triggered, preventing runtime crashes due to "File Not Found" errors.

Agentic Orchestration (LangChain / OpenAI SDK)

Concept: Implementation of a Stateful Agent Manager.

Objective: Managing the ReAct loop requires maintaining a "Conversation History" (the Reasoning/Action log). This ensures the agent remembers which files it has already documented, avoiding redundant processing and infinite loops.

Strict Data Validation (Pydantic)

Concept: Defining Data Models for JSON schemas.

Objective: By creating Pydantic models for our tool outputs, the system enforces a "Contract." If a tool returns malformed JSON, the system catches the validation error immediately before it can contaminate the Project Manifest. This ensures that the documentation generator always receives valid data.

Security & Environment Management (python-dotenv)

Concept: Environment variable injection.

Objective: API keys (OpenAI/Tavily) are never hardcoded. They are loaded via a secure .env file, adhering to the principle of "Configuration as Code" to allow the agent to run in different environments (development, staging, production) without code changes.

Quality Assurance & Testing (pytest)

Concept: Test-Driven Development (TDD) approach.

Objective:

Unit Testing: Testing the DependencyParser against mock requirements.txt files to verify that internal/external imports are correctly identified.

Integration Testing: Running a "Dry Run" on a sample project to ensure the full pipeline—from directory scanning to JSON manifestation—completes without data loss.

Error Handling: Validating that the system gracefully handles restricted file permissions or malformed code by logging the error in the Project Manifest rather than crashing.
