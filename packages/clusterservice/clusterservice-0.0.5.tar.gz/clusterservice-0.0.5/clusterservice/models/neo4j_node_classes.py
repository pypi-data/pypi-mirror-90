from neomodel import (
    FloatProperty,
    Relationship,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Comment(StructuredNode):
    uuid = UniqueIdProperty()
    text = StringProperty(required=True)
    cid = StringProperty(required=True)
    forum_id = StringProperty(required=True)


class Sentence(StructuredNode):
    text = StringProperty(required=True)
    cid = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    relationship = Relationship(Comment, 'IS_FROM_COMMENT')


class ClusterElement(StructuredNode):
    text = StringProperty(required=True)
    cid = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    relationship = Relationship(Sentence, 'IS_FROM_SENTENCE')


class ClusterHead(StructuredNode):
    text = StringProperty(required=True)
    cid = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    relationship = Relationship(ClusterElement, 'HAS_CLUSTER_ELEMENT')
    similarity_score = FloatProperty(required=True)


class Question(StructuredNode):
    text = StringProperty(required=True)
    cid = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    relationship = Relationship(ClusterHead, 'ANSWERED_BY')
