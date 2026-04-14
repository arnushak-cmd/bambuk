1. regex для разбора строк — `regex.py`
2. контрольный сет — `generator.py`
3. внешние данные для обогащения — `enrichment.md` + `enrichment.py`
4. компоненты частоты бронирований — `timeseries.md`

## запуск

pip install -r requirements.txt
python generator.py               
python enrichment.py --dry-run    
