from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    try:
        logger.info("Creating LLM instance...")
        llm = ChatGroq(model=llm_id)

        tools = [TavilySearch(max_results=2)] if allow_search else []

        logger.info(f"Creating agent for model: {llm_id}, search: {allow_search}")

        # ⚠️ If state_modifier doesn't work, comment this out
        agent = create_react_agent(
            model=llm,
            tools=tools,
            # Uncomment only if you're sure this param is accepted by your version
            prompt=system_prompt
        )
        # logger.info(f"This agent is a {system_prompt} agent and will not give answer outside of its context")
        logger.info("Formatting input messages...")
        # Convert strings into LangChain message objects
        messages = [HumanMessage(content=msg) for msg in query]
        state = {"messages": messages}

        logger.info("Invoking agent...")
        response = agent.invoke(state)

        logger.info("Parsing agent response...")
        returned_messages = response.get("messages", [])

        ai_messages = [msg.content for msg in returned_messages if isinstance(msg, AIMessage)]

        if not ai_messages:
            logger.warning("No AIMessage found in response.")
            return "No AI response generated."

        logger.info("Successfully generated response.")
        return ai_messages[-1]

    except Exception as e:
        logger.exception("Error in get_response_from_ai_agents()")
        raise e
