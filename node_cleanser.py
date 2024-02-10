import os
import shutil
import logging


dirname = input("Enter the directory path: ")
totalsize = 0


class CustomLogFormatter(logging.Formatter):
    def format(self, record):
        result = super().format(record)
        return result + "\n" if result.strip() else result


logging.basicConfig(
    filename="cleanup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_directory_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


def convert_unit_sizes(bytes_size):
    units = ["B ", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0
    while bytes_size >= 1024 and unit_index < len(units) - 1:
        bytes_size /= 1024
        unit_index += 1
    return f"{bytes_size:8.2f} {units[unit_index]}"


# search for top level node_module dirs and remove them
for root, dirs, files in os.walk(dirname):
    for dir in dirs:
        if "node_modules" in dir and "node_modules" not in root:
            path = os.path.join(root, "node_modules")
            dirsize = get_directory_size(path)
            totalsize += dirsize

            logging.info(
                f"{convert_unit_sizes(dirsize)}  |  Deleted node_modules directory: {path}"
            )
            print(f"{convert_unit_sizes(dirsize)}  |  node_modules directory: {path}")
            shutil.rmtree(path)


logging.info(f"{convert_unit_sizes(totalsize)} of total memory saved")
# creates log session separator
logger = logging.getLogger()
formatter = CustomLogFormatter()
for handler in logger.handlers:
    handler.setFormatter(formatter)
logging.info(f"───────────────────────────────────────────────────────────────")
