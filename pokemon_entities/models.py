from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='image', null=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=None, null=True)
    disappeared_at = models.DateTimeField(default=None, null=True)
    level = models.IntegerField()
    health = models.IntegerField()
    strenght = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
    
    def __str__(self):
        return self.pokemon.title
# your models here
