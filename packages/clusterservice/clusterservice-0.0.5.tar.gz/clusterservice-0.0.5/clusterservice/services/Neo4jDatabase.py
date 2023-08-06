import logging

from neo4j import GraphDatabase
from neomodel import config, db
from py2neo import Graph

from ..models.BaseGraphDatabase import BaseGraphDatabase
from ..models.neo4j_node_classes import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# alpha ordering is important
NODE_TYPES = {
    'Question': 'a',
    'ClusterHead': 'b',
    'ClusterElement': 'c',
    'Sentence': 'd',
    'Comment': 'e',
}


class Neo4jDatabase(BaseGraphDatabase):

    def __init__(self, host, username, password):
        super(BaseGraphDatabase, self).__init__()
        logger.debug('initialising Neo4jDatabase')
        config.DATABASE_URL = 'bolt://{}:{}@{}:7687'.format(username, password, host)
        config.ENCRYPTED_CONNECTION = False
        self.node_classes = {item:db._NODE_CLASS_REGISTRY[frozenset({item})]
                             for item in NODE_TYPES.keys()}

        self.graph = Graph(host=host, auth=(username, password))
        db_url = 'neo4j://{}:7687'.format(host)
        self.driver = GraphDatabase.driver(db_url, auth=(username, password))

    def add_node(self,
        node_type,
        text,
        cid,
        forum,
        client_id=None,
        uuid=None,
        similarity_score=None,
        element_count=None
    ):
        logger.debug('Neo4jDatabase.add_node')
        input_dic = {}
        input_dic['text'] = text
        input_dic['cid'] = cid
        input_dic['forum_id'] = forum
        if client_id is not None:
            input_dic['client_id'] = client_id

        if uuid is not None:
            input_dic['uuid'] = uuid

        if similarity_score is not None:
            input_dic['similarity_score'] = similarity_score

        if element_count is not None:
            input_dic['element_count'] = element_count

        node = self.node_classes[node_type].get_or_create(input_dic)
        return node

    def add_edge(self, node1, node2):
        logger.debug('Neo4jDatabase.add_edge')
        node1.relationship.connect(node2)

    def query_from_db_helper(self,
        tx,
        input_types,
        input_attributes,
        input_values,
        output_types,
        output_attributes
    ):
        logger.debug('Neo4jDatabase.query_from_db_helper')
        all_vars = []
        input_vars = []
        input_str = ''
        for i_value, i_type, i_attr in zip(input_values, input_types, input_attributes):
            input_type_mapped = NODE_TYPES[i_type]
            if i_type=='id':
                input_str += 'id(%s)="%s" AND '
                input_vars.append(input_type_mapped)
                input_vars.append(i_value)
            else:
                input_str += '%s.%s="%s" AND '
                input_vars.append(input_type_mapped)
                input_vars.append(i_attr)
                input_vars.append(i_value)

        if len(input_str) > 0:
            input_str = input_str[:-4]
        
        all_vars.extend(input_vars)

        output_str = ''
        output_vars = []
        for o_type, o_attr in zip(output_types, output_attributes):
            output_type_mapped = NODE_TYPES[o_type]
            if o_attr == 'id':
                output_str += 'id(%s) AS {}_id ,'.format(o_type)
                output_vars.append(output_type_mapped)
            else:
                output_str += '%s.%s AS {}_{} ,'.format(o_type, o_attr)
                output_vars.append(output_type_mapped)
                output_vars.append(o_attr)

        if len(output_str) > 0:
            output_str = output_str[:-1]

        all_vars.extend(output_vars)

        query = (
            'MATCH (a:Question)-[:ANSWERED_BY]'
            '-(b:ClusterHead)-[:HAS_CLUSTER_ELEMENT]'
            '-(c:ClusterElement)-[:IS_FROM_SENTENCE]'
            '-(d:Sentence)-[:IS_FROM_COMMENT]'
            '-(e:Comment)'
            ' WHERE ' + input_str +
            ' RETURN DISTINCT ' + output_str
        )

        query = query % tuple(all_vars)
        logger.debug('query: %s', query)
        result = tx.run(query)

        return list(result)

    def query_from_db(self,
        input_values,
        input_types=['Question'],
        input_attributes=['text'],
        output_types=None,
        output_attributes=None
    ):
        logger.debug('Neo4jDatabase.query_from_db')
        if output_types is None:
            output_types = ['ClusterHead', 'Sentence', 'Comment']

        if output_attributes is None:
            output_attributes = ['text', 'text', 'text']

        with self.driver.session() as sess:
            results = sess.read_transaction(
                self.query_from_db_helper,
                input_types,
                input_attributes,
                input_values,
                output_types,
                output_attributes
            )

        return results

    def delete_nodes(self, id_list):
        logger.debug('Neo4jDatabase.delete_nodes')
        for id_ in id_list:
            node = self.graph.evaluate('MATCH (n) where id(n) = {} RETURN n'.format(id_))
            if node is not None:
                self.graph.delete(node)

    # TODO unused args
    def exists(self, node_type, attribute, value, forum_id, client_ids):
        logger.debug('Neo4jDatabase.exists')
        if (node_type is None or
            attribute is None or
            value is None or
            node_type == '' or
            attribute == ''):
            return False

        filter_node = ('(n:' + node_type + '')
        filter_value = (') WHERE n.' + attribute + '="' + value + '"') 
        return db.cypher_query('MATCH' + filter_node + filter_value + ' return count(n) > 0 as exists;')[0][0][0]

    def delete_all_nodes(self):
        logger.debug('Neo4jDatabase.delete_all_nodes')
        for node_class in self.node_classes:
            for item in self.node_classes[node_class].nodes.all():
                item.delete()
