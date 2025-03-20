# KinoApp
Kino App für WPF Agile Webanwendung Python

Um die benötigten Bibliotheken zu verwenden:
- cd Cinema
- pip install -r requirements.txt

zum Starten der venv:
- cd Cinema/cinema_project
- .\venv\Scripts\Activate

To migrate:
- Navigiere zum Ordner cinema_project (cd cinema_project)
- python manage.py makemigrations
python manage.py migrate

anschließend Server starten:
- Navigiere zum Ordner cinema_project (cd cinema_project)
- python manage.py runserver

Anschließend URL öffnen:
http://127.0.0.1:8000/



# requirements.txt:
- cd cinema_project
- .\venv\Scripts\Activate
- pip freeze > requirements.txt
