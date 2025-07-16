# scheduler_service.py

from apscheduler.schedulers.background import BackgroundScheduler  # Scheduler that runs in the background
from apscheduler.triggers.date import DateTrigger  # Trigger to run a job at a specific date/time
from datetime import datetime, timedelta  # For working with date and time
from facebook_api import post_to_facebook  # Function to post content to Facebook

# Create an instance of the BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()  # Start the scheduler in the background

def schedule_post(post_time: str, message: str, media_path: str, media_type: str) -> None:
    """
    Schedules a post to be published on Facebook at a specified time.

    This function uses APScheduler to run the `post_to_facebook` function at a future time.
    If the provided time has already passed for the current day, it schedules the post for the next day.

    Args:
        post_time (str): Time to schedule the post in "HH:MM" 24-hour format.
        message (str): The message or caption to include in the post.
        media_path (str): Path to the image or video file to be uploaded.
        media_type (str): Type of the media - one of "text", "image", or "video".

    Returns:
        None
    """

    # Parse the provided time string into hour and minute integers
    hour, minute = map(int, post_time.split(":"))

    # Get the current date and time
    now = datetime.now()

    # Replace the current time with the specified posting time
    scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # If the scheduled time is in the past, adjust to the next day
    if scheduled_time < now:
        scheduled_time += timedelta(days=1)

    # Define the job function to be executed at the scheduled time
    def job():
        print(f"[{datetime.now()}] Posting scheduled content...")

        # Call the Facebook posting function
        result = post_to_facebook(message, media_path, media_type)

        # Log the result of the post
        print("Post result:", result or "Failed")

    # Create a one-time trigger for the scheduled time
    trigger = DateTrigger(run_date=scheduled_time)

    # Add the job to the scheduler
    scheduler.add_job(job, trigger=trigger)

    # Log the scheduled time
    print(f"[Scheduler] Job scheduled for {scheduled_time}")
