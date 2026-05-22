import os
import yaml
from datetime import datetime, timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def main():
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

    with open("reminders.yaml") as f:
        config = yaml.safe_load(f)

    now = datetime.now(timezone.utc)
    # Round down to nearest 5-minute block to match GitHub Actions schedule
    total_minutes = (now.hour * 60 + now.minute) // 5 * 5
    current_time = f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"

    for reminder in config.get("reminders", []):
        if reminder["time"] != current_time:
            continue

        email = reminder["to"]
        message = reminder.get("message", "HEY")

        try:
            user = client.users_lookupByEmail(email=email)
            user_id = user["user"]["id"]
            client.chat_postMessage(channel=user_id, text=message)
            print(f"Sent to {email}: {message}")
        except SlackApiError as e:
            print(f"Failed to send to {email}: {e.response['error']}")


if __name__ == "__main__":
    main()
