from collections import OrderedDict
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
    TYPE_CHECKING,
    Tuple,
    Type,
    Union,
)

import sqlalchemy
from sqlalchemy import text

from ormar.fields import ManyToManyField  # noqa I100
from ormar.relations import AliasManager

if TYPE_CHECKING:  # pragma no cover
    from ormar import Model


class JoinParameters(NamedTuple):
    """
    Named tuple that holds set of parameters passed during join construction.
    """

    prev_model: Type["Model"]
    previous_alias: str
    from_table: str
    model_cls: Type["Model"]


class SqlJoin:
    def __init__(  # noqa:  CFQ002
        self,
        used_aliases: List,
        select_from: sqlalchemy.sql.select,
        columns: List[sqlalchemy.Column],
        fields: Optional[Union[Set, Dict]],
        exclude_fields: Optional[Union[Set, Dict]],
        order_columns: Optional[List],
        sorted_orders: OrderedDict,
    ) -> None:
        self.used_aliases = used_aliases
        self.select_from = select_from
        self.columns = columns
        self.fields = fields
        self.exclude_fields = exclude_fields
        self.order_columns = order_columns
        self.sorted_orders = sorted_orders

    @staticmethod
    def alias_manager(model_cls: Type["Model"]) -> AliasManager:
        """
        Shortcut for ormars model AliasManager stored on Meta.

        :param model_cls: ormar Model class
        :type model_cls: Type[Model]
        :return: alias manager from model's Meta
        :rtype: AliasManager
        """
        return model_cls.Meta.alias_manager

    @staticmethod
    def on_clause(
        previous_alias: str, alias: str, from_clause: str, to_clause: str,
    ) -> text:
        """
        Receives aliases and names of both ends of the join and combines them
        into one text clause used in joins.

        :param previous_alias: alias of previous table
        :type previous_alias: str
        :param alias: alias of current table
        :type alias: str
        :param from_clause: from table name
        :type from_clause: str
        :param to_clause: to table name
        :type to_clause: str
        :return: clause combining all strings
        :rtype: sqlalchemy.text
        """
        left_part = f"{alias}_{to_clause}"
        right_part = f"{previous_alias + '_' if previous_alias else ''}{from_clause}"
        return text(f"{left_part}={right_part}")

    @staticmethod
    def update_inclusions(
        model_cls: Type["Model"],
        fields: Optional[Union[Set, Dict]],
        exclude_fields: Optional[Union[Set, Dict]],
        nested_name: str,
    ) -> Tuple[Optional[Union[Dict, Set]], Optional[Union[Dict, Set]]]:
        """
        Extract nested fields and exclude_fields if applicable.

        :param model_cls: ormar model class
        :type model_cls: Type["Model"]
        :param fields: fields to include
        :type fields: Optional[Union[Set, Dict]]
        :param exclude_fields: fields to exclude
        :type exclude_fields: Optional[Union[Set, Dict]]
        :param nested_name: name of the nested field
        :type nested_name: str
        :return: updated exclude and include fields from nested objects
        :rtype: Tuple[Optional[Union[Dict, Set]], Optional[Union[Dict, Set]]]
        """
        fields = model_cls.get_included(fields, nested_name)
        exclude_fields = model_cls.get_excluded(exclude_fields, nested_name)
        return fields, exclude_fields

    def build_join(  # noqa:  CCR001
        self, item: str, join_parameters: JoinParameters
    ) -> Tuple[List, sqlalchemy.sql.select, List, OrderedDict]:
        """
        Main external access point for building a join.
        Splits the join definition, updates fields and exclude_fields if needed,
        handles switching to through models for m2m relations, returns updated lists of
        used_aliases and sort_orders.

        :param item: string with join definition
        :type item: str
        :param join_parameters: parameters from previous/ current join
        :type join_parameters: JoinParameters
        :return: list of used aliases, select from, list of aliased columns, sort orders
        :rtype: Tuple[List[str], Join, List[TextClause], collections.OrderedDict]
        """
        fields = self.fields
        exclude_fields = self.exclude_fields

        for index, part in enumerate(item.split("__")):
            if issubclass(
                join_parameters.model_cls.Meta.model_fields[part], ManyToManyField
            ):
                _fields = join_parameters.model_cls.Meta.model_fields
                new_part = _fields[part].to.get_name()
                self._switch_many_to_many_order_columns(part, new_part)
                if index > 0:  # nested joins
                    fields, exclude_fields = SqlJoin.update_inclusions(
                        model_cls=join_parameters.model_cls,
                        fields=fields,
                        exclude_fields=exclude_fields,
                        nested_name=part,
                    )

                join_parameters = self._build_join_parameters(
                    part=part,
                    join_params=join_parameters,
                    is_multi=True,
                    fields=fields,
                    exclude_fields=exclude_fields,
                )
                part = new_part

            if index > 0:  # nested joins
                fields, exclude_fields = SqlJoin.update_inclusions(
                    model_cls=join_parameters.model_cls,
                    fields=fields,
                    exclude_fields=exclude_fields,
                    nested_name=part,
                )
            join_parameters = self._build_join_parameters(
                part=part,
                join_params=join_parameters,
                fields=fields,
                exclude_fields=exclude_fields,
            )

        return (
            self.used_aliases,
            self.select_from,
            self.columns,
            self.sorted_orders,
        )

    def _build_join_parameters(
        self,
        part: str,
        join_params: JoinParameters,
        fields: Optional[Union[Set, Dict]],
        exclude_fields: Optional[Union[Set, Dict]],
        is_multi: bool = False,
    ) -> JoinParameters:
        """
        Updates used_aliases to not join multiple times to the same table.
        Updates join parameters with new values.

        :param part: part of the join str definition
        :type part: str
        :param join_params: parameters from previous/ current join
        :type join_params: JoinParameters
        :param fields: fields to include
        :type fields: Optional[Union[Set, Dict]]
        :param exclude_fields: fields to exclude
        :type exclude_fields: Optional[Union[Set, Dict]]
        :param is_multi: flag if the relation is m2m
        :type is_multi: bool
        :return: updated join parameters
        :rtype: ormar.queryset.join.JoinParameters
        """
        if is_multi:
            model_cls = join_params.model_cls.Meta.model_fields[part].through
        else:
            model_cls = join_params.model_cls.Meta.model_fields[part].to
        to_table = model_cls.Meta.table.name

        alias = model_cls.Meta.alias_manager.resolve_relation_alias(
            join_params.prev_model, part
        )
        if alias not in self.used_aliases:
            self._process_join(
                join_params=join_params,
                is_multi=is_multi,
                model_cls=model_cls,
                part=part,
                alias=alias,
                fields=fields,
                exclude_fields=exclude_fields,
            )

        previous_alias = alias
        from_table = to_table
        prev_model = model_cls
        return JoinParameters(prev_model, previous_alias, from_table, model_cls)

    def _process_join(  # noqa: CFQ002
        self,
        join_params: JoinParameters,
        is_multi: bool,
        model_cls: Type["Model"],
        part: str,
        alias: str,
        fields: Optional[Union[Set, Dict]],
        exclude_fields: Optional[Union[Set, Dict]],
    ) -> None:
        """
        Resolves to and from column names and table names.

        Produces on_clause.

        Performs actual join updating select_from parameter.

        Adds aliases of required column to list of columns to include in query.

        Updates the used aliases list directly.

        Process order_by causes for non m2m relations.

        :param join_params: parameters from previous/ current join
        :type join_params: JoinParameters
        :param is_multi: flag if it's m2m relation
        :type is_multi: bool
        :param model_cls:
        :type model_cls: ormar.models.metaclass.ModelMetaclass
        :param part: name of the field used in join
        :type part: str
        :param alias: alias of the current join
        :type alias: str
        :param fields: fields to include
        :type fields: Optional[Union[Set, Dict]]
        :param exclude_fields: fields to exclude
        :type exclude_fields: Optional[Union[Set, Dict]]
        """
        to_table = model_cls.Meta.table.name
        to_key, from_key = self.get_to_and_from_keys(
            join_params, is_multi, model_cls, part
        )

        on_clause = self.on_clause(
            previous_alias=join_params.previous_alias,
            alias=alias,
            from_clause=f"{join_params.from_table}.{from_key}",
            to_clause=f"{to_table}.{to_key}",
        )
        target_table = self.alias_manager(model_cls).prefixed_table_name(
            alias, to_table
        )
        self.select_from = sqlalchemy.sql.outerjoin(
            self.select_from, target_table, on_clause
        )

        pkname_alias = model_cls.get_column_alias(model_cls.Meta.pkname)
        if not is_multi:
            self.get_order_bys(
                alias=alias,
                to_table=to_table,
                pkname_alias=pkname_alias,
                part=part,
                model_cls=model_cls,
            )

        self_related_fields = model_cls.own_table_columns(
            model=model_cls,
            fields=fields,
            exclude_fields=exclude_fields,
            use_alias=True,
        )
        self.columns.extend(
            self.alias_manager(model_cls).prefixed_columns(
                alias, model_cls.Meta.table, self_related_fields
            )
        )
        self.used_aliases.append(alias)

    def _switch_many_to_many_order_columns(self, part: str, new_part: str) -> None:
        """
        Substitutes the name of the relation with actual model name in m2m order bys.

        :param part: name of the field with relation
        :type part: str
        :param new_part: name of the target model
        :type new_part: str
        """
        if self.order_columns:
            split_order_columns = [
                x.split("__") for x in self.order_columns if "__" in x
            ]
            for condition in split_order_columns:
                if condition[-2] == part or condition[-2][1:] == part:
                    condition[-2] = condition[-2].replace(part, new_part)
            self.order_columns = [x for x in self.order_columns if "__" not in x] + [
                "__".join(x) for x in split_order_columns
            ]

    @staticmethod
    def _check_if_condition_apply(condition: List, part: str) -> bool:
        """
        Checks filter conditions to find if they apply to current join.

        :param condition: list of parts of condition split by '__'
        :type condition: List[str]
        :param part: name of the current relation join.
        :type part: str
        :return: result of the check
        :rtype: bool
        """
        return len(condition) >= 2 and (
            condition[-2] == part or condition[-2][1:] == part
        )

    def set_aliased_order_by(
        self, condition: List[str], alias: str, to_table: str, model_cls: Type["Model"],
    ) -> None:
        """
        Substitute hyphens ('-') with descending order.
        Construct actual sqlalchemy text clause using aliased table and column name.

        :param condition: list of parts of a current condition split by '__'
        :type condition: List[str]
        :param alias: alias of the table in current join
        :type alias: str
        :param to_table: target table
        :type to_table: sqlalchemy.sql.elements.quoted_name
        :param model_cls: ormar model class
        :type model_cls: ormar.models.metaclass.ModelMetaclass
        """
        direction = f"{'desc' if condition[0][0] == '-' else ''}"
        column_alias = model_cls.get_column_alias(condition[-1])
        order = text(f"{alias}_{to_table}.{column_alias} {direction}")
        self.sorted_orders["__".join(condition)] = order

    def get_order_bys(  # noqa: CCR001
        self,
        alias: str,
        to_table: str,
        pkname_alias: str,
        part: str,
        model_cls: Type["Model"],
    ) -> None:
        """
        Triggers construction of order bys if they are given.
        Otherwise by default each table is sorted by a primary key column asc.

        :param alias: alias of current table in join
        :type alias: str
        :param to_table: target table
        :type to_table: sqlalchemy.sql.elements.quoted_name
        :param pkname_alias: alias of the primary key column
        :type pkname_alias: str
        :param part: name of the current relation join
        :type part: str
        :param model_cls: ormar model class
        :type model_cls: Type[Model]
        """
        if self.order_columns:
            current_table_sorted = False
            split_order_columns = [
                x.split("__") for x in self.order_columns if "__" in x
            ]
            for condition in split_order_columns:
                if self._check_if_condition_apply(condition, part):
                    current_table_sorted = True
                    self.set_aliased_order_by(
                        condition=condition,
                        alias=alias,
                        to_table=to_table,
                        model_cls=model_cls,
                    )
            if not current_table_sorted:
                order = text(f"{alias}_{to_table}.{pkname_alias}")
                self.sorted_orders[f"{alias}.{pkname_alias}"] = order

        else:
            order = text(f"{alias}_{to_table}.{pkname_alias}")
            self.sorted_orders[f"{alias}.{pkname_alias}"] = order

    @staticmethod
    def get_to_and_from_keys(
        join_params: JoinParameters,
        is_multi: bool,
        model_cls: Type["Model"],
        part: str,
    ) -> Tuple[str, str]:
        """
        Based on the relation type, name of the relation and previous models and parts
        stored in JoinParameters it resolves the current to and from keys, which are
        different for ManyToMany relation, ForeignKey and reverse part of relations.

        :param join_params: parameters from previous/ current join
        :type join_params: JoinParameters
        :param is_multi: flag if the relation is of m2m type
        :type is_multi: bool
        :param model_cls: ormar model class
        :type model_cls: Type[Model]
        :param part: name of the current relation join
        :type part: str
        :return: to key and from key
        :rtype: Tuple[str, str]
        """
        if is_multi:
            to_field = join_params.prev_model.get_name()
            to_key = model_cls.get_column_alias(to_field)
            from_key = join_params.prev_model.get_column_alias(
                join_params.prev_model.Meta.pkname
            )
        elif join_params.prev_model.Meta.model_fields[part].virtual:
            to_field = (
                join_params.prev_model.Meta.model_fields[part].related_name
                or join_params.prev_model.get_name() + "s"
            )
            to_key = model_cls.get_column_alias(to_field)
            from_key = join_params.prev_model.get_column_alias(
                join_params.prev_model.Meta.pkname
            )
        else:
            to_key = model_cls.get_column_alias(model_cls.Meta.pkname)
            from_key = join_params.prev_model.get_column_alias(part)

        return to_key, from_key
