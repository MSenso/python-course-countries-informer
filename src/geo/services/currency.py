from typing import Optional

from geo.clients.shemas import CurrencyRatesDTO
from geo.clients.currency import CurrencyClient
from geo.models import CurrencyRates


class CurrencyService:
    """
    Сервис для работы с данными о валюте.
    """

    def get_currency(self, base: str = "rub") -> Optional[dict]:
        """
        Получение курса валют по базовой валюте.

        :param base: Название базовой валюты
        :return:
        """

        if data := CurrencyClient().get_currency(f"{base}"):
            return data

        return None

    def build_model(self, currency: CurrencyRatesDTO) -> CurrencyRates:
        """
        Формирование объекта модели валюты.

        :param CurrencyRatesDTO currency: Данные о валюте.
        :return:
        """

        return CurrencyRates(
            base=currency.base,
            date=currency.date,
            rates=currency.rates
        )
