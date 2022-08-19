## how to migrate database into another database
- dump the current db of django project settings 
    ```
    python manage.py dumpdata > dbdump.json
    ```
- Change the database settings to new database
- run `migrate` command to set up the new database **if the new database does not have same model (tables), as when creating new database*
    ```
    python manage.py migrate
    ```
- open django shell
    ```
    python manage.py shell
    ```

    Enter the following in the shell
    
    ```
    from django.contrib.contenttypes.models import ContentType
    
    ContentType.objects.all().delete()
    ```
- then, load the data from `dbdump.json`
    ```
    python manage.py loaddata dbdump.json
    ```
