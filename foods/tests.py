import json

from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model

from foods.schema import Query, Mutation
from foods.models import Food, SavedFood

class FoodTestCase(GraphQLTestCase, JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = Query

    def setUp(self):
        self.user = get_user_model().objects.create(username='TestUser')
        self.client.authenticate(self.user)
        self.food = Food.objects.create(id=1,
                                        name="Eau",
                                        nutriscore="a",
                                        url="http://eau.com/",
                                        image="http://eau.com/eau",
                                        category="drinks")

    def test_foods(self):
        ''' Test the foods query '''
        response = self.query(
            '''
            {
              foods {
                id
                name
                nutriscore
                category
              }
            }
            '''
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            {'foods': [
                {'id': '1',
                 'name': 'Eau',
                 'nutriscore': 'a',
                 'category': 'drinks'}]},
            content['data']
        )

    def test_create_saved_foods(self):
        ''' Test the createSavedFood mutation '''
        query = '''
        mutation {
            createSavedFood(foodId: 1) {
                user {
                    username
                }
                food {
                    name
                }
            }
        }'''

        response = self.client.execute(query)
        self.assertIsNone(response.errors)

    GRAPHQL_SCHEMA = Mutation

    def test_create_user(self):
        ''' Test the createUser mutation '''
        response = self.query(
            '''
            mutation {
                createUser(username: "Test", email: "test@mail.com", password: "test") {
                    user {
                        id
                        username
                        email
                    }
                }
            }
            '''
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            {'createUser': {
                'user': {
                    'id': '3',
                    'username': 'Test',
                    'email': 'test@mail.com'}}},
            content['data']
        )

    def test_me(self):
        ''' Test the me query '''
        query = '''
        {
            me {
                username
                email
            }
        }'''

        response = self.client.execute(query)

        self.assertIsNone(response.errors)

        self.assertDictEqual(
            {'me': {'username': 'TestUser', 'email': ''}},
            response.data
        )
