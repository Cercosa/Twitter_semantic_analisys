# Twitter_semantic_analisys
Course Learn Python

Работа с данными.

Цель проекта: Написать сборщик постов и комментариев из Твиттера по товарам марки «Декатлон» и общую
лояльность к марке. Выводить статистику по группе и каждому посту на сайте. По собранным комментариям
делать sentiment analysis и выставлять общую реакцию на пост (положительная/отрицательная).
Функционал:
1. Написать сборщик постов и комментариев из Твиттера
2. Сохранять данные в БД
3. Очистить получаемые данные (удалить комментарии без контента и с слишком малым количеством
контента, комменты с видео)
4. Сделать аналитику по постам в группе за период: количество постов, количество комментариев,
количество постов с картинками, количество лайков
5. Сделать UI, который принимает ссылку на группу, программа получает данные, анализирует их и
делает отчет
6. Сделать sentiment на базе датасета Юлии Рубцовой
7. Прогонять комментарии к каждому посту через sentiment-модель и сохранять результаты в БД
8. Добавить в отчет данные по sentiment-окраске комментариев и постов
Ресурсы:
1. Пример Sentiment Analysis - https://habr.com/company/mailru/blog/417767/
2. Датасет Юлии Рубцовой http://study.mokoron.com/
Задачи:
● Написать скрипт, который выводит в консоль комментарии к указанному посту.
● Спроектировать БД для хранения списка групп, постов и комментариев.
● Доработать скрипт, чтобы он проходил по всем постам указанных группам и сохранял все комментарии
всех постов в БД. Список групп брать из БД. У постов сохраняем текст и есть ли картинка. У
комментариев сохранять текст и количество лайков.
● Сделать jupyter notebok в котором проанализируйте распределение постов по времени, распределение
комментариев по времени и т.д.
● Доработать скрипт так, чтобы он обрабатывал отсутствие интернета, исчерпанные лимиты
использования API.
● Написать скрипт, который обучает модель Word2Vec по датасету Юлии Рубцовой (см две ссылки
выше). На выходе – файл с обученной моделью.
● Написать скрипт, который проводит sentiment для комментариев в БД и сохраняет результат анализа в
БД.
● Написать приложение на Flask, которое отображает статистику по группам по дням/месяцам: сколько
постов, сколько в среднем комментариев, пост с самыми положительными/негативными
комментариями. Группу можно выбирать, отчетный период тоже (дата начала и дата окончания).
● Добавить в интерфейс возможность указывать группу и запускать для неё сбор данных и анализ
тональности.
● Добавить отображение прогресса сбора данных и анализа тональности, чтобы пользователь видел,
сколько времени ему осталось ждать до полной обработки данных.
