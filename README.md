# OllamaExample

A demonstration project showing how to use Ollama with structured outputs in both Python and TypeScript. This example queries information about countries and enforces a specific JSON schema for the response.

## Overview

This project demonstrates:
- Using Ollama's chat API with structured output formatting
- Defining schemas using Pydantic (Python) and Zod (TypeScript)
- Streaming responses from language models
- Writing structured JSON output to files

The example requests information about several countries (Japan, Brazil, Germany, Australia, Canada) and formats the response according to a predefined schema including country name, capital, population, and form of government.

## Prerequisites

- **Ollama** must be installed and running on your system
  - Install from [ollama.com](https://ollama.com)
  - Pull the required model: `ollama pull granite4:350m`

## Python Setup

### Using pip

1. **Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the script:**

```bash
python structured-countries.py
```

### Using uv

1. **Create and activate a virtual environment:**

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**

```bash
uv pip install -r requirements.txt
# Or sync directly from pyproject.toml
uv pip sync
```

3. **Run the script:**

```bash
python structured-countries.py
```

## TypeScript Setup

### Using Bun

1. **Install dependencies:**

```bash
bun install
```

2. **Run the script:**

```bash
bun run structured-countries.ts
```

### Using Node.js

1. **Install dependencies:**

```bash
npm install
```

2. **Run the script:**

```bash
npx tsx structured-countries.ts
```

> **Note:** You may need to install `tsx` globally or as a dev dependency for Node.js:
> ```bash
> npm install -D tsx
> ```

## Output

Both implementations will:
1. Stream the model's response to stdout in real-time
2. Save the final JSON output to `structured-countries-output.json`

Example output structure:
```json
[
  {
    "country": "Japan",
    "capital": "Tokyo",
    "population": 12600000,
    "formOfGovernment": "Republicanism"
  },
  ...
]
```

## Configuration

You can modify the following parameters in either script:

- **Model**: Change `granite4:350m` to any other Ollama model you have installed
- **Temperature**: Adjust the `temperature` option for more or less creative responses (currently set to 0.2)
- **Countries**: Modify the `countries` list to query different countries
- **Seed**: Change the `seed` value for reproducible results

## Troubleshooting

- **Connection Error**: Ensure Ollama is running (`ollama serve`)
- **Model Not Found**: Pull the model with `ollama pull granite4:350m`
- **Schema Validation Errors**: The model output may occasionally not match the schema perfectly; try adjusting the temperature or using a more capable model
