# Simple Task Management API with CI/CD Pipeline

## Project Overview
This is a **FastAPI-based** RESTful API for **task management** with **CRUD operations** and additional functionalities like **searching, filtering**, and a **Bootstrap-powered frontend**.  

The project is fully **CI/CD automated** using **GitHub Actions** and is deployed to **Heroku**.  

**Live Deployment:**  
- **Frontend:** [https://simple-task-app-bdd22b40cf02.herokuapp.com/](https://simple-task-app-bdd22b40cf02.herokuapp.com/)  
- **API Endpoints (Swagger UI):** [https://simple-task-app-bdd22b40cf02.herokuapp.com/docs#/](https://simple-task-app-bdd22b40cf02.herokuapp.com/docs#/)  

---

## Getting Started 

### **1. Clone the Repository**  
```bash
 git clone https://github.com/mavlevich/simple-task-api.git
 cd simple-task-api
```

### **2. Create a Virtual Environment & Install Dependencies**  
```bash
 python -m venv venv
 source venv/bin/activate  # On Mac/Linux
 venv\Scripts\activate  # On Windows
 pip install -r requirements.txt
```

### **3. Run the Application Locally**  
```bash
 uvicorn app.main:app --reload
```

### **4. Open API Documentation**  
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## Frontend Usage 
This project includes a **fully responsive frontend** built with **Bootstrap**.  

- **How to access it?**  
  - Locally: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
  - Deployed version: [https://simple-task-app-bdd22b40cf02.herokuapp.com/](https://simple-task-app-bdd22b40cf02.herokuapp.com/)  

- **Features:**  
  - Create, edit, delete tasks  
  - Search tasks by title or description  
  - Mark tasks as completed/active  

---

## API Endpoints

### Core Task Endpoints (CRUD)
| Method | Endpoint       | Description |
|--------|---------------|-------------|
| `GET`  | `/tasks`      | Retrieve all tasks |
| `POST` | `/tasks`      | Create a new task |
| `GET`  | `/tasks/{id}` | Retrieve a task by ID |
| `PUT`  | `/tasks/{id}` | Update a task by ID |
| `DELETE` | `/tasks/{id}` | Delete a task by ID |

#### **Example: Create a Task**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/tasks' -H 'Content-Type: application/json' -d '{"title": "New Task", "description": "Some description", "completed": false}'
```

#### **Example: Get All Tasks**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/tasks'
```

#### **Example Response**
```json
{
  "id": 1,
  "title": "New Task",
  "description": "Some description",
  "completed": false
}
```

---

### Additional Features
| Method | Endpoint                     | Description |
|--------|------------------------------|-------------|
| `GET`  | `/extra-tasks/search-by-title?title=xyz` | Search tasks by title |
| `GET`  | `/extra-tasks/search-by-description?description=xyz` | Search tasks by description |

#### **Example: Search Task by Title**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/extra-tasks/search-by-title?title=Meeting'
```

#### **Example: Search Task by Description**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/extra-tasks/search-by-description?description=urgent'
```

#### **Example Response**
```json
[
  {
    "id": 3,
    "title": "Meeting",
    "description": "Weekly team meeting",
    "completed": false
  }
]
```

---

## Project Structure
```
app/
├── routers/        # API endpoints
├── services/       # Business logic
├── models/         # Database models
├── schemas/        # Pydantic schemas
├── db/             # Database connection & migrations
├── static/         # Frontend files
└── main.py         # Main entry point
```

---

## Testing
This project includes **unit tests** to ensure API stability.

### **Run Tests Locally**
```bash
pytest tests/
```

### **Test Coverage**
- CRUD operations  
- Data validation  
- Edge cases (empty database, negative IDs, large inputs)  
- Concurrency tests (parallel task creation)  

---

## CI/CD Pipeline
The project is integrated with **GitHub Actions** for automated testing and deployment to **Heroku**.

### **CI/CD Steps**
Run Tests – Ensure all tests pass using `pytest`  

Deploy to Heroku – If tests succeed, the API is deployed automatically  

### **Manual Deployment to Heroku (if needed)**
```bash
heroku login
heroku create simple-task-app
heroku git:remote -a simple-task-app
git push heroku master
```

### **Live Deployment**
- **Frontend:** [https://simple-task-app-bdd22b40cf02.herokuapp.com/](https://simple-task-app-bdd22b40cf02.herokuapp.com/)  
- **API Endpoints (Swagger UI):** [https://simple-task-app-bdd22b40cf02.herokuapp.com/docs#/](https://simple-task-app-bdd22b40cf02.herokuapp.com/docs#/)  

---

##  Summary of Additional Features
This project includes extra functionalities beyond the basic requirements:  
- Task searching by title & description
- Bootstrap-based responsive frontend
- Concurrency testing (handling multiple task creations in parallel)
- Separation of core logic and extra features into separate routers
- Detailed error handling & validation
- Live Heroku deployment link included

---
