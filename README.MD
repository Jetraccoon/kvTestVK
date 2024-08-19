# Документация для API и Инструкции по Запуску

## Оглавление

1. [Инструкции по запуску](#инструкции-по-запуску)
2. [API Документация](#api-документация)
   - [Получение токена авторизации](#получение-токена-авторизации)
   - [Запись данных пачками](#запись-данных-пачками)
   - [Чтение данных пачками](#чтение-данных-пачками)
3. [Ошибки и их коды](#ошибки-и-их-коды)

---

## Инструкции по запуску

### 1. Запуск с Docker Compose

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Jetraccoon/kvTestVK.git
   cd kvTestVK
   ```


2. **Создайте файл `.env` используя в качестве основы .env.example:**

   ```ini
   DATABASE_HOST - Хост БД
   DATABASE_PORT - Порт БД
   TARANTOOL_USER_NAME - Имя пользователя БД
   TARANTOOL_USER_PASSWORD- Пароль пользователя БД
   SECRET_KEY - Секретный ключ используемый при создании токена
   ALGORITHM - Алгоритм шифрования токена
   ACCESS_TOKEN_EXPIRE_MINUTES - Время жизни токена
   ```

3. **Запустите Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Это запустит ваше API и Tarantool, используя конфигурации из `docker-compose.yml`.

### 3. Миграции и начальная настройка

Если ваше пространство не существует в Tarantool, оно будет создано при первом запуске контейнера. Однако, если вам нужно вручную обновить или проверить начальные данные, вы можете использовать следующий скрипт Lua:

```lua
box.cfg{}

local users_space_name = 'users'
local kv_space_name = 'kv_store'

-- Создание пространства для пользователей
local users_space = box.space[users_space_name]
if users_space == nil then
    local users_space = box.schema.space.create(users_space_name, {
        format = {
            {name = 'user_id', type = 'unsigned'},
            {name = 'username', type = 'string'},
            {name = 'password', type = 'string'}
        }
    })

    users_space:create_index('primary', {parts = {'user_id'}})
    users_space:create_index('username', {unique = true, parts = {'username'}})

    local username = 'admin'
    local password = 'presale'
    local user_id = users_space:count() + 1
    users_space:insert{user_id, username, password}
end

-- Создание пространства для хранения ключей-значений
local kv_space = box.space[kv_space_name]
if kv_space == nil then
    local kv_space = box.schema.space.create(kv_space_name, {
        format = {
            {name = 'key', type = 'string'},
            {name = 'value', type = 'string'}
        }
    })

    kv_space:create_index('primary', {parts = {'key'}})
end
```

## API Документация

### Получение токена авторизации

- **URL:** `/api/login`
- **Метод:** `POST`
- **Тело запроса:**

  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```

- **Ответ:**

  ```json
  {
      "token": "your_generated_token"
  }
  ```

- **Ошибки:**

  - **401 Unauthorized**: Неверный логин или пароль.

### Запись данных пачками

- **URL:** `/api/write`
- **Метод:** `POST`
- **Заголовки:**

  ```http
  Authorization: Bearer your_generated_token
  Content-Type: application/json
  ```

- **Тело запроса:**

  ```json
  {
      "data": {
          "key1": "value1",
          "key2": "value2",
          "key3": 123
      }
  }
  ```

- **Ответ:**

  ```json
  {
      "status": "success"
  }
  ```

- **Ошибки:**

  - **401 Unauthorized**: Неверный токен авторизации.
  - **400 Bad Request**: Некорректный формат данных.

### Чтение данных пачками

- **URL:** `/api/read`
- **Метод:** `POST`
- **Заголовки:**

  ```http
  Authorization: Bearer your_generated_token
  Content-Type: application/json
  ```

- **Тело запроса:**

  ```json
  {
      "keys": ["key1", "key2", "key3"]
  }
  ```

- **Ответ:**

  ```json
  {
      "data": {
          "key1": "value1",
          "key2": "value2",
          "key3": 123
      }
  }
  ```

- **Ошибки:**

  - **401 Unauthorized**: Неверный токен авторизации.
  - **400 Bad Request**: Некорректный формат данных.

## Ошибки и их коды

- **401 Unauthorized**: Ошибка авторизации. Проверьте свои учетные данные и токен.
- **400 Bad Request**: Некорректный запрос. Проверьте формат данных и заголовки.
- **404 Not Found**: Запрашиваемый ресурс не найден. Проверьте корректность URL.


