# Fampay-task
**YOUTUBE VIDEO FETCHER**

**DRF_TASK** is a Django REST application which continuously fetches latest videos every 10 seconds sorted in reverse chronological order of their publishing date-time from *YouTube* for a given search query in a paginated response.

---
## **Technologies**

* [DRF] 3.12.4 (www.django-rest-framework.org/): A powerful and flexible toolkit for building Rest APIs with [Django](https://www.djangoproject.com/)
* Database used: [SQLite](https://www.sqlite.org/index.html) (for development)


## **Local Setup**

* Clone the repository

  * Using HTTPS

    ```sh
    git clone https://github.com/abhipachorkar296/DRF_task.git
    ```
  
  * Using SSH

    ```sh
    git clone git@github.com:abhipachorkar296/DRF_task.git
    ```

* Change your working directory to the the cloned folder

    ```bash
    cd path/to/DRF_task
    ```

* Download all the dependencies

    ```bash
    pip3 install -r requirements.txt
    ```
* Generate ***API KEYS*** from Google cloud console

* Make a ``basic_settings.py`` file in the project folder directory (at the project settings.py level) and put all the ***API KEYS*** in a list `API_KEY` obtained from the Google API Console, Django ***SECRET_KEY*** and ***DEBUG*** mode as below

    ```python
    DEBUG = True
    API_KEY_LIST = ["xxx", "zzz"]
    SECRET_KEY = 'django-insecure-sifi0)iyg=2340^lkkasdb!%$%udg8asda3425=#8q!7234e+75)-q7@kie9f%'
    ```

  * While putting `DEBUG = False`, remember to modify `ALLOWED_HOSTS` (for just quick reference, modify as `ALLOWED_HOSTS = ['*']`)

---
### Make sure ```Directory``` looks like

```
DRF_task
├── task
|    ├── migrations
|    ├── __init__.py
|    ├── admin.py
|    ├── apps.py
|    ├── models.py
|    ├── pagination.py
|    ├── search.py
|    ├── serializers.py
|    ├── tests.py
|    ├── urls.py
|    ├── videos_caller.py
|    └── views.py
├── DRF_task
|   ├── __init__.py
|   ├── settings.py
|   ├── asgi.py
|   ├── basic_settings.py
|   ├── wsgi.py
|   └── urls.py
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```
* Migrate to the database

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

* Run server

    ```sh
    python manage.py runserver
    ```


---

## **API Reference**
> ### **GET** the stored video data in a paginated response sorted in descending order of published datetime.

<!-- * HTTP Method - **GET** -->

* Endpoint - **`/task/get_videos`**

* Headers  
    Content-Type: application/json

* Success Response  
  * **Code** - `200`

### Sample Response:

```json
{
    "count": 22,
    "next": null,
    "previous": "http://127.0.0.1:8000/task/get_videos?p=2",
    "results": [
        {
            "id": "eUy8TIgEaHs",
            "title": "A NEW MOBILE FOOTBALL GAME | VIVE LE FOOTBALL | FIRST IMPRESSIONS 🔥",
            "description": "Join this channel to get access to perks: https://www.youtube.com/channel/UClxPe0aepOMWVO8Y8ywjhtw/join Pes Android / iOS ...",
            "urls": "https://i.ytimg.com/vi/eUy8TIgEaHs/default.jpg",
            "created_datetime": "2021-08-25T18:00:10Z"
        },
        {
            "id": "2jmTYmtgxUw",
            "title": "Seattle Seahawks &amp; San Francisco 49ers 2021 Fantasy Football Outlook | Fantasy Focus Live!",
            "description": "Fantasy Focus will be LIVE today from 11am-12pm ET. Matthew Berry, Field Yates, and Daniel Dopp will focus on the Seattle Seahawks and San Francisco ...",
            "urls": "https://i.ytimg.com/vi/2jmTYmtgxUw/default.jpg",
            "created_datetime": "2021-08-25T16:09:05Z"
        }
    ]
}
```
---
> ### **GET** the stored video data with respect to search query in a paginated response sorted in descending order of published datetime.

<!-- * HTTP Method - **GET** -->

* Endpoint - **`search/{query}`**

* Headers  
    Content-Type: application/json

* Success Response  
  * **Code** - `200`



### Sample Response:

```json
[
    {
        "id": "X0gHJElGV9s",
        "title": "Washington Football Team Finally Replaced Trent Williams 😳🔥 | 6”5 Beast",
        "description": "Thanks for all the support don't forget to subscribe for the best Washington Football Content Dontae To My Channel here ...",
        "urls": "https://i.ytimg.com/vi/X0gHJElGV9s/default.jpg",
        "created_datetime": "2021-08-25T18:08:33Z"
    },
    {
        "id": "SiuOfiMQDqc",
        "title": "The PLZ Football Show  - Thu 26th August",
        "description": "SUBSCRIBE ▶️ bit.ly/3kWKeak MORE FROM PLZ SOCCER ON YOUTUBE: ▶️ PLZ FOOTBALL NEWS: https://www.youtube.com/playlist?list... ▶️ PLZ ...",
        "urls": "https://i.ytimg.com/vi/SiuOfiMQDqc/default.jpg",
        "created_datetime": "2021-08-26T16:00:57Z"
    }
]
```

