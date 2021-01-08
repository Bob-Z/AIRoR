import threading


event = threading.Event()


def wait():
    global event
    event.wait()


def set_event():
    global event
    event.set()


def clear_event():
    global event
    event.clear()
