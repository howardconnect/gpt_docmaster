# event_queue.py

from queue import Queue

# a global queue that handler.py will push into,
# and app.py will stream out to clients
event_queue = Queue()
