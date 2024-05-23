import streamlit as st

from llm import get_cover_letter

st.title('Cover Letter Generator')

with st.form('my_form'):
    job_url = st.text_area('LinkedIn URL:', '')

    cv_pdf = st.file_uploader(
      "CV", 
      type=["pdf"], 
      accept_multiple_files=False
    )

    additional_pdfs = st.file_uploader(
      "Additional documents", 
      type=["pdf"], 
      accept_multiple_files=True,
    )

    submitted = st.form_submit_button('Submit')
  
    if submitted:
      output = get_cover_letter(
        job_url, 
        cv_pdf,
        additional_pdfs,
      )

      st.write(output['result'])