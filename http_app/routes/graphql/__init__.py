from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from .query import Query

schema = Schema(query=Query)

graphql_app = GraphQLRouter(schema)
