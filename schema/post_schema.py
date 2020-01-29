from models.post import Post
from models.user import User
import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from db import db
from helpers.middlewares import require_auth


class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        author_uuid = graphene.Int(required=True)
    post = graphene.Field(lambda: PostObject)

    @require_auth
    def mutate(self, info, **kwargs):
        user = User.query.filter_by(uuid=kwargs.get('author_uuid')).first()
        post = Post(title=kwargs.get('title'), body=kwargs.get('body'))
        if user is not None:
            post.author = user
        db.session.add(post)
        db.session.commit()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        uuid = graphene.Int(required=True)
    post = graphene.Field(lambda: PostObject)

    @require_auth
    def mutate(self, info, **kwargs):
        post = Post.query.filter_by(uuid=kwargs.get('uuid')).first()
        author = User.query.filter_by(uuid=post.author.uuid).first()
        if kwargs.get('user') != author:
            raise GraphQLError(
                "You do not have permissions to update this post.")
        else:
            post.title = kwargs.get('title')
            post.body = kwargs.get('body')
            db.session.commit()
            return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        uuid = graphene.Int(required=True)

    status = graphene.String()

    @require_auth
    def mutate(self, info, **kwargs):
        post = Post.query.filter_by(uuid=kwargs.get('uuid')).first()
        author = User.query.filter_by(uuid=post.author.uuid).first()
        if kwargs.get('user') != author:
            raise GraphQLError(
                "You do not have permissions to delete this post.")
        else:
            db.session.delete(post)
            db.session.commit()
            return DeletePost(status="OK")
