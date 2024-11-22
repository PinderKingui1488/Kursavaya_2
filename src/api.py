import requests


class HeadHunterAPI:
    """
    Класс, наследующийся от абстрактного класса, для работы с платформой hh.ru.
    """

    def __init__(self, companies):
        self.companies = companies
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, companies=None):  # companies добавлен как параметр по умолчанию
        """Получает вакансии для указанных компаний."""
        params = {"employer_id": companies or self.companies}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Проверка статуса ответа
            data = response.json()
            if data and "items" in data:
                return data["items"]
            else:
                print("API вернул неожиданный ответ")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
            return []
