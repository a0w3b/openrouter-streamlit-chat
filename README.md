# OpenRouter Streamlit Chat Application

<p align="center">
  <img src="image/ai-chat.png" alt="AI-Chat" height="300">
  &nbsp;&nbsp;&nbsp;
</p>

Author: AnssiO

This project is a chat application built using the OpenRouter API with the "openai/gpt-oss-120b" model. It features a user-friendly interface created with Streamlit, allowing users to interact with the AI model in real time.

<p align="center">
  <img src="image/streamlit.png" alt="Streamlit" height="64">
  &nbsp;&nbsp;&nbsp;
  <img src="image/openrouter.png" alt="OpenRouter" height="64">
</p>

# OpenRouter Streamlit Chat

Minimal Streamlit chat UI powered by OpenRouter.
## Table of Contents

- [OpenRouter Streamlit Chat Application](#openrouter-streamlit-chat-application)
- [OpenRouter Streamlit Chat](#openrouter-streamlit-chat)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Integration](#api-integration)
  - [Testing](#testing)
- [Docker Deployment](#docker-deployment)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Real-time chat interface
- Integration with OpenRouter API for AI responses
- User message logging
- Environment variable management for sensitive information

## Installation

Windows PowerShell + Conda:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/openrouter-streamlit-chat.git
   cd openrouter-streamlit-chat
   ```

2. Initialize Conda for PowerShell (first time only), then restart PowerShell:
   ```
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   conda init powershell
   ```

3. Create and activate the Conda environment:
   ```
   conda create -n openrouter-chat python=3.11 -y
   conda activate openrouter-chat
   ```

4. Install dependencies:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Configure environment variables (choose one):

   - PowerShell (for current session):
     ```
     $env:API_KEY = "sk-or-..."           # Your OpenRouter API key
     $env:MODEL  = "openai/gpt-oss-120b"  # Default model used by the app
     ```

   - Or create a .env file in the project root:
     ```
     API_KEY=sk-or-...
     MODEL=openai/gpt-oss-120b
     ```

## Usage

Run the Streamlit app:
```
streamlit run src/app.py
```
Open http://localhost:8501 in your browser.

## API Integration

The app uses the OpenAI SDK configured for OpenRouter in src/api/openrouter_client.py:
- Base URL: https://openrouter.ai/api/v1
- Model: openai/gpt-oss-120b (configurable via MODEL or OPENROUTER_MODEL)
- Optional headers for rankings: HTTP-Referer and X-Title (config via env)

## Testing

Run tests:
```
pytest -q
```


# Docker Deployment

This guide shows how to build and run the Streamlit + OpenRouter app using:
- Manual environment variables (no .env file)
- A .env file (based on .env.example)
- Docker Compose

Prerequisites
- Docker Desktop on Windows
- OpenRouter API key

Build the image (no .env required)
```powershell
docker build -t openrouter-streamlit-chat:latest .
```

Run with manual environment variables (no .env)
```powershell
# Set env vars for this PowerShell session
$env:API_KEY="sk-or-..." ; $env:MODEL="openai/gpt-oss-120b"

# Run detached, bind host to localhost only
docker run -d --name openrouter-chat --restart unless-stopped `
  -p 127.0.0.1:8501:8501 `
  -e API_KEY `
  -e MODEL `
  openrouter-streamlit-chat:latest
```

Run with an .env file
1) Copy the example, then edit values:
```powershell
Copy-Item -Path ..\.env.example -Destination ..\.env
notepad ..\.env
```
2) Use docker run with --env-file:
```powershell
docker run -d --name openrouter-chat --restart unless-stopped `
  -p 127.0.0.1:8501:8501 `
  --env-file ..\.env `
  openrouter-streamlit-chat:latest
```

Using Docker Compose
- Create docker-compose.yml (root or reuse existing). Example below binds to localhost on the host and uses runtime env vars or a .env in the same directory.

```yaml
# Save as docker-compose.yml at the repository root
services:
  app:
    build:
      context: .
      dockerfile: ./Dockerfile
    image: openrouter-streamlit-chat:latest
    # Host binding limited to localhost
    ports:
      - "127.0.0.1:8501:8501"
    # Option A: supply from your shell (preferred for secrets)
    environment:
      API_KEY: ${API_KEY}
      MODEL: ${MODEL:-openai/gpt-oss-120b}
      STREAMLIT_SERVER_HEADLESS: "true"
      STREAMLIT_SERVER_ADDRESS: "0.0.0.0"
      STREAMLIT_SERVER_PORT: "8501"
    # Option B: or use an .env file placed next to docker-compose.yml
    # env_file:
    #   - ./.env
    restart: unless-stopped
```

Compose commands
```powershell
# Manual env in shell
$env:API_KEY="sk-or-..." ; $env:MODEL="openai/gpt-oss-120b"
docker compose up -d --build

# View logs / stop
docker compose logs -f
docker compose down
```

Open the app
- http://127.0.0.1:8501


## Contributing

Issues and PRs are welcome.

## License

MIT License — see LICENSE.

