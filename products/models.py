from django.db import models
from django.contrib.auth import models as auth_models
from django.db.models import Avg


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    minimum_age_appropriate = models.IntegerField(default=0, blank=False)
    maximum_age_appropriate = models.IntegerField(default=-1, blank=False)
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
    stars = models.IntegerField()
    review = models.TextField()
    product = models.ForeignKey(Product, models.CASCADE)
    user = models.ForeignKey(auth_models.User, models.CASCADE)

    def __str__(self):
        return f"Review for {self.product.name}, {self.stars} stars"
