#!/usr/bin/env python
# -*- coding:utf-8 -*-
import abc
import copy
import datetime

import pandas as pd

from restsql.exception import JsonFormatException, ProgramConfigException, RunningException
from restsql.model import QueryObject, Aggregation, Filter

SHOULD_BE_REMOVED = '__sbr__'


class Engine(metaclass=abc.ABCMeta):
    """
    执行引擎。将query转查询语句、真正查询的过程封装。策略模式，便于后续维护扩展。
    仅仅执行转换，不做任何检查，也就是说，不保证sql注入的安全性，不保证字段存在。
    """

    @abc.abstractmethod
    def parse_object(self, query_object):
        """
        将QueryObject对象转为查询的语句。
        :param query_object: QueryObject对象
        :return: 返回三参数元组，查询语句、查询参数、字段
        """
        pass

    @abc.abstractmethod
    def fetch_result(self, conn, query, params, fields):
        """
        执行具体查询，返回删除无关字段的Dataframe结构
        :param conn:
        :param query:
        :param params:
        :param fields:
        :return:
        """
        pass


class SqlEngine(Engine):

    def __init__(self, quote='"'):
        """
        初始化一个sql engine实例。传入参数为System identifier，也就是为了兼容mysql'`'
        :param quote: system identifier
        """
        self.quote = quote

    def fetch_result(self, conn, sql, params, fields):
        cur = conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchall()
        cur.close()
        df = pd.DataFrame.from_records(result, columns=fields)
        df.drop([SHOULD_BE_REMOVED], axis=1, inplace=True, errors='ignore')
        return df

    def _parse_agg(self, agg_obj, table_alias):
        """
        处理aggregation段。将aggregation转为sql所需的格式。
        :param agg_obj: aggregation对象
        :param table_alias: 当前aggregation的所属表的别名
        :return: sql格式的字符串
        """
        if isinstance(agg_obj, Aggregation):
            if agg_obj.suffix == Aggregation.AVG:
                return 'AVG({}{}{}.{}{}{})'.format(self.quote, table_alias, self.quote, self.quote, agg_obj.field,
                                                   self.quote)
            elif agg_obj.suffix == Aggregation.SUM:
                return 'SUM({}{}{}.{}{}{})'.format(self.quote, table_alias, self.quote, self.quote, agg_obj.field,
                                                   self.quote)
            elif agg_obj.suffix == Aggregation.MAX:
                return 'MAX({}{}{}.{}{}{})'.format(self.quote, table_alias, self.quote, self.quote, agg_obj.field,
                                                   self.quote)
            elif agg_obj.suffix == Aggregation.MIN:
                return 'MIN({}{}{}.{}{}{})'.format(self.quote, table_alias, self.quote, self.quote, agg_obj.field,
                                                   self.quote)
            elif agg_obj.suffix == Aggregation.COUNT:
                return 'COUNT({}{}{}.{}{}{})'.format(self.quote, table_alias, self.quote, self.quote, agg_obj.field,
                                                     self.quote)
            elif agg_obj.suffix == Aggregation.COUNT_DISTINCT:
                return 'COUNT(DISTINCT {}{}{}.{}{}{})'.format(self.quote, table_alias, self.quote, self.quote,
                                                              agg_obj.field, self.quote)
            else:
                raise ProgramConfigException(401, '请联系开发者，parse agg后缀错误。无法识别的后缀{}。', agg_obj.suffix)
        else:
            raise ProgramConfigException(401, '请联系开发者，parse agg参数错误。需要Aggregation类实例，而不是{}。', type(agg_obj))

    def _parse_filter(self, filter_obj, table_alias):
        """
        处理filter段。将filter转为sql所需的格式。
        注意，本方法返回元组，第二个为sql语句的变量部分。为什么不像其他的一样直接编码进去呢？参考了peewee，为了防止时间字段缺少引号。
        :param filter_obj: filter对象
        :param table_alias: 当前aggregation的所属表的别名
        :return: 两元素元组: (sql字符串, 变量字符串 or None)
        """
        if isinstance(filter_obj, Filter):
            if filter_obj.suffix == Filter.EQUAL:
                return '{}{}{}.{}{}{} == %s'.format(self.quote, table_alias, self.quote, self.quote, filter_obj.key,
                                                    self.quote), (filter_obj.value,)
            elif filter_obj.suffix == Filter.GT:
                return '{}{}{}.{}{}{} > %s'.format(self.quote, table_alias, self.quote, self.quote, filter_obj.key,
                                                   self.quote), (filter_obj.value,)
            elif filter_obj.suffix == Filter.GTE:
                return '{}{}{}.{}{}{} >= %s'.format(self.quote, table_alias, self.quote, self.quote, filter_obj.key,
                                                    self.quote), (filter_obj.value,)
            elif filter_obj.suffix == Filter.LT:
                return '{}{}{}.{}{}{} < %s'.format(self.quote, table_alias, self.quote, self.quote, filter_obj.key,
                                                   self.quote), (filter_obj.value,)
            elif filter_obj.suffix == Filter.LTE:
                return '{}{}{}.{}{}{} <= %s'.format(self.quote, table_alias, self.quote, self.quote, filter_obj.key,
                                                    self.quote), (filter_obj.value,)
            elif filter_obj.suffix == Filter.CONTAINS:
                return '{}{}{}.{}{}{} LIKE {}%{}%{}'.format(self.quote, table_alias, self.quote, self.quote,
                                                            filter_obj.key, self.quote, self.quote, filter_obj.value,
                                                            self.quote), None
            elif filter_obj.suffix == Filter.STARTS_WITH:
                return '{}{}{}.{}{}{} LIKE {}{}%{}'.format(self.quote, table_alias, self.quote, self.quote,
                                                           filter_obj.key, self.quote, self.quote, filter_obj.value,
                                                           self.quote), None
            elif filter_obj.suffix == Filter.ENDS_WITH:
                return '{}{}{}.{}{}{} LIKE {}%{}{}'.format(self.quote, table_alias, self.quote, self.quote,
                                                           filter_obj.key, self.quote, self.quote, filter_obj.value,
                                                           self.quote), None
            elif filter_obj.suffix == Filter.RANGE:
                if isinstance(filter_obj.value, list) and len(filter_obj.value) == 2:
                    return '{}{}{}.{}{}{} BETWEEN %s AND %s'.format(self.quote, table_alias, self.quote, self.quote,
                                                                    filter_obj.key, self.quote), filter_obj.value
                else:
                    raise JsonFormatException(3, 'range需要传入长度为2的范围列表。如: [1, 2]。')
            elif filter_obj.suffix == Filter.IN:
                if isinstance(filter_obj.value, list):
                    template = '%s, {}'
                    in_str = ''
                    for i in range(len(filter_obj.value)):
                        in_str = template.format(in_str)
                    in_str = in_str.rsplit(',', 1)[0]
                    return '{}{}{}.{}{}{} IN ({})'.format(self.quote, table_alias, self.quote, self.quote,
                                                          filter_obj.key, self.quote, in_str), filter_obj.value
                else:
                    raise JsonFormatException(3, 'in需要传入元素列表，而不是{}。', type(filter_obj.value))
            else:
                raise ProgramConfigException(401, '请联系开发者，parse filter后缀错误。无法识别的后缀{}。', filter_obj.suffix)
        else:
            raise ProgramConfigException(401, '请联系开发者，parse filter参数错误。需要Filter类实例，而不是{}。', type(filter_obj))

    def parse_object(self, query_object):
        """
        将QueryObject对象转为sql查询语句。
        分为select、where和group by三个部分。
        注意，对于表来说需要有from xx as xx，并且保证字段顺序一致。
        :param query_object: QueryObject对象
        :return: 返回三元素元组，第一个是sql语句，第二个是参数列表，第三个是查询结果的列名列表
        """
        if isinstance(query_object, QueryObject):
            #
            # 拼凑字段
            #
            table_alias_list = ['t{}'.format(i) for i in range(1, len(getattr(query_object, 'join', [])) + 1)]
            params_list = []  # 最终sql参数
            fields_list = []  # 最终列表列名
            # select字段
            select_part = []
            for field in list(query_object.select.fields):  # main-field
                select_part.append('{}t0{}.{}{}{}'.format(self.quote, self.quote, self.quote, field, self.quote))
            fields_list.extend(query_object.select.fields)
            for agg_obj in query_object.select.aggregation:  # main-agg
                select_part.append(self._parse_agg(agg_obj, 't0'))
                fields_list.append('{}__{}'.format(agg_obj.field, agg_obj.suffix))
            if query_object.type != QueryObject.MAIN:  # 非MAIN查询的独立查询中，处理export
                for i in range(len(fields_list)):
                    if fields_list[i] in query_object.export:
                        fields_list[i] = query_object.export[fields_list[i]]
                    else:
                        fields_list[i] = SHOULD_BE_REMOVED
            for idx, sub_object in enumerate(getattr(query_object, 'join', [])):  # sub-field
                sub_fields_list = []
                for field in sub_object.select.fields:
                    select_part.append(
                        '{}{}{}.{}{}{}'.format(self.quote, table_alias_list[idx], self.quote, self.quote, field,
                                               self.quote))
                sub_fields_list.extend(sub_object.select.fields)
                for agg_obj in sub_object.select.aggregation:  # main-field
                    select_part.append(self._parse_agg(agg_obj, table_alias_list[idx]))
                    sub_fields_list.append('{}__{}'.format(agg_obj.field, agg_obj.suffix))
                for i in range(len(sub_fields_list)):  # 替换export部分，将需要export的处理，不需要的标记为删除
                    if sub_fields_list[i] in sub_object.export:
                        sub_fields_list[i] = sub_object.export[sub_fields_list[i]]
                    else:
                        sub_fields_list[i] = SHOULD_BE_REMOVED
                fields_list.extend(sub_fields_list)
            # where字段
            where_part = []
            for filter_obj in query_object.select.filter:  # main-filter
                where, params = self._parse_filter(filter_obj, 't0')
                where_part.append(where)
                if params is not None:
                    params_list.extend(list(params))
            for idx, sub_object in enumerate(getattr(query_object, 'join', [])):  # sub-filter
                for filter_obj in sub_object.select.filter:
                    where, params = self._parse_filter(filter_obj, table_alias_list[idx])
                    where_part.append(where)
                    if params is not None:
                        params_list.extend(list(params))
            # group by 字段
            group_by_part = []
            for group_by_field in query_object.select.group_by:  # main-group-by
                group_by_part.append(
                    '{}t0{}.{}{}{}'.format(self.quote, self.quote, self.quote, group_by_field, self.quote))
            for idx, sub_object in enumerate(getattr(query_object, 'join', [])):  # sub-filter
                for group_by_field in sub_object.select.group_by:  # main-group-by
                    group_by_part.append(
                        '{}{}{}.{}{}{}'.format(self.quote, table_alias_list[idx], self.quote, self.quote,
                                               group_by_field, self.quote))
            #
            # 拼凑SQL语句
            #
            query = 'SELECT '
            for select in select_part:
                if select == select_part[-1]:
                    query += '{} '.format(select)
                else:
                    query += '{}, '.format(select)
            query += 'FROM {}{}{} AS {}t0{} '.format(self.quote, query_object.select.from_, self.quote, self.quote,
                                                     self.quote)
            for idx, sub_object in enumerate(getattr(query_object, 'join', [])):
                if sub_object.type == QueryObject.LEFT_JOIN:
                    query += 'LEFT OUTER JOIN {}{}{} AS {}{}{} '.format(self.quote, sub_object.select.from_, self.quote,
                                                                        self.quote, table_alias_list[idx], self.quote)
                elif sub_object.type == QueryObject.INNER_JOIN:
                    query += 'INNER JOIN {}{}{} AS {}{}{} '.format(self.quote, sub_object.select.from_, self.quote,
                                                                   self.quote, table_alias_list[idx], self.quote)
                elif sub_object.type == QueryObject.FULL_JOIN:
                    query += 'FULL JOIN {}{}{} AS {}{}{} '.format(self.quote, sub_object.select.from_, self.quote,
                                                                  self.quote, table_alias_list[idx], self.quote)
                query += 'ON ( ( TRUE ) '
                for key, value in sub_object.on.items():
                    query += 'AND ( {}t0{}.{}{}{} = {}{}{}.{}{}{} ) '.format(self.quote, self.quote, self.quote, key,
                                                                             self.quote, self.quote,
                                                                             table_alias_list[idx], self.quote,
                                                                             self.quote, value, self.quote)
                query += ') '
            if len(where_part) != 0:
                query += 'WHERE ( ( TRUE ) '
            for where in where_part:
                query += 'AND ( {} ) '.format(where)
            if len(where_part) != 0:
                query += ') '
            if len(group_by_part) != 0:
                query += 'GROUP BY '
            for group_by in group_by_part:
                if group_by == group_by_part[-1]:
                    query += '{} '.format(group_by)
                else:
                    query += '{}, '.format(group_by)
            query += 'LIMIT {}'.format(getattr(query_object, 'limit', 1000))
            return query, params_list, fields_list
        else:
            raise ProgramConfigException(400, '请联系开发者，parse object参数错误。需要QueryObject类实例')


