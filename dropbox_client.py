import dropbox
from dropbox.exceptions import ApiError
from config import DROPBOX_ACCESS_TOKEN, DROPBOX_ROOT_FOLDER

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


def build_trim_path(part_number: str, serial_number: str) -> str:
    part = part_number.strip()
    serial = serial_number.strip()
    return f"/{DROPBOX_ROOT_FOLDER}/{part}/{serial}.trm"


def get_trim_file(part_number: str, serial_number: str) -> tuple[str, bytes]:
    path = build_trim_path(part_number, serial_number)
    try:
        metadata, res = dbx.files_download(path)
    except ApiError as e:
        if isinstance(e.error, dropbox.files.DownloadError):
            raise FileNotFoundError(f"File not found at path: {path}") from e
        raise

    data = res.content
    filename = metadata.name
    return filename, data