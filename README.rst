=====
floppy
=====

Quick start
-----------

1. Add "floppy" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ckeditor',
        'floppy',
    ]

2. Include the floppy URLconf in your project urls.py like this::

    path('floppy/', include('floppy.urls')),

3. Run ``python manage.py migrate`` to create the floppy models.

4. Visit http://127.0.0.1:8000/floppy/
