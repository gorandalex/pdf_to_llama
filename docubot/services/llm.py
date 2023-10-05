from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback



def send_message_to_llm(vectorstore, question: str) -> str:
    if question:
        docs = vectorstore.similarity_search(query=question, k=3)

        # openai rank lnv process
        llm = OpenAI(temperature=0.7)
        chain = load_qa_chain(llm=llm, chain_type="stuff")

        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=question)
            return response
