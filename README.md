## To test locally

```
uvicorn main:app --reload --env-file .env
```

## Deploy to deta

deta clone --name platformer --project default
deta deploy
deta update -e .env
deta logs
