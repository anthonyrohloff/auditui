from pathlib import Path
from datetime import datetime, timezone
import math

# Helper function to get file sizes in a readable format
# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def _convert_size(size_bytes):
   if size_bytes == 0:
       return "0 B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

# Return file tree with last modified time and attributes
def list_files(startpath, level=0):
    path = Path(startpath)
    for item in sorted(path.rglob("*")):
        if item.is_file():
            # Convert standard time to human-readable time
            mtime = datetime.fromtimestamp(round(item.stat().st_mtime / 60) * 60, tz=timezone.utc)
            
            # Convert bytes to MB, GB, etc.
            size = _convert_size(item.stat().st_size)

            print("    " * level + item.name, size, str(mtime)[:-9])
        else:
            print("    " * level + item.name + "/")
            level += 1