"""
Download queue manager.
"""

from queue import Queue


class DownloadQueue:
    """Manage download requests."""

    def __init__(self):
        self.queue = Queue()

    def add(self, url: str):
        """Add a new download request."""
        self.queue.put(url)

    def get(self):
        """Get the next download request."""
        if self.queue.empty():
            return None
        return self.queue.get()

    def is_empty(self) -> bool:
        """Check whether the queue is empty."""
        return self.queue.empty()

    def size(self) -> int:
        """Return the number of queued items."""
        return self.queue.qsize()
