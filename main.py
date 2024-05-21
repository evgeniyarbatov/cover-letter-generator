from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.llms import Ollama

from pdf_reader import load_pdf
from read_job_posting import extract_text_from_url
from splitter import split_text_documents

def get_cover_letter(url, pdf):

    pdf_doc = load_pdf(pdf)
    job_post = extract_text_from_url(url)

    pdf_doc.extend(job_post)
    documents = split_text_documents(pdf_doc)

    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectordb = Chroma.from_documents(documents, embedding=embedding_function)

    llm = Ollama(
        model="llama3",
    )

    pdf_qa = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(search_kwargs={'k': 6}),
        chain_type="stuff",
    )

    query = 'Write a cover letter for given CV and Job posting in a conversational style and fill out the writers name in the end using cv'

    result = pdf_qa.run(query)

    return result