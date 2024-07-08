
# Migrating Nextcloud

## Assumptions
- You're using Podman/Docker compose to run your setup.
- You're planning to migrate from one server to another.
- You're using MySQL/MariaDB as your backend.
- You're writing your MySQL/MariaDB database to a volume ./db
- You're writing your Nextcloud folder to a volume ./nextcloud
- You're using nextcloud-apache image.

## Requirements

### ./db

- Owned by 100998:youruser
- Either completely copied, or you use a backup.(Refer to nextcloud backup docs.)
- If using a backup file then load into the database prior to starting Nextcloud.

### ./nextcloud

Make a new folder called 'nextcloud'
Copy your 'data', 'config', 'themes(optional)' to this new folder and then mount it into the instance. Nextcloud will parse this and generate the rest of the install, but you need to have the old database working for everything to workout.



## TLDR

Copy your database files to the new server.  Make sure the database is working correctly.

Copy your nextcloud folder, OR just the nextcloud/data,config,theme folders to an empty folder on the new server.  Mount that folder into Nextcloud next time you start it up.
