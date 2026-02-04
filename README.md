GenAI Legal Assistant for SMEs

This app helps users understand legal risks in contract text, mainly Intellectual Property (IP) clauses.
It uses rules + AI (Groq LLM) to explain risks in simple language.

What this app can do

Accept contract text (paste or upload)

Split contract into clauses

Detect English or Hindi language

Identify IP-related clauses

Explain ownership and risk

Give SME-friendly suggestions

Generate a clean PDF report

Automatically save audit logs

What this app cannot do

It is not a lawyer

It does not give legal advice

It does not handle scanned PDFs

It does not guarantee legal accuracy

Supported inputs

Plain text

Text-based PDF

DOC / DOCX

Supported languages

English

Hindi

PDF output supports Hindi properly.

Simple example
Input clause
All intellectual property created during the project
shall belong exclusively to the Client.

Output

Ownership: Client

Risk level: High

Explanation: You lose rights to your work

Suggestion: Keep shared or retained ownership

How to run locally
pip install -r requirements.txt
streamlit run app.py


Create .env file:

GROQ_API_KEY=your_groq_key

Streamlit Cloud setup

Add this in Secrets (TOML):

GROQ_API_KEY = "your_groq_key"

Important note

This app is for contract understanding and risk screening only.
Always consult a legal professional for final decisions.
