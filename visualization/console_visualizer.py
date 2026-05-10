# ============================================
# File: visualization/console_visualizer.py
# Description:
# Provides console-based visualization
# for the disaster environment.
# ============================================


class ConsoleVisualizer:
    """
    Visualize simulation environment.
    """

    def __init__(self, environment):

        self.environment = environment

    def display_environment(self):
        """
        Print environment details.
        """

        print("\n=================================")
        print("DISASTER ENVIRONMENT INITIALIZED")
        print("=================================")

        print(f"Rescue Base: {self.environment.rescue_base}")

        print("\nMedical Centers:")
        for center in self.environment.medical_centers:
            print(center)

        print("\nVictims:")
        for victim in self.environment.victims:

            print(
                f"Victim {victim.victim_id} | "
                f"Location: {victim.location} | "
                f"Severity: {victim.severity}"
            )

        print("\nBlocked Roads:")
        for blocked in self.environment.blocked_roads:
            print(blocked)