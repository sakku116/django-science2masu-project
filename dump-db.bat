:: dump current db that used by django settings.py in this project to create backup "in local machine"
:: copy the dump file to another folder as backup

:: * dont forget to .gitignore the dump
:: django will be using mysql connection configuration from settings.py that configured with env vars

:: dont forget to activate python venv first
"venv/scripts/activate" && python manage.py dumpdata > science2masu-dbdump.json