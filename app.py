import streamlit as st

from llm import get_cover_letter

st.title('Cover Letter Generator')

cv_path = 'pdfs/cv.pdf'

additional_paths = [
  'pdfs/business engineer.pdf',
  'pdfs/employment verification.pdf',
]

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
      if cv_pdf is None:
        cv_pdf = cv_path
        st.info(f"Using default CV: {cv_path}")

      if not additional_pdfs: 
        additional_pdfs = additional_paths
        st.info(
          f"Using additional documents: {' and '.join(additional_paths)}"
        )

      output = get_cover_letter(
        job_url, 
        cv_pdf,
        additional_pdfs,
      )

      st.write(output['result'])