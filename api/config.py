import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180)
DATABASE_HOST=os.getenv("DATABASE_HOST", "tarantool")
DATABASE_PORT=os.getenv("DATABASE_PORT", 3301)
DATABASE_USER=os.getenv("DATABASE_USER", "admin_user")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD", "admin_password")
