from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from services.daily_reward_allocation import add_daily_user_points
from database import get_db
from controllers.api.auth import router as auth_router
from controllers.api.users import router as users_router
from controllers.api.points import router as points_router
from controllers.api.swagger_auth import router as swagger_auth
from controllers.api.user_nodes import router as user_nodes_router
from controllers.api.admin_nodes import router as admin_nodes_router
from controllers.api.activity import router as activity_router
from controllers.api.wallet import router as wallet_router
from controllers.api.transaction import router as transaction_router

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI app starting up. Starting scheduler...")
    scheduler.add_job(add_daily_user_points, 'cron', hour=0, minute=0, id='daily_reward_job', replace_existing=True)
    scheduler.start()
    yield
    print("Shutting down scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://nodes.zaiv.io", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(points_router, prefix="/points", tags=["points"])
app.include_router(swagger_auth, prefix="/api", tags=["swager"])
app.include_router(user_nodes_router, prefix="/nodes", tags=["nodes"])
app.include_router(admin_nodes_router, prefix="/admin/nodes", tags=["admin nodes"])
app.include_router(activity_router, prefix="/activity", tags=["activity"])
app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])
app.include_router(transaction_router, prefix="/transaction", tags=["transaction"])


# Add route to check backend status
@app.get("/", tags=["status"])
def zavio_nodes_status(db: Session = Depends(get_db)):
    try:
        # Simple check to ensure the DB connection works
        db.execute(text("SELECT 1"))
        return {"status": "Zavio nodes backend active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
