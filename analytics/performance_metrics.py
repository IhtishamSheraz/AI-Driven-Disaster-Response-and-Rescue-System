# ============================================
# File: analytics/performance_metrics.py
# Description:
# Calculates disaster response KPIs.
# ============================================


class PerformanceMetrics:
    """
    Compute rescue KPIs.
    """

    def calculate_victims_saved(
        self,
        victims
    ):
        """
        Count rescued victims.
        """

        rescued_count = 0

        for victim in victims:

            if victim.is_rescued:

                rescued_count += 1

        return rescued_count

    def calculate_average_rescue_time(
        self,
        rescue_times
    ):
        """
        Compute average rescue time.
        """

        if len(rescue_times) == 0:

            return 0

        return (
            sum(rescue_times)
            /
            len(rescue_times)
        )

    def calculate_resource_utilization(
        self,
        ambulances
    ):
        """
        Compute ambulance utilization.
        """

        total_capacity = 0

        used_capacity = 0

        for ambulance in ambulances:

            total_capacity += ambulance.capacity

            used_capacity += len(
                ambulance.assigned_victims
            )

        if total_capacity == 0:

            return 0

        return (
            used_capacity
            /
            total_capacity
        ) * 100