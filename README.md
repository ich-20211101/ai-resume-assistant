# AI Resume Tailoring Assistant

I built this project to solve a problem I actually struggled with.

Tailoring a resume for every job application takes time, and honestly, it’s hard to stay consistent.  
So I created a simple tool that uses AI to analyze a job description and rewrite resume content to better match it.

---

## 🚀 Overview

The idea is simple:

> Instead of manually adjusting resumes every time, let AI handle the repetitive part — but keep it controlled with clear rules.

This application takes:

- A Job Description (JD)
- Your current resume or experience
- Optional instructions (e.g. "make it more data-focused")

And returns a tailored version that aligns better with the target role.

---

## ✨ What it does

### 1. Analyzes the Job Description
- Extracts key skills and themes
- Shows:
  - What already matches your resume
  - What you're missing

---

### 2. Rewrites Resume Content
It doesn’t just generate random content.

It rewrites based on:
- The JD
- Your actual experience
- Your custom instructions

---

### 3. Generates Structured Output
Instead of messy paragraphs, it gives:

- **Summary** → short and impactful
- **Skills** → only relevant ones
- **Experience bullets** → one line, focused, readable

---

### 4. Lets you control the direction
You can guide the output with instructions like:

- "Reframe backend experience for a data role"
- "Make it more ATS-friendly"
- "Write in Korean"

---

### 5. Enforces Resume Writing Rules
This is actually the core of the project.

All outputs follow rules defined in `rules.txt`, such as:
- One-line bullet points
- No fake experience
- Strong, simple structure
- Focus on impact

So it’s not just AI — it’s **AI with constraints**.

---

## 🏗️ Tech Stack

- Backend: FastAPI
- AI: Groq (LLM API)
- Frontend: HTML, CSS, JavaScript
- Env: python-dotenv

---

## 📂 Project Structure

```
ai-resume-assistant/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── services/
│   │   └── ai_service.py    # AI logic & Groq API integration
│   ├── data/
│   │   └── rules.txt        # Resume writing rules
│   └── static/
│       ├── index.html       # UI
│       ├── style.css        # Styling
│       └── script.js        # API calls & rendering
├── .env                     # API key
├── requirements.txt
└── README.md
```

---

## ⚙️ How it works

### Input
- Job Description
- Resume / Experience
- Optional instruction

### Processing
- Injects resume rules
- Sends structured prompt to Groq
- Generates structured response

### Output
- JD keywords (matched / missing)
- Summary
- Skills
- Experience bullets

---

## 🧠 Why I built it this way

### Structured output instead of free text
I forced the AI to return JSON so:
- it’s easier to render on UI
- output is predictable
- cleaner separation between backend and frontend

---

### Rules-driven prompting
Instead of trusting AI blindly,
I added my own resume rules (`rules.txt`).

This makes the output:
- more consistent
- more realistic
- actually usable

---

### Keeping it simple (on purpose)
I didn’t include:
- file uploads
- database
- authentication

Because the goal was:
👉 **focus on the core problem, not overbuild**

---

## ⚠️ Limitations

- No file upload (text only)
- No persistence
- Output quality depends on input quality
- Keyword extraction is not perfect

---

## 🔮 What I’d improve next

- Resume file parsing (PDF/DOCX)
- Multiple version comparison
- Cover letter generation
- Better keyword scoring
- UI improvements
- Integration with job platforms

---

## 💡 What this project shows

This project demonstrates that I can:

- Integrate LLM APIs into a real web app
- Design structured AI outputs
- Apply domain-specific rules to AI behavior
- Build something practical, not just a demo

---

## 👤 About me

Backend developer with experience in production systems,  
currently focusing on building AI-powered applications that solve real problems.