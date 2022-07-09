from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(
        'имя покемона на русском', 
        max_length=200)
    title_en = models.CharField(
        'имя покемона на английском', 
        max_length=200, 
        blank=True)
    title_jp = models.CharField(
        'имя покемона на японском', 
        max_length=200, 
        blank=True)
    image = models.ImageField(
        'изображение покемона', 
        upload_to='image', 
        blank=True, 
        null=True)
    description = models.TextField(
        'описание покемона', 
        blank=True)
    previous_evolution = models.ForeignKey(
        'self', 
        verbose_name='предок', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, verbose_name='покемон', on_delete=models.CASCADE)
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    appeared_at = models.DateTimeField(
        'время появления', blank=True, default=None, null=True)
    disappeared_at = models.DateTimeField(
        'время пропадания', blank=True, default=None, null=True)
    level = models.IntegerField('уровень', blank=True, null=True)
    health = models.IntegerField('здоровье', blank=True, null=True)
    strenght = models.IntegerField('атака', blank=True, null=True)
    defence = models.IntegerField('защита', blank=True, null=True)
    stamina = models.IntegerField('выносливость', blank=True, null=True)

    def __str__(self):
        return self.pokemon.title_ru
