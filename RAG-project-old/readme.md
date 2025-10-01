rag-k8s-assistant/
├─ data/                 # sample docs & logs to ingest
├─ ingest.py             # ingestion script (builds vector DB)
├─ app.py                # Streamlit UI (chat)
├─ api.py                # optional FastAPI server
├─ requirements.txt
├─ Dockerfile            # optional
└─ README.md
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/4799fc65-d169-4fa4-a843-9473c9201405" />



**Step 0: Create project & Python env**


mkdir rag-k8s-assistant
cd rag-k8s-assistant

create virtualenv (recommended)
python -m venv .venv
 on Windows:
.venv\Scripts\activate

**Step 1 — Prepare sample data**

Create a data/ folder and add a few files:

data/k8s_runbook.md (example):

**Step 2 — Ingestion script (ingest.py)**

Create ingest.py in project root. This script:

Loads files from data/

Splits into chunks

Creates embeddings (OpenAI)

Stores into Chroma (persisted to ./chroma_db)

**Step 3 — Build a simple QA chain (Streamlit UI)**

Run the UI
streamlit run app.py
Open http://localhost:8501
 and ask:
How to fix CrashLoopBackOff? — you should see an answer grounded in k8s_runbook.md and snippets from sample logs.
