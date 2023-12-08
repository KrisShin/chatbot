import bs4
from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from common.settings import OPENAI_API_KEY


class RAGUtil(object):
    client = None
    rag_chain = None

    @classmethod
    def set_client(cls):
        cls.client = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY, model_name="gpt-4", temperature=0
        )

    @classmethod
    def load(cls, web_paths: tuple):
        loader = WebBaseLoader(
            web_paths=web_paths,
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("post-content", "post-title", "post-header")
                )
            ),
        )
        return loader.load()

    @classmethod
    def generate_rag_chain(cls, web_paths: tuple):
        docs = cls.load(web_paths)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )
        retriever = vectorstore.as_retriever()

        prompt = hub.pull("rlm/rag-prompt")

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | cls.client
            | StrOutputParser()
        )
        return rag_chain

    @classmethod
    def invoke(cls, web_paths, question: str):
        cls.set_client()
        rag_chain = cls.generate_rag_chain(web_paths)
        answer = rag_chain.invoke(question)
        return answer


if __name__ == "__main__":
    rag_chain = RAGUtil().generate_rag_chain(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",)
    )
    x = rag_chain.invoke("What is Task Decomposition?")
    print(x)
