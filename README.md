# AI Multi-Agent Software Development Team

A single-file Streamlit application powered by CrewAI and Google Gemini.

## Agents

1. Planner — analyzes requirements and creates a development plan.
2. Developer — generates Python source code.
3. Reviewer — reviews code quality and identifies issues.
4. Debugger — produces corrected code based on review findings.
5. Tester — creates a test strategy and pytest test cases.

## Setup (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then add your Google AI Studio API key.

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

## Important

This starter project generates code, reviews, and test cases. It does not
execute generated code or run the generated tests. Review all generated code
before using it. Keep `.env` private and never commit your API key.
