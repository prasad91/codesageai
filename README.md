# 🚀 CodeSageAPI – Agentic Code Review with Human-in-the-Loop

**CodeSageAPI** is an intelligent, agent-powered backend reviewer for GitHub pull requests. It automatically detects and refactors code changes using AI, then enables developers to approve or edit the improvements through a human-in-the-loop (HITL) interface.

---

## ✨ Features

- ✅ Auto-triggered by GitHub pull request webhooks
- ✅ Clones and analyzes only changed Java files
- ✅ Extracts individual method blocks for focused review
- ✅ Uses OpenAI (or offline mode) to suggest clean, readable refactors
- ✅ Human-in-the-loop dashboard for approve/edit/reject
- ✅ Posts approved suggestions back as GitHub PR comments
- ✅ Offline mock mode available (no API key required)

---

## 🧱 Project Structure

```
codesageapi/
├── app.py                   # Flask webhook receiver
├── ai_agent.py              # OpenAI (or mock) code suggestions
├── code_extractor.py        # Java method extractor (brace-based)
├── github_api.py            # GitHub API interactions (diffs, comments)
├── git_tools.py             # Git clone + branch checkout
├── output/
│   ├── suggestions.json     # Raw AI suggestions
│   └── reviewed.json        # Human-reviewed results
├── send_to_github.py        # Post approved suggestions as PR comments
├── ui/
│   └── review_ui.py         # Streamlit HITL review dashboard
```

---

## 🛠️ Setup

### 1. Clone this repo & install dependencies
```bash
git clone https://github.com/your-org/codesageapi.git
cd codesageapi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up GitHub Webhook
- Start the server:
  ```bash
  python app.py
  ```
- Expose it using `ngrok`:
  ```bash
  ngrok http 5000
  ```
- Use the `https://...ngrok.io/webhook/github` as the GitHub webhook URL

---

## 🚦 Usage Flow

1. Developer opens a PR on GitHub
2. CodeSageAPI:
   - Clones the PR branch
   - Detects changed `.java` files
   - Extracts method blocks
   - Sends them to OpenAI for suggestions (or mocks them)
3. Suggestions are saved to `output/suggestions.json`

4. Run the review UI:
   ```bash
   streamlit run ui/review_ui.py
   ```
   - Developer reviews, edits, or rejects suggestions
   - Final feedback saved to `output/reviewed.json`

5. Push approved suggestions back to PR as comments:
   ```bash
   python send_to_github.py
   ```

---

## 💡 Offline Mode

No OpenAI API key? No problem.

In `ai_agent.py`, turn on mock mode:
```python
USE_OFFLINE_MOCK = True
```

The agent will return fake suggestions like:
```java
// [MOCKED] Refactored version of: ...
```

---

## 🧠 Powered By

- Python + Flask + GitPython
- OpenAI GPT-4 / GPT-3.5 (optional)
- Streamlit for Human-in-the-Loop UX
- GitHub REST API for PR diff & comments

---

## 📌 Next Enhancements (Stretch Goals)

- [ ] Auto-commit approved refactors back to the PR branch
- [ ] Memory-based agent using feedback from `reviewed.json`
- [ ] Slack/Email notifications for pending HITL reviews

---

## 📄 License

MIT — use, fork, and improve freely.

---

## 🙌 Built For
**Prasad Vavilala**  
[Prasad Vavilala](mailto:vavilala.prasad@gmail.com)
