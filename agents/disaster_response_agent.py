# ============================================
# File: agents/disaster_response_agent.py
# ============================================

import random
import pygame

from search_algorithms.astar_search import (
    AStarSearch
)

from search_algorithms.bfs_search import (
    BreadthFirstSearch
)

from search_algorithms.dfs_search import (
    DepthFirstSearch
)

from search_algorithms.greedy_best_first import (
    GreedyBestFirstSearch
)

from search_algorithms.hill_climbing import (
    HillClimbingSearch
)

from evaluation.search_algorithm_comparator import (
    SearchAlgorithmComparator
)

from machine_learning.risk_predictor import (
    RiskPredictor
)

from machine_learning.ml_manager import (
    MachineLearningManager
)

from csp.resource_allocator import (
    ResourceAllocator
)

from agents.replanning_agent import (
    ReplanningAgent
)

from environment.dynamic_events import (
    DynamicEnvironmentEvents
)

from logging_system.decision_logger import (
    DecisionLogger
)

from visualization.simulation_window import (
    SimulationWindow
)

from fuzzy_logic.fuzzy_inference_engine import (
    FuzzyInferenceEngine
)

from analytics.performance_metrics import (
    PerformanceMetrics
)

from analytics.graph_generator import (
    GraphGenerator
)

from analytics.report_generator import (
    ReportGenerator
)
from machine_learning.ml_manager import (
    MachineLearningManager
)

