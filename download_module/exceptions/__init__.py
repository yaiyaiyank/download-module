class DownloadException(Exception):
    """Download系の基底例外"""


class AlreadyDownloadException(Exception):
    """すでにダウンロードしている"""


class NotDiffOnly1Error(Exception):
    """差分が1つではないときのエラー"""
