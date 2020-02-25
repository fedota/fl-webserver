# fl-webserver

### Usage
- Install dependencies using `pip install -r requirements.txt`
- Migrate using `python manage.py migrate`
- Start webserver with `python manage.py runserver`

### Themes
Default themes can be added using:
- `python manage.py loaddata admin_interface_theme_django.json`
- `python manage.py loaddata admin_interface_theme_bootstrap.json`
- `python manage.py loaddata admin_interface_theme_uswds.json`
- `python manage.py loaddata admin_interface_theme_foundation.json`

### Contribute
Fix code style issues before pushing:
`pre-commit run --all-files`
