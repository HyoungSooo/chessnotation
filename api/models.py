from django.db import models

# Create your models here.


class ChessELO(models.Model):
    avg = models.IntegerField(unique=True, blank=False)


class ChessNoationCheckPoint(models.Model):
    fname = models.CharField(max_length=100, unique=True)
    checkpoint = models.IntegerField()


class ChessNotation(models.Model):
    avg = models.ForeignKey(
        ChessELO, on_delete=models.CASCADE, related_name='notation')
    white = models.CharField(max_length=100)
    black = models.CharField(max_length=100)
    site = models.URLField(max_length=200)
    mainline = models.TextField()
    opening = models.TextField()
    event = models.CharField(max_length=50)
    result = models.CharField(max_length=20)


class ChessPuzzles(models.Model):
    pass


class NotataionVersion(models.Model):
    vers = models.CharField(max_length=10, blank=True, null=True)
