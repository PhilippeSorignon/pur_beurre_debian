import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q

import requests

from .models import Food, SavedFood
from users.schema import UserType


class FoodType(DjangoObjectType):
    ''' Informations about a food product '''
    class Meta:
        model = Food

class SavedFoodType(DjangoObjectType):
    ''' Informations about a saved food product '''
    class Meta:
        model = SavedFood

class Query(graphene.ObjectType):
    ''' Food related queries '''
    foods = graphene.List(
        FoodType,
        search_title=graphene.String(description='Used to search in the title'),
        search_category=graphene.String(
            description='Used to search with the categories'
        ),
        description="Get a list of foods"
    )
    food = graphene.Field(FoodType, id=graphene.ID())
    savedFoods = graphene.List(
        SavedFoodType,
        description='Get a list of Saved Foods'
    )

    def resolve_foods(self, info, search_title=None, search_category=None):
        '''
            Return a list of foods

            Use "search_title" to return a list of foods wich contains your entries
            Use "search categoriy to return all the foods in said category"
        '''
        if search_title:
            return Food.objects.filter(name__icontains=search_title)
        elif search_category:
            search = (
                Q(category__icontains=search_category) &
                (Q(nutriscore__icontains="a") | Q(nutriscore__icontains="b"))
            )
            return Food.objects.filter(search)

        return Food.objects.all()


    def resolve_food(self, info, **kwargs):
        try:
            return Food.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return None

    def resolve_saved_food(self, info):
        return SavedFood.objects.all()


class CreateSavedFood(graphene.Mutation):
    ''' Save a food for a logged user '''
    user = graphene.Field(UserType)
    food = graphene.Field(FoodType)

    class Arguments:
        food_id = graphene.Int(required=True)

    def mutate(self, info, food_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Connectez vous pour enregistrer des produits')

        food = Food.objects.get(id=food_id)
        if not food:
            raise GraphQLError('Produit introuvable')

        if SavedFood.objects.filter(user=user, food=food).exists():
            raise GraphQLError('Produit déja enregistré')

        SavedFood.objects.create(
            user=user,
            food=food
        )

        return CreateSavedFood(user=user, food=food)

class DeleteSavedFood(graphene.Mutation):
    ''' Delete a food saved by the user '''
    saved_food_id = graphene.Int()

    class Arguments:
        saved_food_id = graphene.Int(
        required=True,
        description='ID of the saved food to delete'
    )

    def mutate(self, info, saved_food_id):
        user = info.context.user
        saved_food = SavedFood.objects.get(id=saved_food_id)

        if saved_food.user != user:
            raise GraphQLError('Vous ne pouvez pas supprimer cette sauvegarde')

        saved_food.delete()

        return DeleteSavedFood(saved_food_id=saved_food_id)


class Mutation(graphene.ObjectType):
    create_saved_food = CreateSavedFood.Field()
    delete_saved_food = DeleteSavedFood.Field()
