# i.subpolare.ru 

### Old and simple script which helps me to upload, resize and insert pictures to my blog 

Does many handy things using a bit of nginx X-Accel-Redirect magic. Can resize pictures on the go and distribute the final result through nginx.

Written on Flask. Uses Pillow for image processing and PostgreSQL for statistics. Yes, the usage of postgres here is overkill, but the previous version on plain-files constantly became inconsistent and I rewrote everything.

Almost all logic sits in one file (app.py). Also see settings.py before you go. Images can be uploaded through a simple web-interface (sits on the root) or using any script. Works both with multipart-form-data files and raw bytes uploading.

Here is some examples how everything works:

* http://i.subpolare.ru/32p.jpg — canonical image URL. Returns an image resized to an universal width. See COMMON_IMAGE_LENGTH in settings;
* http://i.subpolare.ru/full/32p.jpg — original image file;
* http://i.subpolare.ru/500/32p.jpg — resized to 500px by the longest side. Min = 50, max = 20000;
* http://i.subpolare.ru/width/500/32p.jpg — resized to 500px by the width. For convenient tiling or background usage;
* http://i.subpolare.ru/square/500/32p.jpg — cropped to the square in the center;

## Run locally with Docker
1. Copy `.env.example` to `.env` and adjust secrets
2. Start the stack with `docker compose up --build`.
3. Open http://127.0.0.1:8023 and sign in with the secret code from your `.env` file.

Uploaded media, logs, and the PostgreSQL data directory stay on the host via bind mounts and the named volume declared in `docker-compose.yml`.
