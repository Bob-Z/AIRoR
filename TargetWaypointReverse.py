import TargetWaypoint


class TargetWaypointReverse(TargetWaypoint.TargetWaypoint):
    def __init__(self):
        super().__init__(reverse=True)
