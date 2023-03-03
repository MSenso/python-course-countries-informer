"""Представления Django"""

from django.core.cache import caches
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from app.settings import CACHE_NEWS
from news.serializers import NewsSerializer
from news.services.news import NewsService


@api_view(["GET"])
def get_news(request: Request, alpha2code: str) -> JsonResponse:
    """
    Получение новостей для указанной страны.
    :param Request request: Объект запроса
    :param str alpha2code: ISO Alpha2 код страны
    :return:
    """

    cache_key = f"{alpha2code}_news"
    data = caches[CACHE_NEWS].get(cache_key)
    if not data:
        if data := NewsService().get_news(alpha2code):
            caches[CACHE_NEWS].set(cache_key, data)

    if data:
        serializer = NewsSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)

    raise NotFound
