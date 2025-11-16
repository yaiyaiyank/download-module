import sys
from pathlib import Path

sys.path.append(Path.cwd().__str__())

import download_module

d = download_module.FindDiffPath(download_module.WINDOWS_DOWNLOAD_FOLDER)
(download_module.WINDOWS_DOWNLOAD_FOLDER / "aaa.txt").write_text("aas")
file = d.fetch(10)
file
