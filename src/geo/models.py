"""Сущности для основной БД."""
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models

from base.models import TimeStampMixin


class Country(TimeStampMixin):
    """Модель страны"""

    name = models.CharField(max_length=255, verbose_name="Название страны")
    alpha2code = models.CharField(
        max_length=2,
        verbose_name="ISO Alpha2",
        unique=True,
    )
    alpha3code = models.CharField(
        max_length=3,
        verbose_name="ISO Alpha3",
    )
    capital = models.CharField(max_length=50, verbose_name="Столица")
    region = models.CharField(
        max_length=50,
        verbose_name="Регион",
    )
    subregion = models.CharField(
        max_length=50,
        verbose_name="Субрегион",
    )
    population = models.IntegerField(
        verbose_name="Население",
    )
    latitude = models.FloatField(
        verbose_name="Широта",
    )
    longitude = models.FloatField(
        verbose_name="Долгота",
    )
    demonym = models.CharField(
        max_length=50, verbose_name="Демоним", help_text="Название жителей"
    )
    area = models.FloatField(
        verbose_name="Площадь",
    )
    numeric_code = models.CharField(
        validators=[MinLengthValidator(limit_value=3)],
        max_length=3,
        verbose_name="Трёхзначный код страны",
        help_text="ISO 3166-1 numeric",
    )
    flag = models.CharField(
        max_length=255,
        verbose_name="Флаг",
    )
    currencies = ArrayField(
        models.CharField(max_length=3),
        verbose_name="Валюты",
    )
    languages = ArrayField(
        models.CharField(max_length=20),
        verbose_name="Языки",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ["name"]


class City(TimeStampMixin):
    """Модель города"""

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="country",
        verbose_name="Страна",
    )
    name = models.CharField(max_length=50, verbose_name="Название города")
    region = models.CharField(max_length=50, verbose_name="Регион", blank=True)
    latitude = models.FloatField(
        verbose_name="Широта",
    )
    longitude = models.FloatField(
        verbose_name="Долгота",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name"]


class Weather(TimeStampMixin):
    """Модель погоды"""

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="city",
        verbose_name="Город",
    )
    temp = models.FloatField(verbose_name="Температура")
    pressure = models.IntegerField(verbose_name="Давление")
    humidity = models.IntegerField(verbose_name="Влажность")
    wind_speed = models.FloatField(verbose_name="Скорость ветра")
    description = models.CharField(verbose_name="Описание", max_length=255)
    visibility = models.IntegerField(verbose_name="Видимость")
    dt = models.DateTimeField(verbose_name="Время")
    timezone = models.IntegerField(verbose_name="Часовой пояс")

    def __str__(self) -> str:
        return f"{self.city=} {self.temp=} {self.pressure=} {self.dt=}"

    class Meta:
        verbose_name = "Погода"
        verbose_name_plural = "Погода"


class Currency(TimeStampMixin):
    """Модель валюты"""

    base = models.CharField(verbose_name="Название валюты", max_length=255)
    date = models.DateTimeField(verbose_name="Дата запроса")

    def __str__(self) -> str:
        return f"{self.base=} {self.date=}"

    class Meta:
        verbose_name = "Валюта"


class CurrencyRates(TimeStampMixin):
    """Модель курса валют"""

    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="currency",
        verbose_name="Базовая валюта",
    )
    currency_name = models.CharField(
        verbose_name="Валюта для вычисления курса", max_length=255
    )
    rate = models.FloatField(verbose_name="Курс валюты")

    def __str__(self) -> str:
        return f"{self.currency=} {self.currency_name=} {self.rate=}"
