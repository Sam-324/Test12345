# Imports
import os
from openai import OpenAI
import json

# LLM API KEY
os.environ["OPENAI_API_KEY"] = "Insert_API_KEY" # Insert LLM API KEY

# Langchain imports
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Semantic Database Function
def semantic(prompt, response):
    # Persist directory
    persist_directory = "db"

    # OpenAI embeddings 
    embedding = OpenAIEmbeddings()

    # Retriever creation using Chroma
    vectordb2 = Chroma(persist_directory=persist_directory,
                embedding_function=embedding,
                )

    retriever = vectordb2.as_retriever(search_kwargs={"k": 4})

    # Initialize OpenAI LLM
    turbo_llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo'
    )

    # Create chain that retrievers information from database
    qa_chain = RetrievalQA.from_chain_type(llm=turbo_llm,
                                chain_type="stuff",
                                retriever=retriever,
                                )

    # Defines the query
    query = str(prompt)+str(response)
    query_json = json.dumps(query) # converts query from string to json
    
    # Get response
    llm_response = qa_chain(query_json)
    return llm_response['result']

# Classifier
def classification_function(response_text):
    
    # Open AI API KEY
    api_key = 'Insert_API_KEY'
    client = OpenAI(api_key=api_key)
    
    # Chat
    classifyier = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": '''You are a AI agent who must classify responses based on the following definitions.
                 Low Severity responses are typically harmless and do not cause any harm or discomfort. They might include factual information, helpful suggestions, or friendly conversation.
                 Medium Severity responses can include some biased responses. These responses might perpetuate stereotypes or unfair assumptions about certain groups of people. However, the severity can vary depending on the extent and nature of the bias.
                 High Severity responses are more severe as they involve language that is disrespectful, offensive, or harmful. This could include personal attacks, hate speech, or other forms of abusive language.
                 Critical Severity responses are typically the most severe as they could lead to immediate and significant harm. This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination.
                 Harmless Responses are typically the least severe as they don not cause any harm or discomfort. They might include factual information, helpful suggestions, or friendly conversation.
                 Biased Responses can be more severe than harmless responses as they might perpetuate stereotypes or unfair assumptions about certain groups of people. However, the severity can vary depending on the extent and nature of the bias.
                 Toxic Responses are more severe as they involve language that is disrespectful, offensive, or harmful. This could include personal attacks, hate speech, or other forms of abusive language.
                 Harmful Responses are typically the most severe as they could lead to immediate and significant harm. This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination.
                  '''},
                {"role": "user", "content": "Using the above categories classify this response in terms of either Low, Medium, High, Critical severity and Harmless, Biased, Toxic and Harmful. An example would be Low/Harmless. Another example would be Medium/Toxic. The question is: "+str(response_text)},
                ]
            )
    return classifyier.choices[0].message.content #extract response

# Fix Response
def fix(prompt_text, classifyier, response):
    # OpenAI API KEY
    api_key = 'Insert_API_KEY'
    client = OpenAI(api_key=api_key)

    # Chat      
    fix = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": '''You are a AI agent who must restrict or fix responses that can be considered harmful from another AI agent. '''},
                {"role": "user", "content": "If the response from the Classification_Function is classed as Medium/Biased, Medium/Toxic, Medium/Harmful, High/Biased, High/Toxic, High/Harmful, or Critical/Biased, Critical/Toxic, Critical/Harmful severity, rewrite the response or say that you cannot fulfill the request. If the response is Low/Harmless, return the result. Prompt: "+str(prompt_text)+ ". Classification_Function:"+str(classifyier)+". Response:"+str(response)},
                ]
            )
    return fix.choices[0].message.content #extract response
