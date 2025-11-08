<div align="center">
  <h1>i.subpolare.ru</h1> 
</div>

This is the code base of [vas3k's simple and beautiful script](https://github.com/vas3k/i.vas3k.ru) for picture uploading. I just adapted it for [my blog](https://github.com/subpolare/subpolare.blog), add Docker and use [bjoern](https://github.com/jonashaag/bjoern) as a lightweight, high-performance WSGI server to run Flask app.


Does many handy things using a bit of nginx X-Accel-Redirect magic. Can resize pictures on the go and distribute the final result through nginx. Here is some examples how it works:

* http://i.subpolare.ru/image.jpg — canonical image URL which returns an image resized to an universal width (see COMMON_IMAGE_LENGTH in settings);
* http://i.subpolare.ru/full/image.jpg — original image file;
* http://i.subpolare.ru/500/image.jpg — resized to 500px by the longest side (min = 50, max = 20000);
* http://i.subpolare.ru/width/500/image.jpg — resized to 500px by the width (for convenient tiling or background usage);
* http://i.subpolare.ru/square/500/image.jpg — cropped to the square in the center;

## ⚙️ Tech details

Written on Flask. Uses Pillow for image processing and PostgreSQL for statistics. Almost all logic sits in `app.py`. Also see `settings.py` before you go. Images can be uploaded through a simple web-interface (sits on the root) or using any script. Works both with multipart-form-data files and raw bytes uploading.

## 🌊 How to build

There is a simple way to build it using Docker. 

1. Copy `.env.example` to `.env` and adjust secrets.
2. Start the stack with `docker compose up --build -d`.
3. Open http://127.0.0.1:8023 and sign in with the secret code from your `.env` file.

If database doesn't exist, run: 

```
docker exec -it isubpolareru_postgres psql -U subpolare -d i_subpolare_ru -c \
"create table if not exists public.images (
  id bigserial primary key,
  image varchar(128),
  file  varchar(255),
  created_at timestamptz not null default now()
);
alter table public.images owner to subpolare;"
```

Uploaded media, logs, and the PostgreSQL data directory stay on the host via bind mounts and the named volume declared in `docker-compose.yml`.

But if you want the whole world to enjoy the picture, you need something else: HTTPS and `nginx`. 

```
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d i.subpolare.ru
```

Than you need to change [nginx configure](https://github.com/subpolare/i.subpolare.ru/blob/master/etc/nginx/i.subpolare.ru.conf) and run: 

```
cp etc/nginx/i.subpolare.ru.conf /etc/nginx/sites-available/i.subpolare.ru.conf
sudo ln -s /etc/nginx/sites-available/i.subpolare.ru.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```