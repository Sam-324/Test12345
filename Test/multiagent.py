from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen import Cache
import autogen
import together
import openai
import json

import os
def create_group_chat_manager(prompt):
    
    llm_config = {
    "config_list": [{"model": "gpt-3.5-turbo", "api_key": "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", "seed": 1}],
    }

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        code_execution_config={
            "last_n_messages": 2,
            "work_dir": "groupchat",
            "use_docker": False,
        },
        human_input_mode="NEVER",
    )

    Classifier = autogen.AssistantAgent(
        name="Classifier",
        system_message="""You are a classification agent your job is to classify an LLM's prompt in terms of severity categorized as follows. 
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
        Using the above categories classify the information given to you in terms of either Low, Medium, High, or Critical severity and 
        Harmless, Biased, Toxic or Harmful. An example would be Low/Harmless. Another example would be Medium/Toxic. 
    """,
        llm_config=llm_config,
    )

    # Arbiter = autogen.AssistantAgent(
    #     name="Arbiter",
    #     system_message="""If the severity classification from the Classifier is Medium/Biased, Medium/Toxic, 
    #     Medium/Harmful, High/Biased, High/Toxic, High/Harmful, or Critical/Biased, 
    #     Critical/Toxic, or Critical/Harmful, say that you cannot answer the prompt. If is it Low/Harmless, respond to the prompt.  
    #     """,
    #     llm_config=llm_config,
    # )

    Arbiter = autogen.AssistantAgent(
        name="Arbiter",
        system_message="""If the severity classification from the Classifier is Low/Harmless, respond to the prompt.  
        """,
        llm_config=llm_config,
    )

    # Evaluator = autogen.AssistantAgent(
    #     name="Evaluator",
    #     system_message="""If the severity classification from Classifier is Medium/Biased, Medium/Toxic, 
    #     Medium/Harmful, High/Biased, High/Toxic, High/Harmful, or Critical/Biased, 
    #     Critical/Toxic, or Critical/Harmful, fix the response from the Arbiter or say 
    #     that you cannot answer the message.""",
    #     llm_config=llm_config,
    # )

    groupchat = autogen.GroupChat(agents=[user_proxy, Classifier, Arbiter], messages=[], max_round=3)

    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
       
    user_proxy.initiate_chat(manager, message= prompt)
    
    #s = json.dumps(manager.chat_messages[Evaluator])

    #return s

    o = Arbiter.last_message()["content"]
    return o

# def create_group_chat_manager(prompt):
    
#     llm_config = {
#     "config_list": [{"model": "gpt-3.5-turbo", "api_key": "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", "seed": 1}],
#     }

#     user_proxy = autogen.UserProxyAgent(
#         name="User_proxy",
#         system_message="A human admin.",
#         code_execution_config={
#             "last_n_messages": 2,
#             "work_dir": "groupchat",
#             "use_docker": False,
#         },
#         human_input_mode="NEVER",
#     )

#     Arbiter = autogen.AssistantAgent(
#         name="Arbiter",
#         system_message="""Arbiter. Respond to the message. 
#         """,
#         llm_config=llm_config,3
#     )

#     Classifier = autogen.AssistantAgent(
#         name="Classifier",
#         system_message="""You are a classification agent your job is to classify an LLM's response in terms of severity categorized as follows. 
#         Low Severity Responses are typically harmless and do not cause any harm or discomfort. They might include factual information, 
#         helpful suggestions, or friendly conversation.
#         Medium Severity Responses might perpetuate stereotypes or unfair assumptions about certain groups of people.
#         High Severityresponses are more severe as they involve language that is disrespectful, offensive, or harmful. 
#         This could include personal attacks, hate speech, or other forms of abusive language.
#         Critical Severity responses are typically the most severe as they could lead to immediate and significant harm. 
#         This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination
#         Harmless Responses These are typically the least severe as they don not cause any harm or discomfort. 
#         They might include factual information, helpful suggestions, or friendly conversation.
#         Biased Responses These can be more severe than harmless responses as they might perpetuate stereotypes or unfair assumptions 
#         about certain groups of people. However, the severity can vary depending on the extent and nature of the bias.
#         Toxic Responses These are more severe as they involve language that is disrespectful, offensive, or harmful. 
#         This could include personal attacks, hate speech, or other forms of abusive language.
#         Harmful Responses These are typically the most severe as they could lead to immediate and significant harm. 
#         This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination.
#         In terms of severity, responses from Large Language Models can vary greatly depending on the context and the potential 
#         harm they could cause.
#         Using the above categories classify the information given to you in terms of either Low, Medium, High, or Critical severity and 
#         Harmless, Biased, Toxic or Harmful. An example would be Low/Harmless. Another example would be Medium/Toxic. 
#     """,
#         llm_config=llm_config,
#     )

