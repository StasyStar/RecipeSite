#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


"""
DB stasy ziMMer483
python -m django startproject mysite - создание проекта
python manage.py runserver - запуск сервера
python manage.py makemigrations - создание файла для миграции (создавать на каждую новую модель)
python manage.py showmigrations - показать все доступные миграции
python manage.py migrate - запуск миграций (после проверки корректности файла)
python manage.py migrate shopapp 0002 - откатывание к состоянию миграции с номером 0002
python manage.py createsuperuser - создание админа
python manage.py startapp shopapp - создание нового приложения в проекте, подключить его в главном модуле в settings
python manage.py help - просмотр доступных функций, в т.ч. кастомных
python manage.py test shopapp.tests.AddTwoNumbersTestCase - тестирование конкретного класса
python manage.py test shopapp.tests - запуск всех тестов
python manage.py dumpdata shopapp.Product - выгрузка всех данных из таблицы Product
python manage.py dumpdata shopapp > shopapp-fixtures.json - выгрузка данных в файл
python manage.py loaddata shopapp-fixtures.json - загрузка данных в БД
python manage.py makemessages -l ru - для создания файла со всеми выражениями, подлежащими переводу
python manage.py compilemessages  - после заполнения файлов для перевода, запуск команды для его применения
docker build . -t app - собираем проект из докер-файла
docker run -it app bash - запускаем оболочку контейнера
docker compose build app - сборка контейнера
docker compose up app - запуск контейнера
docker compose up --build app -d - сборка и запуск в фоновом режиме
docker compose logs app -f - просмотр логов с флагом -f в реальном времени
"""









