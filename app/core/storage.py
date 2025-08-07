class Storage:
    """Interface for storage of files."""

    def read(self, file_name: str) -> bytes:
        raise NotImplementedError

    def write(self, file_name: str, data: bytes, container: str | None = None) -> None:
        raise NotImplementedError

    def create_folder(self, folder_name: str) -> None:
        """
        Creates a new folder in the storage
        """

        raise NotImplementedError

    def store_image(self, file_name: str, data: bytes) -> str:
        """
        Stores the image and returns the URL for the image
        """

        raise NotImplementedError

    def store_export(self, file_name: str, data: bytes) -> str:
        """
        Stores the export and returns the URL for the file
        """

        raise NotImplementedError

    def delete(self, file_name: str) -> None:
        raise NotImplementedError

    def list_all_files(self, path: str) -> list[str]:
        """
        Lists all files in the given path
        """

        raise NotImplementedError
