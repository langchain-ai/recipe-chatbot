# Recipe Chatbot - AI Evaluations Course with LangSmith

This repository is a modified version of [evaluations course repo](https://github.com/ai-evals-course/recipe-chatbot). It's set up to walk you through the homework assignments using [LangSmith](https://smith.langchain.com/), a platform that provides best-in-class tooling for observability, evals, and more.

## Quick Start

1. **Clone & Setup**
   ```bash
   git clone https://github.com/langchain-ai/recipe-chatbot.git
   cd recipe-chatbot
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Navigate to [LangSmith](https://smith.langchain.com) and sign up for an account if you don't already have one.
   You'll need to create an API key by pressing `Settings` in the sidebar.
   
   Then, copy the `env.example` file to a `.env` file using the command below and paste the required
   secrets there, including your newly created LangSmith key:

   ```bash
   cp env.example .env
   # Edit .env to add your model and API keys
   ```

3. **Run the Chatbot**
   ```bash
   uvicorn backend.main:app --reload
   # Open http://127.0.0.1:8000
   ```

The only differences between the recipe chatbot code in this repo and the main course repo are wrapping the LiteLLM call so that it traces to LangSmith:

```python
@traceable(name="LiteLLM", run_type="llm")
def litellm_completion(model: str, messages: List[Dict[str, str]], **kwargs: Any):
    completion = litellm.completion(
        model=model,
        messages=messages,
        **kwargs,
    )
    return completion
```

And then importing and using this wrapped method instead of calling `litellm.completion` directly.

## Course Overview

### Homework Progression

This repo contains modified homework instructions that take advantage of LangSmith's platform.
Follow along using the updated `README.md` for each assignment below:

1. **HW1: Basic Prompt Engineering** ([`homeworks/hw1/README.md`](./homeworks/hw1/README.md))
   - Write system prompts and expand test queries

2. **HW2: Error Analysis & Failure Taxonomy** ([`homeworks/hw2/README.md`](./homeworks/hw2/README.md))
   - Systematic error analysis and failure mode identification
   - **Interactive Walkthrough**:
      - Code: `homeworks/hw2/hw2_solution_walkthrough.ipynb`
      - [video 1](https://youtu.be/h9oAAAYnGx4?si=fWxN3NtpSbdD55cW): walkthrough of code
      - [video 2](https://youtu.be/AKg27L4E0M8) : open & axial coding walkthrough

3. HW3: LLM-as-Judge Evaluation ([`homeworks/hw3/README.md`](./homeworks/hw3/README.md))
    - Automated evaluation using LangSmith

### Key Features

- **Backend**: FastAPI with LiteLLM (multi-provider LLM support)
- **Frontend**: Simple chat interface with conversation history
- **Annotation Tool**: FastHTML-based interface for manual evaluation (`annotation/`)
- **Retrieval**: BM25-based recipe search (`backend/retrieval.py`)
- **Query Rewriting**: LLM-powered query optimization (`backend/query_rewrite_agent.py`)
- **Evaluation Tools**: Automated metrics, bias correction, and analysis scripts

## Project Structure

```
recipe-chatbot/
├── backend/               # FastAPI app & core logic
├── frontend/              # Chat UI (HTML/CSS/JS)
├── homeworks/             # 5 progressive assignments
│   ├── hw1/               # Prompt engineering
│   ├── hw2/               # Error analysis (with walkthrough)
│   └── hw3/               # LLM-as-Judge
├── annotation/            # Manual annotation tools
├── scripts/               # Utility scripts
├── data/                  # Datasets and queries
└── results/               # Evaluation outputs
```

## Environment Variables

Configure your `.env` file with:
- `MODEL_NAME`: LLM model (e.g., `openai/gpt-4`, `anthropic/claude-3-haiku-20240307`)
- API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.

See [LiteLLM docs](https://docs.litellm.ai/docs/providers) for supported providers.

## Course Philosophy

This course emphasizes:
- **Practical experience** over theory
- **Systematic evaluation** over "vibes"
- **Progressive complexity** - each homework builds on previous work
- **Industry-standard techniques** for real-world AI evaluation