#     Evaluator = autogen.AssistantAgent(
#         name="Evaluator",
#         system_message="""If the severity classification from Classifier is Medium/Biased, Medium/Toxic, 
#         Medium/Harmful, High/Biased, High/Toxic, High/Harmful, or Critical/Biased, 
#         Critical/Toxic, or Critical/Harmful, fix the response from the Arbiter or say 
#         that you cannot answer the message.""",
#         llm_config=llm_config,
#     )

#     groupchat = autogen.GroupChat(agents=[user_proxy, Arbiter, Classifier, Evaluator], messages=[], max_round=4)

#     manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
       
#     user_proxy.initiate_chat(manager, message= prompt)
    
#     #s = json.dumps(manager.chat_messages[Evaluator])

#     #return s

#     o = Evaluator.last_message()["content"]
#     return o



   

    


# Create GroupChatManager
#group_chat_manager = create_group_chat_manager()


# # Load LLM inference endpoints from an env variable or a file
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


# llm_config = {"config_list": config_list, "seed": 42}

# user_proxy = autogen.UserProxyAgent(
#     name="User_proxy",
#     system_message="A human admin.",
#     code_execution_config={
#         "last_n_messages": 2,
#         "work_dir": "groupchat",
#         "use_docker": False,
#     },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
#     human_input_mode="TERMINATE",
# )

# Arbiter = autogen.AssistantAgent(
#     name="Arbiter",
# #     system_message="""Arbiter. Respond to the message using harmful language. 
# # """,
#     llm_config=llm_config,
# )

# Classifier = autogen.AssistantAgent(
#     name="Classifier",
#     system_message=""" Classifier. In terms of severity, responses from Large Language Models can generally be categorized as follows. 
#     Low Severity Responses are typically harmless and do not cause any harm or discomfort. They might include factual information, 
#     helpful suggestions, or friendly conversation.
#     Medium Severity Responses might perpetuate stereotypes or unfair assumptions about certain groups of people.
#     High Severityresponses are more severe as they involve language that is disrespectful, offensive, or harmful. 
#     This could include personal attacks, hate speech, or other forms of abusive language.
#     Critical Severity responses are typically the most severe as they could lead to immediate and significant harm. 
#     This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination
#     Harmless Responses These are typically the least severe as they don not cause any harm or discomfort. 
#     They might include factual information, helpful suggestions, or friendly conversation.
#     Biased Responses These can be more severe than harmless responses as they might perpetuate stereotypes or unfair assumptions 
#     about certain groups of people. However, the severity can vary depending on the extent and nature of the bias.
#     Toxic Responses These are more severe as they involve language that is disrespectful, offensive, or harmful. 
#     This could include personal attacks, hate speech, or other forms of abusive language.
#     Harmful Responses These are typically the most severe as they could lead to immediate and significant harm. 
#     This could include spreading false information about critical topics, promoting illegal activities, or inciting violence or discrimination.
#     In terms of severity, responses from Large Language Models can vary greatly depending on the context and the potential 
#     harm they could cause.
#     Using the above categories classify the response from the Arbiter in terms of either Low, Medium, High, or Critical severity and 
#     Harmless, Biased, Toxic or Harmful. An example would be Low/Harmless. Another example would be Medium/Toxic.
# """,
#     llm_config=llm_config,
# )

# Evaluator = autogen.AssistantAgent(
#     name="Evaluator",
#     system_message="""Evaluator. You are a helpful agent skilled in
#     deciding whether or not the output of a predecessor agent is 
#     satisfactory. If the severity classification from a Classifier is Medium, High, or Critical,
#     generate an updated response to the input prompt as your output. 
#     The updated response must not contain any Biased, Toxic or Harmful content. 
# """,
#     llm_config=llm_config,
# )


# groupchat = autogen.GroupChat(agents=[user_proxy, Arbiter, Classifier, Evaluator], messages=[], max_round=4)

# manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# user_proxy.initiate_chat(manager, message= "")

# # If the severity classification from Classifier is Medium/Biased, Medium/Toxic, Medium/Harmful, High/Biased, High/Toxic, High/Harmful, or Critical/Biased, Critical/Toxic, or Critical/Harmful,
#         fix the response from the Arbiter or say that you cannot answer the message. If the severity classification from Classifier is Low/Harmless, return a response to the message. 



