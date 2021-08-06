# Webserver
Webserver for Fedota

## Overview
Webserver has the following responsibilities: 
- Interface for problem setter and data organizations
- Manages database and stores uploaded files at appropriate locations
- Spawns FL infrastructure for a FL problem and tracks the status of round for FL problems

## Workflow
- Problem setter uses the Webserver to create the FL problem providing with description, data format, initial files required, client docker image link, etc. 
- For storing uploaded files and files generated during a FL round, a common file storage is used with appropriate directory partitions and permissions to avoid inconsistencies as shown in [fedota-infra](https://github.com/fedota/fedota-infra#shared-file-storage-structure)
- With uploaded files placed at the appropriate location, the Webserver creates the FL, Coordinator and Selectors, for the problem and notes their addresses. The Coordinator and Selectors for a FL problem run in isolated namespaces.
- Data organization wishing to contribute in the training of the model with their local data use the instructions provided to run the client docker image with required arguments and makes a connection request to the respective selector. Data organizations should coordinate among themselves on when to run clients to ensure goal count is reached.
- Coordinator for a FL problem sends updates about the round to the Webserver which notes the changes.

### Setup
- Install dependencies: `pip install -r requirements.txt`
- Fedota migrations: `python manage.py makemigrations fedota`
- Migrate: `python manage.py migrate`
- Start webserver: `python manage.py runserver`
- Superuser : `python manage.py createsuperuser`

When running locally the selector and coordinator can share the /data directory for the model and checkpoint files as shown in the last section of [fedota-infra](https://github.com/fedota/fedota-infra) repo. Otherwise deploy the nfs-service and change the mount for the k8s/fl-pv.yaml as shown in the NFS section of fedota-infra repo.

### Themes
Default themes can be added using:
- `python manage.py loaddata admin_interface_theme_django.json`
- `python manage.py loaddata admin_interface_theme_bootstrap.json`
- `python manage.py loaddata admin_interface_theme_uswds.json`
- `python manage.py loaddata admin_interface_theme_foundation.json`

### Contribute
Fix code style issues before pushing:
`pre-commit run --all-files`

### TODO
- Add code to create the client docker image passing the selector address as a argument for the data holders to download