import Event
import Input
import HeliDirection
import HeliHeight
import WayPoint


def init():
    pass


def run():
    print("Mode helicopter waypoint")

    height_manager = HeliHeight.HeliHeight()
    direction_manager = HeliDirection.HeliDirection()
    waypoint_manager = WayPoint.WayPoint()

    while True:
        Event.wait()

        position = Input.get_position()
        rotation = Input.get_rotation()
        waypoint = waypoint_manager.get_current_waypoint()
        speed = Input.get_norm_speed()
        rotation_speed = Input.get_rotation_speed()

        direction_manager.event(position, rotation, waypoint)
        height_manager.event(position, rotation, waypoint)

        waypoint_manager.check_waypoint_distance(position, speed)
