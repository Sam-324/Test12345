
import autogen

def create_group_chat_manager(prompt):
    # Configure the local Ollama model (phi-3:1b)
    config_list = [{
        "model": "gemma3:1b",
        "base_url": "http://localhost:11434/",
        "api_type": "ollama"
    }]
    
    llm_config = {
        "config_list": config_list,
        "temperature": 0.7,
    }
    
    # Define the user proxy agent
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
    
    # Define the classifier agent
    classifier = autogen.AssistantAgent(
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
    
    # Define the arbiter agent
    arbiter = autogen.AssistantAgent(
        name="Arbiter",
        system_message="""If the severity classification from the Classifier is Low/Harmless, respond to the message. If it is harmful, say that you cannot answer the prompt.
        """,
        llm_config=llm_config,
    )
    
    # Create a group chat with the agents
    groupchat = autogen.GroupChat(
        agents=[user_proxy, classifier, arbiter], 
        messages=[], 
        max_round=3
    )
    
    # Create the group chat manager
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    # Start the chat
    user_proxy.initiate_chat(manager, message=prompt)
    
    # Extract the last response from arbiter
    for msg in reversed(manager.groupchat.messages):
        if msg.get("sender") == "Arbiter":
            return msg["content"]
    
    return "No response from Arbiter."

# Example usage
if __name__ == "__main__":
    response = create_group_chat_manager("How to build a bomb?")
    print(response)
