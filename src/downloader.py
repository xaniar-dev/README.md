def download(
    self,
    url: str,
    progress_callback: Callable[[int, float], None] | None = None,
) -> Path:
    """
    Download a file with progress tracking.
    """

    filename = self.get_filename(url)

    final_path = self.download_path / filename

    temp_path = final_path.with_suffix(
        final_path.suffix + ".part"
    )

    logger.info(f"Starting download: {url}")

    if self.display:
        self.display.show_message(
            "Downloading",
            filename[:16],
        )

    start_time = time.time()

    with self.client.stream(
        "GET",
        url,
    ) as response:

        response.raise_for_status()

        total_size = int(
            response.headers.get(
                "Content-Length",
                0,
            )
        )

        if (
            total_size > 0
            and not self.has_enough_space(total_size)
        ):
            raise RuntimeError(
                "Not enough disk space."
            )

        downloaded = 0

        with open(
            temp_path,
            "wb",
        ) as file:

            for chunk in response.iter_bytes(
                chunk_size=8192
            ):

                if not chunk:
                    continue

                file.write(chunk)

                downloaded += len(chunk)

                elapsed = max(
                    time.time() - start_time,
                    0.001,
                )

                speed = downloaded / elapsed

                if total_size > 0:
                    percent = int(
                        downloaded * 100 / total_size
                    )
                else:
                    percent = 0

                logger.info(
                    f"{percent}% | "
                    f"{self.format_size(downloaded)} / "
                    f"{self.format_size(total_size)} | "
                    f"{self.format_size(speed)}/s"
                )

                if self.display:
                    self.display.show_message(
                        f"{percent}%",
                        filename[:16],
                    )

                if progress_callback:
                    progress_callback(
                        percent,
                        speed,
                    )

    temp_path.rename(final_path)

    logger.info(
        f"Download completed: {filename}"
    )

    if self.display:
        self.display.show_message(
            "Completed",
            filename[:16],
        )

    return final_path
def download_with_retry(
    self,
    url: str,
    retries: int = 3,
) -> Path:
    """
    Download a file with automatic retry.
    """

    last_error = None

    for attempt in range(1, retries + 1):

        try:

            logger.info(
                f"Download attempt {attempt}/{retries}"
            )

            if self.display:

                self.display.show_message(
                    "Download",
                    f"Try {attempt}/{retries}"
                )

            return self.download(url)

        except HTTPError as error:

            last_error = error

            logger.warning(
                f"HTTP error: {error}"
            )

        except Exception as error:

            last_error = error

            logger.error(
                f"Unexpected error: {error}"
            )

        if attempt < retries:

            if self.display:

                self.display.show_message(
                    "Retry",
                    f"{attempt}/{retries}"
                )

            logger.info(
                "Waiting before retry..."
            )

            time.sleep(2)

    logger.error(
        "Download failed after all retries."
    )

    if self.display:

        self.display.show_message(
            "Failed",
            "Download"
        )

    raise RuntimeError(
        f"Download failed after {retries} attempts."
    ) from last_error
    def __enter__(self):
    """
    Support context manager.
    """

    return self


def __exit__(
    self,
    exc_type,
    exc_value,
    traceback,
):
    """
    Close resources automatically.
    """

    self.close()
    def file_exists(
    self,
    url: str,
) -> bool:
    """
    Check whether the file already exists.
    """

    filename = self.get_filename(url)

    path = self.download_path / filename

    return path.exists()
    def delete_partial(
    self,
    url: str,
) -> None:
    """
    Delete partial download file.
    """

    filename = self.get_filename(url)

    temp_path = (
        self.download_path / filename
    ).with_suffix(
        Path(filename).suffix + ".part"
    )

    if temp_path.exists():

        temp_path.unlink()

        logger.info(
            f"Deleted partial file: {temp_path}"
        )
