from typing import Optional
from django.db.models import Q
from news.clients.news import NewsClient
from news.clients.shemas import NewsItemDTO
from geo.services.country import CountryService
from news.models import News


class NewsService:
    """
    Сервис для работы с данными о новостях.
    """

    def get_news(self, country_code: str) -> Optional[list[NewsItemDTO]]:
        """
        Получение актуальных новостей по коду страны.

        :param str country_code: ISO Alpha2 код страны
        :return:
        """
        news = News.objects.filter(Q(country__alpha2code__contains=country_code))
        if not news:  # В БД еще нет новостей по искомой стране
            if news := NewsClient().get_news(country_code):
                if not CountryService.is_country_code_in_codes(country_code):
                    CountryService().get_countries(
                        country_code
                    )  # Обновляем данные по странам, т.к., искомая страна
                    # может быть найдена после обновления данных
                    if not CountryService().is_country_code_in_codes(country_code):
                        return None
                country_code_number = CountryService().get_countries_codes()[
                    country_code
                ]
                self.save_news(country_code_number, news)
        return news  # type: ignore

    def save_news(self, country_pk: int, news: list[NewsItemDTO]) -> None:
        """
        Сохранение новостей в базе данных.

        :param country_pk: Первичный ключ страны в базе данных
        :param news: Список объектов новостей
        :return:
        """

        if news:
            News.objects.bulk_create(
                [self.build_model(news_item, country_pk) for news_item in news],
                batch_size=1000,
            )

    def build_model(self, news_item: NewsItemDTO, country_id: int) -> News:
        """
        Формирование объекта модели новости.

        :param NewsItemDTO news_item: Данные о новости
        :param int country_id: Идентификатор страны в БД
        :return:
        """

        return News(
            country_id=country_id,
            source=news_item.source,
            author=news_item.author if news_item.author else "",
            title=news_item.title,
            description=news_item.description if news_item.description else "",
            url=news_item.url if news_item.url else "",
            published_at=news_item.published_at,
        )
