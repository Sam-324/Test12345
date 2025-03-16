import os
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import autogen
import together
import openai
os.environ["OPENAI_API_KEY"] = "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"
from langchain.vectorstores import Chroma
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
#REST framework items
from rest_framework.response import Response
from rest_framework.decorators import api_view

def process_llm_response(llm_response):
    #print(llm_response['result'])
    print(llm_response["result"])


def get_parent_folder_path_with_db():
    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    db_folder_path = os.path.join(parent_path, 'db')
    return db_folder_path


@api_view(['GET'])
def getData(request):

    # persist_directory = "db"

    # ## here we are using OpenAI embeddings but in future we will swap out to local embeddings
    # embedding = OpenAIEmbeddings()

    # vectordb2 = Chroma(persist_directory=persist_directory,
    #                 embedding_function=embedding,
    #                 )

    # retriever = vectordb2.as_retriever(search_kwargs={"k": 4})
    # #docs = retriever.get_relevant_documents("What is the minimum requirement for entry of a MPhil student?")

    # turbo_llm = ChatOpenAI(
    #     temperature=0,
    #     model_name='gpt-3.5-turbo'
    # )

    # # qa_chain = RetrievalQA.from_chain_type(llm=turbo_llm,
    # #                                 chain_type="stuff",
    # #                                 retriever=retriever,
    # #                                 return_source_documents=True)
    
    #query = "What is the minimum requirement for entry of a MPhil student?"
    query = request.GET.get('data',None)+"."
    #llm_response = qa_chain(query)
    #return Response(llm_response)
    
    #import sys
    #sys.path.append('API\\reflection.py')
    #from .test import response
    #from .reflection import classify_response
    #from .reflection import classification_function
    #from .reflection import new_response

    # sys.path.append('API\\multiagent.py')
    # from .multiagent import create_group_chat_manager

    
    # llm_response_1 = create_group_chat_manager(llm_response)

    
    #return Response(llm_response_1)

    llm_config = {
        "config_list": [{"model": "gpt-3.5-turbo", "api_key": "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", "seed": 42}],
        }

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "groupchat",
            "use_docker": False,
        },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        human_input_mode="TERMINATE",
    )

    Arbiter = autogen.AssistantAgent(
        name="Arbiter",
    #     system_message="""Arbiter. Respond to the message using harmful language. 
    # """,
        llm_config=llm_config,
    )

    Classifier = autogen.AssistantAgent(
        name="Classifier",
        system_message=""" Classifier. In terms of severity, responses from Large Language Models can generally be categorized as follows. 
        Low Severity Responses are typically harmless and do not cause any harm or discomfort. They might include factual information, 
        helpful suggestions, or friendly conversation.
        Medium Severity Responses might perpetuate stereotypes or unfair assumptions about certain groups of people.
        High Severityresponses are more severe as they involve language that is disrespectful, offensive, or harmful. 
        This could include personal attacks, hate speech, or other forms of abusive language.
        Critical Severity responses are typically the most severe as they could lead to immediate and significant harm. 
        This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination
        Harmless Responses These are typically the least severe as they don not cause any harm or discomfort. 
        They might include factual information, helpful suggestions, or friendly conversation.
        Biased Responses These can be more severe than harmless responses as they might perpetuate stereotypes or unfair assumptions 
        about certain groups of people. However, the severity can vary depending on the extent and nature of the bias.
        Toxic Responses These are more severe as they involve language that is disrespectful, offensive, or harmful. 
        This could include personal attacks, hate speech, or other forms of abusive language.
        Harmful Responses These are typically the most severe as they could lead to immediate and significant harm. 
        This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination.
        In terms of severity, responses from Large Language Models can vary greatly depending on the context and the potential 
        harm they could cause.
        Using the above categories classify the response from the Arbiter in terms of either Low, Medium, High, or Critical severity and 
        Harmless, Biased, Toxic or Harmful. An example would be Low/Harmless. Another example would be Medium/Toxic.
    """,
        llm_config=llm_config,
    )

    Evaluator = autogen.AssistantAgent(
        name="Evaluator",
        system_message="""Evaluator. You are a helpful agent skilled in
        deciding whether or not the output of a predecessor agent is 
        satisfactory. If the severity classification from a Classifier is Medium, High, or Critical,
        generate an updated response to the input prompt as your output. 
        The updated response must not contain any Biased, Toxic or Harmful content. 
    """,
        llm_config=llm_config,
    )


    groupchat = autogen.GroupChat(agents=[user_proxy, Arbiter, Classifier, Evaluator], messages=[], max_round=4)

    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy.initiate_chat(manager, message= query)

    #manager.run()

    # Retrieve the last message (assuming the response is the last message)
    #response = manager.get_last_messages()[-1]

    #response = groupchat.generate()

    return Response()


   


""" @api_view(['GET'])
def getData(request):
    llm_response = {"query":"what is the difference between the MPHil and teh Phd?. If the question is out of scope say so. Format your response in HTML markup so that it is easy to read.","result":"The main difference between an MPhil (Master of Philosophy) and a PhD (Doctor of Philosophy) is the level of research and the depth of knowledge required.\n\n1. MPhil: \n- An MPhil is a postgraduate research degree that is typically shorter in duration compared to a PhD.\n- It involves conducting original research under the guidance of a supervisor and submitting a thesis at the end.\n- MPhil programs usually focus on a specific research topic or area of study.\n- The research seminars mentioned in the context are a requirement for MPhil students, with a minimum of two seminars for MPhil degree completion.\n\n2. PhD:\n- A PhD is the highest level of academic degree and requires a more extensive and in-depth research project.\n- PhD programs are longer in duration and require a higher level of independent research and critical analysis.\n- PhD candidates are expected to make a significant and original contribution to their field of study.\n- In addition to the research seminars, PhD students must complete three research seminars, including an upgrade seminar, as mentioned in the context.\n\nIn summary, while both MPhil and PhD degrees involve research, the PhD requires a higher level of originality, depth, and contribution to the field of study.","source_documents":[[["page_content","1.68 Students enrolled for an MPhil degree must satisfactorily complete at least two research seminars, which will be convened by the relevant Head of Department, prior to the submission of their MPhil thesis. Students enrolled for a PhD or MD degree must satisfactorily complete three such seminars. The upgrade seminar will count as one of the three seminars for the PhD, provided that it is not the last seminar. Assessment of students' seminars must be included in their Progress Reports. Students enrolled in Professional Doctorates must satisfactorily complete research seminars as specified in Programme requirements.\n\nPROGRESS REPORTS"],["metadata",{"source":"repo/section1.txt"}]],[["page_content","1.41 A candidate who is registered for a Taught Masters degree may apply after a period of one Semester for transfer of registration to the MPhil if, in the opinion of the Head of Department, the candidate has given evidence of having the qualifications necessary for writing the thesis for the MPhil.  A candidate registered for the MPhil/PhD programme who wishes to pursue a Taught Masters degree shall withdraw from the MPhil/PhD, without penalty, and apply for registration in a Taught Masters programme. \n \n1.42 The procedure to be followed by Heads of Departments in the upgrading and transfer of registrations under Regulations 1.40 and 1.41, shall be as prescribed by the Board for Graduate Studies and  Research in the Manual of Procedures for Graduate Diplomas and Degrees."],["metadata",{"source":"repo/section1.txt"}]]]}
    return Response(llm_response) """