class EsEngine(Engine):
    """
    ElasticSearch查询引擎
    """
    _template = {
        'size': 1000,
        'query': {  # Query context
            'filter': [  # Filter context
            ],
        },
        '_source': {
            'includes': []
        },
        'aggs': {
            'groupby': {
                'terms': {
                    'script': {
                        'source': ''
                    }
                },
                'aggs': {}
            },
        },
    }

    def fetch_result(self, conn, query, params, fields):
        """
        根据dsl查询elasticsearch，并返回结果dataframe。
        对于非main查询，返回结果应该是只有export暴露的字段。main查询返回所有source。
        :param conn: Elasticsearch实例
        :param query: es查询dsl
        :param params: es查询的index
        :param fields: 若是main查询，则为None；否则为export的dict
        :return:
        """
        raw_result = conn.search(index=params, body=query)
        df = None
        if 'aggs' in raw_result or 'aggregations' in raw_result:  # dsl中有aggs.groupby.aggs
            if raw_result.get('aggregations'):
                df = pd.concat(map(pd.DataFrame.from_dict, raw_result['aggregations']['groupby']['buckets']))
            else:
                df = pd.concat(map(pd.DataFrame.from_dict, raw_result['aggs']['groupby']['buckets']))
            df.drop('doc_count', axis=1, inplace=True)
            example_val = df['key'].iat[0]  # 1
            col_name = example_val.split(':', 1)[0]
            df.rename({'key': col_name}, axis=1, inplace=True)
            df[col_name] = df[col_name].map(lambda x: x.split(':', 1)[1])
        elif 'hits' in raw_result and 'hits' in raw_result['hits']:
            df = pd.concat(map(pd.DataFrame.from_dict, raw_result['hits']['hits']), axis=1)['_source'].T
        else:
            raise RunningException(1, 'es查询失败: 未在结果中看到aggs、hits数据部分。请查看日志')
        if fields is not None:  # 非main查询，需要根据export删减部分分支
            columns_list = df.columns.tolist()
            for column in columns_list:
                if column not in fields:
                    df.drop(column, axis=1, inplace=True)
        columns_list = df.columns.tolist()
        for column in columns_list:  # 为了后续转为时间戳格式方便处理，这里不得不采用这种低效的方式
            value = df[column].iat[0]
            if EsEngine._is_time(value) is not None:
                df[column] = df[column].map(lambda x: EsEngine._is_time(x))
        return df

    @staticmethod
    def _is_time(value):
        """
        判断是否是时间类型，若是返回datetime，否则返回None
        """
        try:
            res = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            return res
        except:
            pass
        try:
            value_tmp = value.replace('T', ' ', 1).replace('Z', '', 1)
            res = datetime.datetime.strptime(value_tmp, '%Y-%m-%d %H:%M:%S.%f')
            return res
        except:
            pass
        try:
            res = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return res
        except:
            pass
        try:
            res = datetime.datetime.strptime(value, '%Y%m%d%H')
            return res
        except:
            pass
        try:
            res = datetime.datetime.strptime(value, '%Y-%m-%d')
            return res
        except:
            return None

    def _parse_filter(self, filter_obj_list):
        must_list = []
        for filter_obj in filter_obj_list:
            if isinstance(filter_obj, Filter):
                if filter_obj.suffix == Filter.EQUAL:
                    must_list.append({
                        'term': {
                            filter_obj.key: filter_obj.value
                        }
                    })
                elif filter_obj.suffix == Filter.GT:
                    must_list.append({
                        'range': {
                            filter_obj.key: {'gt': filter_obj.value}
                        }
                    })
                elif filter_obj.suffix == Filter.GTE:
                    must_list.append({
                        'range': {
                            filter_obj.key: {'gte': filter_obj.value}
                        }
                    })
                elif filter_obj.suffix == Filter.LT:
                    must_list.append({
                        'range': {
                            filter_obj.key: {'lt': filter_obj.value}
                        }
                    })
                elif filter_obj.suffix == Filter.LTE:
                    must_list.append({
                        'range': {
                            filter_obj.key: {'lte': filter_obj.value}
                        }
                    })
                elif filter_obj.suffix == Filter.CONTAINS:
                    """"
                    TODO: 本来想用match/match_phrase来进行模糊匹配，但是由于这两种查询由于分词的缘故，现有的
                          分词情况并不能完美的模拟sql中的like，所以暂时采用正则查询。正则查询的效率很低。
                    dsl_where.append({
                        'match_phrase': {
                            field_name: {
                                'query': value
                            }
                        }
                    })
                    """
                    must_list.append({
                        'wildcard': {filter_obj.key: ''.join(['*', filter_obj.value, '*'])}
                    })
                elif filter_obj.suffix == Filter.STARTS_WITH:
                    must_list.append({
                        'prefix': {filter_obj.key: filter_obj.value}
                    })
                elif filter_obj.suffix == Filter.ENDS_WITH:
                    must_list.append({
                        'wildcard': {filter_obj.key: ''.join(['*', filter_obj.value])}
                    })
                elif filter_obj.suffix == Filter.RANGE:
                    if len(filter_obj.value) != 2:
                        raise JsonFormatException(3, 'range需要传入长度为2的范围列表。如: [1, 2]。')
                    must_list.append({
                        'range': {
                            filter_obj.key: {'gte': filter_obj.value[0], 'lte': filter_obj.value[1]}
                        }
                    })
                elif filter_obj.suffix == Filter.IN:
                    if isinstance(filter_obj.value, list):
                        must_list.append({
                            'terms': {filter_obj.key: filter_obj.value}
                        })
                    else:
                        raise JsonFormatException(3, 'in需要传入元素列表，而不是{}。', type(filter_obj.value))
                else:
                    raise ProgramConfigException(401, '请联系开发者，parse filter后缀错误。无法识别的后缀{}。', filter_obj.suffix)
            else:
                raise ProgramConfigException(401, '请联系开发者，parse filter参数错误。需要Filter类实例，而不是{}。', type(filter_obj))
        return must_list

    def parse_object(self, query_object):
        """
        转为elasticsearch的查询dsl。
        由于es的特殊性，query_object不应该有join字段，每个join都需要单独查询后在内存中处理。
        只会访问select字段内容(其实还有fields/export)
        :param query_object:
        :return:
            三元组: dsl、index和字段/None
        """
        if isinstance(query_object, QueryObject):
            fields = getattr(query_object, 'export', None)  # 非main查询应该暴露的字段
            dsl = copy.deepcopy(EsEngine._template)
            dsl['size'] = query_object.limit
            dsl['_source']['includes'].extend([field for field in query_object.select.fields])

            must_list = self._parse_filter(query_object.select.filter)
            dsl['query']['filter'].extend(must_list)
            if not dsl['query']['filter']:  # 若filter为空直接删除
                del dsl['query']['filter']
            if not dsl['query']:  # 若query为空直接删除
                del dsl['query']

            dsl_group_by = ''
            dsl_aggs = dsl['aggs']['groupby']['aggs']
            if len(query_object.select.group_by) != 0:  # 只有有group by，agg才有意义
                """
                由于ES 6.x以下版本不支持 composite 语法，所以这里采用script方式来实现group by，用来兼容不同版本ES这部分语法的差异性
                script中source的格式：key:value;key:value
                定义成这个样子是方便后面从查询结果中提取数据
                """
                for field in query_object.select.group_by:
                    dsl_group_by = ''.join(
                        [dsl_group_by, "'", field, "'", " + ':' + ", "doc['", field, "'].value", " + ';' + "])
                dsl_group_by = dsl_group_by[:len(dsl_group_by) - len(" + ';' + ")]  # 去掉结尾的 " + ';' + "
                dsl['aggs']['groupby']['terms']['script']['source'] = dsl_group_by
                # 处理 aggregation
                func_map = {'count': 'value_count', 'sum': 'sum', 'avg': 'avg', 'max': 'max', 'min': 'min',
                            'count_distinct': 'cardinality'}
                for agg_obj in query_object.select.aggregation:
                    if isinstance(agg_obj, Aggregation):
                        if agg_obj.suffix in func_map:
                            dsl_aggs['{}__{}'.format(agg_obj.field, agg_obj.suffix)] = {
                                func_map[agg_obj.suffix]: {'field': agg_obj.field}}
                        else:
                            raise ProgramConfigException(401, '请联系开发者，parse agg后缀错误。无法识别的后缀{}。', agg_obj.suffix)
                    else:
                        raise ProgramConfigException(401, '请联系开发者，parse agg参数错误。需要Aggregation类实例，而不是{}。', type(agg_obj))
            else:
                del dsl['aggs']
            return dsl, query_object.select.from_, fields
        else:
            raise ProgramConfigException(400, '请联系开发者，parse object参数错误。需要QueryObject类实例')
