--- Prompt ---

- I need to create AI Agents using Autogen framework using Python script in a single file (consider the current codebase for the suggestion of the Agents). 
- The script must be 99-MultiAgentHR.py 
- Agents need to be created with their dependencies. 
- Create the code the Agents and propose the System Prompts (system_message). 
- Also simulate the initial "Audio file" with a conversation between Hiring Manager and HR Specialist talking about a role of Senior Cloud Solution Architect for Azure working on Innovation using on Cloud Native technologies in The Netherlands. 
- Add logic to store the Job Requisition to a local html file. 
- Each LLM interaction must be output to the terminal like: ------------{ Step Name }--------

-> Agent 1
Agent Name: Summarization Agent
Input: Audio file
Output: Conversation Speech to Text and Summarize it focusing on the Job requirements
Depends on agent: N/A

-> Agent 2
Agent: HR Specialist Agent
Input: Summarized text with Job Requirements 
Output: Create a Job Requisition with - Technical Details, Benefits, Seniority and Salary Range. The output must be HTML format.
Depends on agent: Summarization
Additional login: chats with "External Communications Reviewer Agent" - if there are "Errors to fixed", bots need to chat with each other to fix the errors. Use the "initiate_chat" method to initiate the Chat between the "HR Specialist Agent" and "External Communications Reviewer Agent" with Max Number of Chat Interations: 4

-> Agent 3
Agent: External Communications Reviewer Agent 
Input: Job Requisition Form
Output: Validate the external communications for language errors. Also check if the logo "microsoft_logo.png" is part of the Job Requisition. 
        - If Ok: Create the Job Requisition Form
        - If Nok: List the errors to be fixed with ""Errors to be fixed:"" at the beginning
Depends on agent: N/A 

-> Agent 4
Agent: Workday Integrations Agent
Input: Job Requisition Form
Output: Send Job Requisitiion to Workday using API https://workday.com/api/v1/job-requisitions. Output a curl command to upload the Job requisition form.
Depends on agent: Chat between HR Specialist and External Communications Reviewer 
