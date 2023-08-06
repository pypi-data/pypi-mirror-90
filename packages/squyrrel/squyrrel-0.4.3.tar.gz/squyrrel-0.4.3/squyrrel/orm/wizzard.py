import sqlite3
from typing import Type

from squyrrel.db.connection import SqlDatabaseConnection
from squyrrel.orm.entity_format import EntityFormat
from squyrrel.orm.exceptions import *
from squyrrel.orm.field import (ManyToOne, ManyToMany, OneToMany)
from squyrrel.orm.filter import (ManyToOneFilter, ManyToManyFilter)
from squyrrel.orm.model import Model
from squyrrel.orm.signals import model_loaded_signal
from squyrrel.orm.utils import sanitize_id_array, m2m_aggregation_subquery_alias, field_to_sql_data_type
from squyrrel.sql.query import (Query, UpdateQuery, InsertQuery,
                                DeleteQuery, CreateTableQuery)
from squyrrel.sql.clauses import *
from squyrrel.sql.expressions import (Equals, NumericalLiteral,
                                      StringLiteral, And, Parameter)
from squyrrel.sql.query_builder import QueryBuilder
from squyrrel.sql.references import ColumnReference
from squyrrel.sql.join import OnJoinCondition, JoinConstruct, JoinType


class QueryWizzard:

    def __init__(self, db: SqlDatabaseConnection, builder=None):
        self.db = db
        self.builder = builder
        self.last_sql_query = None
        self.models = {}
        model_loaded_signal.connect(self.on_model_loaded)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def last_insert_rowid(self):
        # todo: this only implements sqlite
        # other like postgres..

        self.execute_sql(sql="SELECT last_insert_rowid()")

        data = self.db.fetchone()
        if not data:
            return None
        return data[0]

    def execute_sql(self, sql, params=None):
        self.db.execute(sql=sql, params=params)
        # try:
        #    self.db.execute(sql=sql, params=params)
        # except self.db.database_error_cls as exc:
        #    # todo: log
        #    # log sql? (but don't give it out in exception! otherwise it would land in request responses
        #    raise SqlException(f'Database during execution of query: : {str(exc)}')

    def execute_query(self, query):
        # todo: log!
        sql = self.builder.build(query)
        # print('\n'+sql)
        # print('params:', query.params)
        self.last_sql_query = query
        self.execute_sql(sql, params=query.params)

    def execute_queries_in_transaction(self, queries):
        # print(f'start transaction, {len(queries)} queries')
        try:
            for query in queries:
                # print('execute query with params', query.params)
                self.execute_query(query)
        except Exception as exc:
            self.rollback()
            raise exc
        else:
            self.commit()
            # print('successfully committed all queries in transaction')

    def on_model_loaded(self, *args, **kwargs):
        new_model_class_meta = kwargs.get('class_meta') or args[0]
        new_model_class = new_model_class_meta.class_reference
        self.register_model(
            model_cls_meta=new_model_class_meta,
            table_name=new_model_class.table_name)

    def register_model(self, model_cls_meta, table_name):
        if table_name is None:
            # print(f'Warning: Model {model_cls_meta.class_name} has table_name=None. Will not be registered.')
            return
        key = model_cls_meta.class_name
        if key in self.models.keys():
            # print(f'There is already a model on key <{key}>')
            return
        self.models[key] = model_cls_meta.class_reference
        # print('register_model:', key)

    def get_model(self, model) -> Type[Model]:
        if isinstance(model, str):
            try:
                return self.models[model]
            except KeyError:
                models = ', '.join(self.models.keys())
                raise ModelNotFoundException(model, models)
        return model

    def get_model_by_table(self, table_name):
        for model_name, model in self.models.items():
            if model.table_name == table_name:
                return model
        return None

    def build_m2m_aggregation_subquery(self, model, relation_name, m2m_relation):
        # todo: refactor using QueryBuilder
        model = self.get_model(model)
        foreign_model = self.get_model(m2m_relation.foreign_model)
        subquery_tablename = m2m_aggregation_subquery_alias(model, relation_name)
        select_fields = [ColumnReference(model.id_field_name(), alias=model.id_field_name()),
                         m2m_relation.aggregation]
        join_condition = OnJoinCondition(
            Equals(ColumnReference(foreign_model.id_field_name(), table=foreign_model.table_name),
                   ColumnReference(foreign_model.id_field_name(), m2m_relation.junction_table))
        )
        from_clause = JoinConstruct(
            table1=FromClause(m2m_relation.junction_table),
            join_type=JoinType.LEFT_OUTER_JOIN,
            table2=foreign_model.table_name,
            join_condition=join_condition
        )
        return Query(
            select_clause=SelectClause(*select_fields),
            from_clause=from_clause,
            groupby_clause=GroupByClause(model.id_field_name()),
            is_subquery=True,
            alias=subquery_tablename
        )

    def handle_many_to_one(self, model, select_fields, relation, from_clause):
        model = self.get_model(model)
        relation.foreign_model = self.get_model(relation.foreign_model)
        foreign_model = self.get_model(relation.foreign_model)
        foreign_select_fields = foreign_model.build_select_fields()

        # todo: make builder method specially for columns on OnJoinCondition
        join_condition = OnJoinCondition(
            Equals(ColumnReference(relation.foreign_key_field, table=model.table_name),
                   ColumnReference(relation.foreign_model_key_field, table=foreign_model.table_name))
        )

        # todo: make into builder method on table_reference
        from_clause.table_reference = JoinConstruct(
            table1=from_clause.table_reference,
            join_type=JoinType.LEFT_OUTER_JOIN,
            table2=foreign_model.table_name,
            join_condition=join_condition
        )

        select_fields.extend(foreign_select_fields)

    def handle_many_to_one_entities(self, model, select_fields, from_clause):
        model = self.get_model(model)
        many_to_one_entities = []
        for relation_name, relation in model.many_to_one_relations():
            if relation.lazy_load:
                continue
            # todo: check if instead intance..
            self.handle_many_to_one(model=model,
                                    select_fields=select_fields,
                                    relation=relation,
                                    from_clause=from_clause)
            many_to_one_entities.append((relation_name, relation))
        return many_to_one_entities

    def handle_many_to_many_aggregations(self, model, from_clause, select_fields):
        model = self.get_model(model)
        many_to_many_aggregations = []
        for relation_name, relation in model.many_to_many_relations():
            self.handle_many_to_many_aggregation(
                model=model,
                relation_name=relation_name,
                relation=relation,
                from_clause=from_clause,
                select_fields=select_fields,
                aggregations=many_to_many_aggregations
            )
        return many_to_many_aggregations

    def handle_many_to_many_aggregation(self, model, relation_name, relation,
                                        from_clause, select_fields,
                                        aggregations):
        model = self.get_model(model)
        relation.foreign_model = self.get_model(relation.foreign_model)
        if relation.aggregation is None:
            return

        aggr_subquery = self.build_m2m_aggregation_subquery(
            model=model,
            relation_name=relation_name,
            m2m_relation=relation
        )
        join_condition = OnJoinCondition(
            Equals(ColumnReference(model.id_field_name(), table=aggr_subquery.alias),
                   ColumnReference(model.id_field_name(), table=model.table_name))
        )
        from_clause.join(
            join_type=JoinType.LEFT_OUTER_JOIN,
            table2=aggr_subquery,
            join_condition=join_condition
        )
        aggr_column_ref = ColumnReference('aggr', table=aggr_subquery.alias)
        select_fields.append(aggr_column_ref)
        aggregations.append((relation_name, aggr_column_ref))

    def handle_one_to_many_aggregation(self, model, relation_name, relation,
                                       from_clause, select_fields,
                                       aggregations):
        model = self.get_model(model)
        relation.foreign_model = self.get_model(relation.foreign_model)
        if relation.aggregation is None:
            return

        subquery_tablename = f'{model.table_name}_{relation_name}'
        aggregation = relation.aggregation
        aggregation.alias = 'aggr'
        aggr_select_fields = [ColumnReference(model.id_field_name(), alias=model.id_field_name()),
                              aggregation]
        subquery = Query(
            select_clause=SelectClause(*aggr_select_fields),
            from_clause=FromClause(relation.foreign_model.table_name),
            groupby_clause=GroupByClause(model.id_field_name()),
            is_subquery=True,
            alias=subquery_tablename
        )
        join_condition = OnJoinCondition(
            Equals(ColumnReference(model.id_field_name(), table=subquery.alias),
                   ColumnReference(model.id_field_name(), table=model.table_name))
        )
        from_clause.table_reference = from_clause.table_reference.join(
            join_type=JoinType.LEFT_OUTER_JOIN,
            table2=subquery,
            join_condition=join_condition
        )
        column_reference = ColumnReference('aggr', table=subquery_tablename)
        select_fields.append(column_reference)
        relation.table_name = subquery_tablename
        aggregations.append((relation_name, relation))

    def build_relation_to_many_query(self, model, instance_id, relation, options) -> Query:
        model = self.get_model(model)
        orderby = None
        page_size = None
        active_page = None

        if options is not None:
            orderby = options.get('orderby', None)
            page_size = options.get('page_size', None)
            active_page = options.get('active_page', None)

        # deprecated:
        # filter_condition = Equals(ColumnReference(model.id_field_name(), table=model.table_name),
        #                           NumericalLiteral(instance_id))
        filter_condition = Equals.id_as_parameter(model, instance_id)
        return QueryBuilder(relation.foreign_model, self) \
            .add_filter_condition(filter_condition) \
            .orderby(orderby) \
            .pagination(active_page, page_size) \
            .build()

    def load_relation_to_many_entities(self, model, instance_id, relations_dict, options):
        if not options.get('load_entities', True):
            return {}

        model = self.get_model(model)
        data = {}
        for relation_name in relations_dict:
            relation = model.get_relation(relation_name)  # getattr(model, relation_name)
            if relation.lazy_load:
                continue
            relation_options = options.get(relation_name, None)
            if relation_options is not None and relation_options.get('skip', False):
                continue
            query = self.build_relation_to_many_query(model, instance_id, relation, relation_options)
            query.model = relation.foreign_model
            data[relation_name] = self.get_all(query, entity_format=options.get('entity_format', EntityFormat.MODEL))
        return data

    # todo: make this method to method of FromClause
    def include_many_to_many_join(self, model, relation, from_clause):
        model = self.get_model(model)
        # !! todo: first check if not already joined!!

        # todo: refactor: compare with QueryBuilder._include_many_to_many_join

        # foreign_model = self.get_model(relation.foreign_model)
        # foreign_select_fields = self.build_select_fields(foreign_model)
        junction_join_condition = OnJoinCondition(
            Equals(ColumnReference(model.id_field_name(), table=model.table_name),
                   ColumnReference(model.id_field_name(), table=relation.junction_table))
        )
        from_clause.table_reference = from_clause.table_reference.join(
            join_type=JoinType.INNER_JOIN,
            table2=relation.junction_table,
            join_condition=junction_join_condition
        )

    def include_many_to_many_aggregations(self, model, from_clause, select_fields):
        model = self.get_model(model)
        m2m_aggregations = []
        for relation_name, relation in model.many_to_many_relations():
            self.handle_many_to_many_aggregation(
                model=model,
                relation_name=relation_name,
                relation=relation,
                from_clause=from_clause,
                select_fields=select_fields,
                aggregations=m2m_aggregations
            )
        return m2m_aggregations

    def include_one_to_many_aggregations(self, model, from_clause, select_fields):
        model = self.get_model(model)
        one_to_many_aggregations = []
        for relation_name, relation in model.one_to_many_relations():
            self.handle_one_to_many_aggregation(
                model=model,
                relation_name=relation_name,
                relation=relation,
                from_clause=from_clause,
                select_fields=select_fields,
                aggregations=one_to_many_aggregations
            )
        return one_to_many_aggregations

    def get_by_id(self,
                  model,
                  id,
                  select_fields=None,
                  exclude_fields=None,
                  m2m_options=None,
                  one_to_many_options=None,
                  raise_if_not_found=True,
                  load_relations_entities=True,
                  load_relations_aggregations=False,
                  entity_format=EntityFormat.MODEL):

        model = self.get_model(model)
        filter_condition = Equals.id_as_parameter(model, id)
        instance = self.get(model=model,
                            select_fields=select_fields,
                            exclude_fields=exclude_fields,
                            filter_condition=filter_condition,
                            m2m_options=m2m_options,
                            one_to_many_options=one_to_many_options,
                            load_relations_entities=load_relations_entities,
                            load_relations_aggregations=load_relations_aggregations,
                            entity_format=entity_format)
        if instance is None and raise_if_not_found:
            raise DidNotFindObjectWithIdException(
                msg=f'Did not find {model.__name__} with id {id}',
                model_name=model.__name__,
                id=id)
        return instance

    def get(self,
            model: Type[Model] or str,
            select_fields=None,
            exclude_fields=None,
            filter_condition=None,
            m2m_options=None,
            one_to_many_options=None,
            load_relations_entities=True,
            load_relations_aggregations=False,
            entity_format=EntityFormat.MODEL):

        query = QueryBuilder(model, self) \
            .select(select_fields, exclude_fields) \
            .add_filter_condition(filter_condition) \
            .build()

        select_fields = query.select_clause.items

        # todo: move blow to next if not disable_relations...
        if load_relations_aggregations:
            one_to_many_aggregations = self.include_one_to_many_aggregations(model=query.model,
                                                                             from_clause=query.from_clause,
                                                                             select_fields=select_fields)
            m2m_aggregations = self.include_many_to_many_aggregations(model=query.model,
                                                                      from_clause=query.from_clause,
                                                                      select_fields=select_fields)
        else:
            one_to_many_aggregations = []
            m2m_aggregations = []

        many_to_one_entities = self.handle_many_to_one_entities(model=query.model,
                                                                select_fields=select_fields,
                                                                from_clause=query.from_clause)

        print(query)

        self.execute_query(query)
        data = self.db.fetchone()

        if data is None:
            return None

        data = self.model_instance_dict(query.model, data, entity_format, select_fields,
                                        many_to_one_entities, one_to_many_aggregations,
                                        m2m_aggregations)
        entity_id = data.get(query.model.id_field_name())

        print('keys')
        print(data.keys())

        if load_relations_entities:
            data.update(
                **self.load_relation_to_many_entities(query.model,
                                                      instance_id=entity_id,
                                                      relations_dict=query.model.many_to_many_dict(),
                                                      options={**(m2m_options or {}),
                                                               'entity_format': entity_format})
            )
            data.update(
                **self.load_relation_to_many_entities(query.model,
                                                      instance_id=entity_id,
                                                      relations_dict=query.model.one_to_many_dict(),
                                                      options={**(one_to_many_options or {}),
                                                               'entity_format': entity_format})
            )

        # todo: refactor in method/class entitybuilder
        if entity_format == EntityFormat.MODEL:
            entity = self.build_entity(
                query.model,
                data,
                m2m_aggregations=m2m_aggregations
            )
            # self.handle_one_to_many(entity, one_to_many_options=one_to_many_options)
            return entity
        elif entity_format == EntityFormat.JSON:
            return data

    # todo: remove or refactor this method
    def load_filter_values(self, filters):
        if filters is None:
            return
        for filter_ in filters:
            if isinstance(filter_, (ManyToOneFilter, ManyToManyFilter)):
                filter_.entities = list()
                if filter_.value:
                    for id_value in filter_.value:
                        filter_.entities.append(
                            self.get_by_id(model=filter_.relation.foreign_model,
                                           id=id_value, load_relations_entities=False, load_relations_aggregations=True)
                        )

    def get_all(self, query: Query, include_count=False,
                entity_format=EntityFormat.MODEL):
        # todo: put include_count and entity_format into options
        # todo: somehow manage query.model better: possibly as extra parameter of this method instead of attribute of query

        from_clause = query.from_clause
        select_fields = query.select_clause.items

        # war vorher vor filter_condition is not None..
        many_to_one_entities = self.handle_many_to_one_entities(
            model=query.model, select_fields=select_fields, from_clause=from_clause)
        one_to_many_aggregations = self.include_one_to_many_aggregations(
            model=query.model, from_clause=from_clause, select_fields=select_fields)
        m2m_aggregations = self.include_many_to_many_aggregations(
            model=query.model, from_clause=from_clause, select_fields=select_fields)

        self.db.create_cursor()
        try:
            self.execute_query(query)
        except (sqlite3.OperationalError, sqlite3.Error, sqlite3.Warning) as e:
            print(query)
            raise e

        res = self.db.fetchall()
        return self.build_get_all_response(res=res, include_count=include_count, query=query,
                                           entity_format=entity_format,
                                           model=query.model, select_fields=select_fields,
                                           many_to_one_entities=many_to_one_entities,
                                           one_to_many_aggregations=one_to_many_aggregations,
                                           m2m_aggregations=m2m_aggregations)

    def build_get_all_response(self, res, include_count, query, entity_format, model,
                               select_fields, many_to_one_entities, one_to_many_aggregations, m2m_aggregations):
        if not res:
            if include_count:
                return {
                    'entities': [],
                    'count': 0
                }
            return []
        entities = []
        if entity_format == EntityFormat.MODEL:
            for r in res:
                data = self.model_instance_dict(
                    model,
                    r,
                    entity_format,
                    select_fields,
                    many_to_one_entities,
                    one_to_many_aggregations,
                    m2m_aggregations)
                entities.append(
                    self.build_entity(
                        model,
                        data,
                        m2m_aggregations=m2m_aggregations)
                )
        elif entity_format == EntityFormat.JSON:
            for data in res:
                entities.append(
                    self.model_instance_dict(model, data, entity_format, select_fields,
                                             many_to_one_entities, one_to_many_aggregations,
                                             m2m_aggregations)
                )
        if include_count:
            count = self.count(model, query=query)
            return {'entities': entities, 'count': count}
        return entities

    def model_instance_dict(self, model, data, entity_format, select_fields,
                            many_to_one_relations, one_to_many_aggregations,
                            m2m_aggregations):
        model = self.get_model(model)
        kwargs = {}
        for i, column_reference in enumerate(select_fields):
            if column_reference.table == model.table_name:
                kwargs[column_reference.name] = data[i]

        # todo: refactor for loops by putting col_ref onto select_fields
        for relation_name, relation in many_to_one_relations:
            foreign_kwargs = {}
            results = self.get_data(data, select_fields, relation.foreign_model.table_name)
            for result in results:
                # todo: type result into namedtuple
                field_index = result[0]
                foreign_kwargs[select_fields[field_index].name] = result[1]
            if entity_format == EntityFormat.MODEL:
                kwargs[relation_name] = relation.foreign_model(**foreign_kwargs)
            elif entity_format == EntityFormat.JSON:
                # print(foreign_kwargs)
                kwargs[relation_name] = dict(foreign_kwargs)
        # print(kwargs)

        for relation_name, relation in one_to_many_aggregations:
            # TODO: überarbeiten-> gleich wie m2m oder umgekehrt
            results = self.get_data(data, select_fields, relation.table_name)
            if results:
                first_result = results[0]
                kwargs[relation_name] = first_result[1]

        for relation_name, relation in m2m_aggregations:
            results = self.get_data(data, select_fields, relation)
            if results:
                first_result = results[0]
                kwargs[relation_name] = first_result[1]

        return kwargs

    def build_entity(self, model, data, m2m_aggregations=None):
        model = self.get_model(model)
        return model(m2m_aggregations=m2m_aggregations, **data)

    # todo: make static or utility
    def get_data(self, data, select_fields, reference):
        results = []
        # print('get_Data, reference:', reference)
        # print(data)
        # todo: type result into namedtuple: index and value
        if isinstance(reference, ColumnReference):
            for i, column_ref in enumerate(select_fields):
                if column_ref == reference:
                    results.append((i, data[i]))
        else:
            for i, column_ref in enumerate(select_fields):
                if column_ref.table == reference:
                    results.append((i, data[i]))
        return results

    def get_m2m_related_ids(self, model, instance_id, relation_name):
        m2m_relation = model.get_many_to_many_relation(relation_name)
        foreign_model = self.get_model(m2m_relation.foreign_model)
        select_clause = SelectClause(ColumnReference(foreign_model.id_field_name(), table=m2m_relation.junction_table))
        where_clause = Equals.column_as_parameter(ColumnReference(model.id_field_name(),
                                                                  table=m2m_relation.junction_table), instance_id)
        query = Query(select_clause=select_clause,
                      from_clause=FromClause(m2m_relation.junction_table),
                      where_clause=WhereClause(where_clause))
        self.execute_query(query)
        return self.db.fetchall()

    def get_one_to_many_related_ids(self, model, instance_id, relation_name):
        one_to_many_relation = model.get_one_to_many_relation(relation_name)
        foreign_model = self.get_model(one_to_many_relation.foreign_model)
        filter_condition = Equals.column_as_parameter(
            ColumnReference(model.id_field_name(), table=foreign_model.table_name),
            instance_id)
        query = QueryBuilder(foreign_model, self) \
            .select([foreign_model.id_field_name()]) \
            .add_filter_condition(filter_condition) \
            .build()
        self.execute_query(query)
        res = self.db.fetchall()
        return [val for sublist in res for val in sublist]

    def count_m2m(self, entity, relation_name):
        model = entity.model
        relation = getattr(entity, relation_name)

        filter_condition = Equals.id_as_parameter(model, entity.id)
        query = QueryBuilder(model, self) \
            .select([f'count (*)']) \
            .add_filter_condition(filter_condition) \
            .orderby(None) \
            .build()
        self.include_many_to_many_join(model, relation, query.from_clause)

        self.execute_query(query)
        data = self.db.fetchone()
        return int(data[0])

    def count(self, model, filter_condition=None, filters=None, fulltext_search=None, query=None):
        model = self.get_model(model)

        if query is not None:
            # or count(*)
            select_fields = [f'count ({ColumnReference(model.id_field_name(), table=model.table_name)})']
            query.select_clause = SelectClause(*select_fields)
            query.pagination = None
            # query.select_clause.select_fields = [f'count ({ColumnReference(model.id_field_name(), table=model.table_name)})']
        else:
            query = QueryBuilder(model, self) \
                .select([f'count ({ColumnReference(model.id_field_name(), table=model.table_name)})']) \
                .add_filter_condition(filter_condition) \
                .model_filters(filters) \
                .fulltext_search(fulltext_search) \
                .build()
        query.orderby_clause = None

        self.execute_query(query)
        data = self.db.fetchone()
        if data:
            return int(data[0])
        return 0

    def build_simple_search_query(self, model, select_fields, search_column, value):
        model = self.get_model(model)

        literal = value
        if isinstance(value, str):
            literal = StringLiteral(value)
        elif isinstance(value, int):
            literal = NumericalLiteral(value)
        # todo: replace with parameter builder method
        filter_condition = Equals(ColumnReference(search_column, table=model.table_name),
                                  literal)

        return QueryBuilder(model, self) \
            .select(select_fields) \
            .add_filter_condition(filter_condition) \
            .build()

    def prepare_m2m_data(self, model, prepared_data, instance=None):
        model = self.get_model(model)
        for m2m_relation_name, m2m_relation in model.many_to_many_relations():
            prepared_data[m2m_relation_name] = getattr(instance, m2m_relation_name).entities

    def prepare_m21_data(self, model, data, prepared_data):
        model = self.get_model(model)
        for column, value in data.items():
            try:
                relation_name, relation = model.get_relation_by_fk_id_column(column)
            except RelationNotFoundException as exc:
                # todo: log
                # print(str(exc))
                print('did not find relation ', column)
                pass
            else:
                if isinstance(relation, ManyToOne):
                    # print('handle m21:', relation_name)
                    # if columns not equal
                    # refactor: retrieve value by id
                    relation_foreign_model = self.get_model(relation.foreign_model)
                    if relation.load_all:
                        # print('load_all')
                        query = QueryBuilder(relation_foreign_model, self).build()
                        prepared_data[relation_name + '_all'] = self.get_all(query)
                        # print(prepared_data[relation_name + '_all'])

                    prepared_value = self.retrieve_value_by_value(
                        model=relation_foreign_model,
                        lookup_column=relation.update_search_column,
                        filter_column=relation_foreign_model.id_field_name(),
                        filter_value=value
                    )
                    prepared_data[relation_name] = prepared_value
                else:
                    # todo: log
                    raise Exception(f'Error during data preparation: Could not handle {relation}')

    def retrieve_value_by_value(self, model, lookup_column, filter_column, filter_value):
        # todo generalize to search function
        if filter_value is None:
            return None
        model = self.get_model(model)
        query = self.build_simple_search_query(model,
                                               select_fields=[lookup_column],
                                               search_column=filter_column,
                                               value=filter_value
                                               )
        self.execute_query(query)

        data = self.db.fetchone()
        if data is None:
            return None
        # todo: handle case if more than one row is returned
        return data[0]

    def retrieve_id_by_value(self, model, filter_column, filter_value):
        model = self.get_model(model)
        id_ = self.retrieve_value_by_value(
            model=model,
            lookup_column=model.id_field_name(),
            filter_column=filter_column,
            filter_value=filter_value
        )
        if id_ is None:
            raise DidNotFindForeignIdException(
                f'Did not find {model.__name__} with {filter_column} = {filter_value}',
                field=filter_column)
        return id_

    def fulltext_search(self, model, search_value, pagesize, active_page, include_count=True, json=False):
        query = QueryBuilder(model, self) \
            .fulltext_search(search_value) \
            .pagination(active_page, page_size=pagesize) \
            .build()

        data = {'list': self.get_all(query)}

        if include_count:
            data['count'] = self.count(model=model, query=query)
        if json:
            data['list'] = [el.as_json() for el in data['list']]
        return data

    def build_m2m_update_queries(self, model, instance_id, relation, current_ids, new_ids):
        model = self.get_model(model)
        foreign_model = self.get_model(relation.foreign_model)
        current_ids = set(sanitize_id_array(foreign_model, current_ids))
        new_ids = set(sanitize_id_array(foreign_model, new_ids))
        ids_to_add = new_ids - current_ids
        ids_to_remove = current_ids - new_ids
        queries = []
        id_field_name = model.id_field_name()
        foreign_id_field_name = foreign_model.id_field_name()
        table = relation.junction_table

        for id_to_add in ids_to_add:
            queries.append(
                InsertQuery.build(table, inserts={
                    id_field_name: instance_id,
                    foreign_id_field_name: id_to_add
                })
            )
        for ids_to_remove in ids_to_remove:
            condition = And.concat([
                Equals(ColumnReference(id_field_name, table), Parameter(instance_id)),
                Equals(ColumnReference(foreign_id_field_name, table), Parameter(ids_to_remove))
            ])
            queries.append(DeleteQuery(table, condition))

        # todo: delete in one query with 'IN' expression
        return queries

    def build_one_to_many_update_queries(self, model, instance_id, relation, related_ids):
        model = self.get_model(model)
        foreign_model = self.get_model(relation.foreign_model)
        queries = []
        updates = {model.id_field_name(): instance_id}
        for related_id in related_ids:
            filter_condition = Equals.id_as_parameter(foreign_model, related_id)
            queries.append(
                UpdateQuery.build(foreign_model,
                                  filter_condition=filter_condition,
                                  updates=updates)
            )
        return queries

    def delete_by_condition(self, model, filter_condition, commit=True):
        model = self.get_model(model)
        delete_query = DeleteQuery(model.table_name, filter_condition)
        self.execute_query(delete_query)
        if commit:
            self.commit()

    def delete_by_id(self, model, instance_id, commit=True):
        model = self.get_model(model)
        self.delete_by_condition(model, Equals.id_as_parameter(model, instance_id), commit=commit)

    def get_related_to_many_insert_and_update_queries(self, model, instance_id, data):
        related_queries = []
        for column, value in data.items():
            field = model.get_field(column)
            if field is None:
                if not value:
                    continue
                relation = model.get_relation(column)
                if isinstance(relation, ManyToMany):
                    related_queries.extend(
                        self.build_m2m_update_queries(
                            model=model,
                            instance_id=instance_id,
                            relation=relation,
                            current_ids=[],
                            new_ids=value
                        )
                    )
                elif isinstance(relation, OneToMany):
                    related_queries.extend(
                        self.build_one_to_many_update_queries(
                            model=model,
                            instance_id=instance_id,
                            relation=relation,
                            related_ids=value
                        )
                    )
        return related_queries

    def get_m21_value(self, relation, value):
        if relation.load_all:
            return int(value)
        else:
            return self.retrieve_id_by_value(
                model=relation.foreign_model,
                filter_column=relation.update_search_column,
                filter_value=value
            )

    def insert_query(self, model, data):
        # todo: refactor: put on merge query builder?
        model = self.get_model(model)
        inserts = dict()
        for column, value in data.items():
            field = model.get_field(column)
            if field is None:
                if not value:
                    continue
                relation = model.get_relation(column)
                if isinstance(relation, ManyToOne):
                    fk_id = self.get_m21_value(relation, value)
                    if fk_id:
                        inserts[relation.foreign_key_field] = fk_id
            else:
                # todo: refactor
                # if isinstance(field, DateTimeField):
                #     #SELECT datetime('now')
                #     if value == 'now':
                #         value = Query(
                #             select_clause=SelectClause.build(*select_fields),
                #             from_clause=from_clause,
                #             groupby_clause=GroupByClause(model.id_field_name()),
                #             is_subquery=True,
                #             alias=subquery_tablename
                #         )
                inserts[column] = value
        return InsertQuery.build(
            table=model.table_name, inserts=inserts)

    def merge(self, model, new_instance_data, old_instance_ids, return_created_object=True):
        model = self.get_model(model)

        # update_one_to_many_queries = []
        # for relation_name, relation in model.one_to_many_relations():
        #    foreign_model = self.get_model(relation.foreign_model)
        #    for old_instance_id in old_instance_ids:
        #        filter_condition = Equals.column_as_parameter(
        #            ColumnReference(model.id_field_name(), table=foreign_model.table_name),
        #            old_instance_id)
        #        updates = {model.id_field_name(): 'placeholder'}
        #        update_one_to_many_queries.append(
        #            UpdateQuery.build(foreign_model,
        #                              filter_condition=filter_condition,
        #                              updates=updates)
        #        )

        delete_queries = [DeleteQuery(model.table_name, Equals.id_as_parameter(model, instance_id)) for instance_id in
                          old_instance_ids]

        inserted_id = None
        try:
            for query in delete_queries:
                self.execute_query(query)
            inserted_id = self.create(model, new_instance_data, return_created_object=False, commit=False)
            # for query in update_one_to_many_queries:
            #    query.set_clause.updates[0].rhs.value = inserted_id
            #    print('update_query:')
            #    print(query)
            #    self.execute_query(query)
        except Exception as exc:
            self.rollback()
            raise exc
        else:
            self.commit()
        if return_created_object and inserted_id is not None:
            return self.get_by_id(model, inserted_id, entity_format=EntityFormat.JSON)
        return inserted_id

    def execute_insert(self, model, data, insert_query):
        self.execute_query(insert_query)
        inserted_id = self.last_insert_rowid()

        related_queries = self.get_related_to_many_insert_and_update_queries(model, inserted_id, data)
        print('related_queries')
        for query in related_queries:
            print(query)
            print(query.params)
        for query in related_queries:
            self.execute_query(query)

        return inserted_id

    def create(self, model, data, return_created_object=True, commit=True):
        model = self.get_model(model)
        insert_query = self.insert_query(model, data)
        try:
            inserted_id = self.execute_insert(model, data, insert_query)
        except Exception as exc:
            self.rollback()
            # todo: reraise special exception class
            raise exc
        else:
            if commit:
                self.commit()
        if return_created_object:
            return self.get_by_id(model, inserted_id, entity_format=EntityFormat.JSON)
        return inserted_id

    def update(self, model, filter_condition, instance_id, prev_data, data, fetch_m21_values=False):
        # todo only update changed data
        # i.e. difference data - instance.data
        # todo: what about commit?
        model = self.get_model(model)
        updates = dict()
        m2m_update_queries = []

        for column, value in data.items():
            # todo value into sql value
            field = model.get_field(column)

            # todo refactor
            if field is not None:
                updates[column] = value
                continue

            relation = model.get_relation(column)

            # todo: refactor
            if isinstance(relation, ManyToOne):
                if fetch_m21_values:
                    fk_id = self.get_m21_value(relation, value)
                else:
                    fk_id = value
                if fk_id:
                    updates[relation.foreign_key_field] = fk_id

            elif isinstance(relation, ManyToMany):
                # compare difference
                # if instance is None, needs to be loaded first..
                m2m_update_queries.extend(
                    self.build_m2m_update_queries(
                        model=model,
                        instance_id=instance_id,
                        relation=relation,
                        current_ids=prev_data.get(column),
                        new_ids=value
                    )
                )
            elif relation is None:
                raise Exception(f'Error during update: Did not find column {column}')
            else:
                raise Exception(f'Error during update: Could not handle relation {repr(relation)}')

        update_query = UpdateQuery.build(
            model, filter_condition=filter_condition, updates=updates)

        self.execute_queries_in_transaction(queries=[update_query] + m2m_update_queries)

    def update_by_id(self, model, instance_id, data, prev_data, commit=True, return_updated_object=True):
        # todo: add extensive doc string for params!!

        model = self.get_model(model)
        filter_condition = Equals.id_as_parameter(model, instance_id)
        # todo: add logging
        self.update(model=model, filter_condition=filter_condition, data=data, prev_data=prev_data,
                    instance_id=instance_id)
        if return_updated_object:
            return self.get_by_id(model, instance_id, entity_format=EntityFormat.JSON)

    # todo: put into CreateQueryBuilder
    def build_create_table_query(self, model, if_not_exists=False):
        model = self.get_model(model)
        columns = {}
        for field_name, field in model.fields(include_never_select_fields=True):
            columns[field_name] = {
                'data_type': field_to_sql_data_type(field),
                'primary_key': field.primary_key,
                'foreign_key': field.foreign_key,
                'not_null': field.not_null,
                'default': field.default,
                'unique': field.unique,
                'collate': field.collate if hasattr(field, 'collate') else None
            }
        query = CreateTableQuery.build(
            table=model.table_name,
            columns=columns,
            if_not_exists=if_not_exists,
            uniqueness_constraints=model.uniqueness_constraints
        )
        return query

    # def build_

    def create_table(self, model, if_not_exists=False):
        model = self.get_model(model)
        query = self.build_create_table_query(model, if_not_exists=if_not_exists)
        self.execute_query(query)
        # todo: commit missing
