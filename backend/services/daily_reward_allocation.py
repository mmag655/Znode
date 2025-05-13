from collections import defaultdict
from datetime import datetime, time, timedelta, timezone
import pytz
from sqlalchemy.orm import Session
from crud.activity import create_user_reward_activity
from crud.points import create_user_points, get_all_user_points, update_user_points
from crud.nodes import get_node_by_status
from crud.user_nodes import get_all_user_nodes
from crud.users import Users
from models.models import UserRewardActivity
from database import get_db
from schemas.points import UserPointsCreate, UserPointsUpdate
from database import SessionLocal


def add_daily_user_points():
    db = SessionLocal()
    print(f"⏰ Running daily reward job at {datetime.now(timezone.utc)}")

    # today = datetime.now(timezone.utc).date()

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
                date_updated=datetime.now(timezone.utc)
            )
            user_points = create_user_points(db, points=new_points)

        print("user_points", user_points.to_dict())
        update_data = UserPointsUpdate(
            total_points=user_points.total_points,
            available_for_redemtion=user_points.available_for_redemtion,
            date_updated=datetime.now(timezone.utc)
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
                activity_timestamp=datetime.now(timezone.utc)
            )
        )

        print(f"✅ Rewarded user {user_id}: {points_to_add:.2f} points")

    db.commit()
    print("🎉 All eligible users have been rewarded successfully.")

# Function to fetch user reward activities from the database
# def fetch_user_activities(db: Session):
#     return db.query(UserRewardActivity).filter(UserRewardActivity.user_id < 55).all()


# def insert_daily_rewards_based_on_may11(db: Session):
#     utc = pytz.utc
#     insert_dates = ['2025-05-10', '2025-05-12']
#     reference_date = '2025-05-11'
#     ref_dt = datetime.strptime(reference_date, "%Y-%m-%d")
#     ref_start = utc.localize(datetime.combine(ref_dt, time(5, 0)))
#     ref_end = ref_start + timedelta(days=1)

#     users = db.query(Users).filter(Users.user_id < 55).all()

#     print("\n🔍 Inserting Reward Entries:\n")

#     for user in users:
#         # Find May 11 activity
#         may11_activity = db.query(UserRewardActivity).filter(
#             UserRewardActivity.user_id == user.user_id,
#             UserRewardActivity.activity_timestamp >= ref_start,
#             UserRewardActivity.activity_timestamp < ref_end,
#             UserRewardActivity.isCredit == True,
#             UserRewardActivity.description == 'Daily rewarded nodes'
#         ).first()

#         if not may11_activity:
#             print(f"❌ User {user.user_id}: No reward found for May 11 — skipping.\n")
#             continue

#         print(f"👤 User ID: {user.user_id} | May 11 Points: {may11_activity.points}")

#         for date_str in insert_dates:
#             target_dt = utc.localize(datetime.combine(
#                 datetime.strptime(date_str, "%Y-%m-%d"), time(5, 0)
#             ))

#             # Avoid duplicate insert
#             exists = db.query(UserRewardActivity).filter(
#                 UserRewardActivity.user_id == user.user_id,
#                 UserRewardActivity.activity_timestamp == target_dt,
#                 UserRewardActivity.description == 'Daily rewarded nodes'
#             ).first()

#             if exists:
#                 print(f"   ⚠️ Already exists for {date_str} — skipping.")
#                 continue

#             # Insert new activity if it does not exist
#             new_activity = UserRewardActivity(
#                 user_id=user.user_id,
#                 points=may11_activity.points,
#                 type='reward',
#                 isCredit=True,
#                 description='Daily rewarded nodes',
#                 activity_timestamp=target_dt
#             )

#             db.add(new_activity)
#             print(f"   ✅ Inserted → Date: {date_str} 05:00 UTC | Points: {may11_activity.points}")

#     db.commit()
#     print("\n✅ All new reward activities have been inserted.\n")


# # Function to process user activities and group them by user_id and date
# def process_user_activities(db: Session, activities):
#     utc_tz = pytz.utc

