# ============================================
# File: analytics/report_generator.py
# Description:
# Generate final disaster response report.
# ============================================

from datetime import datetime


class ReportGenerator:
    """
    Generate final simulation report.
    """

    def generate_report(
        self,
        victims_saved,
        average_rescue_time,
        resource_utilization
    ):
        """
        Print final project report.
        """

        print("\n=================================")
        print("FINAL DISASTER RESPONSE REPORT")
        print("=================================")

        print(
            f"\nReport Time: "
            f"{datetime.now()}"
        )

        print(
            f"\nVictims Saved: "
            f"{victims_saved}"
        )

        print(
            f"\nAverage Rescue Time: "
            f"{average_rescue_time:.2f}"
        )

        print(
            f"\nResource Utilization: "
            f"{resource_utilization:.2f}%"
        )