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

7. Disabling heavy ML models on Azure

- If you do not want the application to attempt downloading or using heavy ML models (for example on low-resource or CPU-only App Service plans), set the application setting `DISABLE_HAIRSTYLE_AI` to `True` (`1`/`true`/`yes`). This will make the service use the faster fallback transformations.
- If you plan to use Replicate for inpainting/inference, add `REPLICATE_API_TOKEN` to your App Settings. Without it, the app will skip Replicate calls.

8. Environment variables (summary)

- `SECRET_KEY` : required for production
- `DEBUG` : `False` in production
- `ALLOWED_HOSTS` : comma-separated hosts (or leave to `*` for quick test)
- `DATABASE_URL` : optional Postgres connection string (recommended for production)
- `DISABLE_HAIRSTYLE_AI` : `True` to disable heavy ML/model downloads on deploy
- `REPLICATE_API_TOKEN` : token for Replicate API if you want cloud-based inpainting

Update these in Azure Portal → your Web App → Configuration → Application settings.

## Quick deploy checklist

- Ensure `requirements.txt` is at the project root and lists `gunicorn` and `whitenoise`.
- Ensure `runtime.txt` (Python version) matches the App Service runtime.
- Ensure `Procfile` exists (this repo includes a `Procfile` that runs `startup.py` then `gunicorn`).
- Set `ALLOWED_HOSTS` in App Settings (or leave `*` only for quick testing).
- Set `SECRET_KEY` and `DEBUG=False` in App Settings for production.
- Set `DISABLE_HAIRSTYLE_AI=True` in App Settings to avoid heavy model downloads on low-tier App Service plans.
- (Optional) Add `REPLICATE_API_TOKEN` if you want to enable Replicate-based inpainting.

## Minimal GitHub Actions build hint

Azure will detect `requirements.txt` and `runtime.txt`, but a typical GitHub Actions job should:

1. Check out the repository
2. Set up Python (match `runtime.txt`)
3. Install dependencies: `pip install -r requirements.txt`
4. Run `python manage.py collectstatic --noinput`
5. Run migrations: `python manage.py migrate --noinput` (if using Azure Postgres)
6. Let Azure deploy the built artefact

Example (snippet for Actions job step):

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: "3.11"

- name: Install dependencies
  run: pip install -r requirements.txt

- name: Collect static files
  run: python manage.py collectstatic --noinput

- name: Run migrations
  run: python manage.py migrate --noinput
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Post-deploy

- Verify App Service application settings include the env vars described above.
- If using Postgres, run any remaining migrations via Azure SSH/console or an Action.
- Monitor logs in Azure Portal → App Service → Log stream for runtime errors.

## Troubleshooting tips

- If the App Service plan is CPU-only and small, set `DISABLE_HAIRSTYLE_AI=True` to avoid model downloads and timeouts.
- If you see missing package errors, ensure `requirements.txt` contains the package and the correct version.
- If static files are missing, confirm `collectstatic` ran and `STATICFILES_STORAGE` is set to WhiteNoise in `settings.py`.
