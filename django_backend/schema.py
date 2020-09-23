import graphene
import foods.schema
import users.schema
import graphql_jwt

class Query(users.schema.Query, foods.schema.Query, graphene.ObjectType, description='Pur Beurre Queries'):
    pass

class Mutation(
    users.schema.Mutation,
    foods.schema.Mutation,
    graphene.ObjectType,
    description='Pur Beurre Mutations'
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
