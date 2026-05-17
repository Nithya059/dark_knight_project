🦇 Dark Knight Developer Score

A privacy-presing AI system that analyzes GitHub activity and converts developer behavior into a hiring signal — without exposing raw data.

---

🚀 Problem

Hiring developers based only on resumes or GitHub profiles is inefficient:

- Raw GitHub data is noisy and hard to interpret
- No standardized way to measure developer consistency, impact, or behavior
- Privacy concerns when analyzing user activity

---

💡 Solution

Dark Knight Developer Score transforms GitHub activity into a single reputation score using behavioral signals:

- 🌙 Night activity detection
- ⚡ Code complexity estimation
- 🔁 Pull request contribution analysis
- 📊 Consistency tracking
- 🧠 Lightweight AI-based commit message analysis

All while preserving user privacy.

---

🔐 Privacy First Design

- User identity is hashed → "User#XXXX"
- No personal data is stored
- All analysis happens in real-time
- Output is behavioral abstraction, not raw data
- Proof hash ensures result integrity

---

🤖 AI Layer (Lightweight)

This system uses:

- NLP-based keyword analysis on commit messages
- Behavioral heuristics to infer developer patterns

«Note: This is an AI-assisted scoring system, not a heavy ML model.»

---

🧠 How It Works (Step-by-Step)

1. User enters GitHub username
2. Backend fetches:
   - Repositories
   - Commits
   - Pull requests
3. System processes:
   - Timestamp → detect night activity
   - Code changes → estimate complexity
   - PR lifecycle → measure collaboration
4. AI layer analyzes commit messages
5. Score is calculated using weighted formula
6. Result returned as:
   - Score
   - Badge
   - Insights
   - Benchmark percentile

---

📊 Features

- 🎯 Dark Knight Score (0–500)
- 📈 Commit distribution visualization
- 🧪 Burnout risk detection
- 🏆 Leaderboard (top users)
- 📉 Benchmark comparison (percentile)
- 🔍 Insight generation
- ⚡ Merge speed analysis

---

🛠 Tech Stack

Frontend

- HTML
- CSS
- JavaScript
- Chart.js

Backend

- FastAPI
- Python
- Requests

Deployment

- Netlify (Frontend)
- Render (Backend)

---

⚙️ API Endpoint

GET "/score"

Example:

/score?username=torvalds

Response includes:

- Score
- Activity metrics
- Insights
- Benchmark
- Privacy proof

---

🔑 Environment Variables

Create environment variable in backend:

GITHUB_TOKEN=your_personal_access_token

⚠️ Never expose your token in code.

---

📦 Setup (Local)

pip install -r requirements.txt
uvicorn main:app --reload

Open:

http://localhost:8000

---

🌍 Deployment

Frontend

- Upload to Netlify

Backend

- Deploy on Render
- Add environment variable:
  - "GITHUB_TOKEN"

---

⚠️ Limitations

- Uses public GitHub data only
- Pseudonymity (not full anonymity)
- Lightweight AI (not deep learning model)
- Small dataset for benchmarking

---

🚀 Future Improvements

- Token-based anonymous verification
- Advanced ML model for behavior analysis
- Larger dataset for benchmarking
- Team matching system (day vs night developers)
- Caching + performance optimization

---

🎯 Use Cases

- Developer hiring
- Skill benchmarking
- Open-source contributor analysis
- Behavioral productivity insights

---

🧠 Key Insight

«GitHub shows activity.
This system converts activity into trust.»

---

👨‍💻 Author

Nithya Shashidhara

---

⭐ Final Note

This project is not just a GitHub analyzer.

It is a privacy-preserving developer reputation system.
