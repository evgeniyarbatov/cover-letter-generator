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

CV is the text between triple backticks. The job description is the text between <> brackets.

CV: ```{cv}```

Job description: <{job_description}>

Additional context: {context}
"""

def get_cover_letter(
    job_url, 
    cv_pdf,
    additional_pdfs,
):
    job_description = url_text(job_url)
    cv = pdf_text(cv_pdf)

    additional_text = ""
    for additional_pdf in additional_pdfs:
        additional_text += pdf_text(additional_pdf)

    documents = []
    
    documents.extend(get_documents(cv))
    documents.extend(get_documents(job_description))
    documents.extend(get_documents(additional_text))

    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(documents, embedding=embedding_function)

    llm = Ollama(
        model="llama3",
    )

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
        "query": "Write a cover letter for given CV and Job posting in a conversational style"
    })

    return result