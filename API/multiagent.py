# Imports
import autogen

# Autogen Multiagent Function
def create_group_chat_manager(prompt):
    
    # Open AI configuration
    llm_config = {
    "config_list": [{"model": "gpt-3.5-turbo", "api_key": "Insert_API_KEY", "seed": 1}],
    }

    # user_proxy configuration
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

    # Classifier Agent configuration
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

    # Arbiter agent configuration
    Arbiter = autogen.AssistantAgent(
        name="Arbiter",
        system_message="""If the severity classification from the Classifier is Low/Harmless, respond to the message. If it is harmful, say that you cannot answer the prompt.
        """,
        llm_config=llm_config,
    )

    # Create group chat with the agents
    groupchat = autogen.GroupChat(agents=[user_proxy, Classifier, Arbiter], messages=[], max_round=3)

    # Initiate group chat manager
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
       
    # Initiate chat via user proxy
    user_proxy.initiate_chat(manager, message= prompt)
    
    # Extract last response for arbitier
    response = Arbiter.last_message()["content"]
    return response
