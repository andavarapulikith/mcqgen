import json
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st

# Langchain packages
from langchain_community.callbacks import get_openai_callback

# Load the response JSON
with open('C:/Users\likit/mcqgen/Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("Create MCQs with ease (langchain)")

with st.form("user_inputs"):
    text_input = st.text_area("Enter the text for MCQ generation")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    st.caption("Please enter the complexity level of questions (e.g., Simple, Advanced):")
    tone = st.text_input("Complexity Level of Questions", max_chars=20)

    button = st.form_submit_button("Create MCQs")

    if button and text_input and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = text_input
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            
                            
                        else:
                            st.error("Error in the table data")
                    else:
                        st.write(response)
