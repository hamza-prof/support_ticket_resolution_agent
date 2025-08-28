# agent/nodes/retriever.py
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from agent.config import OPENROUTER_API_KEY
import os

embedding = HuggingFaceEmbeddings(model_name="thenlper/gte-large")

# Preload expanded documents for demonstration
CATEGORY_DOCS = {
    "billing": [
        Document(page_content="Billing occurs monthly and invoices are sent via email."),
        Document(page_content="Refunds can only be issued with supervisor approval."),
        Document(page_content="You can update your payment method under account settings."),
        Document(page_content="Failed payments will automatically retry after 3 days."),
        Document(page_content="Discount codes must be applied before checkout is completed.")
    ],
    "technical": [
        Document(page_content="For technical issues, clear your app cache or reinstall the application."),
        Document(page_content="Version 2.1.0 fixed most known bugs from 2.0."),
        Document(page_content="Mobile login failures are often resolved by updating the app."),
        Document(page_content="If the system crashes, check the log file in your install directory."),
        Document(page_content="Some features are only available on the desktop version of the app.")
    ],
    "security": [
        Document(page_content="Security protocols include 2FA and encryption-at-rest for data."),
        Document(page_content="Do not share login credentials or recovery tokens."),
        Document(page_content="All admin access is logged and reviewed weekly."),
        Document(page_content="We comply with GDPR and follow industry-standard data protection."),
        Document(page_content="Security questions can be reset via the verified email address.")
    ],
    "general": [
        Document(page_content="We are always happy to help with account issues, preferences, or feedback."),
        Document(page_content="Support hours are Monday–Friday, 9 AM to 6 PM PST."),
        Document(page_content="Use our in-app chat to reach a support agent instantly."),
        Document(page_content="You can access tutorials and guides in the Help Center."),
        Document(page_content="Our team is trained to handle both product and account queries.")
    ]
}

FAISS_DB = {
    cat: FAISS.from_documents(docs, embedding)
    for cat, docs in CATEGORY_DOCS.items()
}

def retrieve_context(state):
    category = state["category"].lower()
    query = f"{state['subject']} {state['description']}"
    retriever = FAISS_DB.get(category, FAISS_DB["general"]).as_retriever(search_type="similarity", k=2)
    results = retriever.invoke(query)
    return {**state, "context": [doc.page_content for doc in results]}
