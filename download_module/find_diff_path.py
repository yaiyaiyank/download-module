from pathlib import Path
from dataclasses import dataclass
import time_module

# 自作ライブラリ
from download_module import CACHE_EXTENSION_LIST
from download_module.exceptions import NotDiffOnly1Error


@dataclass
class FindDiffPath:
    """フォルダー内のファイルたちの差分を取る形でダウンロードファイルを取得する"""

    download_dir: Path | str
    cache_ext_list: list[str] | None = None

    def __post_init__(self):
        # ダウンロードフォルダ
        self.download_dir = Path(self.download_dir)
        # キャッシュのファイルの拡張子リスト
        if self.cache_ext_list is None:
            self.cache_ext_list = CACHE_EXTENSION_LIST
        # ダウンロード前のダウンロードフォルダの中身を取得
        self.pre_file_list = self._get_file_list()

    def _get_file_list(self) -> list[Path]:
        """ダウンロード前のダウンロードフォルダの中身を取得"""
        file_list = []
        file_iter = self.download_dir.glob("*")

        for file in file_iter:
            # フォルダーは除外
            if file.is_dir():
                continue
            # キャッシュ系拡張子は除外
            if file.suffix in self.cache_ext_list:
                continue
            file_list.append(file)

        return file_list

    def fetch(self, wait_time: int | float | time_module.MutableWaitTime) -> Path:
        for _ in time_module.WaitTry(wait_time):
            file_list = self._get_file_list()
            # ダウンロードフォルダ内の構造が変わるまで待機
            if not self.pre_file_list != file_list:
                continue
            # パスの差分を取る
            diff_file_list = list(set(file_list) - set(self.pre_file_list))
            if diff_file_list.__len__() != 1:
                raise NotDiffOnly1Error("差分が1つではないです。")
            # 継続して利用できるように現在のパスの情報を保持しておく。
            self.pre_file_list = self._get_file_list()
            # 差分結果ファイルを出力
            return diff_file_list[0]
        else:
            raise TimeoutError("ファイルのダウンロードが検知できませんでした")
