# Digital Portfolio

Digital Portfolio - это веб-сервис для организации, хранения, публикации проектов конкретного человека (студента).

## Основные функции

- Каталог пользователей и проектов
- Регистрация и заполнение информации о пользователе
- Добавление информации о выполненных проектах
- Система оценок проектов
- Возможность комментирования проектов
- Подписка на профили других пользователей
- Возможность прикреплять сертификаты в профиле пользователя

## Технические детали

Проект использует следующие технологии:

- FastAPI
- ORM peewee (peewee_async)
- PostgreSQL

### Запуск проекта

1. Установите все необходимые зависимости.
2. Создайте базу данных PostgreSQL.
3. Настройте переменные окружения в файле `.env`.
4. Запустите сервер командой `uvicorn main:app --reload`.

## Гайдлайн по разработке

1. **Клонирование проекта**: Для клонирования репозитория на свой компьютер. Напиши команду `git clone <url>`
2. **Получение обновлений**: Используй команду `git pull` для получения обновлений из репозитория.
