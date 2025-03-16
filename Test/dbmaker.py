import os

# LLM API KEY
os.environ["OPENAI_API_KEY"] = "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" # Insert LLM API KEY

from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader

import json

def jsonl_to_text(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w") as outfile:
        for line in infile:
            json_data = json.loads(line)  # Load each JSON object individually
            text_data = json.dumps(json_data, indent=4)  # Pretty-print with indentation
            outfile.write(text_data + "\n")  # Write to text file with a newline

# Example usage:
input_file = "C:\\Users\\saman\\Documents\\Year 4 Semester 1\\ECNG 3020\\Code Files\\Semantic Database\\repo\\train.jsonl"
output_file = "C:\\Users\\saman\\Documents\\Year 4 Semester 1\\ECNG 3020\\Code Files\\Semantic Database\\repo\\semantic.txt"
jsonl_to_text(input_file, output_file)


# Load and process the text files
loader = DirectoryLoader('./repo/', glob="./*.txt", loader_cls=TextLoader)
documents = loader.load()

# Splitting the text into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)


# Embed and store the texts
persist_directory = 'db'

# OpenAI embeddings 
embedding = OpenAIEmbeddings()

vectordb = Chroma.from_documents(documents=texts,
                                 embedding=embedding,
                                 persist_directory=persist_directory)

# Persist the db to disk
vectordb.persist()
vectordb = None

# Load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)

retriever = vectordb.as_retriever()

docs = retriever.get_relevant_documents("What if...?")
print(len(docs))
retriever = vectordb.as_retriever(search_kwargs={"k": 2})