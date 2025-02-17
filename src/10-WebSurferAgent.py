from autogen import GroupChatManager
from autogen import GroupChat
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from autogen.agentchat.contrib.web_surfer import WebSurferAgent
from mysettings import llm_config
from mysettings import llm_websurfer
from mysettings import browser_config

user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config=False,
    human_input_mode="ALWAYS",
    default_auto_reply="",
    is_termination_msg=lambda x: True,
)

web_surfer = WebSurferAgent(
    name="web_surfer",
    llm_config=llm_websurfer,
    summarizer_llm_config=llm_websurfer,
    browser_config=browser_config,
)

task1 = """
Latest technical news on Microsoft Semantic Kernel
"""

user_proxy.initiate_chat(web_surfer, message=task1)
