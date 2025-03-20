# KinoApp
Kino App für WPF Agile Webanwendung Python

## requirements.txt installieren:
- pip install -r requirements.txt

## Virtuelle Umgebung erstellen:
- python -m venv venv

### zum Starten der venv:
- .\venv\Scripts\Activate

## anschließend Server starten:
- python manage.py runserver

## Anschließend URL öffnen:
http://127.0.0.1:8000/




# requirements.txt erstellen:
- .\venv\Scripts\Activate
- pip freeze > requirements.txt

# Nach Änderungen an Modellen:
- python manage.py makemigrations
python manage.py migrate