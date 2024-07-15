## Project features
* Search for employees or documents
* Clean Architecture
* Administators can update information
* Users can request admin rights
## How to run
Set environment variables in .env for local development
```python
#.env
BOT_TOKEN=

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

HEAD_ADMIN_TG_ID=
```
Set the same variables in .env.production for deployment, except POSTGRES_HOST
```python
#.env.production
POSTGRES_HOST=searchbot_db
```
### Dev
* Run `docker compose up -d` or `make app` in the project directory
### Production
* Run `docker compose -f docker-compose.production.yml up -d` or `make prod` in the project directory

## Commands
* **/start** - Start interacting with the bot
* **/info** - Informations for admins
* **/request_access** - Request admin rights
* **/search** - Search for employees and documents
* **/update_info** - Update information about employees or documents
* **/promote_user \<user id\>** - Promote user
* **/demote_user \<user id\>** - Demote user
* **/admins** - List of admins

