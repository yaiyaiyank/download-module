from pathlib import Path
from dataclasses import dataclass
import time_module

# 自作ライブラリ
from download_module import CACHE_EXTENSION_LIST


@dataclass
class FindDiffPath:
    download_dir: Path | str
    cache_ext_list: list[str] | None = None

    def __post_init__(self):
        # ダウンロードフォルダ
        self.download_dir = Path(self.download_dir)
        # キャッシュのファイルの拡張子リスト
        if self.cache_ext_list is None:
            self.cache_ext_list = CACHE_EXTENSION_LIST
        # ダウンロード前のダウンロードフォルダの中身を取得
        self.pre_file_list = []
        self._set_file_list(self.pre_file_list)

    def _set_file_list(self, file_list: list[Path]):
        """ダウンロード前のダウンロードフォルダの中身を取得"""
        file_iter = self.download_dir.glob("*")

        for file in file_iter:
            # フォルダーは除外
            if file.is_dir():
                continue
            # キャッシュ系拡張子は除外
            if file.suffix in self.cache_ext_list:
                continue
            file_list.append(file)

    def fetch(self, wait_time: int | float | time_module.MutableWaitTime) -> Path:
        file_list = []
        self._set_file_list(file_list)
        for _ in time_module.WaitTry(wait_time):
            # ダウンロードフォルダ内の構造が変わるまで待機
            if not self.pre_file_list != file_list:
                continue
            # パスの差分を取る
            file = list(set(file_list) - set(self.pre_file_list))[0]
            return file
        else:
            raise TimeoutError("ファイルのダウンロードが検知できませんでした")
