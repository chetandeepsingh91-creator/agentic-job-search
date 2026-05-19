from utils import call_llm
from job_agent import fetch_jobs

def job_understanding_agent(jd):
    prompt = f"""
You are an expert recruiter.

Analyze the job description and extract:

1. Key skills required
2. Seniority level
3. Important keywords
4. Hidden expectations

Job Description:
{jd}

Output in structured bullet points.
"""
    return call_llm(prompt)
    
    
def fit_agent(resume, jd_summary):
    prompt = f"""
You are a hiring expert.

Evaluate how well the candidate fits the job.

Inputs:
Resume:
{resume}

Job Summary:
{jd_summary}

Tasks:
1. Give Fit Score (0–100)
2. Explain reasoning
3. Identify key gaps

Output clearly.
"""
    return call_llm(prompt)    
    
    
def resume_agent(resume, jd, learning=None):
    prompt = f"""
You are a resume expert.

Use past learning insights if available.

Learning Insights:
{learning}

Resume:
{resume}

Job Description:
{jd}

Improve resume accordingly.
"""
    return call_llm(prompt)
    
    
from memory import load_memory

def learning_agent():
    memory = load_memory()

    if len(memory) < 2:
        return "Not enough data to learn yet."

    recent_data = memory[-5:]

    prompt = f"""
You are an AI system improving job applications.

Analyze past interactions and identify:

1. Common patterns in resumes
2. Frequent skill gaps
3. Suggestions to improve future applications

Data:
{recent_data}

Output clear insights.
"""

    return call_llm(prompt)
    

def job_crawler_agent(role):
    jobs = fetch_jobs(role)

    # prompt = f"""
# You are a job search assistant.

# Here are some job listings:
# {jobs}

# Tasks:
# 1. Clean and structure job listings
# 2. Highlight best matches
# 3. Summarize each role briefly
# """

    # return call_llm(prompt)
    
    return jobs
    
    
def ranking_agent(results):
    prompt = f"""
You are a career advisor.

Given job opportunities with fit analysis:

{results}

Tasks:
1. Rank jobs from best to worst
2. Explain why
3. Recommend top 3 to apply

Output clearly.
"""
    return call_llm(prompt)    
    
def apply_decision_agent(job, fit_analysis):
    prompt = f"""
You are a career advisor.

Given this job:
{job}

And fit analysis:
{fit_analysis}

Tasks:
1. Should the candidate apply? (Yes/No)
2. Why?
3. Priority (High/Medium/Low)

Be concise.
"""
    return call_llm(prompt)
    
def application_agent(job, resume):
    prompt = f"""
You are an expert job application assistant.

Job:
{job}

Candidate Resume:
{resume}

Tasks:
1. Write a short tailored cover note
2. Suggest 2–3 answers for common questions
3. Highlight key strengths to mention

Keep it concise and practical.
"""
    return call_llm(prompt)
    
    
def tailored_resume_agent(resume, job_description):
    prompt = f"""
You are an expert resume writer.

IMPORTANT RULES:
- Do NOT add fake experience or skills
- Only rephrase and optimize existing content
- Make it ATS-friendly

Inputs:
Resume:
{resume}

Job Description:
{job_description}

Tasks:
1. Rewrite resume tailored to the job
2. Optimize bullet points using relevant keywords
3. Highlight most relevant experience
4. Keep it concise and impactful

Output format:
Updated resume with the same sections and experiences but updated as below
- Professional summary (2–3 lines)
- 4–6 tailored bullet points
"""
    return call_llm(prompt)