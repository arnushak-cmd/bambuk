# bambuk take-home

take-home задание на аналитика в «Бамбук» (сервис бронирования загородных домиков).

лог на 6кк+ бронирований за 2023-2025, поля через `;`

## что тут лежит

- `regex.py` — парсинг строк лога
- `generator.py` — генерит тестовые данные
- `enrichment.py` — обогащение через nominatim и open-meteo
- `enrichment.md` — какие внешние данные подключать и зачем
- `timeseries.md` — декомпозиция частоты бронирований
- `bambuk_interview.ipynb` — всё вместе в ноутбуке

## запуск

```bash
pip install -r requirements.txt
python generator.py               # -> sample_bookings.csv
python enrichment.py --dry-run    # без реальных запросов
```
