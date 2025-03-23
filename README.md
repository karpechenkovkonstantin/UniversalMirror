# Universal Mirror

## Описание проекта

Этот проект — простое веб-приложение, которое можно использовать для автоматической синхронизации файлов из внешнего интернета и доступа к ним через локальную сеть.

## Функции

- **Автоматическая загрузка файлов**: Приложение может загружать файлы с указанных URL-адресов и сохранять их на вашем сервере создавая ссылки для прямой доступности.
- **Планировщик задач**: Приложение поддерживает настройку синхронизации по CRON, чтобы файлы всегда были актуальны.
- **Доступ по внутренним ссылкам**: Вы можете легко получать доступ к загруженным файлам через специальный URL. 

## Установка

Чтобы установить и запустить приложение, выполните следующие шаги:

1. **Клонируйте репозиторий**:
   ```bash
   git clone <URL репозитория>
   cd <название папки>
   ```

2. **Установите необходимые зависимости**:
   Убедитесь, что у вас установлен Python. Затем выполните:
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте конфигурацию**:
   Создайте файл `config.ini` на основе примера `config_example.ini` и заполните его нужными настройками.

4. **Создайте файл со ссылками**:
   Создайте файл `links.yaml` на основе примера `links_example.yaml` и укажите URL-адреса файлов, которые вы хотите загрузить.

## Запуск приложения

Для запуска приложения выполните команду:

```bash
python app.py
```

После этого приложение будет доступно по адресу `http://localhost:3000`.

## Использование

1. **Синхронизация файлов**: При первом запуске приложение автоматически загрузит файлы из указанных URL. Вы можете также настроить автоматическую синхронизацию по расписанию.
  
2. **Доступ к файлам**: Чтобы получить доступ к загруженным файлам, откройте браузер и перейдите по адресу `http://localhost:3000/links/<путь к файлу>`. Например, если файл сохранен в папке `documents`, используйте `http://localhost:3000/links/documents/имя_файла`.

## Логирование

Приложение ведет лог всех действий и ошибок, включая IP-адреса подключений и запрашиваемые файлы

## Поддержка

Если у вас есть вопросы или проблемы с приложением, не стесняйтесь обращаться за помощью. Вы можете создать новый issue-запрос в репозитории или написать мне напрямую.

## Лицензия

Этот проект под лицензией MIT. Вы можете свободно использовать и изменять код, но не забудьте указать авторство.