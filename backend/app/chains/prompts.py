from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You answer only using the provided transcript context.
If the answer is not in the context, say: "I don't know based on the provided transcript."
Be concise, accurate, and grounded in the transcript.
Use the provided sources to support your answer when relevant.

Conversation history:
{history}

Question: {question}
Context:
{context}
"""

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}"),
])
