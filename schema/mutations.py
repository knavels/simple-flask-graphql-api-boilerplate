import graphene
from schema.user_schema import UserObject, SignUp, Login
from schema.post_schema import PostObject, CreatePost, UpdatePost, DeletePost


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    signup = SignUp.Field()
    login = Login.Field()
