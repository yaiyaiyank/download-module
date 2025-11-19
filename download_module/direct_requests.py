# 標準ライブラリ
from pathlib import Path
from dataclasses import dataclass
import subprocess

# 外部ライブラリ
import requests
import time_module
from tqdm import tqdm

# 自作ライブラリ
from download_module.exceptions import AlreadyDownloadException
from download_module.const import VIDEO_EXTENSION_LIST


def direct_requests(
    url: str,
    save_path: Path | str | None = None,
    expected_size: int | None = None,
    chunk_size: int = 1024 * 1024,
    wait_time: int | float = 15,
    use_video_ffmpeg: bool = False,
    is_404_ok: bool = False,
) -> bytes | None:
    # save_pathがNoneのときはバイナリを返す
    if not save_path is None:
        save_path = Path(save_path)
    if not save_path is None and save_path.exists() and save_path.stat().st_size == expected_size:
        raise AlreadyDownloadException("すでにダウンロード済みです。")

    try:
        res = requests.get(url, stream=True, timeout=wait_time)
        res.raise_for_status()
    except requests.HTTPError:
        if res.status_code == 404 and not is_404_ok:
            raise
        # TODO 522, 520の場合もis_500_okみたいなのやるかも

    if save_path is None:
        return res.content

    # 以下ちゃっぴー

    # 進捗バー用
    total = int(res.headers.get("Content-Length", 0) or (expected_size or 0))
    bar = tqdm(total=total, unit="B", unit_scale=True, unit_divisor=1024, desc=save_path.name, ascii=True, leave=False)

    if use_video_ffmpeg and save_path.suffix in VIDEO_EXTENSION_LIST:
        command = [
            "ffmpeg",
            "-protocol_whitelist",
            "file,http,https,tcp,tls,crypto",
            "-i",
            url,
            "-c",
            "copy",
            "-bsf:a",
            "aac_adtstoasc",
            save_path.__str__(),
        ]

        subprocess.run(command, check=True)
    else:
        with save_path.open("wb") as fh:
            for chunk in tqdm(res.iter_content(chunk_size)):
                if chunk:
                    if not chunk:
                        continue
                    fh.write(chunk)
                    bar.update(len(chunk))

    bar.close()
