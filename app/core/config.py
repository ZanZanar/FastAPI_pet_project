import os
from dotenv import load_dotenv

# TODO: добавить пояснения и документации
DEFAULT_DB_URL = "postgresql+psycopg://user:password@localhost:5432/notes_db"
DEFAULT_SECRET_KEY = "y0jzdiJ22BvKOf5"

class AppSettings:

    def __init__(self):
        load_dotenv()

        self.DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_DB_URL)
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
        env = os.getenv("ENV", "development")
        env = env.lower()
        if env not in {"development", "production", "test"}:
            raise ValueError("ENV должен быть одним из: 'development', 'production', 'test'")
        self.ENV: str = env
        self.DEBUG: bool = (self.ENV == "development")
        self.IS_SQLITE: bool = self.DATABASE_URL.strip().lower().startswith("sqlite")    
    
        def get_int_env(var_name: str, default: int) -> int:
            value = os.getenv(var_name)
            # Возвращаем int(value), если value не None и не пустая строка, 
            # иначе возвращаем default
            if value is None or value == "":
                return default
            
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"Неверное значение '{value}' для переменной '{var_name}'.")
        
        self.DB_POOL_SIZE: int = get_int_env("DB_POOL_SIZE", 5)
        self.DB_MAX_OVERFLOW: int = get_int_env("DB_MAX_OVERFLOW", 10)
        self.DB_POOL_TIMEOUT: int = get_int_env("DB_POOL_TIMEOUT", 30)
    
    def _check_production_safety(self):
        if self.ENV == "production":
            errors = []
            
            if self.IS_SQLITE:
                errors.append("В production нельзя использовать SQLite. Укажите PostgreSQL URL")
            
            if self.DATABASE_URL == DEFAULT_DB_URL:
                errors.append("DATABASE_URL имеет значение по умолчанию (локальное/тестовое).")
                
            if self.SECRET_KEY == DEFAULT_SECRET_KEY:
                errors.append("SECRET_KEY имеет значение по умолчанию ('y0jzdiJ22BvKOf5').")
                
            if not (16 <= len(self.SECRET_KEY) <= 32):
                errors.append("SECRET_KEY должен быть длиной от 16 до 32 символов.")

            if errors:
                error_message = (
                    "\n\n🚨 ОШИБКА БЕЗОПАСНОСТИ: ЗАПУСК ПРОДАКШЕНА НА ДЕФОЛТАХ 🚨\n\n"
                    "Окружение установлено как 'production', но обнаружены небезопасные значения:\n"
                    f"- {os.linesep.join(errors)}\n\n"
                    "Пожалуйста, установите уникальные значения для DATABASE_URL и SECRET_KEY "
                    "в вашем файле .env.\n"
                )
                
                # Вызываем исключение, чтобы остановить инициализацию приложения
                raise ValueError(error_message)
    
settings = AppSettings()
settings._check_production_safety()