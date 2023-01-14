# fast-api-social-media
FastAPI Social Media 

## Как запустить проект

Скачать как архив из **GitHub** репозитория или с помощью команды ```git clone```

Установить зависимости из файла **requirements.txt** с помощью команды

```
pip install -r requirements.txt
```

В файл **config.py** необходимо занести данные о Вашей базе данных

Запустить проект командой 

```
uvicorn main:app --reload
```

Перейти по адресу [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Кроме того, можно запустить тесты
