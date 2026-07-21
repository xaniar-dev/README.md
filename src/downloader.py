    def download(
        self,
        url: str,
        progress_callback: Callable[[int, float], None] | None = None,
    ) -> Path:
        """Download file with progress."""

        filename = self.get_filename(url)

        final_path = self.download_path / filename

        temp_path = final_path.with_suffix(
            final_path.suffix + ".part"
        )

        logger.info(f"Downloading {url}")

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

            downloaded = 0

            with open(temp_path, "wb") as file:

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

                    percent = 0

                    if total_size > 0:
                        percent = int(
                            downloaded * 100 / total_size
                        )

                    logger.info(
                        f"{percent}% "
                        f"{self.format_size(downloaded)} / "
                        f"{self.format_size(total_size)} "
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
            f"Completed: {filename}"
        )

        if self.display:
            self.display.show_message(
                "Completed",
                filename[:16],
            )

        return final_path
