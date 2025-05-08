from datetime import datetime, timezone
from sqlalchemy.orm import Session
from utils.timezone import now_gmt5
from crud.activity import create_user_reward_activity
from crud.points import create_user_points, get_all_user_points, update_user_points
from crud.nodes import get_node_by_status
from crud.user_nodes import get_all_user_nodes
from models.models import UserPoints, UserRewardActivity
from database import get_db
from schemas.points import UserPointsCreate, UserPointsUpdate


def add_daily_user_points():
    db: Session = next(get_db())
    print(f"⏰ Running daily reward job at {now_gmt5()}")

    # today = now_gmt5().date()

    # Step 1: Get total active nodes and reward amount
    active_nodes = get_node_by_status(db, status="active")
    if not active_nodes or active_nodes.total_nodes == 0:
        print("⚠️ No active nodes or total_nodes is 0. Skipping reward allocation.")
        return

    reward_per_node = int(active_nodes.daily_reward / active_nodes.total_nodes)
    if reward_per_node <= 0:
        print("⚠️ Daily reward per node is zero or negative. Skipping reward allocation.")
        return

    print(f"🔢 Calculated reward_per_node = {reward_per_node:.4f}")

    # Step 2: Fetch user-wise node counts
    users_nodes = get_all_user_nodes(db)  # Expected to return list of UserNodes objects

    for node in users_nodes:
        user_id = node.user_id
        node_count = node.nodes_assigned
        points_to_add = int(reward_per_node * node_count)

        # Step 3: Prevent duplicate reward (optional check, implement get_user_reward_activities if needed)
        # existing_reward = get_user_reward_activities(db, user_id=user_id, type="reward", date=today)
        # if existing_reward:
        #     print(f"⏭️ User {user_id} already rewarded today. Skipping.")
        #     continue

        # Step 4: Create or update user_points
        user_points = get_all_user_points(db, user_id=user_id)
        if user_points is not None:
            user_points.total_points += points_to_add
            user_points.available_for_redemtion += points_to_add
        else:
            new_points = UserPointsCreate(
                user_id=user_id,
                total_points=points_to_add,
                available_for_redemtion=points_to_add,
                zavio_token_rewarded=0,
                date_updated=now_gmt5()
            )
            user_points = create_user_points(db, points=new_points)

        print("user_points", user_points.to_dict())
        update_data = UserPointsUpdate(
            total_points=user_points.total_points,
            available_for_redemtion=user_points.available_for_redemtion,
            date_updated=now_gmt5()
        )
        update_user_points(db, user_id=user_id, updates=update_data)

        # Step 5: Log reward activity
        create_user_reward_activity(
            db,
            user_reward_activity=UserRewardActivity(
                user_id=user_id,
                points=points_to_add,
                type="reward",
                isCredit=True,
                description=f"Daily rewarded nodes",
                activity_timestamp=now_gmt5()
            )
        )

        print(f"✅ Rewarded user {user_id}: {points_to_add:.2f} points")

    db.commit()
    print("🎉 All eligible users have been rewarded successfully.")
