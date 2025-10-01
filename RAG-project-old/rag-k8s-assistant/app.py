# app.py
import os
from dotenv import load_dotenv
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("Set OPENAI_API_KEY in environment (or .env)")
    st.stop()

PERSIST_DIR = "chroma_db"

@st.cache_resource
def load_chain():
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(temperature=0.0)  # or use OpenAI(model="gpt-4o-mini")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

st.title("K8s Troubleshooting Assistant (RAG)")

chain = load_chain()
query = st.text_input("Ask a question about your cluster / runbooks / logs")

if st.button("Ask") and query:
    with st.spinner("Thinking..."):
        response = chain({"query": query})
        answer = response["result"] if "result" in response else response
        st.subheader("Answer")
        st.write(answer)

        if "source_documents" in response:
            st.subheader("Sources")
            for i, doc in enumerate(response["source_documents"]):
                st.markdown(f"**Source #{i+1}** - metadata: {doc.metadata}")
                st.code(doc.page_content[:800] + ("..." if len(doc.page_content) > 800 else ""))
