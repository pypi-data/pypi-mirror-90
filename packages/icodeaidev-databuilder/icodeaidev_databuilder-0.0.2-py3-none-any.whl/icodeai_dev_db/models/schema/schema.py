from typing import (
    Any,
    Iterator,
    Union,
)

from icodeai_dev_db.models.graphs import GraphRelationship, GraphSerializable, GraphNode
from icodeai_dev_db.models.schema import SCHEMA_NAME_ATTR, SCHEMA_NODE_LABEL
from icodeai_dev_db.models.table import DescriptionMetadata


class SchemaModel(GraphSerializable):
    def __init__(
        self,
        schema_key: str,
        schema: str,
        description: str = None,
        description_source: str = None,
        **kwargs: Any,
    ) -> None:
        self._schema_key = schema_key
        self._schema = schema
        self._description = (
            DescriptionMetadata.create_description_metadata(
                text=description, source=description_source
            )
            if description
            else None
        )
        self._node_iterator = self._create_node_iterator()
        self._relation_iterator = self._create_relation_iterator()

    def create_next_node(self) -> Union[GraphNode, None]:
        try:
            return next(self._node_iterator)
        except StopIteration:
            return None

    def _create_node_iterator(self) -> Iterator[GraphNode]:
        node = GraphNode(
            key=self._schema_key,
            label=SCHEMA_NODE_LABEL,
            attributes={
                SCHEMA_NAME_ATTR: self._schema,
            },
        )
        yield node

        if self._description:
            yield self._description.get_node(self._get_description_node_key())

    def create_next_relation(self) -> Union[GraphRelationship, None]:
        try:
            return next(self._relation_iterator)
        except StopIteration:
            return None

    def _get_description_node_key(self) -> str:
        desc = (
            self._description.get_description_id()
            if self._description is not None
            else ""
        )
        return f"{self._schema_key}/{desc}"

    def _create_relation_iterator(self) -> Iterator[GraphRelationship]:
        if self._description:
            yield self._description.get_relation(
                start_node=SCHEMA_NODE_LABEL,
                start_key=self._schema_key,
                end_key=self._get_description_node_key(),
            )
