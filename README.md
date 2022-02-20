# Blog Application

### The blog where you can post arcticles, search something interesting for you or share posts with your friends

___
![](preview.gif)

## Build & Run

### requirements

* docker
* .env file in root directory with following rules:

```shell
SECRET_KEY=
DEBUG=

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_HOST=db
DATABASE_PORT=5432

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

#or use default conf in settings file: 
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

```

Use **docker-compose up --build** command to run app in docker

## Description

1. Create articles wich will be edited by stuff users and posted in blog
2. Main page gives short description about each post with apropriate tags, image, date and author info
3. Use search that implement postgresql trigram engine at the back
4. Share post with anybody by emails
5. Comment any post if you have something to say
6. Sitemap and RSS feed for subscribtions
