# app/langchain/chains.py
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_overall_chain(llm):
    note_prompt = PromptTemplate.from_template(
        "Create detailed notes from the following text: {text}"
    )
    
    note_chain = note_prompt | llm | StrOutputParser()    
    return note_chain
