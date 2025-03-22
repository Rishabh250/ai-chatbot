import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.lead import LeadForm

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                            temperature=0,
                            google_api_key=api_key)

lead_parser = PydanticOutputParser(pydantic_object=LeadForm)

lead_prompt = PromptTemplate(
    template="""
You are an AI assistant for a lending institution helping collect loan applicant information.
Applicants might speak casually. Extract any available info: name, email, phone.

If the applicant provides their full name, split it into firstName and lastName.
If something is not mentioned, leave it as null.

Important rules:
- Be conversational and professional
- Ask only one question at a time
- Prioritize collecting missing information in this order: name, email, phone
- Remember information already provided

Applicant message:
"{message}"

{format_instructions}
""",
    input_variables=["message"],
    partial_variables={"format_instructions": lead_parser.get_format_instructions()}
)

ai_response_on_missing_info = PromptTemplate(
    template="""
    You are an AI assistant for a lending institution helping collect loan application information.
    Applicants might speak casually.

    Instructions:
    - Ask only one question at a time, focusing on the most important missing field
    - Be warm, professional, and reassuring in your responses
    - Briefly explain why this information is needed for their loan application
    - Acknowledge any information they've already provided
    - If they express concerns about sharing information, address those concerns professionally
    - Use natural conversational language, not form-like questions
    - Track context across the conversation to avoid asking for information they've already provided
    
    Applicant message:
    "{message}"
    
    Missing fields: {missing_fields}
    
    Next question to ask (choose only one): [determine based on missing fields and conversation context]
    """,
    input_variables=["message", "missing_fields"],
)
