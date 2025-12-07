#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### **3. En Render, cambiá el Start Command**

En la configuración de Render, donde dice **"Start Command"**, poné:
```
gunicorn Reviewflix.wsgi:application
