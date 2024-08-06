# Cuisiner project

Cuisiner - is a cooking platform that can help users to save, share, create recipes with ease and makes recipe search proceess much more easier. 

Here you can save you food preferences ( favorite/hated categories/products or even choose diet type) and then you can use recipe filters to find the best recipe in the world.
For better user expirience ingridients will be marked in green/red. Whether user likes that ingridient or not.

## Launch
Install all needed python modules/libraries from `requirements`

After that connect DB and enter all needed VENV variables. 

In `core/settings.py`

Set django secret key
```python
SECRET_KEY = os.environ.get("SECRET_KEY")
```
Set google email, password
```python
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
```
Set DB url ( I'm using from Render, PostgreSql)
```python
DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DB_URL"))
}
```
Now connect cloud storage ( I'm using Cloudinary )
<br>
And don't forget to change if you using different storage service
```python
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME' : os.environ.get("CLOUD_NAME"),
    'API_KEY' : os.environ.get("API_KEY"),
    'API_SECRET' : os.environ.get("API_SECRET")
}
```
### Django migrations
```console
python3 manage.py makemigrations
```
```console
python3 manage.py migrate
```
If needed you can add admin user
```console
python3 manage.py createsuperuser
```
### Django local launch
```console
python3 manage.py runserver
```

# Screenshots
<img width="1016" alt="Screenshot 2024-08-06 at 12 26 23" src="https://github.com/user-attachments/assets/4a62784e-fbaa-438c-b9e4-e353e0bec23f">

### Recipe view
<img width="568" alt="Screenshot 2024-08-06 at 12 30 51" src="https://github.com/user-attachments/assets/6fdb4066-bc12-4fbc-a024-28bb10d7cd06">

<img width="563" alt="Screenshot 2024-08-06 at 12 30 57" src="https://github.com/user-attachments/assets/a18e304f-3ca0-4b03-8522-edf5a177b509">

<img width="854" alt="Screenshot 2024-08-06 at 12 28 03" src="https://github.com/user-attachments/assets/ecb4abb0-a3d7-4eec-b579-6dfc0d5d54ef">
<img width="572" alt="Screenshot 2024-08-06 at 12 31 07" src="https://github.com/user-attachments/assets/b31e8075-3b47-4b33-9437-448e9dd97742">


