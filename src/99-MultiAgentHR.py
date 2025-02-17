# ...existing imports...
from autogen import ConversableAgent
import os
from mysettings import llm_config  # Updated import

# --- Agent Definitions ---
summarization_agent = ConversableAgent(
    "Summarization Agent",
    system_message="You are responsible for converting speech to text and summarizing it focusing solely on the job requirements.",
    llm_config=llm_config  # Updated llm_config
)

hr_specialist_agent = ConversableAgent(
    "HR Specialist Agent",
    system_message="You create a Job Requisition with technical details, benefits, seniority and salary range in HTML format for a Senior Cloud Solution Architect role. You must use clear HTML. If errors are indicated by External Communications Reviewer Agent, update the output accordingly.",
    llm_config=llm_config  # Updated llm_config
)

external_comm_agent = ConversableAgent(
    "External Communications Reviewer Agent",
    system_message="Validate the Job Requisition for language errors and ensure the logo 'microsoft_logo.png' is included. If not, reply with 'Errors to be fixed:' followed by details.",
    llm_config=llm_config  # Updated llm_config
)

workday_agent = ConversableAgent(
    "Workday Integrations Agent",
    system_message="Receive the final Job Requisition and output a curl command to send it to Workday API at https://workday.com/api/v1/job-requisitions.",
    llm_config=llm_config  # Updated llm_config
)

# --- Step 1: Summarization of Audio File ---
print("------------Summarization Step--------")
# Simulate an audio file transcript
audio_transcript = (
    "Hiring Manager: We require a Senior Cloud Solution Architect for Azure to drive innovation using Cloud Native technologies in The Netherlands. "
    "HR Specialist: We need a candidate with extensive experience, leadership skills, and a strong technical background."
)
# Simulate LLM summary (using generate_reply for demonstration)
summary = summarization_agent.generate_reply(
    messages=[{"role": "user", "content": audio_transcript}]
)
# For simulation purposes, if no real LLM integration, set a dummy summary.
if not summary:
    summary = ("Summary: Role - Senior Cloud Solution Architect for Azure; Focus on innovation using Cloud Native technologies in The Netherlands; "
               "Requirements include extensive technical experience and leadership skills.")
print("Summarization Agent Output:")
print(summary)

# --- Step 2: HR Specialist Agent creates initial Job Requisition ---
print("------------HR Specialist Step--------")
# HR agent uses the summary to create Job Requisition in HTML (initial version without logo)
initial_job_req = hr_specialist_agent.generate_reply(
    messages=[{"role": "user", "content": summary}]
)
if not initial_job_req:
    initial_job_req = (
        "<html>\n<head><title>Job Requisition</title></head>\n<body>\n"
        "<h1>Senior Cloud Solution Architect for Azure</h1>\n"
        "<p><strong>Technical Details:</strong> Expertise in Cloud Native technologies required.</p>\n"
        "<p><strong>Benefits:</strong> Competitive benefits package.</p>\n"
        "<p><strong>Seniority:</strong> Senior level</p>\n"
        "<p><strong>Salary Range:</strong> Competitive</p>\n"
        # Missing company logo intentionally to trigger review feedback
        "</body>\n</html>"
    )
print("HR Specialist Agent Output (Initial):")
print(initial_job_req)

# --- Step 3: External Communications Reviewer validates the job requisition ---
print("------------External Communications Review Step--------")
# Simulate a chat between HR Specialist and External Communications Reviewer with max 4 interactions
# Using initiate_chat to simulate conversation (here we assume a single round message for simulation)
review_response = hr_specialist_agent.initiate_chat(
    external_comm_agent,
    message=initial_job_req,
    max_turns=4
)
# Simulate checking of review output; if missing logo, external agent returns error message.
if not review_response or "Errors to be fixed:" not in review_response:
    # For simulation, assume error detected (missing company logo)
    review_response = "Errors to be fixed: The Job Requisition is missing the company logo. Please include <img src=\"microsoft_logo.png\" alt=\"Microsoft Logo\">."
print("External Communications Reviewer Agent Output:")
print(review_response)

# HR Specialist updates the job requisition if errors are returned.
if review_response.startswith("Errors to be fixed:"):
    # Update output to include the logo
    final_job_req = (
        "<html>\n<head><title>Job Requisition</title></head>\n<body>\n"
        "<img src=\"microsoft_logo.png\" alt=\"Microsoft Logo\">\n"
        "<h1>Senior Cloud Solution Architect for Azure</h1>\n"
        "<p><strong>Technical Details:</strong> Expertise in Cloud Native technologies required.</p>\n"
        "<p><strong>Benefits:</strong> Competitive benefits package including health, dental, and vision.</p>\n"
        "<p><strong>Seniority:</strong> Senior level</p>\n"
        "<p><strong>Salary Range:</strong> Competitive, commensurate with experience.</p>\n"
        "</body>\n</html>"
    )
else:
    final_job_req = initial_job_req
print("HR Specialist Final Job Requisition:")
print(final_job_req)

# --- Save the Job Requisition to a local HTML file ---
output_file = "job_requisition.html"
with open(output_file, "w") as f:
    f.write(final_job_req)
print(f"Job Requisition saved to {os.path.abspath(output_file)}")

# --- Step 4: Workday Integration ---
print("------------Workday Integration Step--------")
workday_response = workday_agent.generate_reply(
    messages=[{"role": "user", "content": final_job_req}]
)
if not workday_response:
    workday_response = (
        "curl -X POST https://workday.com/api/v1/job-requisitions -F 'file=@job_requisition.html'"
    )
print("Workday Integrations Agent Output:")
print(workday_response)
# ...existing code...
