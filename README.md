# 🚀 Career Copilot - AI-Powered Multi-Agent Job Search Assistant

> An AI-powered Career Copilot that helps professionals discover relevant jobs, evaluate their fit, tailor resumes, and make smarter application decisions using a persistent career profile and multiple AI agents.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Groq](https://img.shields.io/badge/Groq-LLM-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📌 Why I Built This

Applying for jobs is repetitive.

Every application requires candidates to:

- Search multiple job portals
- Evaluate whether they're a good fit
- Tailor their resume
- Decide whether it's worth applying
- Repeat the process dozens of times

I wanted to build an AI-powered Career Copilot that acts like a personal career assistant by understanding the candidate once and using that knowledge throughout the job search journey.

Instead of simply chatting with an LLM, the application uses **multiple specialized AI agents** working together.

---

# 🎯 Features

### 👤 AI Career Profile

- Upload Resume (PDF/DOCX)
- AI extracts career information
- Persistent Career Profile
- SQLite storage

---

### 🔍 Intelligent Job Search

- Personalized search based on preferred roles
- Location-aware search
- SerpAPI integration
- Google Jobs aggregation

---

### 🤖 Multi-Agent AI Workflow

✅ Job Understanding Agent

- Understands each job description

✅ Fit Analysis Agent

- Evaluates candidate-job fit

✅ Resume Tailoring Agent

- Tailors resume for each opportunity

✅ Apply Decision Agent

- Recommends whether to apply

---

### 💾 Persistent Memory

- Stores user profile
- Reuses profile across the workflow
- Single source of truth for all agents

---

# 🏗 Architecture

> *(Insert architecture diagram here)*

Example:

```
                        Career Profile
                              │
        ┌─────────────────────┼────────────────────┐
        ▼                     ▼                    ▼
 Job Search Agent      Fit Analysis Agent   Resume Tailoring Agent
        │                     │                    │
        └─────────────────────┼────────────────────┘
                              ▼
                     Apply Decision Agent
                              │
                              ▼
                         Streamlit UI
```

---

# 🛠 Tech Stack

### Frontend

- Streamlit

### Backend

- Python

### AI

- Groq LLM
- Prompt Engineering

### Search

- SerpAPI
- Google Jobs

### Database

- SQLite
- SQLAlchemy

### Resume Parsing

- PyMuPDF
- python-docx

---

# 📂 Project Structure

```
career-copilot/

agents/
database/
models/
services/
prompts/
ui/
utils/

app.py
requirements.txt
README.md
```

---

# 🚀 Getting Started

## Clone

```bash
git clone https://github.com/chetandeepsingh91-creator/agentic-job-search.git
```

## Install

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env`

```text
GROQ_API_KEY=YOUR_KEY
SERP_API_KEY=YOUR_KEY
```

## Run

```bash
streamlit run app.py
```

---

# 📸 Screenshots

## Profile Extraction

<img width="893" height="320" alt="image" src="https://github.com/user-attachments/assets/3c1f92f9-4cba-4d2f-a4f1-34211fbfcd2b" />


---

## Job Search

<img width="899" height="378" alt="image" src="https://github.com/user-attachments/assets/782a3481-03ce-4758-8308-fd18ea24032b" />

---

## Fit Analysis

<img width="877" height="408" alt="image" src="https://github.com/user-attachments/assets/43a5abd0-ffaa-4f99-948e-1423b7ad19b9" />


---

## Resume Tailoring

<img width="848" height="397" alt="image" src="https://github.com/user-attachments/assets/bac7bf83-035a-4ee2-a932-7e7b1e20e88e" />


---

# 📍 Current Workflow

```
Upload Resume
      │
      ▼
AI extracts Career Profile
      │
      ▼
Save Profile
      │
      ▼
Search Jobs
      │
      ▼
Understand Job
      │
      ▼
Evaluate Fit
      │
      ▼
Tailor Resume
      │
      ▼
Recommend Apply / Skip
```

---

# 🛣 Roadmap

## ✅ Sprint 1

- Resume Upload
- Resume Parsing
- Persistent Profile
- Personalized Job Search
- Fit Analysis
- Resume Tailoring
- Apply Decision

---

## 🚧 Sprint 2

- Skill Gap Analysis
- Learning Planner
- Course Recommendations

---

## 🚧 Sprint 3

- AI Interview Coach
- Mock Interviews
- STAR Answer Evaluation

---

## 🚧 Sprint 4

- Application Tracker
- Recruiter CRM
- Follow-up Reminders

---

## 🚧 Sprint 5

- Salary Intelligence
- ATS Score
- Resume Score
- Market Insights

---

## 🚧 Sprint 6

- Authentication
- PostgreSQL
- Docker
- Cloud Deployment
- CI/CD

---

# 💡 Key Product Decisions

Instead of using a single AI prompt, the application uses specialized AI agents, each responsible for one task.

This makes the system:

- Modular
- Easier to maintain
- Easier to extend
- Closer to production AI architectures

Another key design decision was introducing a persistent **Career Profile** that acts as the single source of truth across all AI agents.

---

# 👨‍💻 About This Project

This project is being built publicly as part of my journey to deepen my expertise in **AI Product Management**, **Agentic AI**, and **LLM-powered product experiences**.

Each sprint introduces new capabilities while keeping the architecture modular and extensible.

---

# ⭐ If you found this project interesting

Feel free to:

- ⭐ Star the repository
- 🍴 Fork it
- 💬 Share feedback
- 🤝 Connect with me on LinkedIn
