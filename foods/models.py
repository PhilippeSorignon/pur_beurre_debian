from django.db import models
from django.contrib.auth import get_user_model

class Food(models.Model):
    name = models.CharField(max_length=250)
    nutriscore = models.CharField(max_length=1)
    url = models.TextField()
    image = models.TextField()
    category = models.CharField(max_length=250)

class SavedFood(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE
    )
    food = models.ForeignKey(
        'foods.Food',
        related_name='food',
        on_delete=models.CASCADE
    )
