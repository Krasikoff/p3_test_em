# p3_test_em
Тестовое задание. Описание в корне репозитория: ТЗpython_EM_июль.docx.

##  Технологии
* Django 5.2
* Python 3.12
* DRF (Django REST Framework)

## Сборка и запуск
```shell
git clone git@github.com:Krasikoff/p3_test_em.git
cd auth_n_auto
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
python manage.py migrate
python manage.py role_init
python manage.py createsuperuser
python manage.py runserver

```
## Пояснения к решению.
После запуска мы имеем админку и swagger на их стандартных url (для удобства)

* email_login - аутенфикация по email, password c выдачей jwt access токенов.
(logout не доделан, если бы использовать simplejwt, о нем и думать бы не нужно было бы. А так нужно помещать токен в блэклист и отслеживать при новом login, потом удалять истекшие по срокам. Много движений из-за неиспользования стандартных механизмов. Не успел.)
* drf-role - система разрешений основана на 
    - ролях: админ, менеджер, покупатель, продавец.
    - url-ах приложения, к примеру: products-detail, products-list
    - типах доступа: NO_ACCESS, READ, WRITE
    - правилах доступа: в админке в Access controls можно добавить правила, которые будут выполнятся. Они касаются только бизнес объектов. То же можно сделать через /api/v1/drf-role/ роутеры. Исключения: правила доступа этим роутерам и роутерам аутенфикации. Их изменить нельзя, т.к они жестко привязаны в коде. Потестить postman-ом бизнес-объект Products можно в business_app.
    
    Принцип работы проверки пермишинов в drf_role/permissions.py: 
    IsAdminOrNoAccess применен к /api/v1/drf-role/ - изменяется только программно 
    BaseRolePermission по умолчению в настройках django можно менять через админку или drf-role routers. Основная работа по анализу соответствия установленным правилам доступа пользователя к business/<какой-то url> происходит в этом пермишене. 
    пример, если завести соответствующие данные в БД через админку, drf, с постмана сделать запрос к /business/products/ результат обращения в cli будет следующий:
    ```shell
    permission_classes = [<class 'drf_role.permissions.BaseRolePermission'>]
    user = DanDm <Dan@ya.ru>
    user_role = Manager
    url_name = products-detail
    permission = NO_ACCESS
    ```
    постман покажет:
    ```shell
    403 "detail": "Authentication credentials were not provided."
    ```

    после исправления через админку или drf-role/accesses/ на access_type на 0 (READ) (необходимо быть в админке админом, через drf роль админ.)
    
    повторим запрос и увидим:
    ```shell
    {
        "data": "Product_data"
    }
    ```





    PS.  Сделано как MVP. При решении пользовался активно интернетом...
    