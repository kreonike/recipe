# Кулинарная книга API

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
3. pip install -r requirements.txt

## Запуск

uvicorn main:app --reload


## Документация

- [API Reference](API_DOCS.md)
- [Postman Collection](CookingAPI.postman_collection.json)
- Интерактивная документация: http://localhost:8000/docs

## Структура проекта

```
project/
├── main.py         # Основной файл приложения
├── models.py       # Модели данных
├── API_DOCS.md     # Документация API
├── README.md       # Общая документация
└── requirements.txt
```                  