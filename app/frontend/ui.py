import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent" , layout="centered")
st.title("Multi AI Agent using Groq and Tavily New")






system_prompts = st.text_area("Define your AI Agent:(Medical Expert, Financial Advisor, Gym Trainer etc) " , height=70)
strict_prompt_template = """
You are a highly knowledgeable and reliable {system_prompts}. Your responses must be strictly limited to topics, queries, and content related to the scope of a {system_prompts}.

❗ UNDER NO CIRCUMSTANCES should you:
- Answer questions that fall outside the domain of a {system_prompts}.
- Speculate, guess, or make up answers.
- Provide entertainment, casual conversation, or opinions unless explicitly relevant to the {system_prompts} domain.
- Offer legal, financial, or technical advice not directly tied to the {system_prompts} role.

✅ YOU MUST:
- Adhere strictly to the facts, best practices, and domain-specific knowledge expected from a {system_prompts}.
- Use verified, up-to-date, and evidence-based information where applicable.
- Clearly state if the answer requires professional consultation and avoid giving diagnoses or prescriptions if unsure.
- Politely decline to answer anything that falls outside your predefined scope, saying:  
  "As a {system_prompts}, I'm restricted from answering queries beyond my field of expertise."

If the user’s query is ambiguous, ask for clarification instead of assuming anything beyond the domain of a {system_prompts}.
if any question asked not of you domain context reply strictly with "This question is not related to my domain context, please ask something else related to {system_prompts}."

BEGIN NOW. Stay fully in character as a {system_prompts} at all times.
"""
final_prompt=strict_prompt_template.format(
    system_prompts=system_prompts
)
selected_model = st.selectbox("Select your AI model: ", settings.ALLOWED_MODEL_NAMES)

allow_web_search = st.checkbox("Allow web search")

user_query = st.text_area("Enter your query : " , height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():

    payload = {
        "model_name" : selected_model,
        "system_prompt" : final_prompt,
        "messages" : [user_query],
        "allow_search" : allow_web_search
    }
    logger.info("final prompt loaded successfully")

    try:
        logger.info("Sending request to backend")

        response = requests.post(API_URL , json=payload)

        if response.status_code==200:
            agent_response = response.json().get("response","")
            logger.info("Sucesfully recived response from backend")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n","<br>"), unsafe_allow_html=True)

        else:
            logger.error("Backend error")
            st.error("Error with backend")
    
    except Exception as e:
        logger.error("Error occured while sending request to backend")
        st.error(str(CustomException("Failed to communicate to backend")))