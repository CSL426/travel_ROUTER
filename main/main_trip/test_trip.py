from feature.trip import TripPlanningSystem
from feature.trip.sample_data import DEFAULT_LOCATIONS, DEFAULT_REQUIREMENT

system = TripPlanningSystem()

result = system.plan_trip(
    locations=DEFAULT_LOCATIONS,
    requirement=DEFAULT_REQUIREMENT
)

system.print_itinerary(
    result,
    show_navigation=False
)
