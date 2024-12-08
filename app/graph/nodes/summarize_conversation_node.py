from langchain.schema import HumanMessage
from app.graph.state import GraphState
from app.graph.utils.time import track_execution_time
from app.graph.consts import MODEL_NAME
from langchain_google_genai import ChatGoogleGenerativeAI


@track_execution_time
def summarize_conversation_node(state: GraphState):
    state.execution_times.clear()

    if len(state.messages) > 4:
        state = summarize_conversation(state)
        messages = state.messages
    else:
        messages = state.messages

    return {
        "enhanced_query": "",
        "documents": [],
        "messages": messages,
        "generation": "",
        "execution_times": state.execution_times,
    }


def summarize_conversation(state: GraphState):
    MAX_TOKENS = 250

    # Extract content from chat history
    chat_content = "\n".join([msg.content for msg in state.messages])

    # Create our summarization prompt
    summary_message = f"""
Summarize the following conversation in a clear and concise way.

Requirements:
- Provide a brief overview of the main topics and key points
- Use simple, direct language
- Stay under {MAX_TOKENS} tokens
- Format output in Markdown
- Focus on essential information only

Input conversation:
{chat_content}

Format your response as:
# Summary
[Your concise summary here]

# Key Points
- [Point 1]
- [Point 2]
- [Point 3]
"""

    # Add prompt to our history
    summarized_messages = [HumanMessage(content=summary_message)]
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    response = llm.invoke(summarized_messages)

    messages = state.messages[-2:]
    state.messages = [
        HumanMessage(content="Here's a summary of our conversation up to this point:"),
        response,
        *messages,
    ]
    return state
