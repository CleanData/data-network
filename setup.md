## Steps that are needed to get this up and running

* Install django
* Install django-registration (install via pip install)
* Copy settings_local.template to settings_local.py and rewrite the sections that are in <...>
* Particulalry, make sure that you specify an email server for the user validation (I use a Gmail smtp server as a test email server)
* Change the site entry in the database through the django admin page (admin page is at <your test django server/admin>, then click Sites -> change example.com details)
* Install django-south (pip install south)

South changes the way databases are handled in django. After installing south, do the following (see [here for the full discussion](http://south.readthedocs.org/en/latest/convertinganapp.html#converting-an-app), and for a possible error):

    python manage.py syncdb
    python manage.py convert_to_south data_connections

See the README.md for basic instructions on how to use South to perform database migrations.
