# telegram-archive-of-satellite-images

Боты для Telegram, которые следят за папкой с декодированными проходами,
выбирают дневной/ночной продукт, делают скриншот лога и публикуют результат
в каналы. Есть две точки входа:

- `testBot_fast.py` отправляет изображения + скрин лога.
- `testBot_all.py` отправляет изображения + скрин лога + загружает `.cadu`.

## Возможности

- Опрос папки с защитой от повторов через pass list.
- Выбор дневного/ночного продукта по UTC времени.
- Сжатие изображения перед отправкой.
- Скриншот лога через headless‑браузер.
- Опциональная загрузка `.cadu` (версия all).

## Требования

- Python 3.9+ (рекомендуется)
- Telegram bot token и доступ к каналу
- Telethon API credentials для загрузки `.cadu`

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Конфигурация

Создайте `config_bot.json` в корне проекта. В нем должны быть:

- `data_directory` путь до папки с проходами
- `chat_fast` / `chat_all` каналы Telegram
- `TOKEN`, `api_id`, `api_hash`
- `dawn_utc`, `sunset_utc`
- `sat_list_x` с продуктами для каждого спутника

Альтернативный конфиг `config_arch_bot.json` включен как шаблон, но он тоже
может содержать чувствительные данные. Держите реальные токены вне git.

## Формат данных

Каждый проход — это папка вида `YYYYMMDD_HHMMSS_SATELLITE`. Внутри бот ищет
продукты из `sat_list_x` и, при необходимости, файл `.cadu`.

## Запуск

```bash
python testBot_fast.py
```

или

```bash
python testBot_all.py
```

При первом запуске `pyppeteer` может скачать Chromium для скриншотов.

## Примечания

- Pass list (`pass_list_*.txt`) хранит уже обработанные папки.
- Логи пишутся в `.logs/` по умолчанию.