#     for activity in activities:
#         # Assuming activity.timestamp is in UTC
#         activity_time = activity.activity_timestamp
#         if activity_time:
#             utc_date = activity_time.astimezone(utc_tz)
#             expected_date = utc_date.replace(hour=5, minute=0, second=0, microsecond=0)

#             if utc_date.hour >= 5:
#                 expected_date = expected_date + timedelta(days=1)

#             # Print the current date and expected date
#             print(f"Current date: {utc_date} -> Expected date: {expected_date}")
            
#             activity.activity_timestamp = expected_date
            
#     db.commit()
#     return activities

        

# Function to find missing and duplicate days for each user (between May 6, 2025 to May 12, 2025)

# def find_missing_and_duplicate_days(user_activities):
#     utc_tz = pytz.utc
    
#     # Iterate through each user and their activities
#     updated_dates = []
#     for user_id, dates in user_activities.items():
#         print(f"\nUser {user_id}")

#         for date in dates:
#             # Ensure the date is in UTC timezone (already in UTC in your case)
#             utc_date = date.astimezone(utc_tz)
            
#             # Set the expected UTC time to 05:00:00 for the same day
#             expected_date = utc_date.replace(hour=5, minute=0, second=0, microsecond=0)
            
#             # If the current UTC time is after 05:00:00, the expected date should be the next day
#             if utc_date.hour >= 5:
#                 expected_date = expected_date + timedelta(days=1)

#             # Print the current date and expected date
#             print(f"Current date: {utc_date} -> Expected date: {expected_date}")
#         updated_dates.append({user_id: {}})

# def update_user_points_based_on_rewards(db: Session):
#     utc = pytz.utc
#     target_dates = ['2025-05-10', '2025-05-12']

#     user_points_map = {}

#     # Step 1: Collect reward activities for both target dates
#     for date_str in target_dates:
#         date_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         start_dt = utc.localize(datetime.combine(date_dt, time(5, 0)))
#         end_dt = start_dt + timedelta(days=1)

#         activities = db.query(UserRewardActivity).filter(
#             UserRewardActivity.activity_timestamp >= start_dt,
#             UserRewardActivity.activity_timestamp < end_dt,
#             UserRewardActivity.isCredit == True,
#             UserRewardActivity.description == 'Daily rewarded nodes'
#         ).all()

#         for activity in activities:
#             user_id = activity.user_id
#             if user_id not in user_points_map:
#                 user_points_map[user_id] = {
#                     'total_add': 0,
#                     'daily': {}
#                 }
#             user_points_map[user_id]['total_add'] += activity.points
#             user_points_map[user_id]['daily'][date_str] = activity.points

#     updated_count = 0

#     # Step 2: Update user_points with detailed console output
#     for user_id, data in user_points_map.items():
#         user_point = db.query(UserPoints).filter(UserPoints.user_id == user_id).first()
#         if not user_point:
#             print(f"❌ User {user_id} not found in user_points table — skipping.")
#             continue

#         existing_total = user_point.total_points
#         daily_str = " + ".join(str(data['daily'].get(d, 0)) for d in target_dates)
#         print(f"👤 User {user_id} | Adding {daily_str} = {data['total_add']} to total {existing_total}")

#         user_point.total_points += data['total_add']
#         user_point.date_updated = datetime.utcnow().replace(tzinfo=utc)
#         updated_count += 1

#     db.commit()
#     print(f"\n✅ Updated total_points for {updated_count} user(s).\n")


# Main function to check missing and duplicate days in user activities
# def check_missing_and_duplicate_days(db: Session):
#     print(f"⏰ Checking for missing and duplicate days at {datetime.now(timezone.utc)}")

#     # Step 1: Fetch all user reward activities
#     activities = update_user_points_based_on_rewards(db)

    # Step 2: Process activities to group by user_id and date
    # user_activities = process_user_activities(db, activities)

    # Step 3: Find missing and duplicate days for each user
    # find_missing_and_duplicate_days(user_activities)

# if __name__ == "__main__":
#     db = SessionLocal()
#     check_missing_and_duplicate_days(db)