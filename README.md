## Project features
* Search for employees or documents
* Clean Architecture
* Administators can update information
* Users can request admin rights
## How to run
Set environment variables in `.env`
```python
#.env
BOT_TOKEN=

POSTGRES_HOST=searchbot_db
POSTGRES_PORT=5432
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

HEAD_ADMIN_TG_ID=
```
### Dev
* Run `docker compose up -d` or `make app` in the project directory
* Now you can run `docker compose restart searchbot ` to restart bot and apply your code changes
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

