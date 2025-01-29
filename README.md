«Фудграм» — сайт, на котором пользователи публикуют свои рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Зарегистрированным пользователям также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Запуск проекта

1. Клонируйте репозиторий
```bash
git clone https://github.com/badpascal/foodgram-st.git
```

2. Перейдите в директорию `infra` и создайте файл .env на примере .env.example
```bash
cd foodgram-st/infra
```
```bash
touch .env
```

3. В директории `infra` Запустите проект:
```bash
docker-compose up 
```

4. Выполните миграции:
```bash
docker-compose exec backend python manage.py migrate
```

5. Заполните базу ингредиентами и тестовыми данными:
```bash
docker-compose exec backend python manage.py load_ingredients
```

## Адреса

- Веб-интерфейс: [Localhost](http://localhost/)
- API документация: [Localhost docs](http://localhost/api/docs/)
- Админ-панель: [Localhost admin](http://localhost/admin/)
