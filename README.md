# Twitter semantic analysis

Twitter semantic analysis - это flask-приложение, которое собирает твиты по определенному хэштегу и анализирует их тональность.
Пользователь вводит название хэштега и получает в ответ от 0 до 1, где 0 - негативное отношение, а 1 - позитивное.

## Установка

1. Клонируйте репозиторий https://github.com/Cercosa/Twitter_semantic_analysis
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Создайте в `settings.py` переменные:
```
API_key = 
API_secret_key = 
```
6. Создайте файл `config.py`
7. Создайте в `config.py` переменные:
```
SECRET_KEY = 
SENTENCE_LENGTH = 26 
NUM = 100000
```

## Создание и обучение модели
Обучение проводилось по https://habr.com/company/mailru/blog/417767/
Данные для обучения взяты из датасета Юлии Рубцовой http://study.mokoron.com/

Выполните `word2vec_model.py`
Затем выполните `sentiment_analysis.py`

## Создание базы данных твитов
Выполните `create_bd.py`

## Запуск
Выполните `webapp.py`
Перейдите по локальному адресу
