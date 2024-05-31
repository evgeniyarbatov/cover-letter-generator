import socket

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
  SentenceTransformerEmbeddings,
)
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

from utils import url_text, pdf_text, get_documents

PROMPT_TEMPLATE = """
{question}

{context}

CV is the text between triple backticks. 

Job description is between <> brackets.

CV: ```{cv}``` 

Job description: <{job_description}>
"""

def get_llm():
  hostname = socket.gethostname()
  match hostname:
    case "Evgenys-iMac.local":
      return Ollama(
          model="llama3",
      )
    case "HangLe-MacBook.local":
      return Ollama(
          model="phi3",
      )
    case _:
      raise Exception(f"{hostname} is unsupported")     

def get_cover_letter(
  job_url, 
  cv_pdf,
):
  job_description = url_text(job_url)
  cv = pdf_text(cv_pdf)

  documents = []
  documents.extend(get_documents(cv))
  documents.extend(get_documents(job_description))

  embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
  )

  vectordb = Chroma.from_documents(documents, embedding=embedding_function)

  llm = get_llm()

  prompt = PromptTemplate(
    input_variables=["context", "query"],
    template=PROMPT_TEMPLATE,
    partial_variables={
      'cv': cv,
      'job_description': job_description,
    }
  )

  qa = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True,
    chain_type="stuff", 
    chain_type_kwargs={
      "prompt": prompt,
    }
  )

  result = qa({
    "query": "Write a cover letter for given CV and Job posting in a conversational style. Make it conscise. Do not copy sentences from job description."
  })

  return result