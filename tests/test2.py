import sys
from pathlib import Path

sys.path.append(Path.cwd().__str__())

import download_module

url = "https://pbs.twimg.com/media/G4zpJO8aMAAIkwQ?format=jpg"
save_path = download_module.WINDOWS_DOWNLOAD_FOLDER / "イラスト.jpg"

download_module.direct_requests(url, save_path)
