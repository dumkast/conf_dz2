Проект visual

https://github.com/dumkast/conf_dz2

Задание:

Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя.
Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление Mermaid. Визуализатор должен выводить результат на экран в виде графического изображения графа.
Построить граф зависимостей для коммитов, в узлах которого содержатся номера коммитов в хронологическом порядке. Граф необходимо строить только для тех коммитов, где фигурирует файл с заданным именем.

Ключами командной строки задаются:

• Путь к программе для визуализации графов.

• Путь к анализируемому репозиторию.

• Файл с заданным именем в репозитории.

Все функции визуализатора зависимостей должны быть покрыты тестами.


Используемые библиотеки:

![image](https://github.com/user-attachments/assets/62bc6c05-5b8e-4e23-be99-8fd1b4504c60)


1) import os: Импортирует модуль os, который предоставляет функции для взаимодействия с операционной системой. Он позволяет работать с файлами и каталогами (создавать, удалять, переименовывать, считывать информацию о них), управлять процессами, получать информацию о среде выполнения и многое другое. Примеры использования: os.path.exists(), os.mkdir(), os.listdir(), os.environ.

2) import subprocess: Этот модуль позволяет запускать внешние команды и программы из вашего Python-скрипта. Это полезно, когда вам нужно выполнить задачу, для которой нет готовой библиотеки на Python, или когда вы хотите интегрировать код Python с другими инструментами командной строки. Он предоставляет функции для запуска процессов, управления их вводом/выводом и получения результатов. Ключевые функции: subprocess.run(), subprocess.Popen().

3) import argparse: Библиотека Python, предназначенная для парсинга аргументов командной строки. Она позволяет разработчикам определять, какие аргументы программа принимает, а также автоматически генерировать справку и сообщения об ошибках.

4) import tempfile: Предоставляет функции для создания временных файлов и каталогов. Эти временные объекты обычно используются для хранения данных, которые не нужно сохранять после завершения программы.

5) import webbrowser: Позволяет открывать веб-страницы в браузере по умолчанию. Она предоставляет простой интерфейс для взаимодействия с браузерами и может использоваться для автоматизации открытия URL.

Содержимое некоторых файлов:

1) зависмости коммитов.png

![зависимости](https://github.com/user-attachments/assets/f74000ae-7261-45c6-a561-0859fe28170c)


2) graph.png (после выполнения программы)

![graph](https://github.com/user-attachments/assets/955e9cb9-af10-4050-8fdf-d6c48fe03910)



Запуск программы через командную строку:

![image](https://github.com/user-attachments/assets/cdbad91f-bfbe-4f28-b144-897560b7f084)


Результаты тестирования:

![image](https://github.com/user-attachments/assets/7eb1bb3e-c49d-44d4-b04f-7e59c6665b73)

