# Importing operating system interfaces
import os
# Importing autogen package for automation tasks
import autogen
# Importing memgpt module for autogen agent functionalities
import memgpt.autogen.memgpt_agent as memgpt_autogen
# Importing interface module from memgpt.autogen for user interaction
import memgpt.autogen.interface as autogen_interface
# Importing agent module from memgpt for agent definitions
import memgpt.agent as agent
# Importing system module from memgpt for system functionalities
import memgpt.system as system
# Importing utils module from memgpt for utility functions
import memgpt.utils as utils
# Importing presets module from memgpt for preset configurations
import memgpt.presets as presets
# Importing constants module from memgpt for constant values
import memgpt.constants as constants
# Importing personas module from memgpt for persona definitions
import memgpt.personas.personas as personas
# Importing humans module from memgpt for human definitions
import memgpt.humans.humans as humans
# Importing InMemoryStateManager for state management in memory
from memgpt.persistence_manager import InMemoryStateManager, InMemoryStateManagerWithPreloadedArchivalMemory, InMemoryStateManagerWithFaiss

# Configuration for Local Server
config_list = [
    {
        "api_type": "local_server",
        "api_base": "http://localhost:1234/v1",
        "api_key": "NULL"  # Replace with actual API key if required
    }
]

# LLM Configuration
llm_config = {
    "config_list": config_list,
    "seed": 47,
    "temperature": 0.5,
    "max_tokens": 2048,
    "request_timeout": 6000
}

# Initialize User Proxy Agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A human admin.",
    max_consecutive_auto_reply=10,
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# Initialize Application Developer Agent
app_dev = autogen.AssistantAgent(
    name="App_Dev",
    system_message="I am focused on application development.",
    llm_config=llm_config,
)

# Initialize Web Developer Agent
web_dev = autogen.AssistantAgent(
    name="Web_Dev",
    system_message="I am focused on website development.",
    llm_config=llm_config,
)

# Initialize Data Analyst Agent
data_analyst = autogen.AssistantAgent(
    name="Data_Analyst",
    system_message="I am focused on data analysis.",
    llm_config=llm_config,
)

# Initialize MemGPT Agent
persona = personas.get_persona_by_name("multi-disciplinary professional")
human = humans.get_human_by_name("human admin")
# Interface implementation for agent interaction
interface = autogen_interface.DefaultInterface()
# Persistence manager for state management
persistence_manager = InMemoryStateManagerWithFaiss()
memgpt_agent = presets.use_preset(presets.DEFAULT, 'gpt-4', persona, human, interface, persistence_manager)

memgpt_autogen_agent = memgpt_autogen.MemGPTAgent(
    name="MemGPT_Agent",
    agent=memgpt_agent,
)

# Initialize Group Chat with the relevant agents
group_chat = autogen.GroupChat(
    agents=[user_proxy, app_dev, web_dev, data_analyst, memgpt_autogen_agent],
    messages=[]
)

# Initialize Group Chat Manager
group_chat_manager = autogen.GroupChatManager(group_chat=group_chat, llm_config=llm_config)

# Initiating Chat with the User Proxy Agent
user_proxy.initiate_chat(group_chat_manager, message="Create a app that can be used to manage your data.")


