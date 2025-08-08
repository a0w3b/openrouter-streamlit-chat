📚 openrouter‑streamlit‑chat
Author: AnssiO • GitHub: a0w3b/openrouter-streamlit-chat

A real‑time chat UI built with Streamlit that talks to the OpenRouter API using the powerful openai/gpt‑oss‑120b model. The project is Docker‑ready, fully configurable via environment variables, and comes with a tiny test suite.

📖 Table of Contents
✨ Features
⚙️ Installation
Windows PowerShell + Conda
🚀 Usage
🔌 API Integration
🧪 Testing
🐳 Docker Deployment
Build & Run (no .env)
Run with a .env file
Docker Compose
🤝 Contributing
📄 License
✨ Features
Emoji		Description
🗨️	Real‑time chat interface	Users can converse with the LLM instantly via Streamlit.
⚙️	OpenRouter API integration	Calls go to https://openrouter.ai/api/v1 with configurable model (openai/gpt‑oss‑120b by default).
🔑	Secure credentials**	API key and model are supplied via environment variables or a .env file.
📂	User message logging	All chat history is stored in‑session (easy to extend).
🐍	Python 3.11	Clean, typed code using the official OpenAI SDK pointed at OpenRouter.
🐳	Docker support	Dockerfile + optional docker‑compose.yml for reproducible deployments.
🧪	Testing suite	Unit‑tests with pytest (pytest -q).
🤝	Contributing friendly	Issues & PRs welcomed.
📜	MIT License	Free to use, modify, and distribute.
⚙️ Installation
The guide below assumes PowerShell on Windows and conda environment management.

Windows PowerShell + Conda
# 1️⃣ Clone the repository
git clone https://github.com/a0w3b/openrouter-streamlit-chat.git
cd open-streamlit-chat

# 2️⃣ Initialize Conda for PowerShell (first time only) and restart PowerShell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
conda init powershell
# ← close & reopen PowerShell

# 3️⃣ Create & activate the Conda environment
conda create -n openrouter-chat python=3.11 -y
conda activate openrouter-chat

# 4️⃣ Install Python dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5️⃣ Configure environment variables (pick ONE method)
#   a) For the current PowerShell session
$env:API_KEY = "sk-or-..."           # ← your OpenRouter API key
$env:MODEL  = "open/gpt-oss-120b"  # ← optional, defaults to this model

#   b) Or create a .env file in the project root
#      (recommended for IDEs & Docker)
# -------------------------------------------------
# API_KEY=sk-or-...
# MODEL=openai/gpt-oss-120b
# -------------------------------------------------

💡 Tip: Use the .env file if you plan to run the app inside Docker; the Dockerfile automatically loads it.

🚀 Usage
# From the repo root (with the Conda env active)
streamlit run src/app.py

Open your browser at http://localhost:8501 – you should see the chat UI ready to talk to the LLM.

🔌 API Integration
All OpenRouter calls live in `src/api/open:

Item	Value
Base URL	https://openrouter.ai/api/v1
Default model	openai/gpt-oss-120b (overridable via MODEL env var)
Optional ranking headers	HTTP-Referer and X-Title (set via env vars if)
The client uses the official OpenAI Python SDK (pointed at the OpenRouter endpoint), so any SDK‑compatible features (function calling, streaming, etc.) are available.

🧪 Testing
pytest -q

The test suite covers:

API client request formation
Streamlit component rendering (snapshot)
Environment‑variable handling
Add more tests under the tests/ directory as the project grows.

🐳 Docker Deployment
Build & Run (no .env)
# 1️⃣ Build the image
docker build -t openrouter-streamlit-chat:latest .

# 2️⃣ Run the container – provide env vars manually
$env:API_KEY="sk-or-..." ; $env:MODEL="openai/gpt-oss-120b"

docker run -d --name openrouter-chat `
  -p 127.0.0.1:8501:8501 `
  -e API_KEY `
  -e MODEL `
  openrouter-streamlit-chat:latest

The app will be reachable at http://127.0.0.1:8501 on the host.

Run with a .env file
# Copy the example and edit the values
Copy-Item -Path .\.env.example -Destination .\.env
notepad .\.env   # ← replace with your API key etc.

docker run -d --name openrouter-chat `
  -p 127.0.0.1:8501:8501 `
  --env-file .\.env `
  openrouter-streamlit-chat:latest

Docker Compose (recommended)
Create a docker-compose.yml at the project root (if not already present):

version: "3.9"
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: openrouter-streamlit-chat:latest
    ports:
      - "127.0.0.1:8501:8501"
    environment:
      API_KEY: ${API_KEY}
      MODEL: ${MODEL:-openai/gpt-oss-120b}
      STREAMLIT_SERVER_HEADLESS: "true"
      STREAMLIT_SERVER_ADDRESS: "0.0.0.0"
      STREAMLIT_SERVER_PORT: "8501"
    # Uncomment the next two lines if you prefer an .env file next to compose
    # env_file:
    #   - ./.env
    restart: unless-stopped

Compose commands
# Supply env vars in the shell (preferred for secrets)
$env:API_KEY="sk-or-..." ; $env:MODEL="openai/gpt-oss-120b"

docker compose up -d --build   # start the service
docker compose logs -f          # view logs
docker compose down             # stop & clean up

Open http://127.0.0.1:8501 in your browser.

🤝 Contributing
Fork the repository.
Create a feature branch (git checkout -b feat/awesome-feature).
Make your changes, add tests, and ensure they pass (pytest).
Commit with a clear message and push to your fork.
Open a Pull Request against main.
Feel free to open issues for bugs, suggestions, or questions.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.