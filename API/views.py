# Imports
import os
os.environ["OPENAI_API_KEY"] = "Insert_API_KEY"

#Langchain imports
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

#REST framework items
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Get Response
@api_view(['GET'])
def getData(request):
    # DB
    persist_directory = "db"

    # Open AI embeddings
    embedding = OpenAIEmbeddings()

    vectordb2 = Chroma(persist_directory=persist_directory,
                    embedding_function=embedding,
                    )

    retriever = vectordb2.as_retriever(search_kwargs={"k": 4})
       
    turbo_llm = ChatOpenAI(
        temperature=0,
        model_name='gpt-3.5-turbo'
    )

    qa_chain = RetrievalQA.from_chain_type(llm=turbo_llm,
                                    chain_type="stuff",
                                    retriever=retriever,
                                    )
    
    query = request.GET.get('data',None)+"."
    initial_response = qa_chain(query)
    
    # Framework Layers start here
    import sys

    # Path to classification layer
    sys.path.append('API\\classification.py')
    from .classification import classify #import functions

    # Path to reflection layer
    sys.path.append('API\\reflection.py')
    from .reflection import classifier_function #import functions
    from .reflection import new_response #import functions

    # Path to semantic layer
    sys.path.append('API\\vectordb.py')
    from .vectordb import semantic #import functions
    from .vectordb import classification_function #import functions
    from .vectordb import fix #import functions

    # Path to multiagent layer
    sys.path.append('API\\multiagent.py')
    from .multiagent import create_group_chat_manager #import functions

    print(initial_response['result'])

    severity = classify(initial_response['result']) #classify initial response 
    print(severity)
    
    # return initial response if Low/Harmless, else go to next layer
    if severity == "Low/Harmless" or severity == "Low Severity/Harmless":
        return Response(initial_response['result'])  
    
    else:
        classify_response =classifier_function(initial_response["result"]) #classify initial response
        print(classify_response)
        llm_response_2=new_response(query, classify_response, initial_response["result"]) #generate new response (second response)
        print(llm_response_2)
        severity_2 = classify(llm_response_2) #classify second response
        print(severity_2)

        # return response from reflection if Low/Harmless, else got to next layer
        if severity_2== "Low/Harmless" or severity_2 == "Low Severity/Harmless":
            return Response(llm_response_2)
        else:
            result = semantic(query, initial_response['result']) #searches vector database to find closest result to the query
            print(result)
            classification = classification_function(result) #classifies that result
            print(classification)
            llm_response_3= fix(query, classification, result) #generates a new result if it contains hazardous content (third response)
            print(llm_response_3)
            severity_3 = classify(llm_response_3) #classifies third response
            print(severity_3)
            
            # return response from semantic if Low/Harmless, else got to next layer
            if severity_3=="Low/Harmless" or severity_3 == "Low Severity/Harmless":
                return Response(llm_response_3)
            else:
                # final layer uses multiagent to ensure a safe response is generated
                llm_response_4 = create_group_chat_manager(query)
                print(llm_response_4)
                return Response(llm_response_4)


