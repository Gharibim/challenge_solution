from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from pydantic_models import JsonResponseModel

from dotenv import load_dotenv
import os

load_dotenv()

TEMPRATURE = os.getenv('TEMPRATURE')
MODEL_NAME = os.getenv('MODEL_NAME')

def generate_template(user_input, json_input, parser):
    template = '''
Given the following conversation: \n
{json_input_format} 
\n And the instructions to: {user_input_format} \n
interpret the instructions and apply them to generate a structured response in JSON format
The response format should specify actions to be taken (add, delete, modify)
with the appropriate details. For 'add' instructions, specify the message ID after which the new content should be added.
For 'delete' instructions, specify the message ID to be deleted.
For 'modify' instructions, specify the message ID and the new content.
Format the response as follows: \n" 
{format_instructions}
Based on the instructions, generate the structured response indicating the necessary modifications.
    '''

    prompt = PromptTemplate(
        input_variables=["json_input_format", "user_input_format"],
        template=template,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt.format(json_input_format=json_input, user_input_format=user_input)


def gpt_request(user_input, json_input):
    llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPRATURE)
    parser = PydanticOutputParser(pydantic_object=JsonResponseModel)
    gpt_response =  llm.invoke(generate_template(user_input, json_input, parser))
    return (parser.parse(gpt_response.content))
