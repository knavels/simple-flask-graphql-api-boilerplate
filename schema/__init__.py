import graphene
from helpers.middlewares import require_auth
from schema.viewers import ProtectedViewer, Viewer
from schema.mutations import Mutation


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    protected_viewer = graphene.Field(ProtectedViewer)
    viewer = graphene.Field(Viewer)

    @staticmethod
    @require_auth
    def resolve_protected_viewer(root, info, **kwargs):
        return ProtectedViewer()

    @staticmethod
    def resolve_viewer(root, info, **kwargs):
        return Viewer()


schema = graphene.Schema(query=Query, mutation=Mutation)
