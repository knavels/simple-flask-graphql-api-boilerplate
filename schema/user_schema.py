from models.user import User
import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from db import db


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )
        exclude_fields = ('password_hash')


class SignUp(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(lambda: UserObject)
    auth_token = graphene.String()

    def mutate(self, info, **kwargs):
        user = User(username=kwargs.get('username'))
        user.set_password(kwargs.get('password'))
        db.session.add(user)
        db.session.commit()
        return SignUp(user=user, auth_token=user.encode_auth_token(user.uuid).decode())


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(lambda: UserObject)
    auth_token = graphene.String()

    def mutate(self, info, **kwargs):
        user = User.query.filter_by(username=kwargs.get('username')).first()
        if user is None or not user.check_password(kwargs.get('password')):
            raise GraphQLError("Invalid Credentials")
        return Login(user=user, auth_token=user.encode_auth_token(user.uuid).decode())
