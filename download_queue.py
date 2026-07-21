from queue import Queue
from threading import Thread
import logging

logger = logging.getLogger(__name__)


class DownloadQueue:

    def __init__(self, downloader):

        self.downloader = downloader

        self.queue = Queue()

        self.worker = Thread(
            target=self._worker,
            daemon=True,
        )

        self.running = False

    def start(self):

        if self.running:
            return

        self.running = True

        self.worker.start()

        logger.info("Download queue started.")

    def stop(self):

        self.running = False

        logger.info("Download queue stopped.")

    def add(self, url):

        self.queue.put(url)

        logger.info(
            f"Added to queue: {url}"
        )

    def _worker(self):

        while self.running:

            url = self.queue.get()

            try:

                self.downloader.download_with_retry(
                    url
                )

            except Exception as error:

                logger.error(error)

            finally:

                self.queue.task_done()

    def pending(self):

        return self.queue.qsize()

    def wait(self):

        self.queue.join()
