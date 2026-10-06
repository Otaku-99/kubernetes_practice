from fastapi import FastAPI
import redis
import os 
import psycopg
from psycopg_pool import ConnectionPool

app = FastAPI()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)


# PostgreSQL
DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER', 'appuser')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'apppassword')}@"
    f"{os.getenv('POSTGRES_HOST', 'postgres')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB', 'appdb')}"
)

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=5
)



@app.get("/")
def root():
    return {"message": "Hello from backend"}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/hello")
def hello():
    return {"message": "Hello from backend"}


@app.get("/cache/{key}")
def get_cache(key: str):

    value = redis_client.get(key)

    return {
        "key": key,
        "value": value
    }


@app.post("/cache/{key}")
def set_cache(key: str, value: str):

    redis_client.set(key, value)

    return {
        "message": "Value stored",
        "key": key,
        "value": value
    }

@app.get("/db-test")
def db_test():

    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

    return {
        "database": "connected",
        "result": result[0]
    }


@app.post("/users")
def create_user(name: str):

    with pool.connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                "INSERT INTO users (name) VALUES (%s) RETURNING id",
                (name,)
            )

            user_id = cursor.fetchone()[0]

        conn.commit()

    return {
        "id": user_id,
        "name": name
    }

@app.get("/users")
def get_users():

    with pool.connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT id, name FROM users ORDER BY id"
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in rows
    ]

@app.get("/users")
def get_users():

    with pool.connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT id, name FROM users ORDER BY id"
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in rows
    ]

@app.get("/users/{user_id}")
def get_user(user_id: int):

    with pool.connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT id, name FROM users WHERE id = %s",
                (user_id,)
            )

            row = cursor.fetchone()

    if row is None:
        return {
            "error": "User not found"
        }

    return {
        "id": row[0],
        "name": row[1]
    }


@app.get("/ready")
def ready():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")

        return {
            "status": "ready"
        }

    except Exception:
        return {
            "status": "not ready"
        }

@app.get("/ready")
def ready():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")

        return {
            "status": "ready"
        }

    except Exception:
        return {
            "status": "not ready"
        }