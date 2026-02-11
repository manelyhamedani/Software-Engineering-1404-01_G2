"""
Service instances for Team10 application.

This module provides singleton instances of application services that can be
imported and reused across the application. This is the standard Django pattern
for stateless services.

All services here should be stateless - they should not store request-specific
data as instance variables.
"""

from .application.services.trip_planning_service_impl import TripPlanningServiceImpl


# Singleton service instances
# These are created once when the module is first imported
# and reused for all requests

trip_planning_service = TripPlanningServiceImpl()
"""
Singleton instance of TripPlanningService.
Use this for all trip planning operations across the application.

Example:
    from team10.services import trip_planning_service

    trip = trip_planning_service.create_initial_trip(data, user)
"""


# Export all services
__all__ = [
    'trip_planning_service',
]
