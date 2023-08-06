import json
from abc import ABCMeta


class ElasticSearchDocument:
    """
    Base class for ElasticSearch document
    each different resource ESDoc will be a subclass
    """

    __metaclass__ = ABCMeta

    def to_json(self) -> str:
        """
        convert to json
        :return:
        """
        obj_dict = {k: v for k, v in sorted(self.__dict__.items())}
        data = json.dumps(obj_dict) + "\n"
        return data
