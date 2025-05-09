from datetime import datetime, timedelta, timezone

# Fixed GMT-5 timezone (no DST adjustment)
GMT_MINUS_5 = timezone(timedelta(hours=-5))

def now_gmt5():
    return datetime.now(GMT_MINUS_5)

def to_gmt5(dt: datetime) -> datetime:
    """Convert any aware datetime to GMT-5"""
    return dt.astimezone(GMT_MINUS_5)

print(datetime.now(timezone.utc))