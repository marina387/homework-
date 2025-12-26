class VisitManager:
    def __init__(self, visits):
        self.visits = visits
    
    def get_visits_from_country(self, country):
        """Возвращает визиты из указанной страны"""
        result = []
        for visit in self.visits:
            if country in list(visit.values())[0]:
                result.append(visit)
        return result


# Исходные данные
geo_logs = [
    {'visit1': ['Москва', 'Россия']},
    {'visit2': ['Дели', 'Индия']},
    {'visit3': ['Владимир', 'Россия']},
    {'visit4': ['Лиссабон', 'Португалия']},
    {'visit5': ['Париж', 'Франция']},
    {'visit6': ['Лиссабон', 'Португалия']},
    {'visit7': ['Тула', 'Россия']},
    {'visit8': ['Тула', 'Россия']},
    {'visit9': ['Курск', 'Россия']},
    {'visit10': ['Архангельск', 'Россия']}
]

# Использование
manager = VisitManager(geo_logs)
russian_visits = manager.get_visits_from_country('Россия')

print("Отфильтрованный список визитов из России:")
for visit in russian_visits:
    print(visit)
