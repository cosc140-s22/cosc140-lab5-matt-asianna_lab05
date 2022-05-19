from django.db import models
from django.contrib.auth import models as auth_models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator 

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, validators=[MinValueValidator(0.01)])
    minimum_age_appropriate = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(1), MaxValueValidator(99)])
    maximum_age_appropriate = models.IntegerField(default=-1, blank=False, validators=[MinValueValidator(1), MaxValueValidator(99)])
    release_date = models.DateField()

    def __str__(self):
        return f"Product {self.name}, price {self.price:.02f}"

    def avg_rating(self):
        return self.review_set.all().aggregate(Avg('stars'))['stars__avg']

    def age_range(self):
        if self.maximum_age_appropriate == -1:
            return f"Ages {self.minimum_age_appropriate} and up"
        elif self.maximum_age_appropriate == self.minimum_age_appropriate:
            return f"Age {self.minimum_age_appropriate}"
        else:
            return f"Ages {self.minimum_age_appropriate} to {self.maximum_age_appropriate}"

class Review(models.Model):
    stars = models.IntegerField(blank=False, validators = [MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    product = models.ForeignKey(Product, models.CASCADE)
    user = models.ForeignKey(auth_models.User, models.CASCADE)

    def __str__(self):
        return f"Review for {self.product.name}, {self.stars} stars"
