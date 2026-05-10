# ============================================
# File: logging_system/decision_logger.py
# Description:
# Logs AI decisions and replanning events.
# ============================================

from datetime import datetime


class DecisionLogger:
    """
    Decision logging system.
    """

    def __init__(self):

        self.logs = []

    def log_event(
        self,
        event_type,
        description,
        data=None
    ):
        """
        Store simulation events.
        """

        timestamp = datetime.now()

        log_message = {

            "time": str(timestamp),

            "event_type": event_type,

            "description": description,

            "data": data or {}
        }

        self.logs.append(log_message)

        print("\n[DECISION LOG]")
        print(f"Time: {timestamp}")
        print(f"Event: {event_type}")
        print(f"Description: {description}")

    def display_complete_logs(self):
        """
        Display all stored logs.
        """

        print("\n=================================")
        print("COMPLETE DECISION LOGS")
        print("=================================")

        for log in self.logs:

            print("\n-------------------------")

            print(f"Time: {log['time']}")

            print(
                f"Event Type: "
                f"{log['event_type']}"
            )

            print(
                f"Description: "
                f"{log['description']}"
            )
