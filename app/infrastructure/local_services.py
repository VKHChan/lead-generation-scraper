import json
from pathlib import Path

from configuration import Settings
from core.storage import Storage
from core.utils import json_serial
from injector import Binder, Module, inject

from .app_host import AppHost


class LocalModule(Module):
    """
    Local module.
    """

    def __init__(self, app_host: str):
        self.app_host = app_host

    def configure(self, binder: Binder) -> None:
        if self.app_host == AppHost.LOCAL:
            binder.bind(Storage, to=LocalStorage)


class LocalStorage(Storage):
    """
    Local storage implementation.
    """

    @inject
    def __init__(self, settings: Settings):
        self.settings = settings
        self.storage_path = Path(settings.local_settings.local_storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def read(self, file_name: str) -> bytes:
        """
        Reads the file from the local storage.
        """

        file_path = self.storage_path / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_name} not found")

        data = file_path.read_bytes()

        return data

    def read_json(self, file_name: str) -> dict:
        """
        Reads the JSON file from the local storage.
        """

        data = self.read(file_name)
        return json.loads(data)

    def write(self, file_name: str, data: bytes, container: str | None = None) -> None:
        """
        Writes the file to the local storage.
        """

        file_path = self.storage_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            file_path.write_bytes(data)
        else:
            raise ValueError(f"Invalid data type: {type(data)}")

    def write_json(self, file_name: str, data: dict) -> None:
        """
        Writes the JSON file to the local storage.
        """

        file_path = self.storage_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, default=json_serial, indent=4))

    def list_all_files(self, path: str) -> list[str]:
        """
        Lists all files in the given path
        """

        file_path = self.storage_path / path
        if not file_path.exists():
            raise FileNotFoundError(f"Path {path} not found")

        files = []
        for file in file_path.iterdir():
            if file.is_file():
                files.append(str(file.relative_to(self.storage_path)))

        return files

    def create_folder(self, folder_name: str) -> None:
        """
        Creates a new folder in the local storage.
        """

        folder_path = self.storage_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
