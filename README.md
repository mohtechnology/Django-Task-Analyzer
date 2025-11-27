# Smart Task Analyzer
This project is a Django-based task management tool that automatically scores and sorts tasks using a custom system-recommended priority algorithm. The application supports adding tasks, editing tasks, deleting tasks, and switching between multiple sorting strategies.

The system score is calculated and stored in the database for every task and updated whenever any task is added or edited.

---

## Features
- Add tasks with:
  - Title
  - Due date
  - Estimated hours
  - Importance (1–10)
  - Dependencies (Many-to-Many task links)
- Automatic priority scoring stored in DB
- Multiple sorting modes:
  - System Recommended (custom algorithm)
  - Deadline-based
  - Fastest First
  - Importance
  - Balanced hybrid logic
- Edit and delete tasks
- Score recalculation for all tasks whenever data changes

---

## Priority Scoring
Each task receives a score on a **0–10 scale**, calculated using:

1. **Importance (30%)**  
   Normalized from user input (1–10).

2. **Urgency (30%)**  
   - Overdue tasks receive max urgency.  
   - Near deadlines get higher scores.  
   - Far deadlines decrease urgency.

3. **Effort (10%)**  
   Fewer estimated hours → higher priority.

4. **Depends-On Score (10%)**  
   Tasks that depend on many others get a slight penalty.

5. **Influence Score (20%)**  
   Tasks that **block more tasks** get higher priority.

Final formula:
* score = (weighted sum) * 10

The score is saved in the `Task` model and used directly for sorting.

---

## Sorting Logic
Sorting options include:

- **System Recommended**  
  Orders by stored `score` descending.
  
- **Deadline**  
  Soonest due date first.

- **Fastest**  
  Lowest estimated hours first.

- **Important**  
  Highest importance first.

- **Balanced**  
  Custom hybrid:

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/mohtechnology/Django-Task-Analyzer
cd task-analyzer
````

### 2. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the Django server

```bash
python manage.py runserver
```

## Priority Scoring

Each task is assigned a score based on four key factors:

1. **Urgency** – Tasks with closer or overdue due dates receive higher priority.
2. **Importance** – User rating on a 1–10 scale.
3. **Effort** – Shorter tasks can be prioritized as quick wins.
4. **Dependencies** – Tasks required by others are ranked higher.

Circular dependency detection is implemented using DFS and tasks in cycles receive a penalty.

### Strategy Weights

| Strategy        | Urgency | Importance | Effort | Dependency |
| --------------- | ------- | ---------- | ------ | ---------- |
| Smart Balance   | 3       | 4          | 1.5    | 2          |
| Fastest Wins    | 1       | 2          | 5      | 1          |
| High Impact     | 1       | 6          | 1      | 2          |
| Deadline Driven | 6       | 2          | 1      | 1          |

---

Covers:

* Overdue task priority
* Fastest strategy logic
* Circular dependency detection

---

## Design Decisions (Short)

* All data is stored in the DB; the frontend does not store tasks in memory.
* JSON-based endpoints are used without Django REST Framework to keep the backend simple.
* Scoring algorithm is modular and easily configurable.
* Frontend is intentionally lightweight and dependency-free outside Bootstrap.

---

## Time Breakdown

* Backend and DB structure: 2 hours
* Priority scoring logic: 1.5 hour
* Frontend UI and interactions: 1 hour
* Integration and testing: 1 minutes
* README and cleanup: 25 minutes

---

## Future Improvements

* Edit and delete task functionality
* Category and tagging system
* Visual dependency graph
* Eisenhower matrix view
* Analytics dashboard
* Weekend/holiday-aware urgency
