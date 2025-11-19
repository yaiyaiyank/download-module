# downloadモジュール

自分のエコシステム用につくったダウンロードモジュール<br>
役立ちそう ∧ 機密情報なし なのでパブリックで公開

# install
### 動作環境
* Python 3.13↑
### インストール方法 
uvなら
```bash
uv add git+https://github.com/yaiyaiyank/download-module
```
pipなら
```bash
pip install git+https://github.com/yaiyaiyank/download-module
```

# usage
フォルダー内のファイルたちの差分を取る形でダウンロードファイルを取得する<br>
※ 「download_module.WINDOWS_DOWNLOAD_FOLDER」はWindows標準のダウンロードフォルダ
```python
import download_module
# 事前に現在のフォルダー内のファイルたちを取得
find_diff_path = download_module.FindDiffPath(download_module.WINDOWS_DOWNLOAD_FOLDER)
# ダウンロードフォルダ内に適当にファイルを作ってみる
(download_module.WINDOWS_DOWNLOAD_FOLDER / "test_texts.txt").write_text("test")
# 差分を取ってそのファイルが出力される。引数は待機時間[s]
file = find_diff_path.fetch(10)
```

```python
import download_module
# フォルダー内のファイルたちの差分を取る形でダウンロードファイルを取得する
# download_module.WINDOWS_DOWNLOAD_FOLDERはWindows標準のダウンロードフォルダ

# 対象URL
url = "https://pbs.twimg.com/media/G4zpJO8aMAAIkwQ?format=jpg"
# 保存先
save_path = download_module.WINDOWS_DOWNLOAD_FOLDER / "イラスト.jpg"
# ダウンロード
download_module.direct_requests(url, save_path)
```