# This file contains the core time-tracking functionality for the application.
# It handles the clock-in and clock-out processes, including calculating the total time worked by a user,
# and saving this information in a JSON file (`time_logs.json`).

import json
import os
from datetime import datetime
from app.utils import save_time_logs, load_time_logs

TIME_LOGS_FILE = "time_logs.json"  # Define the file to store time logs


def clock_in(user_id):
    """
    Clock in the user by recording the current timestamp as their clock-in time.

    Args:
        user_id (str): The unique identifier for the user clocking in.

    Description:
        This function checks if a user is already clocked in. If they are, it prevents further clocking in.
        If not, it records the clock-in time (current timestamp) in the time logs.
    """
    time_logs = load_time_logs()  # Load existing time logs

    # Check if the user is already clocked in and prevent re-clock-in
    if user_id in time_logs and time_logs[user_id].get("clock_in_time") and not time_logs[user_id].get(
            "clock_out_time"):
        print(f"User {user_id} is already clocked in.")
        return

    # Record clock-in time (current time)
    clock_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp
    time_logs[user_id] = {"clock_in_time": clock_in_time, "clock_out_time": None, "total_time": 0}
    save_time_logs(time_logs)  # Save the updated time logs
    print(f"User {user_id} clocked in at {clock_in_time}")


def clock_out(user_id):
    """
    Clock out the user by recording the current timestamp as their clock-out time
    and calculating the total time worked.

    Args:
        user_id (str): The unique identifier for the user clocking out.

    Description:
        This function checks if a user is clocked in. If the user is not clocked in, it prevents clocking out.
        It calculates the total time worked by finding the difference between the clock-out time and clock-in time.
        The total time worked is calculated in seconds and saved in the time logs.
    """
    time_logs = load_time_logs()  # Load existing time logs

    # Ensure the user is clocked in
    if user_id not in time_logs or time_logs[user_id].get("clock_in_time") is None:
        print(f"User {user_id} is not clocked in.")
        return

    # Record clock-out time and calculate total time worked
    clock_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp
    clock_in_time = datetime.strptime(time_logs[user_id]["clock_in_time"],
                                      "%Y-%m-%d %H:%M:%S")  # Convert string to datetime object
    clock_out_time_obj = datetime.strptime(clock_out_time, "%Y-%m-%d %H:%M:%S")

    # Calculate total time worked in seconds
    total_time_worked = (clock_out_time_obj - clock_in_time).total_seconds()

    # Update time logs with clock-out time and total time worked
    time_logs[user_id]["clock_out_time"] = clock_out_time
    time_logs[user_id]["total_time"] = total_time_worked
    save_time_logs(time_logs)  # Save the updated time logs

    print(f"User {user_id} clocked out at {clock_out_time}")
    print(f"Total time worked: {total_time_worked / 3600:.2f} hours")


def view_time_log(user_id):
    """
    View the user's time log.

    Args:
        user_id (str): The unique identifier for the user whose log we want to view.

    Description:
        This function loads the time logs and prints out the clock-in time, clock-out time, and total time worked for the specified user.
        If the user does not exist in the logs, it prints a message saying no logs were found for the user.
    """
    time_logs = load_time_logs()  # Load existing time logs
    if user_id not in time_logs:
        print(f"No time log found for user {user_id}.")
        return

    log = time_logs[user_id]
    print(f"User {user_id} Time Log:")
    print(f"Clock-in time: {log.get('clock_in_time')}")
    print(f"Clock-out time: {log.get('clock_out_time')}")
    print(f"Total time worked: {log.get('total_time') / 3600:.2f} hours")

