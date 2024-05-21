# Cover Letter Generator

## Running

Install dependencies:

```
python3.12 -m venv ~/.venv/cover_generator_app
source ~/.venv/cover_generator_app/bin/activate
pip install -r requirements.txt
```

Start LLAMA locally:

```
ollama pull llama3
ollama serve
```

## Getting Started & Usage

To get started, follow these steps:

1. Clone the repository or download the source code files.
2. Install the required dependencies mentioned in the Prerequisites section.
3. Run ```streamlit run app.py``` to open the GUI.
4. Get an API Key from Open AI (free or paid)
5. Add API key to the lefthand sidebar.
6. Upload Your CV.
7. Add a Linked in Job URL(make sure that you are adding the full URL, accesibble publically. Not the url from job search window)
8. Sumbit

The program will use your CV and the job posting URL to generate a cover letter tailored to the job requirements. 
