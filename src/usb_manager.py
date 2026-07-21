from pathlib import Path
import shutil


class USBManager:

    def __init__(self):
        self.mount_points = [
            Path("/media/pi"),
            Path("/media"),
            Path("/mnt"),
        ]

    def find_usb(self):

        for base in self.mount_points:

            if not base.exists():
                continue

            for item in base.iterdir():

                if item.is_dir():
                    return item

        return None

    def copy_to_usb(
        self,
        file_path,
    ):

        usb = self.find_usb()

        if usb is None:
            raise RuntimeError(
                "USB drive not found."
            )

        destination = usb / file_path.name

        shutil.copy2(
            file_path,
            destination,
        )

        return destination