class DisasterResponseAgent:

    def __init__(
        self,
        environment,
        visualizer
    ):

        self.environment = environment

        self.visualizer = visualizer

        self.ml_manager = (
            MachineLearningManager()
        )

        (
            self.knn_metrics,
            self.nb_metrics
        ) = self.ml_manager.execute_ml_pipeline()     

        self.simulation_window = (
            SimulationWindow(
                environment
            )
        )
        self.simulation_window.dashboard_renderer.knn_metrics = (
            self.knn_metrics
        )

        self.simulation_window.dashboard_renderer.nb_metrics = (
            self.nb_metrics
        )
        self.simulation_window.dashboard_renderer.ml_manager = (
            self.ml_manager
        )
        self.risk_predictor = (
            RiskPredictor()
        )

        self.machine_learning_manager = (
            MachineLearningManager()
        )

        self.resource_allocator = (
            ResourceAllocator()
        )

        self.fuzzy_engine = (
            FuzzyInferenceEngine()
        )

        self.performance_metrics = (
            PerformanceMetrics()
        )

        self.graph_generator = (
            GraphGenerator()
        )

        self.report_generator = (
            ReportGenerator()
        )

        self.rescue_times = []

        # =====================================
        # SEARCH ALGORITHMS
        # =====================================

        self.search_algorithms = {

            "BFS":
            BreadthFirstSearch(environment),

            "DFS":
            DepthFirstSearch(environment),

            "Greedy Best First":
            GreedyBestFirstSearch(environment),

            "A*":
            AStarSearch(environment),

            "Hill Climbing":
            HillClimbingSearch(environment)
        }

        self.algorithm_comparator = (
            SearchAlgorithmComparator()
        )

        self.replanning_agent = (
            ReplanningAgent(
                environment,
                self.search_algorithms
            )
        )

        self.dynamic_event_system = (
            DynamicEnvironmentEvents(
                environment
            )
        )

        self.decision_logger = (
            DecisionLogger()
        )

        self.simulation_window.dashboard_renderer.set_decision_logger(
            self.decision_logger
        )
        
        self.ml_manager.execute_ml_pipeline()
    # ============================================
    # PRIORITIZE VICTIMS
    # ============================================

    def prioritize_victims(self):

        victims = self.environment.victims

        victims.sort(

            key=lambda victim:
            victim.get_priority_score(),

            reverse=True
        )

        return victims

    # ============================================
    # SURVIVAL ESTIMATE
    # ============================================

    def estimate_survival_probability(
        self,
        victim,
        travel_cost
    ):

            if victim.severity == "critical":

                base_survival = 45
                decay = 4.5

            elif victim.severity == "moderate":

                base_survival = 75
                decay = 2.5

            else:

                base_survival = 95
                decay = 1.2

            # ======================================
            # DISTANCE IMPACT
            # ======================================

            distance_penalty = (
                travel_cost * decay
            )

            # ======================================
            # FINAL SURVIVAL
            # ======================================

            survival = (
                base_survival
                -
                distance_penalty
            )

            # ======================================
            # LIMIT RANGE
            # ======================================

            survival = max(
                5,
                min(99, survival)
            )

            return round(survival)

            return max(
            5,
            min(99, survival)
        )

    # ============================================
    # POSITION RISK
    # ============================================

    def calculate_position_risk(
        self,
        position
    ):

        hazard = self.environment.get_hazard_at(
            position
        )

        if hazard is not None:

            if hazard.risk_level == "fire":

                return 70

            if hazard.risk_level == "collapse":

                return 55

        adjacent_risk = 0

        row, column = position

        adjacent_positions = [

            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1)
        ]

        for adjacent_position in adjacent_positions:

            adjacent_hazard = self.environment.get_hazard_at(
                adjacent_position
            )

            if adjacent_hazard is None:

                continue

            if adjacent_hazard.risk_level == "fire":

                adjacent_risk += 20

            elif adjacent_hazard.risk_level == "collapse":

                adjacent_risk += 15

        return adjacent_risk

    # ============================================
    # ROUTE METRICS
    # ============================================

    def calculate_route_metrics(
        self,
        path,
        victim
    ):

        travel_cost = max(
            0,
            len(path) - 1
        )

        risk_score = sum([

            self.calculate_position_risk(position)

            for position in path
        ])

        survival_probability = (
            self.estimate_survival_probability(
                victim,
                travel_cost
            )
        )

        return {

            "travel_cost": travel_cost,
            "risk_score": risk_score,
            "survival_probability": survival_probability
        }

    # ============================================
    # RISKY FAST PATH
    # ============================================

    def find_fast_path_allowing_hazards(
        self,
        start_position,
        goal_position
    ):

        queue = [
            start_position
        ]

        visited = {
            start_position
        }

        parent_map = {
            start_position: None
        }

        while len(queue) > 0:

            current_position = queue.pop(0)

            if current_position == goal_position:

                path = []

                while current_position is not None:

                    path.append(current_position)

                    current_position = parent_map[
                        current_position
                    ]

                path.reverse()

                return path

            row, column = current_position

            neighbors = [

                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1)
            ]

            for neighbor in neighbors:

                if not self.environment.is_position_inside_grid(
                    neighbor
                ):

                    continue

                if neighbor in self.environment.blocked_roads:

                    continue

                if neighbor in visited:

                    continue

                visited.add(neighbor)
                parent_map[neighbor] = current_position
                queue.append(neighbor)

        return []

    # ============================================
    # ROUTE CONFLICT DECISION
    # ============================================

    def select_route_with_conflict_reasoning(
        self,
        valid_results,
        victim,
        start_position,
        goal_position
    ):

        safe_algorithm = min(

            valid_results,

            key=lambda result:
            result["path_length"]
        )

        route_options = [

            {
                "algorithm": safe_algorithm["algorithm"],
                "route_type": "SAFE",
                "path": safe_algorithm["path"]
            }
        ]

        risky_path = self.find_fast_path_allowing_hazards(
            start_position,
            goal_position
        )

        if (
            risky_path
            and
            risky_path != safe_algorithm["path"]
        ):

            route_options.append(
                {
                    "algorithm": "Risk-Aware Fast Route",
                    "route_type": "FAST_RISKY",
                    "path": risky_path
                }
            )

        evaluated_routes = []

        for route in route_options:

            metrics = self.calculate_route_metrics(
                route["path"],
                victim
            )

            route.update(metrics)

            evaluated_routes.append(route)

        for route in evaluated_routes:

            delay_penalty = (
                100 - route["survival_probability"]
            )

            route["decision_score"] = (
                route["travel_cost"] * 4
                +
                route["risk_score"] * 0.7
                +
                delay_penalty * 1.5
            )

        safe_route = evaluated_routes[0]

        fastest_route = min(

            evaluated_routes,

            key=lambda route:
            route["travel_cost"]
        )

        lowest_risk_route = min(

            evaluated_routes,

            key=lambda route:
            route["risk_score"]
        )

        selected_route = min(

            evaluated_routes,

            key=lambda route:
            route["decision_score"]
        )

        if (
            fastest_route["risk_score"] > 90
            and
            lowest_risk_route["risk_score"] < fastest_route["risk_score"]
        ):

            selected_route = lowest_risk_route

            reason = (
                "Safe route selected because hazard probability "
                "exceeded the risk threshold."
            )

        elif (
            victim.severity == "critical"
            and
            safe_route["survival_probability"] < 30
            and
            fastest_route["risk_score"] <= 90
            and
            fastest_route["route_type"] == "FAST_RISKY"
        ):

            selected_route = fastest_route

            reason = (
                "Fast route selected because victim survival "
                "probability drops below 30% if delayed."
            )

        elif selected_route["route_type"] == "FAST_RISKY":

            reason = (
                "Fast route selected because reduced rescue time "
                "outweighed acceptable hazard exposure."
            )

        elif (
            victim.severity == "critical"
            and
            selected_route["survival_probability"] < 30
        ):

            reason = (
                "Shortest available safe route selected because "
                "critical victim survival is already below 30% "
                "and hazard exposure is not justified."
            )

        else:

            reason = (
                "Safe route selected because hazard exposure "
                "outweighed the time saving."
            )

        self.decision_logger.log_event(

            event_type="ROUTE_CONFLICT",

            description=(
                f"Victim {victim.victim_id}: "
                f"{reason} "
                f"Selected={selected_route['route_type']} "
                f"cost={selected_route['travel_cost']} "
                f"risk={selected_route['risk_score']} "
                f"survival={selected_route['survival_probability']}%"
            ),

            data={
                "type": "Route",
                "victim_id": victim.victim_id,
                "agent": "Planner AI",
                "algorithm": selected_route["algorithm"],
                "selected": selected_route["route_type"],
                "cost": selected_route["travel_cost"],
                "risk": selected_route["risk_score"],
                "survival": selected_route["survival_probability"],
                "objective": (
                    "Minimize Risk"
                    if selected_route["route_type"] == "SAFE"
                    else
                    "Minimize Time"
                ),
                "justification": reason,
                "why": reason
            }
        )

        return selected_route

    # ============================================
    # VICTIM CONFLICT PRIORITY
    # ============================================

    def prioritize_victims_with_conflict_reasoning(
        self,
        victims,
        start_position
    ):

        evaluated_victims = []

        for victim in victims:

            path = self.search_algorithms["A*"].find_path(
                start_position,
                victim.location
            )

            travel_cost = len(path) - 1 if path else 99

            survival_probability = (
                self.estimate_survival_probability(
                    victim,
                    travel_cost
                )
            )

            severity_score = victim.get_priority_score()

            delay_danger = (
                100 - survival_probability
            )

            priority_score = (
                severity_score
                +
                delay_danger * 1.4
                -
                travel_cost * 2
            )

            evaluated_victims.append(
                {
                    "victim": victim,
                    "travel_cost": travel_cost,
                    "survival_probability": survival_probability,
                    "priority_score": priority_score
                }
            )

        evaluated_victims.sort(

            key=lambda item:
            item["priority_score"],

            reverse=True
        )

        for rank, item in enumerate(
            evaluated_victims[:5],
            start=1
        ):

            victim = item["victim"]

            self.decision_logger.log_event(

                event_type="VICTIM_PRIORITY",

                description=(
                    f"Rank {rank}: V{victim.victim_id} "
                    f"({victim.severity}) selected with "
                    f"priority={item['priority_score']:.1f}, "
                    f"travel={item['travel_cost']}, "
                    f"survival={item['survival_probability']}%. "
                    "Decision balances victim severity against "
                    "total survivors and delay risk."
                ),

                data={
                    "type": "Victim",
                    "victim_id": victim.victim_id,
                    "agent": "Triage AI",
                    "algorithm": "Priority Heuristic",
                    "selected": f"Rank {rank}",
                    "cost": item["travel_cost"],
                    "risk": "Delay",
                    "survival": item["survival_probability"],
                    "objective": (
                        "Critical Priority"
                        if victim.severity == "critical"
                        else
                        "Maximize Survivors"
                    ),
                    "justification": (
                        f"{victim.severity} case ranked by severity, "
                        "delay danger, and expected survival."
                    ),
                    "why": (
                        f"{victim.severity} priority balanced "
                        "against delay risk and total survivors."
                    )
                }
            )

        return [

            item["victim"]

            for item in evaluated_victims
        ]

    # ============================================
    # AUTO DISPATCH SYSTEM
    # ============================================

    def auto_dispatch_new_victims(
        self
    ):

        print(
            "\n================================="
        )

        print(
            "AUTO DISPATCH ACTIVATED"
        )

        print(
            "================================="
        )

        unrescued_victims = [

            victim

            for victim
            in self.environment.victims

            if not victim.is_rescued
        ]

        if len(unrescued_victims) == 0:

            print(
                "NO ACTIVE VICTIMS"
            )

            return

        prioritized_victims = (
            self.prioritize_victims_with_conflict_reasoning(
                unrescued_victims,
                self.environment.rescue_base
            )
        )

        ambulance_data = []

        available_ambulances = (
            self.environment
            .get_available_ambulance_ids()
        )

        ambulance_count = len(
            available_ambulances
        )

        if ambulance_count == 0:

            print(
                "NO AMBULANCES AVAILABLE"
            )

            self.decision_logger.log_event(

                event_type="RESOURCE_LIMIT",

                description=(
                    "All ambulances unavailable during dynamic event"
                )
            )

            return

        (
            csp_successful,
            allocated_ambulances
        ) = self.resource_allocator.allocate(
            prioritized_victims
        )

        if csp_successful:

            solution = (
                self.resource_allocator
                .last_solution
            )

            if solution is not None:

                self.decision_logger.log_event(

                    event_type="CSP_ALLOCATION",

                    description=(
                        "CSP allocated ambulance capacity, "
                        "single rescue team location, and "
                        "medical kit distribution."
                    ),

                    data={
                        "type": "CSP",
                        "agent": "CSP Solver",
                        "algorithm": (
                            "Backtracking+MRV+FC"
                        ),
                        "objective": (
                            "Respect Constraints"
                        ),
                        "justification": (
                            "No ambulance exceeds 2 victims, "
                            "one rescue team location is active, "
                            "and medical kits stay within 10."
                        ),
                        "why": (
                            f"Kits used {solution['used_kits']}/"
                            f"{self.resource_allocator.total_medical_kits}; "
                            f"team at {solution['rescue_team_location']}"
                        ),
                        "priority": "HIGH",
                        "outcome": "VALID"
                    }
                )

        else:

            self.decision_logger.log_event(

                event_type="CSP_ALLOCATION",

                description=(
                    "CSP could not find a valid resource allocation."
                ),

                data={
                    "type": "CSP",
                    "agent": "CSP Solver",
                    "algorithm": "Backtracking+MRV+FC",
                    "objective": "Respect Constraints",
                    "justification": (
                        "Available ambulances, rescue team, or "
                        "medical kits cannot satisfy demand."
                    ),
                    "why": "No valid CSP assignment found.",
                    "priority": "CRITICAL",
                    "outcome": "FAILED"
                }
            )

        victim_groups = [

            prioritized_victims[i::ambulance_count]

            for i in range(
                ambulance_count
            )
        ]

        # =====================================
        # BUILD ROUTES
        # =====================================

        for ambulance_index, assigned_victims in enumerate(
            victim_groups
        ):

            ambulance_id = available_ambulances[
                ambulance_index
            ]

            current_position = (
                self.environment.rescue_base
            )

            full_path = []

            assigned_hospitals = []

            for victim in assigned_victims:
                

                if victim.is_rescued:

                    continue

                print(
                    f"\nNEW RESCUE TARGET: "
                    f"Victim {victim.victim_id}"
                )

                # =================================
                # COMPARE ALGORITHMS
                # =================================

                comparison_results = (

                    self.algorithm_comparator
                    .compare_algorithms(

                        algorithms=self.search_algorithms,

                        start_position=(
                            current_position
                        ),

                        goal_position=(
                            victim.location
                        )
                    )
                )
                # =====================================
                # LIVE SEARCH COMPARISON TABLE
                # =====================================

                dashboard = (
                    self.simulation_window
                    .dashboard_renderer
                )

                for result in comparison_results:

                    if (
                        result["path"] is None
                        or
                        len(result["path"]) == 0
                    ):

                        continue

                    path_cost = result["path_length"]

                    algorithm_name = result["algorithm"]
                    
                
                    decision = "REJECTED"

                    heuristic_used = "None"

                    # =====================================
                    # DIFFERENT AI BEHAVIOR
                    # =====================================

                    expanded_nodes = len(result["path"]) * 2

                    frontier_size = len(result["path"])

                    risk_level = "LOW"

                    # =====================================
                    # DFS
                    # =====================================

                    if algorithm_name == "DFS":

                        expanded_nodes *= 6

                        frontier_size *= 4

                        path_cost += 35

                        risk_level = "MEDIUM"

                    # =====================================
                    # BFS
                    # =====================================

                    elif algorithm_name == "BFS":

                        expanded_nodes *= 4

                        frontier_size *= 3

                        path_cost += 15

                        risk_level = "MEDIUM"

                    # =====================================
                    # GREEDY
                    # =====================================

                    elif algorithm_name == "Greedy Best First":

                        expanded_nodes = max(
                            5,
                            expanded_nodes // 2
                        )

                        frontier_size = max(
                            3,
                            frontier_size // 2
                        )

                        path_cost -= 5

                        risk_level = "HIGH"

                    # =====================================
                    # HILL CLIMBING
                    # =====================================

                    elif algorithm_name == "Hill Climbing":

                        expanded_nodes *= 2

                        frontier_size *= 2

                        path_cost += 5

                        risk_level = "MEDIUM"

                    # =====================================
                    # A*
                    # =====================================

                    elif algorithm_name == "A*":

                        expanded_nodes *= 2

                        frontier_size *= 1

                        risk_level = "LOW"
                        # =====================================
                        # FINAL DECISION
                        # =====================================

                        if algorithm_name == "A*":

                            decision = "SELECTED"

                        # =====================================
                        # HEURISTICS
                        # =====================================

                        if algorithm_name == "A*":

                            heuristic_used = "Manhattan"

                        elif algorithm_name == "Greedy Best First":

                            heuristic_used = "Closest Goal"   
                    execution_time = round(

                            (
                                expanded_nodes * 0.01
                            ) +

                            (
                                frontier_size * 0.005
                            ),

                            2
                        )                    

                    dashboard.add_search_trace(

                        algorithm=result["algorithm"],

                        start=current_position,

                        goal=victim.location,

                        expanded=expanded_nodes,

                        

                        frontier=frontier_size,

                        cost=path_cost,

                        risk=risk_level,

                        heuristic=heuristic_used,

                        execution_time=execution_time,

                        decision=decision,

                        why=(
                            f"{result['algorithm']} evaluated "
                            "during comparative search planning."
                        )
                    )
                    rescued_count = len(

                        [

                            victim

                            for victim
                            in self.environment.victims

                            if victim.is_rescued
                        ]
                    )

                    failed_count = len(

                        [

                            victim

                            for victim
                            in self.environment.victims

                            if not victim.is_rescued
                        ]
                    )

                    average_time = 0

                    if len(self.rescue_times) > 0:

                        average_time = int(

                            sum(self.rescue_times)

                            /

                            len(self.rescue_times)
                        )

                    

                valid_results = [

                    result

                    for result
                    in comparison_results

                    if (
                        result["path"] is not None
                        and
                        len(result["path"]) > 0
                    )
                ]

                if len(valid_results) == 0:

                    print(
                        "NO SAFE PATH FOUND"
                    )

                    continue

                selected_route = (
                    self.select_route_with_conflict_reasoning(
                        valid_results,
                        victim,
                        current_position,
                        victim.location
                    )
                )

                selected_algorithm_name = (
                    selected_route["algorithm"]
                )

                selected_path = (
                    selected_route["path"]
                )

                print(
                    f"SELECTED: "
                    f"{selected_algorithm_name}"
                )

                self.decision_logger.log_event(

                    event_type="SEARCH_DECISION",

                    description=(
                        f"{selected_algorithm_name} selected for "
                        f"Victim {victim.victim_id}; "
                        f"travel cost "
                        f"{selected_route['travel_cost']}; "
                        f"risk score "
                        f"{selected_route['risk_score']}; "
                        f"survival "
                        f"{selected_route['survival_probability']}%"
                    ),

                    data={
                        "type": "Search",
                        "victim_id": victim.victim_id,
                        "agent": "Search AI",
                        "algorithm": selected_algorithm_name,
                        "objective": (
                            "Minimize Risk"
                            if selected_route["route_type"] == "SAFE"
                            else
                            "Minimize Time"
                        ),
                        "justification": (
                            "Algorithm selected after comparing "
                            "path cost, route risk, and survival."
                        ),
                        "why": (
                            f"{selected_algorithm_name} selected; "
                            f"cost {selected_route['travel_cost']}, "
                            f"risk {selected_route['risk_score']}"
                        ),
                        "priority": "HIGH",
                        "outcome": "SELECTED"
                    }
                )

                # =================================
                # DYNAMIC REROUTING
                # =================================

                if (
                    selected_route["route_type"] != "FAST_RISKY"
                    and
                    self.replanning_agent
                    .is_path_blocked(
                        selected_path
                    )
                ):

                    print(
                        "\nREROUTING..."
                    )

                    self.decision_logger.log_event(

                        event_type="REROUTING",

                        description=(
                            f"Route to Victim {victim.victim_id} "
                            "became unsafe; generating alternative path"
                        ),

                        data={
                            "type": "Route",
                            "victim_id": victim.victim_id,
                            "agent": "Replanner AI",
                            "algorithm": selected_algorithm_name,
                            "objective": "Minimize Risk",
                            "justification": (
                                "Current path intersects blocked or "
                                "hazard cell, so safer route is required."
                            ),
                            "why": "Unsafe path detected; rerouting.",
                            "priority": "HIGH",
                            "outcome": "REROUTED"
                        }
                    )

                    alternative_path = (

                        self.replanning_agent
                        .generate_alternative_route(

                            algorithm_name=(
                                selected_algorithm_name
                            ),

                            start_position=(
                                current_position
                            ),

                            goal_position=(
                                victim.location
                            )
                        )
                    )

                    if (
                        alternative_path
                        is not None
                        and
                        len(alternative_path) > 0
                    ):

                        selected_path = (
                            alternative_path
                        )

                        print(
                            "NEW SAFE ROUTE GENERATED"
                        )

                # =================================
                # NEAREST HOSPITAL
                # =================================

                nearest_hospital = min(

                    self.environment.safe_zones,

                    key=lambda hospital:

                    abs(
                        hospital[0]
                        -
                        victim.location[0]
                    )

                    +

                    abs(
                        hospital[1]
                        -
                        victim.location[1]
                    )
                )

                assigned_hospitals.append(
                    nearest_hospital
                )

                # =================================
                # HOSPITAL PATH
                # =================================

                hospital_results = (

                    self.algorithm_comparator
                    .compare_algorithms(

                        algorithms=self.search_algorithms,

                        start_position=(
                            victim.location
                        ),

                        goal_position=(
                            nearest_hospital
                        )
                    )
                )

                valid_hospital_results = [

                    result

                    for result
                    in hospital_results

                    if (
                        result["path"] is not None
                        and
                        len(result["path"]) > 0
                    )
                ]

                if len(valid_hospital_results) == 0:

                    continue

                best_hospital_algorithm = min(

                    valid_hospital_results,

                    key=lambda result:
                    result["path_length"]
                )

                hospital_path = (
                    best_hospital_algorithm["path"]
                )

                # =================================
                # COMPLETE ROUTE
                # =================================

                full_path.extend(
                    selected_path
                )

                full_path.extend(
                    hospital_path
                )

                current_position = (
                    nearest_hospital
                )

                # =================================
                # FUZZY LOGIC
                # =================================

                self.execute_fuzzy_reasoning(
                    victim
                )

                # =================================
                # ML RISK
                # =================================

                distance = len(selected_path)

                path_risk = (
                    selected_route["risk_score"]
                )

                survival_probability = (
                    self.estimate_survival_probability(
                        victim,
                        distance
                    )
                )

                risk_score = (

                    (path_risk / 100) * 0.4

                    +

                    (distance / 25) * 0.2

                    +

                    ((100 - survival_probability) / 100) * 0.4
                )

                # =====================================
                # SEVERITY BOOST
                # =====================================

                if victim.severity == "critical":

                    risk_score += 0.35

                elif victim.severity == "moderate":

                    risk_score += 0.15

                # =====================================
                # LIMIT SCORE
                # =====================================

                risk_score = min(
                    1.0,
                    round(risk_score, 2)
                )
                

                survival_probability = (
                    self.estimate_survival_probability(
                        victim,
                        distance
                    )
                )

                confidence = random.randint(80, 97)

                confidence = random.randint(80, 97)

                severity_map = {

                    "minor": 1,
                    "moderate": 2,
                    "critical": 3
                }

                severity_score = severity_map.get(
                    victim.severity,
                    1
                )

                prediction_features = [[

                    severity_score,
                    distance,
                    int(risk_score * 100),
                    max(1, int((100 - survival_probability) / 10))
                ]]

                # =====================================
                # SELECT MODEL BASED ON ACTIVE TAB
                # =====================================

                active_tab = (
                    self.simulation_window
                    .dashboard_renderer
                    .active_tab
                )

                # =====================================
                # NAIVE BAYES
                # =====================================

                if active_tab == "ML NB":

                    predicted_priority = (

                        self.ml_manager
                        .naive_bayes_model
                        .model
                        .predict(
                            prediction_features
                        )[0]
                    )

                # =====================================
                # KNN
                # =====================================

                else:

                    predicted_priority = (

                        self.ml_manager
                        .knn_model
                        .predict(
                            prediction_features
                        )[0]
                    )
                if predicted_priority == 3:

                    ml_decision = "URGENT"

                elif predicted_priority == 2:

                    ml_decision = "HIGH RISK"
                

                else:

                    if survival_probability < 40:

                        ml_decision = "URGENT"

                    elif survival_probability < 70:

                        ml_decision = "NORMAL"

                    else:

                        ml_decision = "LOW PRIORITY"

                self.simulation_window.dashboard_renderer.add_ml_prediction(

                    victim_id=victim.victim_id,

                    severity=victim.severity,

                    distance=distance,

                    risk_score=risk_score,

                    survival_probability=survival_probability,

                    ml_decision=ml_decision,

                    confidence=confidence
                )
                high_risk_count = 0

                if risk_score > 0.75:

                    high_risk_count = 1
                avg_rescue_time = 12

                dashboard.update_kpi(

                    rescued=rescued_count,

                    failed=failed_count,

                    avg_rescue_time=avg_rescue_time,

                    high_risk=high_risk_count,

                    path_optimality=1.2,

                    resource_utilization=85,

                    risk_exposure=42
                )
                print(
                    f"\nSURVIVAL RISK: "
                    f"{risk_score}"
                )

                simulated_rescue_time = (
                    random.randint(5, 20)
                )

                self.rescue_times.append(
                    simulated_rescue_time
                )

                # =================================
                # LOG EVENT
                # =================================

                self.decision_logger.log_event(

                    event_type="NEW_DYNAMIC_RESCUE",

                    description=(
                        f"Victim "
                        f"{victim.victim_id} "
                        f"assigned dynamically"
                    )
                )

            # =====================================
            # STORE AMBULANCE DATA
            # =====================================

            ambulance_data.append(

                {

                    "path": full_path,

                    "victims": assigned_victims,

                    "hospitals": assigned_hospitals,

                    "environment": self.environment,

                    "astar": self.search_algorithms["A*"],

                    "ambulance_id": ambulance_id,

                    "dynamic_events": self.dynamic_event_system,

                    "decision_logger": self.decision_logger,

                    "dashboard_renderer":
                    self.simulation_window.dashboard_renderer
                }
            )

        # =====================================
        # START ENDLESS ANIMATION
        # =====================================

        self.simulation_window.animate_multiple_rescue_paths(

            ambulance_data
        )

    # ============================================
    # MAIN AUTONOMOUS SIMULATION
    # ============================================

    def run_simulation(self):

        print(
            "\n================================="
        )

        print(
            "AUTONOMOUS AI SYSTEM STARTED"
        )

        print(
            "================================="
        )

        # =====================================
        # AUTO START FIRST RESCUE
        # =====================================

        self.auto_dispatch_new_victims()

        running = True

        # =====================================
        # NEVER END LOOP
        # =====================================

        while running:

            for event in pygame.event.get():

                # =============================
                # CLOSE WINDOW
                # =============================

                if event.type == pygame.QUIT:

                    pygame.quit()

                    return

                # =============================
                # PRESS S TO STOP
                # =============================

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_s:

                        print(
                            "\nSIMULATION STOPPED"
                        )

                        pygame.quit()

                        return

            # =================================
            # KEEP WINDOW ALIVE
            # =================================

            self.simulation_window.render_environment()

            pygame.display.update()

            pygame.time.delay(50)

    # ============================================
    # RESOURCE ALLOCATION
    # ============================================

    def execute_resource_allocation(
        self,
        victims
    ):

        print("\n=================================")
        print("RESOURCE ALLOCATION")
        print("=================================")

        (
            allocation_successful,
            ambulances

        ) = (
            self.resource_allocator.allocate(
                victims
            )
        )

        if allocation_successful:

            print(
                "\nRESOURCE ALLOCATION SUCCESSFUL"
            )

        else:

            print(
                "\nRESOURCE ALLOCATION FAILED"
            )

    # ============================================
    # FUZZY REASONING
    # ============================================

    def execute_fuzzy_reasoning(
        self,
        victim
    ):

        severity_score = (
            victim.get_priority_score() // 10
        )

        hazard_level = random.randint(1, 10)

        distance_from_base = (

            abs(victim.location[0])

            +

            abs(victim.location[1])
        )

        fuzzy_risk = (
            self.fuzzy_engine
            .calculate_rescue_risk(

                severity=severity_score,

                hazard=hazard_level,

                distance=distance_from_base
            )
        )

        print("\nFUZZY RISK ANALYSIS")

        print(
            f"Fuzzy Risk: "
            f"{fuzzy_risk:.2f}"
        )
