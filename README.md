# 🧠 SmartTask – Backend API  
![Python](https://img.shields.io/badge/Backend-Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Framework-Flask-000000?logo=flask&logoColor=white)
![PuLP](https://img.shields.io/badge/Optimization-PuLP-FF6F61?logo=python&logoColor=white)
![Render](https://img.shields.io/badge/Deployed%20On-Render-46E3B7?logo=render&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> **SmartTask Backend** – A **Flask-based REST API** that uses **Linear Programming (PuLP)** to optimize tasks and generate the **most productive daily schedules**.

---

## 📌 Overview
SmartTask is an **intelligent to-do list app** powered by **Linear Programming (LPP)**.  
The backend handles:
- Task scheduling
- Time & labor optimization
- Deadline management
- Task dependencies

It communicates with the **React + Tailwind frontend** to deliver a **personalized, optimized to-do list**.

🔗 **Frontend Repo:** [SmartTask Frontend](https://github.com/Rajshakya0101/smart-task-frontend)  
🌐 **Live Demo:** [SmartTask Web App](https://rajshakya0101.github.io/smart-task-frontend/)

---

## ✨ Features
- 🧩 **Optimization Engine** → Uses **Linear Programming** to maximize total priority.
- ⏳ **Time Constraints** → Ensures total scheduled hours ≤ `max_hours`.
- 👷 **Labor Constraints** → Ensures total effort ≤ `labor_capacity`.
- 🔗 **Task Dependencies** → Supports prerequisites between tasks.
- ⏱️ **Deadline Support** → Honors task-specific deadlines.
- 🟢 **Partial Task Handling** → Allows fractional selection if enabled.
- 📡 **REST API** → Accepts JSON input & returns optimized schedules.
- 🌐 **CORS Enabled** → Seamless integration with the frontend.

---

## 🛠️ Tech Stack
- **Language:** [Python 3.10+](https://www.python.org/)
- **Framework:** [Flask](https://flask.palletsprojects.com/)
- **Optimization Library:** [PuLP](https://coin-or.github.io/pulp/)
- **Deployment:** [Render](https://render.com/)
- **Frontend:** [React + Tailwind](https://github.com/Rajshakya0101/smart-task-frontend)

---

## 📂 Folder Structure
SmartTask-backend/
├── app.py               # Main Flask app
├── requirements.txt     # Python dependencies
└── README.md

---

## ⚡ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Rajshakya0101/SmartTask-backend.git

# Navigate to the project folder
cd SmartTask-backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py

```
---

📡 API Documentation

1️⃣ Solve Task Scheduling Problem

Endpoint:
```bash

POST /solve
```

Request Body (JSON):
```bash

{
  "tasks": [
    {
      "name": "Study ML",
      "priority": 5,
      "time": 120,
      "labor": 2,
      "partial_allowed": false
    },
    {
      "name": "Project Work",
      "priority": 4,
      "time": 180,
      "labor": 3,
      "partial_allowed": true,
      "deadline": 200
    },
    {
      "name": "Gym",
      "priority": 3,
      "time": 60,
      "labor": 1
    }
  ],
  "max_hours": 300,
  "labor_capacity": 5,
  "task_dependencies": [["Project Work", "Study ML"]]
}
```

Request Fields:

| Field               | Type    | Required | Description                                                  |
| ------------------- | ------- | -------- | ------------------------------------------------------------ |
| `tasks`             | Array   | ✅ Yes    | List of task objects                                         |
| `name`              | String  | ✅ Yes    | Name of the task                                             |
| `priority`          | Number  | ✅ Yes    | Task priority (higher = more important)                      |
| `time`              | Number  | ✅ Yes    | Time required for the task (in minutes)                      |
| `labor`             | Number  | ✅ Yes    | Effort required for the task                                 |
| `partial_allowed`   | Boolean | ❌ No     | Allow partial task completion                                |
| `deadline`          | Number  | ❌ No     | Maximum time allowed for the task                            |
| `max_hours`         | Number  | ✅ Yes    | Total available time (in minutes)                            |
| `labor_capacity`    | Number  | ✅ Yes    | Maximum total labor available                                |
| `task_dependencies` | Array   | ❌ No     | List of task dependencies (`[["A","B"]]` means A requires B) |

Response Example (JSON):
```bash

{
  "status": "Optimal",
  "results": {
    "Study ML": 1,
    "Project Work": 1,
    "Gym": 0
  },
  "objective_value": 9
}
```

Response Fields:

| Field             | Description                                                                          |
| ----------------- | ------------------------------------------------------------------------------------ |
| `status`          | Status of the optimization (`Optimal`, `Infeasible`, etc.)                           |
| `results`         | Selected tasks and their completion fractions (1 = full, 0 = skipped, 0.5 = partial) |
| `objective_value` | Maximum achievable total priority                                                    |

---

2️⃣ Health Check

Endpoint:

GET /api/health


Response:

{
  "status": "OK",
  "message": "SmartTask Backend is running 🚀"
}

---

🚀 Deployment

The backend is deployed on Render.
To redeploy, push your latest code to the main branch:

git add .
git commit -m "Update backend"
git push origin main

---

👨‍💻 Author

Raj Shakya
📧 rajshakya.orai18@gmail.com

🌐 LinkedIn
 | GitHub