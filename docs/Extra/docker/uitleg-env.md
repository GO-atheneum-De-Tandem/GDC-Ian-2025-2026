1. Maak je settings in Python met Pydantic BaseSettings (leest automatisch environment of .env):

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
# gebruik settings.DB_HOST etc.
```


2. Bouw je image zonder harde credentials in de code (geen secrets in image):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```


3. Run container met environment variables (runtime, niet in code):
- Direct:
```
docker run -e DB_HOST=host -e DB_USER=user -e DB_PASS=pass -e DB_NAME=db -p 8000:8000 myimage
```
- Of met een env-file:
```
docker run --env-file .env -p 8000:8000 myimage
```

4. Gebruik docker-compose voor gemak:

```yaml
version: "3.8"
services:
  app:
    image: myimage
    ports:
      - "8000:8000"
    env_file:
      - .env
```


5. .env voorbeeld (houd dit buiten je repo of in .gitignore):
```
DB_HOST=db.example.com
DB_USER=appuser
DB_PASS=supersecret
DB_NAME=mydb
```

6. Productie: gebruik Docker Secrets, Kubernetes Secrets of een geheimbeheerder (Azure Key Vault / AWS Secrets Manager) in plaats van .env voor gevoelige data.