#### Go into python venv env under direction: `django-jwt-demo` with(support Linux/Mac os only)
```python
source django-env/bin/activate
```

#### Run api service under direction: `django-jwt-demo` with
```python
uvicorn data_api.main:app --host 0.0.0.0 --port 5555 --reload
```

#### Customer get jwt token with
```python
curl --location --request GET 'http://127.0.0.1:8000/o/my_auth' \
--header 'customer-name: customer_9' \
--header 'customer-secret: HcZnZBBjW8yz96hQrZ25' \
--header 'scope: w' \
--header 'resource-name: wf' \
--data-raw ''
```


#### Customer get resource using jwt token with
```python
curl --location --request GET 'http://0.0.0.0:8888/weather_forecast?lon=111&lat=12&hours=144' \
--header 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NzE1MjM3NDcsImV4cCI6MTY3MTUyNDM0NywiZGF0YSI6eyJyZXNvdXJjZV9uYW1lIjoid2YifX0.iPid23HzkCUqy-11YvetbthYaSB7x0u7lqg8YAVfo0o'
```

#### To do: record django-oauth-toolkit output jwt token process