from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MainCycle(models.Model):
    user = models.OneToOneField(User, related_name='cycle', null=False, on_delete=models.CASCADE)
    coinsCount = models.IntegerField(default=0)
    clickPower = models.IntegerField(default=1)

    def click(self):
        self.coinsCount += self.clickPower


class Boost(models.Model):
    mainCycle = models.ForeignKey(MainCycle, related_name='boosts', null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=1)
    price = models.IntegerField(default=5)

    def upgrade(self):
        self.mainCycle.clickPower += self.power
        self.mainCycle.coinsCount -= self.price
        self.power += 2
        self.price *= 2