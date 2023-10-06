from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
import pickle
from PyPDF2 import PdfFileReader, PdfFileWriter,PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from config import BASE_DIR



async def send_message_to_llm(vectorstore, question: str) -> str:
    if question:
        docs = vectorstore.similarity_search(query=question, k=3)

        # openai rank lnv process
        llm = OpenAI(temperature=0.7)
        chain = load_qa_chain(llm=llm, chain_type="stuff")

        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=question)
            return response, cb

async def vectorise_file(pdf_name):

    pdf = os.path.join(BASE_DIR,'storage', f"{pdf_name}")

    if pdf.endswith('.pdf'):
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text+= page.extract_text()

        #langchain_textspliter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )

        chunks = text_splitter.split_text(text=text)

        
        #store pdf name
        store_name = pdf[:-4]
        
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl","rb") as f:
                vectorstore = pickle.load(f)
            #st.write("Already, Embeddings loaded from the your folder (disks)")
        else:
            #embedding (Openai methods) 
            embeddings = OpenAIEmbeddings()

            #Store the chunks part in db (vector)
            vectorstore = FAISS.from_texts(chunks,embedding=embeddings)

            with open(f"{store_name}.pkl","wb") as f:
                pickle.dump(vectorstore,f)
                
            return vectorstore
