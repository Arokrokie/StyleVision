This file explains the minimal steps to deploy the Django project to Microsoft Azure App Service.

1. Prepare environment variables

- In Azure Portal > your Web App > Settings > Configuration, add the following application settings:
  - `SECRET_KEY` : (your production secret)
  - `DEBUG` : `False`
  - `ALLOWED_HOSTS` : yourapp.azurewebsites.net (or comma-separated hosts)
  - `DATABASE_URL` : optional Postgres connection string if using Azure Database for PostgreSQL
- Alternatively, create a `.env` file locally for testing (see `.env.example`).

2. Configure deployment

- Add the `AZURE_WEBAPP_PUBLISH_PROFILE` secret (contents of the publishing profile) and `AZURE_WEBAPP_NAME` to your GitHub repository secrets.
- The included GitHub Actions workflow will install dependencies, run `collectstatic`, and deploy.

3. Static files

- `Whitenoise` is configured in `settings.py` and `STATICFILES_STORAGE` is set. The `collectstatic` step in CI will create the static assets in `staticfiles`.

4. Database

- For production use, provision Azure Database for PostgreSQL and set `DATABASE_URL` accordingly. The app falls back to SQLite if no `DATABASE_URL` is provided.

5. Local testing

- Copy `.env.example` to `.env`, fill values, then run:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

6. Notes

- Before pushing to main, ensure `SECRET_KEY` and other secrets are stored in Azure or GitHub Secrets, not in the repo.
- Adjust Python version in `runtime.txt` as needed.
