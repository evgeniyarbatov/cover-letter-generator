import streamlit as st

from llm import get_cover_letter

st.set_page_config(page_title="LLM")

st.title('Cover Letter Generator')

cv_path = 'pdfs/cv.pdf'

with st.form('my_form'):
    job_url = st.text_area('LinkedIn URL:', '')

    cv_pdf = st.file_uploader(
      "CV", 
      type=["pdf"], 
      accept_multiple_files=False
    )

    submitted = st.form_submit_button('Submit')
  
    if submitted:
      if cv_pdf is None:
        cv_pdf = cv_path
        st.info(f"Using default CV: {cv_path}")

      output = get_cover_letter(
        job_url, 
        cv_pdf,
      )

      st.write(output['result'])