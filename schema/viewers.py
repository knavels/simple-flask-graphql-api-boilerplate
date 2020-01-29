import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from schema.post_schema import PostObject, CreatePost, UpdatePost, DeletePost
from schema.user_schema import UserObject, SignUp, Login


class ProtectedViewer(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node, )

    all_posts = SQLAlchemyConnectionField(PostObject)


class Viewer(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node, )

    all_users = SQLAlchemyConnectionField(UserObject)
