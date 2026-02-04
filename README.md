GenAI Legal Assistant for SMEs

This application helps small and medium enterprises (SMEs) understand legal risks in contracts, with a focus on Intellectual Property (IP) clauses.
It uses a combination of deterministic NLP rules and a GenAI model (Groq LLM) to analyze contract text and generate explanations.

Key Features
Core Capabilities

Contract text input (paste text or upload file)

Clause and sub-clause extraction

Language detection (English and Hindi)

IP clause detection using rule-based logic

Clause-level risk analysis using Groq LLM

Ownership, exclusivity, and risk scoring

Plain-language explanation of risks

SME-friendly alternative suggestions

Automatic audit logging

PDF report generation (Unicode-safe, supports Hindi)

What This App Is Designed For

First-level legal risk screening

Contract review assistance

SME contract understanding

Hackathons, demos, internal tools

Non-lawyer users who need explanations

What This App Is NOT

Not a replacement for a lawyer

Not jurisdiction-specific legal advice

Not suitable for court submission

Does not include OCR for scanned PDFs

Does not guarantee legal completeness

These are optional advanced features and can be added later.

Supported Input Formats

Plain text (paste)

Text-based PDF

DOC / DOCX (text only)

Note: Scanned PDFs are not supported unless OCR is added.

Supported Languages

English

Hindi

Internal processing can normalize Hindi for analysis.
PDF output supports Unicode, so Hindi text renders correctly.

Tech Stack

Python 3.10+

Streamlit

Groq LLM API

Rule-based NLP

ReportLab (PDF generation)

Project Structure
legal_ai_app/
│
├── app.py
├── requirements.txt
├── core/
│   ├── parser.py
│   ├── language.py
│   ├── clause_splitter.py
│   ├── ip_rules.py
│   ├── risk_engine.py
│   ├── llm_engine.py
│   └── audit.py
│
├── utils/
│   └── helpers.py
│
└── data/
    └── audit_logs.json

Environment Setup (Local)

Clone the repository

Create a virtual environment

Install dependencies

pip install -r requirements.txt


Create a .env file (for local use only)

GROQ_API_KEY=your_groq_api_key


Run the app

streamlit run app.py

Streamlit Cloud Deployment (Important)
Do NOT use .env on Streamlit Cloud

Instead, add secrets in TOML format:

GROQ_API_KEY = "gsk_your_actual_key_here"


Path:

Manage app

Settings

Secrets

The app reads the key using st.secrets.

Audit Logging Behavior

Audit log is updated automatically

User does NOT need to click any save button

Each analysis appends results to audit_logs.json

Includes clause text, risk score, and explanation

PDF Export

Generates a clean, readable PDF

Supports English and Hindi (Unicode)

No external downloads required

Uses in-memory generation for Streamlit Cloud

Limitations

No OCR for scanned documents

Risk scoring is heuristic, not legal certainty

Entity extraction is basic (extendable)

Depends on Groq API availability

Future Enhancements (Optional)

OCR support for scanned PDFs

Jurisdiction-specific rules

Clause similarity matching

Full NER (parties, amounts, dates)

Contract-level composite risk score

Standard contract templates

Disclaimer

This tool provides informational analysis only.
It does not constitute legal advice.

Always consult a qualified legal professional for final decisions.

If you want, I can also:

tailor this README for GitHub

simplify it further

add screenshots section

add architecture diagram explanation
