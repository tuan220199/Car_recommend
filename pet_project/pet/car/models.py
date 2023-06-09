from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='auth_users',  # Add a related name to the groups field in the auth app
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='auth_users',  # Add a related name to the user_permissions field in the auth app
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Category(models.Model):
    groups = models.CharField(max_length=30)
    image_url_brand = models.CharField(max_length=1000,  blank=True, null=True) 

    def __str__(self):
        return f"{self.groups}" 

    def serialize(self):
        return {
            "id": self.id,
            "groups": self.groups,
            "image_url_brand": self.image_url_brand
        }

class Car(models.Model):
    price = models.FloatField()
    year = models.FloatField()
    mileage = models.FloatField()
    engine_capacity = models.FloatField()
    
    model = models.CharField(max_length=64)
    transmission = models.CharField(max_length=64)
    drive = models.CharField(max_length=64)
    hand_drive = models.CharField(max_length=64)
    fuel = models.CharField(max_length=64)
    image_url = models.CharField(max_length=1000)

    mark_category =  models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.username,
            "price": self.price,
            "year": self.year,
            "mileage": self.mileage,
            "engine_capacity": self.engine_capacity,
            "model": self.model,
            "transmission": self.transmission,
            "drive": 2 if self.drive == "2wd" else 4,
            "hand_drive": self.hand_drive,
            "fuel": self.fuel,
            "image_url": self.image_url,
            "mark_category": self.mark_category.groups
        }

class Watch_list(models.Model):
    user_watch_list = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True, related_name="user_watch_list")
    list_watch = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank= True, related_name="list_watch")


