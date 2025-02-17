from autogen import ConversableAgent
from mysettings import llm_config

# Simulate the initial audio file as a conversation transcript
audio_transcript = """
Hiring Manager: Hi, I'd like to discuss creating a new position.
HR Specialist: Sure, what role are you considering?
Hiring Manager: We need a Senior Cloud Solution Architect for Azure to work on innovation using cloud-native technologies in The Netherlands.
HR Specialist: That sounds exciting! Can you provide more details on the responsibilities and requirements?
Hiring Manager: The candidate should have extensive experience with Azure, cloud-native technologies, and a passion for innovation. Salary expectations are around €80,000 per year.
"""

# ------------Summarization Agent------------

summarization_agent = ConversableAgent(
    name="Summarization Agent",
    system_message="You are a speech-to-text and summarization agent. Transcribe the given audio and summarize it, focusing on the job requirements.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

summary = summarization_agent.generate_reply(
    messages=[{"role": "user", "content": audio_transcript}]
)

print("------------Summarization Agent------------")
print(summary)

# ------------HR Specialist Agent------------

hr_specialist_agent = ConversableAgent(
    name="HR Specialist Agent",
    system_message=(
        "You are an HR Specialist. Based on the provided job requirements, create a Job Requisition "
        "with Technical Details, Benefits, Seniority, and Salary Range. The output must be in HTML format using the 'microsoft_logo.png' as logo. Also brand it as Microsoft. "
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

job_requisition = hr_specialist_agent.generate_reply(
    messages=[{"role": "user", "content": summary}]
)

print("------------HR Specialist Agent------------")
print(job_requisition)

# ------------External Communications Reviewer Agent------------

external_reviewer_agent = ConversableAgent(
    name="External Communications Reviewer Agent",
    system_message=(
        "You are responsible for validating external communications against predefined rules, such as language errors. "
        "If everything is okay, confirm that the Job Requisition Form is ready. If not, list the errors to be fixed, starting with 'Errors to be fixed:'."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

review = external_reviewer_agent.generate_reply(
    messages=[{"role": "user", "content": job_requisition}]
)

print("------------External Communications Reviewer Agent------------")
print(review)

# If there are errors, initiate chat between HR Specialist and External Reviewer to fix them
if "Errors to be fixed:" in review:
    conversation = hr_specialist_agent.initiate_chat(
        external_reviewer_agent,
        message=review,
        max_turns=4
    )
    # Update the job requisition based on the conversation
    final_job_requisition = conversation[-1]["content"]
else:
    final_job_requisition = job_requisition

# Save the final Job Requisition to a local file
with open("Job_Requisition.html", "w") as file:
    file.write(final_job_requisition)

print("------------Job Requisition Saved------------")
print("The Job Requisition has been saved to Job_Requisition.html")

# ------------Workday Integrations Agent------------

workday_agent = ConversableAgent(
    name="Workday Integrations Agent",
    system_message=(
        "You are responsible for sending the Job Requisition Form to Workday using the API "
        "https://workday.com/api/v1/job-requisitions. Provide a curl command to upload the Job Requisition Form."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

curl_command = workday_agent.generate_reply(
    messages=[{"role": "user", "content": final_job_requisition}]
)

print("------------Workday Integrations Agent------------")
print(curl_command)
