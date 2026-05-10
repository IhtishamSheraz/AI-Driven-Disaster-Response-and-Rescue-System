# ============================================
# File: main.py
# ============================================

from environment.grid_environment import (
    GridEnvironment
)

from visualization.console_visualizer import (
    ConsoleVisualizer
)

from agents.disaster_response_agent import (
    DisasterResponseAgent
)


def start_disaster_response_simulation():

    # =====================================
    # CREATE ENVIRONMENT
    # =====================================

    environment = GridEnvironment()

    # =====================================
    # CONSOLE VISUALIZER
    # =====================================

    visualizer = ConsoleVisualizer(
        environment
    )

    # =====================================
    # CREATE AI AGENT
    # =====================================

    agent = DisasterResponseAgent(

        environment=environment,

        visualizer=visualizer
    )

    # =====================================
    # DISPLAY INITIAL ENVIRONMENT
    # =====================================

    visualizer.display_environment()

    # =====================================
    # START AUTONOMOUS LIVE SYSTEM
    # =====================================

    agent.simulation_window.run_live_simulation(
        agent
    )


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    start_disaster_response_simulation()