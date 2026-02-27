# Python AI Agent

This is a command-line AI agent powered by Google Gemini that analyzes user requests, calls local tools (functions), and iteratively works toward a final response.

## Features

- **Tool Calling**: The AI can choose and execute local Python functions
- **Iterative Agent Loop**: The model reasons step-by-step until the task is complete
- **Conversation Memory**: Each iteration remembers prior messages and tool results
- **Verbose Mode**: Optional debugging output showing token usage and tool execution
- **Safe Execution**: Iteration limits prevent infinite loops and excessive token usage

## Requirements

- Python 3.x
- Google Gemini API key
- Python packages:
  - `google-genai`
  - `python-dotenv`

## Installation

No installation required! Just clone or download this repository:

```bash
git clone <your-repo-url>
cd python-ai-agent
```

Install dependencies:

```bash
pip install google-genai python-dotenv
```

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the AI assistant by providing a prompt (uv):

```bash
uv run main.py "<your prompt>"
```

Enable verbose debugging output:

```bash
uv run main.py "<your prompt>" --verbose
```

### Example

```bash
uv run main.py "how does the calculator render results to the console?"
```

### Output

The AI Code Assistant will:

- Send your prompt to Gemini
- Decide whether tools are needed
- Execute local functions when requested
- Feed results back to the model
- Produce a final response

Example verbose output:

```
User prompt: what files are in the root?

Calling function: get_files_info({})
-> {'files': ['main.py', 'functions', 'README.md']}

Response:
The project contains main.py, a functions directory, and README.md.
```

If the agent exceeds its iteration limit:

```
Error: reached maximum iterations (20) without producing a final response.
```

## Available Tools

- **get_files_info** — Lists files in a directory
- **get_file_content** — Reads file contents
- **run_python_file** — Executes a Python script
- **write_file** — Writes content to a file

Each tool includes:

- A Gemini function schema (for the model)
- A Python implementation (for execution)

## Project Structure

```
main.py              — Entry point and agent loop
call_function.py     — Tool dispatcher and execution logic
prompts.py           — System prompt instructions
functions/
├── get_files_info.py
├── get_file_content.py
├── run_python_file.py
└── write_file.py
```

## How It Works

1. User prompt is sent to Gemini.
2. The model may request a function call.
3. The tool is executed locally.
4. Tool results are added back into the conversation.
5. The model continues reasoning until a final answer is produced.
6. The agent loop runs for a maximum of 20 iterations to ensure safe execution.

## License

Open source — feel free to use and modify as you like.
