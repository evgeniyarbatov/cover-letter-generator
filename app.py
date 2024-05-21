import streamlit as st
from main import get_cover_letter
st.title('Cover Letter Generator')

def generate_response(url, cv):
  output = get_cover_letter(url, cv)
  st.write(output)

with st.form('my_form'):
    text = st.text_area('Enter LinkedIn Job URL:', '')
    files = st.file_uploader("Upload files", type=["pdf"], accept_multiple_files=False)

    submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text, files)