# street-trade-backend

## Запуск

Перед запуском сервиса необходимо установить следующие переменные окружения

#### S3_URL

- **Описание:** URL-адрес для службы хранения S3.
- **Пример:** `https://obs.ru-moscow-1.hc.sbercloud.ru`

#### S3_ACCESS_KEY

- **Описание:** Ключ доступа для подключения к службе хранения S3.
- **Пример:** `AKIAYourAccessKey`

#### S3_SECRET_ACCESS_KEY

- **Описание:** Секретный ключ доступа для подключения к службе хранения S3.
- **Пример:** `YourSecretAccessKey`

#### S3_BUCKET

- **Описание:** Имя бакета S3, где ваше приложение будет хранить данные.
- **Пример:** `my-awesome-bucket`

#### SECRET_KEY

- **Описание:** Секретный ключ, используемый для JWT в приложении.
- **Пример:** `supersecretkey123`

#### DB_URL

- **Описание:** URL для подключения к базе данных PostgreSQL.
- **Пример:** `postgresql+psycopg://{user}:{password}@{ip}/{db_name}`
- **Примечание:** Используйте соответствующий тип базы данных и данные подключения.

#### ADMIN_PASSWORD

- **Описание:** Пароль для учетной записи администратора.
- **Пример:** `admin@123`

### RTSPTOWEB_URL

- **Описание:** URL сервиса [RTSPToWeb](https://github.com/deepch/RTSPtoWeb).
- **Пример:** `http://{user}:{password}@rtsptoweb.example.com`
- **Примечание:** Если запускать в Docker, то логин и пароль `demo`

## Запуск
`docker-compose up -d --build`

Интерактивную документацию к API можно будет найти по адресу `{ip}/docs`
