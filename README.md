## Project features
* Search for employees or documents
* Clean Architecture
* Administators can update information
* Users can request admin rights
## How to run
Set environment variables .env
```
BOT_TOKEN=

POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

HEAD_ADMIN_TG_ID=
```

Run `docker compose up -d` in the project directory

## Commands
* **/start** - Start interacting with the bot
* **/info** - Informations for admins
* **/request_access** - Request admin rights
* **/search** - Search for employees and documents
* **/update_info** - Update information about employees or documents
* **/promote_user <user id>** - Promote user
* **/demote_user <user id>** - Demote user
* **/admins <user id>** - List of admins

