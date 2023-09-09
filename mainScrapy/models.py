from django.db import models

class Recherche(models.Model):
    texte = models.CharField(max_length=240, blank=False, null=False)

    def __str__(self):
        return self.texte

