# DuoQuanto backend – local development

Quickstart:

```bash
# install dependencies
pip install -r backend/requirements.txt

# initialise database
python -m backend.scripts.init_db

# run dev server (reload)
uvicorn backend.main:app --reload
```

Front-end dev server (e.g. React) is assumed to run on http://localhost:3000 –
CORS is already configured for that origin.
