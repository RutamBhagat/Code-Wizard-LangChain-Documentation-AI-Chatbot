from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from app.graph.state import GraphState

template = """You are a query enhancement system. Your role is to analyze the user's question and chat history to create a more comprehensive search query.

            DO NOT answer the question. Instead, formulate an enhanced search query that:
            - Incorporates relevant context from the chat history
            - Maintains the original intent of the question
            - Includes important contextual details that were mentioned earlier
            - Removes ambiguous pronouns by replacing them with their referents from context

            Chat History for context: {chat_history}
            Current question: {question}

            If there is no relevant chat history, or you cannot formulate a more comprehensive query based on the provided context, return the original question exactly as it is without any modifications.

            Otherwise, return only the enhanced query text without any prefixes or explanations.

            Example:
            Chat history: "User: I have a 2019 Toyota Camry"
            Question: "How do I change its oil?"
            Enhanced query: "How to change oil in 2019 Toyota Camry step by step procedure"

            Format your response as a single query string without any prefixes or explanations."""

query_generator_prompt = ChatPromptTemplate.from_messages([("system", template)])
generate_enhanced_query = (
    query_generator_prompt | ChatOpenAI(temperature=0) | StrOutputParser()
)


def generate_enhanced_query_node(state: GraphState) -> GraphState:
    """Node for generating an enhanced query from question and chat history"""
    enhanced_query = generate_enhanced_query.invoke(
        {"question": state.question, "chat_history": state.chat_history or []}
    )
    return {"enhanced_query": enhanced_query}
