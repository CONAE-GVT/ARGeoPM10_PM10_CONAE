from abc import ABC, abstractmethod
from typing import Any

import attr
from empatia.settings.log import logger, timed


@attr.s
class BaseWriter(ABC):
    """
        Base class to implement write to a file.
        Child clases must implement the write method. If data is splitted,
        the write method will be called for each split.
    """

    path = attr.ib(type=str, kw_only=True)
    file_format = attr.ib(type=str, kw_only=True)
    suffix = attr.ib(type=str, default=None, kw_only=True)

    @timed
    def __call__(self, data: Any) -> None:
        """
            Calls write with data or every split.
            In the case of splits, the split_name is passed as
            a suffix.
        """
        self.validate_directory_path()
        self.validate_destination()
        self.write(data)

    @abstractmethod
    def write(self, data: Any) -> None:
        raise NotImplementedError()

    @path.validator
    def _validate_destination(self, *args: Any, **kwargs: Any) -> None:
        self.validate_destination()

    @abstractmethod
    def validate_directory_path(self) -> None:
        pass

    @abstractmethod
    def validate_destination(self) -> None:
        pass

    @property
    def destination(self) -> str:
        """
            Returns the path to the output file. Applies the file format
            and suffix if present
        """
        if self.suffix:
            return f"{self.path}_{self.suffix}.{self.file_format}"

        return f"{self.path}.{self.file_format}"
