from models.user import User
from graphql import GraphQLError


def require_auth(method):
    def wrapper(self, *args, **kwargs):
        auth_resp = User.decode_auth_token(args[0].context)
        if not isinstance(auth_resp, str):
            kwargs['user'] = User.query.filter_by(uuid=auth_resp).first()
            return method(self, *args, **kwargs)
        raise GraphQLError(auth_resp)
    return wrapper
