import os
from langchain_chroma import Chroma  # Updated import
from langchain_ollama import OllamaEmbeddings, OllamaLLM  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
import json

# Function to convert JSONL to text
def jsonl_to_text(input_file, output_file):
    # Convert JSON file to text
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        json_data = json.load(infile)  # Load the entire JSON file
        text_data = json.dumps(json_data, indent=4)  # Pretty-print with indentation
        outfile.write(text_data)  # Write to text file

# Example usage (adjust paths as needed)
input_file = "C:\\Users\\jonat\\OneDrive\\Desktop\\final_dataset.json"
output_file = ".\\repo\\output.txt"
jsonl_to_text(input_file, output_file)
# Load and process the text files

loader = DirectoryLoader('./repo/', glob="./*.txt", loader_cls=TextLoader)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

embedding = OllamaEmbeddings(
    model="nomic-embed-text"  # You can use nomic-embed-text or any other embedding model in Ollama
)

persist_directory = 'db3'
vectordb = Chroma.from_documents(
    documents=texts,
    embedding=embedding,
    persist_directory=persist_directory
)
#vectordb.persist()



vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)

retriever = vectordb.as_retriever(search_kwargs={"k": 2})
docs = retriever.get_relevant_documents("What if...?")
print(f"Found {len(docs)} relevant documents")


