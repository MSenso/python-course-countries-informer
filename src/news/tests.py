from datetime import datetime
from typing import List

from django.urls import reverse
from rest_framework.test import APITestCase
from geo.models import Country
from news.models import News


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
    def create_news(country: Country) -> List[News]:
        """
        Инициализация данных о новостях.
        :return:
        """
        return [
            News.objects.create(
                country=country,
                source="BBC",
                author="author1",
                title="some news",
                description="",
                url="example.com",
                published_at=datetime.now().astimezone(),
            ),
            News.objects.create(
                country=country,
                source="Google",
                author="author2",
                title="another news",
                description="smth there",
                url="www.example.com",
                published_at=datetime.now().astimezone(),
            ),
        ]


class NewsTestCase(APITestCase):
    """
    Класс тестов для информации о новостях.
    """

    def setUp(self) -> None:
        """
        Инициализация данных.
        :return:
        """
        self.country = Utils.create_country()
        self.news = Utils.create_news(self.country)

    def test_get_news(self) -> None:
        """
        Тест получения новостей.
        :return:
        """
        response = self.client.get(reverse("news", kwargs={"alpha2code": "ax"}))
        data = response.json()
        self.assertEqual(len(data), 2)
        for i in range(len(data)):
            self.assertEqual(data[i]["country"]["name"], self.news[i].country.name)
            self.assertEqual(data[i]["source"], self.news[i].source)
            self.assertEqual(data[i]["author"], self.news[i].author)
            self.assertEqual(data[i]["title"], self.news[i].title)
            self.assertEqual(data[i]["description"], self.news[i].description)
            self.assertEqual(data[i]["url"], self.news[i].url)
