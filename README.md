# NeonAPI 🔌

API bilan ishlash - so'rovlar yuborish, javob olish va boshqarish kutubxonasi.

## Kalit so'zlar
`api`, `get`, `post`, `put`, `delete`, `patch`, `rest`, `http`, `request`, `auth`

## O'rnatish
```bash
pip install neonapi
```

## Ishlatish

```python
from NeonAPI import NeonAPI

api = NeonAPI(base_url="https://jsonplaceholder.typicode.com")
api.set_auth("my_jwt_token")

result = api.get("/users/1")
print(f"Status: {result['status']}, OK: {result['ok']}")
print(result['data'])

new_post = api.post("/posts", {"title": "Test", "body": "NeonAPI bilan yozildi", "userId": 1})
print(f"Yaratildi: {new_post['status']}")

updated = api.put("/posts/1", {"title": "Yangilandi"})
api.delete("/posts/1")
```

## Real misol

```python
from NeonAPI import NeonAPI

api = NeonAPI(base_url="https://jsonplaceholder.typicode.com", timeout=15)

users = api.get("/users")
print(f"Foydalanuvchilar: {len(users['data'])}")

for u in users['data'][:3]:
    posts = api.get("/posts", params={"userId": u['id']})
    print(f"  {u['name']}: {len(posts['data'])} ta post")

new = api.post("/posts", {"title": "NeonAPI Test", "body": "Ishlayapti!", "userId": 1})
print(f"\nYangi post ID: {new['data'].get('id')}")
```
