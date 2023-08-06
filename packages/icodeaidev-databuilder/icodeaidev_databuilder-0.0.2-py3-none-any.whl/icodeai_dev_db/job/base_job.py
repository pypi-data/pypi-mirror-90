import abc

from pyhocon import ConfigTree

from icodeai_dev_db import Scoped
from icodeai_dev_db.utils.closer import Closer


class Job(Scoped):
    closer = Closer()

    """
    A Databuilder job that represents single work unit.
    """

    @abc.abstractmethod
    def init(self, conf: ConfigTree) -> None:
        pass

    @abc.abstractmethod
    def launch(self) -> None:
        """
        Launch a job
        :return: None
        """
        pass

    def get_scope(self) -> str:
        return "job"
