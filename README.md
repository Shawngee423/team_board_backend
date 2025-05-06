# team_board_backend

A backend service for TeamBoard application with MySQL database support.

## Project Structure
```
TeamBoard Backend
├───app
│   ├───config
│   ├───controller
│   ├───db
│   ├───models
│   ├───schemas
│   ├───services
│   ├───.env
├───tests

```

## Environment Configuration (.env)

Create a `.env` file in the `/` directory with the following variables:

```ini
# Application Settings
APP_NAME="Team Board API"
HOST="0.0.0.0"
PORT=23333
DEBUG=True

# Database Configuration
DATABASE_URL="mysql+pymysql://{user_name}:{password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_POOL_RECYCLE=3600

# Logging
LOG_LEVEL="DEBUG"
```