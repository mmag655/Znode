from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from utils.response import error_response, success_response
from database import get_db
from crud import points
from schemas.points import UserPointsCreate, UserPointsUpdate, UserPointsOut
from typing import List
from utils.dependencies import get_current_user_id

router = APIRouter()


@router.post("/create")
def create_points(points: UserPointsCreate, db: Session = Depends(get_db)):
    try:
        result = points.create_user_points(db, points)
        return success_response(result, "UserPoints created successfully")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/get")
def read_all(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        data = points.get_all_user_points(db, user_id)
        if data == None:
            return success_response(data = {}, message="No points data found")
        return success_response(data.to_dict(), "All user points retrieved")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.get("/get/{user_points_id}")
def read_single(user_points_id: int, db: Session = Depends(get_db)):
    try:
        db_points = points.get_user_points(db, user_points_id)
        if not db_points:
            return error_response("UserPoints not found", status.HTTP_404_NOT_FOUND)
        return success_response(db_points, "UserPoints retrieved")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/update")
def update_points(updates: UserPointsUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        db_points = points.update_user_points(db, user_id, updates)
        if not db_points:
            return error_response("UserPoints not found", status.HTTP_404_NOT_FOUND)
        return success_response(db_points, "UserPoints updated")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{user_points_id}")
def delete_points(user_points_id: int, db: Session = Depends(get_db)):
    try:
        db_points = points.delete_user_points(db, user_points_id)
        if not db_points:
            return error_response("UserPoints not found", status.HTTP_404_NOT_FOUND)
        return success_response(db_points, "UserPoints deleted")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/redeem/{points_to_redeem}")
def redeem_points(points_to_redeem: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        result = points.redeem_user_points(points_to_redeem=points_to_redeem, db=db, user_id=user_id)
        if not result:
            return error_response("Insufficient points or user not found", status.HTTP_400_BAD_REQUEST)
        return success_response(result, "Points redeemed successfully")
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
