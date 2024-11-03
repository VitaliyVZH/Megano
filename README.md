<h1 style="display: flex; align-items: center; justify-content: center">Интернет-магазин MEGANO</h1>
<img src="./img_for_README/Megano_1.png" alt="Картинка сайта">
<h2 style="display: flex; align-items: center; justify-content: center">
Описание проекта
</h2>
<div>
    <p>
        Megano — это интернет магазин на основе фреймворка Django.
        Фронтенд и Бэкенд в данном проекте являются отдельными приложениями и взаимодействуют между собой 
        через API используя Django Rest Framework.
    </p>
</div>


<h2 style="display: flex; align-items: center; justify-content: center">
Функциональность
</h2>

<p>На данный момент Megano предоставляет следующие возможности:</p>
<ul>
    <li>Регистрация и аутентификация пользователей</li>
    <li>Просмотр каталога товаров</li>
    <li>Фильтрация, сортировка товаров</li>
    <li>Просмотр карточки товара</li>
    <li>Добавление товара в корзину</li>
    <li>Покупка товара</li>
    <li>Добавление комментариев к товару</li>
    <li>Административная панель для управления пользователями, товарами и заказами.</li>

</ul>

<h2 style="display: flex; align-items: center; justify-content: center">
    Технологии
</h2>

<ul>
    <li>Python — язык программирования, на котором написан проект</li>
    <li>Django — фреймворк для веб-разработки на Python</li>
    <li>Django REST framework (DRF) — набор инструментов для создания веб-сервисов и API на основе фреймворка Django</li>
    <li>Poetry — инструмент для управления зависимостями и сборкой пакетов в Python</li>
    <li>Django Debug Toolbar — инструмент для отладки Django-кода</li>
    <li>Django Filter — сторонняя библиотека, которая упрощает создание фильтров для Django моделей.</li>
</ul>


<h2 style="display: flex; align-items: center; justify-content: center">
    Установка и запуск
</h2>

<h3>
    Предварительные требования
</h3>
<ul>
    <li>Python (3.8 или выше)</li>
    <li>Django (3.2.7 или выше)</li>
</ul>

<p>Для установки и запуска Megano следуйте приведенным ниже инструкциям:</p>

<ol>
    <li>
        Клонируйте репозиторий с проектом:
        <p>git clone https://github.com/VitaliyVZH/Megano.git</p>
    </li>
    <li>
        Установите приложение "frontend":
        <p>pip install python_django_diploma/diploma-frontend/dist/diploma-frontend-0.6.tar.gz</p>
    </li>
    <li>Перейдите в каталог проекта:
    <p>cd Megano</p>
</li>
    <li>Создайте и активируйте виртуальное окружение:
    <p>python -m venv venv</p>
    <p>source venv/bin/activate  # на Windows: venv\Scripts\activate</p>
</li>
    <li>Установите poetry (контроль зависимостей)
    <p>pip install poetry</p>
</li>
    <li>Установите зависимости проекта:
    <p>poetry install</p>
</li>
    <li>Перейдите в подкаталог megano:
    <p>cd megano</p>
</li>
    <li>Примените миграции базы данных:
    <p>python manage.py migrate</p>
</li>
    <li>Загрузите фикстуры для тестового просмотра сайта:
    <p>python manage.py loaddata all_data.json</p>
    В результате, БД наполнится ограниченным колличеством данных, включая профиль администратора.
</li>
    <li>Запустите проект:
    <p>python manage.py runserver</p>
</li>
</ol>

<h2 style="display: flex; align-items: center; justify-content: center">Использование</h2>

<h3>Регистрация и аутентификация пользователей</h3>
<div>
<img src="./img_for_README/register_user.png" alt="Страница регистрации пользователя">
</div>
Для регистрации перейдите на страницу http://127.0.0.1:8000/sign-up/ и заполните форму. После регистрации вы можете войти в систему, перейдя на страницу http://127.0.0.1:8000/login/.
<p>Для входа от лица администратора сайта используйте логин: admin, пароль: Lol2023!</p>

<h3>Управление товарами</h3>
<div>
<img src="./img_for_README/administrator.png" alt="Страница администратора">
</div>
<p>Для управления товарами перейдите в административную панель по адресу http://127.0.0.1:8000/admin/ и войдите, используя учетные данные суперпользователя. В разделе "Товары" вы можете добавлять, редактировать и удалять товары.</p>

<h3>Просмотр списка товаров</h3>
<div>
<img src="./img_for_README/catalog.png" alt="Каталог товаров">
</div>
<p>Для просмотра списка товаров перейдите на главную страницу проекта по адресу http://127.0.0.1:8000/. Здесь вы увидите список всех доступных товаров. Для просмотра подробной информации о товаре щелкните на его название.</p>

<h3>Просмотр карточки товара</h3>
<div>
<img src="./img_for_README/product_detail.png" alt="Карточка товара">
</div>
<p>Для просмотра карточки товара перейдите на главную страницу проекта по адресу http://127.0.0.1:8000/product/2/.</p>
<h3>Добавление товаров в корзину и просмотр содержимого корзины</h3>
<img src="./img_for_README/cart.png" alt="Корзина">
<p>Для добавления товара в корзину щелкните кнопку "Добавить в корзину" на странице товара. Для просмотра содержимого корзины перейдите на страницу http://127.0.0.1:8000/cart/.</p>

<h3>Оформление заказа</h3>
<img src="./img_for_README/orders.png" alt="Оформление заказа">
<p>Для оформления заказа перейдите на страницу корзины (http://127.0.0.1:8000/orders/num_order) и нажмите кнопку "Оформить заказ". После оформления заказа вы увидите страницу с информацией о заказе и его статусе.</p>                     

<h3>Оплата заказа</h3>
<img src="./img_for_README/payment.png" alt="Оплата заказа">
<p>Ввод реквезитов карты http://127.0.0.1:8000/payment/num_orders </p>                     
