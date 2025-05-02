# Zaivio Node App

This project is a full-stack application consisting of:
- **Frontend**: Next.js (TypeScript)
- **Backend**: FastAPI (Python)
- **Database**: MySQL 8+

---

## 📦 Project Structure

```
zaivio-nodes-app/
├── backend/              # FastAPI backend code
├── frontend/             # Next.js frontend code
├── db_dump.sql           # MySQL DB initialization dump
├── docker-compose.yml    # Docker orchestration
├── Dockerfile.frontend   # Dockerfile for Next.js
├── Dockerfile.backend    # Dockerfile for FastAPI
└── README.md             # Project documentation
```

---

## 🚀 Getting Started with Docker

### Step 1: Build and start all services

```bash
docker-compose up --build
```

### Step 2: Access services
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs (FastAPI docs)
- MySQL: Port 3306

---

## 🐳 Docker Setup

### `docker-compose.yml`

```
docker compose up
```

---

## 🧠 Learn More

- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [MySQL 8 Docs](https://dev.mysql.com/doc/)

---

## 📦 Deployment

Use the same `docker-compose.yml` file to deploy everything consistently across environments.


