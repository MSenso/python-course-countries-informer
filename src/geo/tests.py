from datetime import datetime
from typing import List

from django.urls import reverse
from rest_framework.test import APITestCase
from geo.models import City, Country, Currency, CurrencyRates, Weather


class Utils:
    """
    Класс с функциями для создания тестовых данных.
    """

    @staticmethod
    def create_country() -> Country:
        """
        Инициализация данных о стране.
        :return:
        """
        return Country.objects.create(
            name="Aland",
            alpha2code="ax",
            alpha3code="ala",
            capital="Mariehamn",
            region="Europe",
            subregion="Northern Europe",
            population=10000,
            latitude=100,
            longitude=20,
            demonym="Åländare",
            area=10000,
            numeric_code=1,
            flag="flag",
            currencies=[],
            languages=[],
        )

    @staticmethod
    def create_city(country: Country) -> City:
        """
        Инициализация данных о городе.
        :return:
        """
        return City.objects.create(
            country=country,
            name="Mariehamn",
            region="Europe",
            latitude=100,
            longitude=21,
        )

    @staticmethod
    def create_weather(city: City) -> Weather:
        """
        Инициализация данных о погоде.
        :return:
        """
        return Weather.objects.create(
            city=city,
            temp=13.92,
            pressure=1023,
            humidity=54,
            wind_speed=6,
            description="rain",
            visibility=1000,
            dt=datetime.now().astimezone(),
            timezone=3,
        )

    @staticmethod
    def create_currency() -> Currency:
        """
        Инициализация данных о валюте.
        :return:
        """
        return Currency.objects.create(base="rub", date=datetime.now().astimezone())

    @staticmethod
    def create_currency_rates(currency: Currency) -> List[CurrencyRates]:
        """
        Инициализация данных о валютном курсе.
        :return:
        """
        return [
            CurrencyRates.objects.create(
                currency=currency, currency_name="usd", rate=70.0
            ),
            CurrencyRates.objects.create(
                currency=currency, currency_name="eur", rate=80.0
            ),
        ]


class CountryTest(APITestCase):
    """
    Класс тестов для информации о странах.
    """

    def setUp(self) -> None:
        """
        Инициализация данных.
        :return:
        """
        self.country = Utils.create_country()

    def test_get_countries(self) -> None:
        """
        Тест получения списка всех стран.
        :return:
        """
        response = self.client.get(reverse("countries"), {"codes": "ax"})
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.country.name)

    def test_get_country(self) -> None:
        """
        Тест получения страны.
        :return:
        """
        response = self.client.get(reverse("country", kwargs={"name": "Aland"}))
        data = response.json()[0]
        self.assertEqual(data["name"], self.country.name)


class CityTest(APITestCase):
    """
    Класс тестов для информации о городах.
    """

    def setUp(self) -> None:
        """
        Инициализация данных.
        :return:
        """
        self.country = Utils.create_country()
        self.city = Utils.create_city(self.country)

    def test_get_cities(self) -> None:
        """
        Тест получения списка городов.
        :return:
        """
        response = self.client.get(reverse("cities"), {"codes": "ax,mariehamn"})
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.city.name)
        self.assertEqual(data[0]["country"]["name"], self.city.country.name)

    def test_get_city(self) -> None:
        """
        Тест получения одного города.
        :return:
        """
        response = self.client.get(reverse("city", kwargs={"name": "Mariehamn"}))
        data = response.json()
        self.assertEqual(data[0]["name"], self.city.name)


class WeatherTest(APITestCase):
    """
    Класс тестов для информации о погоде.
    """

    def setUp(self) -> None:
        """
        Инициализация данных.
        :return:
        """
        self.country = Utils.create_country()
        self.city = Utils.create_city(self.country)
        self.weather = Utils.create_weather(self.city)

    def test_get_weather(self) -> None:
        """
        Тест получения погоды.
        :return:
        """
        response = self.client.get(
            reverse("weather", kwargs={"alpha2code": "ax", "city": "Mariehamn"})
        )
        item = response.json()
        self.assertEqual(item["temp"], self.weather.temp)
        self.assertEqual(item["pressure"], self.weather.pressure)
        self.assertEqual(item["humidity"], self.weather.humidity)
        self.assertEqual(item["wind_speed"], self.weather.wind_speed)
        self.assertEqual(item["description"], self.weather.description)
        self.assertEqual(item["visibility"], self.weather.visibility)
        self.assertEqual(item["timezone"], self.weather.timezone)


class CurrencyTest(APITestCase):
    """
    Класс тестов для информации о валюте.
    """

    def setUp(self) -> None:
        """
        Инициализация данных.
        :return:
        """
        self.currency = Utils.create_currency()
        self.currency_rates = Utils.create_currency_rates(self.currency)

    def test_get_currency(self) -> None:
        """
        Тест получения валютного курса.
        :return:
        """
        data = self.client.get(reverse("currency", kwargs={"base": "rub"})).json()
        self.assertEqual(len(data), 2)
        for i in range(len(data)):
            self.assertEqual(
                data[i]["currency_name"], self.currency_rates[i].currency_name
            )
            self.assertEqual(data[i]["rate"], self.currency_rates[i].rate)
