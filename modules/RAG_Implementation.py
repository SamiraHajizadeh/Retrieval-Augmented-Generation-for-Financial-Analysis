"""
Implementing RAG

"""

from langchain.vectorstores import Chroma

class RAG:
  def __init__(self, llm, embedding, text_splitter):
    self.llm = llm
    self.embedding = embedding
    self.text_splitter = text_splitter


  def create_vector_store(self, documents):
    all_splits = self.text_splitter.split_documents(documents)
    vectordb = Chroma.from_documents(documents=all_splits, embedding=self.embedding, persist_directory="chroma_db")
    self.retriever = vectordb.as_retriever()


  def init_chain(self, chain_type="stuff"):
    self.qa = RetrievalQA.from_chain_type(
        llm=self.llm,
        chain_type=chain_type,
        retriever=self.retriever,
        return_source_documents = True,
        verbose=True)
    
  def run_rag(self, query):
      return self.qa(query)

  def run(self, documents, queries, chain_type="stuff", limiting_prompt=""):
    self.create_vector_store(documents)
    self.init_chain(chain_type)
    self.results = []
    self.contexts = []
    self.prompts = []
    for i in range(len(queries)):
        output = self.run_rag(queries[i] + limiting_prompt)
        self.results.append(output['result'])
        self.prompts.append(output['result'][:output['result'].find('Helpful Answer:')])
        self.contexts.append(output['source_documents'])
    return self.results, self.contexts, self.prompts


