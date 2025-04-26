import json
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from crud import activity as crud_user_reward_activity
from schemas import activity as schemas_user_reward_activity
from database import get_db
from utils.response import success_response, error_response
from fastapi import status
from utils.dependencies import get_current_user_id

# Define the router for UserRewardActivity endpoints
router = APIRouter()

@router.post("/create")
def create_user_reward_activity(user_reward_activity: schemas_user_reward_activity.UserRewardActivityCreate, db: Session = Depends(get_db)):
    try:
        # You can add any additional validation or business logic here
        created_activity = crud_user_reward_activity.create_user_reward_activity(db, user_reward_activity)
        return success_response(created_activity.to_dict(), "User reward activity created", status.HTTP_201_CREATED)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/all")
def read_user_reward_activities(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        activities = crud_user_reward_activity.get_user_reward_activities(db, user_id=user_id)  # SQLAlchemy model instances
        activity_list = [activity.to_dict() for activity in activities]
        
        if not activity_list:
            return success_response(data = {}, message="No reward activities found")
        
        return success_response(activity_list, "User reward activities retrieved")
    
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/all_reward")
def read_user_reward_activities(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        activities = crud_user_reward_activity.get_user_reward_activities(db, user_id=user_id, type = "reward")  # SQLAlchemy model instances
        activity_list = [activity.to_dict() for activity in activities]
        
        if not activity_list:
            return success_response(data = {}, message="No reward activities found", code=status.HTTP_204_NO_CONTENT)
        
        return success_response(activity_list, "User reward activities retrieved")
    
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.patch("/update")
async def update_user_reward_activity(request: Request, activity_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        raw = await request.json()
        print("🔍 Raw body received:", raw)
        user_reward_activity = schemas_user_reward_activity.UserRewardActivityUpdate(**raw)  # Convert to Pydantic schema
        updated_activity = crud_user_reward_activity.update_user_reward_activity(db, activity_id, user_reward_activity)
        if not updated_activity:
            return error_response("Activity not found", status.HTTP_404_NOT_FOUND)
        return success_response(updated_activity.to_dict(), "User reward activity updated")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/id/{activity_id}")
def delete_user_reward_activity(activity_id: int, db: Session = Depends(get_db)):
    try:
        deleted_activity = crud_user_reward_activity.delete_user_reward_activity(db, activity_id)
        if not deleted_activity:
            return error_response("Activity not found", status.HTTP_404_NOT_FOUND)
        return success_response(None, "User reward activity deleted")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
