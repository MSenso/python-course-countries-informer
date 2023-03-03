from django.db.models import Q, QuerySet
from geo.clients.currency import CurrencyClient
from geo.models import CurrencyRates
from geo.models import Currency


class CurrencyService:
    """
    Сервис для работы с данными о валюте.
    """

    def get_currency(self, base: str = "rub") -> QuerySet[CurrencyRates]:
        """
        Получение курса валют по базовой валюте.

        :param base: Название базовой валюты
        :return:
        """

        currency_rates = CurrencyRates.objects.filter(Q(currency__base__contains=base))
        if not currency_rates:  # В БД еще нет курсов валют для искомой валюты
            if currency_data := CurrencyClient().get_currency(base):
                currency = self.save_currency(currency_data.base, currency_data.date)
                self.save_rates(currency, currency_data.rates)
                currency_rates = CurrencyRates.objects.filter(
                    Q(currency__base__contains=currency.base)
                )
        return currency_rates

    def save_rates(self, currency: Currency, rates: dict) -> None:
        CurrencyRates.objects.bulk_create(
            [self.build_model(currency, name, rate) for name, rate in rates.items()],
            batch_size=1000,
        )

    def save_currency(self, base: str, date: str) -> Currency:
        return Currency.objects.create(
            base=base,
            date=date,
        )

    def build_model(self, currency: Currency, name: str, rate: float) -> CurrencyRates:
        """
        Формирование объекта модели валюты.

        :param CurrencyRatesDTO currency: Данные о валюте.
        :return:
        """

        return CurrencyRates(
            currency=currency,
            currency_name=name,
            rate=rate,
        )
