from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

from app.chains.prompts import PROMPT_TEMPLATE
from app.chains.retrieval_chain import format_docs, get_session_retriever, get_source_docs
from app.config import settings


def get_llm():
    if settings.llm_provider == "google":
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY is missing.")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=settings.llm_model, api_key=settings.google_api_key)
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing.")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=settings.llm_model, api_key=settings.openai_api_key)
    if settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is missing.")
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=settings.llm_model, api_key=settings.anthropic_api_key)
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")


def build_rag_chain(session_id: str):
    retriever = get_session_retriever(session_id)
    llm = get_llm()

    retrieval_chain = RunnableParallel(
        {
            "question": RunnablePassthrough(),
            "history": lambda x: x.get("history", []),
            "context_docs": lambda x: retriever.invoke(x["question"]),
        }
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You answer only using the provided transcript context. If the answer is not in the context, say: 'I don't know based on the provided transcript.' Be concise, accurate, and grounded in the transcript. Use the provided sources to support your answer when relevant.\n\nConversation history:\n{history}\n\nQuestion: {question}\nContext:\n{context}"),
        ("human", "{question}"),
    ])

    def compose_result(inputs):
        docs = inputs["context_docs"]
        history = inputs.get("history", [])
        history_text = "\n".join(f"{item.get('role', 'user')}: {item.get('content', '')}" for item in history)
        context_text = format_docs(docs)
        sources = get_source_docs(docs)
        return {
            "question": inputs["question"],
            "history": history_text,
            "context": context_text,
            "sources": sources,
        }

    answer_chain = (
        retrieval_chain
        | RunnableLambda(compose_result)
        | prompt
        | llm
        | StrOutputParser()
    )

    def chain(question: str, history: list[dict[str, str]] | None = None):
        answer = answer_chain.invoke({"question": question, "history": history or []})
        docs = retriever.invoke(question)
        sources = get_source_docs(docs)
        return {"answer": answer, "sources": sources}

    return chain
