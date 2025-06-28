# Exa Helper

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-uvicorn-green?logo=fastapi)
![Instagram](https://img.shields.io/badge/Instagram-Bot-purple?logo=instagram)

---

## 🚀 Project Overview

**Exa Helper** is an AI-powered Instagram automation tool that manages comments, DMs, and user engagement using advanced AI and a simple web UI. It stores task history and data in a lightweight JSON database.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd exa_helper
   ```
2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔐 Configuration

1. **Set up your environment variables:**
   - Copy `env.example` to `.env`:
     ```bash
     cp env.example .env
     ```
   - Open `.env` and add your Instagram `USERNAME` and `PASSWORD`.

2. **(Optional) Set the DM URL:**
   - In your `.env`, add the key `DM_URL` with the link you want to DM to potential clients.

---

## 🏁 Running the App

1. **Start the backend server:**
   ```bash
   uvicorn app:app
   ```
   - Watch the terminal for logs and status updates.

2. **Open the UI:**
   - Open `uiscreen/index.html` in your browser.
   - Paste the link (DM URL) you want to send to potential clients.
   - Tap the **Play** button.
   - Keep an eye on the terminal (where `uvicorn app:app` is running) to ensure everything is working smoothly.

---

## 🗃️ Database

- `anniedb.json` is a lightweight JSON database used for storing data and task history completed by the AI.
- **Important:** Make sure to set the correct path to `anniedb.json` in `helper.py`. The AI uses this file to store and retrieve all relevant details and history. If you move or rename the file, update the path in `helper.py` accordingly.

---

## 🆘 Troubleshooting

- If you encounter any issues, glitches, or errors, please contact me directly:
  - [LinkedIn: Debdut Bhaduri](https://www.linkedin.com/in/debdut-bhaduri-32323156/)

---

## 🎬 Demo Video

*Video coming soon!*

---

## 📚 Tags

`#python` `#fastapi` `#uvicorn` `#instagram-bot` `#ai` `#automation` `#webui` `#jsondb` `#gemini` `#asyncio`

---

## ✨ Enjoy using Exa Helper! ✨
