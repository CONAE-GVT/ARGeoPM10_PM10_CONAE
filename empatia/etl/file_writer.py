import os
import attr
from empatia.etl.base_writer import BaseWriter
from empatia.exceptions import DirDoesntExists, FileExists


@attr.s
class FileWriter(BaseWriter):
    """
        Write implementation to store files locally.
    """

    file_format = attr.ib(default="csv", type="str", kw_only=True)
    force = attr.ib(type=bool, default=False, kw_only=True)

    def validate_directory_path(self) -> None:
        """
            Method to ensure a dir exists.
            If it doesn't exists and force is setted, it creates the directory,
            else raise DirDoesntExists.
        """
        dirname = os.path.abspath(os.path.dirname(self.destination))
        if not os.path.exists(dirname):
            if self.force is True:
                os.makedirs(dirname)
            else:
                raise DirDoesntExists()

    def validate_destination(self) -> None:
        if os.path.exists(self.destination):
            raise FileExists(f"{self.destination} already exists.")

    def write(self, data) -> None:
        with open(self.destination, "wb") as f:
            f.write(data)
