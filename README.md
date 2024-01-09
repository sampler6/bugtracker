# Багтрекер
## App
http://127.0.0.1:8000/docs
## Пользователи
Реализована регистрация и аутентификация пользователей. При регистрации указывается роль(Менеджер, Тимлид, Разработчик или QA).

Менеджер имеет доступ к управлению пользователями, а именно:
1) Получать список всех пользователей
2) Получать конкретного пользователя по id
3) Изменять роль пользователя
4) Изменять электронную почту пользователя
## Задачи
Для задач реализованы следующие эндпоинты, доступные авторизованным пользователям:
Get:
1) Получить список задач
2) Получить задачу по номеру или по поиску части текста в описании или заголовке
Post:
1) Добавить задачу
2) Указать связь между задачами(одна является подзадачей другой)
Patch:
1) Продвинуть задачу в статусе(либо на To do, либо на Wontfix, либо просто на следующий статус) с указанием исполнительно(необязательно)
2) Изменить конкретный столбец задачи
Delete:
1) Удалить задачу(доступно только менеджеру)
## Docker
Прописан dockerfile и docker-compose.
Сборка:
Docker compose build
Docker compose up
## Тесты
Авторизация и регистрация покрыта асинхронными тестами библиотеки pytest
