'''
Input format and output format:
{
    'question-1': {
        'cluster-head1': {
            'similarity_score': 0.4,
            'element_count': 10,
            'cluster_elements': [
                [element1, sentence1, comment1],
                [element2, sentence2, comment2]
            ]
        }
    }
}
'''
import hashlib
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GraphDbReaderWriter:

    def __init__(self, db):
        logger.debug('initialising GraphDbReaderWriter')
        self.db = db

    def save_to_db(self, cluster_dic, forum, client_id):
        logger.debug('GraphDbReaderWriter.save_to_db')
        # TODO use uuids
        question_id = 1
        element_id = 1

        to_delete_node_ids = set()
        remove_from_delete = {
            'Question': set(),
            'ClusterHead': set(),
            'ClusterElement': set(),
            'Sentence': set(),
            'Comment': set(),
        }

        for question in cluster_dic:
            delete_after = False
            if self.db.exists('Question','text', question, forum, client_id):
                id_list = self.db.query_from_db(
                    input_values=[question, forum],
                    input_types=['Question', 'Question','Question'],
                    input_attributes=['text', 'forum_id', 'client_id'],
                    output_types=['Question', 'ClusterHead', 'ClusterElement', 'Sentence', 'Comment'],
                    output_attributes=['id', 'id', 'id', 'id', 'id']
                )
                node_types = ['Question', 'ClusterHead', 'ClusterElement', 'Sentence', 'Comment']
                for item in id_list:
                    for node_type in node_types:
                        to_delete_node_ids.add(item['%s_id' % node_type])

                delete_after = True

            q_node = self.db.add_node(
                node_type='Question',
                text=question,
                cid=question_id,
                client_id=client_id,
                forum=forum
            )[0]
            if delete_after and q_node.__dict__['id'] in to_delete_node_ids:
                to_delete_node_ids.remove(q_node.__dict__['id'])
                remove_from_delete['Question'].add(q_node.__dict__['id'])

            cluster_id = 1

            # each item is in the form: head, similarity, element count, element list
            for cluster_head in cluster_dic[question]:
                cluster_node = self.db.add_node(
                    node_type='ClusterHead',
                    text=cluster_head,
                    cid='cluster-%d' % cluster_id,
                    forum=forum,
                    similarity_score=cluster_dic[question][cluster_head]['similarity_score']
                )[0]
                if delete_after and cluster_node.__dict__['id'] in to_delete_node_ids:
                    to_delete_node_ids.remove(cluster_node.__dict__['id'])
                    remove_from_delete['ClusterHead'].add(cluster_node.__dict__['id'])

                self.db.add_edge(q_node, cluster_node)

                for cluster_element in cluster_dic[question][cluster_head]['cluster_elements']:
                    cluster_element_node = self.db.add_node(
                        node_type='ClusterElement',
                        text=cluster_element[0],
                        cid='element-%d' % element_id,
                        forum=forum
                    )[0]
                    if delete_after and cluster_element_node.__dict__['id'] in to_delete_node_ids:
                        to_delete_node_ids.remove(cluster_element_node.__dict__['id'])
                        remove_from_delete['ClusterElement'].add(cluster_element_node.__dict__['id'])

                    self.db.add_edge(cluster_node, cluster_element_node)

                    sentence_node = self.db.add_node(
                        node_type='Sentence',
                        text=cluster_element[1],
                        cid='sentence-%d' % element_id,
                        forum=forum
                    )[0]
                    if delete_after and sentence_node.__dict__['id'] in to_delete_node_ids:
                        to_delete_node_ids.remove(sentence_node.__dict__['id'])
                        remove_from_delete['Sentence'].add(sentence_node.__dict__['id'])

                    self.db.add_edge(cluster_element_node, sentence_node)

                    hash_object = hashlib.md5(cluster_element[2].encode())
                    uuid = str(hash_object.hexdigest())

                    comment_node = self.db.add_node(
                        uuid=uuid,
                        node_type='Comment',
                        text=cluster_element[2],
                        cid='comment-%d' % element_id,
                        forum=forum
                    )[0]
                    if delete_after and comment_node.__dict__['id'] in to_delete_node_ids:
                        to_delete_node_ids.remove(comment_node.__dict__['id'])
                        remove_from_delete['Comment'].add(comment_node.__dict__['id'])

                    self.db.add_edge(sentence_node, comment_node)

                    element_id += 1

                cluster_id += 1

            question_id += 1
        
        logger.debug('Saved to db')
        logger.debug('Deleting nodes:', to_delete_node_ids)
        logger.debug('Nodes removed from delete list:', remove_from_delete)
        self.db.delete_nodes(to_delete_node_ids)
        logger.debug('Deleted old nodes')

    # TODO unused args
    def get_from_db(self, question_list, forum, client_id):
        logger.debug('GraphDbReaderWriter.get_from_db')
        cluster_dic = {}
        for question in question_list:
            cluster_dic[question] = {}
            query_return_list=self.db.query_from_db(
                # input_values=[question, forum, client_id],
                input_values=[question, forum],
                input_types=['Question', 'Question', 'Question'],
                input_attributes=['text', 'forum_id', 'client_id'],
                output_types=['Question', 'ClusterHead', 'ClusterHead', 'ClusterHead', 'ClusterElement', 'Sentence', 'Comment'],
                output_attributes=['text', 'text', 'similarity_score', 'element_count', 'text', 'text', 'text']
            )
            for query_item in query_return_list:
                if query_item['ClusterHead_text'] not in cluster_dic[question]:
                    cluster_dic[question][query_item['ClusterHead_text']] = {
                        'similarity_score': None,
                        'element_count': None,
                        'cluster_elements': {}
                    }

                if cluster_dic[question][query_item['ClusterHead_text']]['similarity_score'] is None:
                    cluster_dic[question][query_item['ClusterHead_text']]['similarity_score'] = query_item['ClusterHead_similarity_score']
                
                cluster_element = query_item['ClusterElement_text']
                sent_comment = {'sentence' : query_item['Sentence_text'], 'comment': query_item['Comment_text']} 
                if cluster_element not in cluster_dic[question][query_item['ClusterHead_text']]['cluster_elements']:
                    cluster_dic[question][query_item['ClusterHead_text']]['cluster_elements'][cluster_element] = []

                cluster_dic[question][query_item['ClusterHead_text']]['cluster_elements'][cluster_element].append(sent_comment)

            for cluster_head in cluster_dic[question]:
                if cluster_dic[question][cluster_head]['element_count'] is None:
                    cluster_dic[question][cluster_head]['element_count'] = len(cluster_dic[question][cluster_head]['cluster_elements'])

        return cluster_dic
