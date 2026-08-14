# Hierarchical Django Router Guide

## Overview

This router system lets you organize Django views using a **Ninja-like API** with support for:
- ✅ Hierarchical/nested routers
- ✅ Namespace management for reverse URL lookups
- ✅ Path converters (`<int:id>`, `<str:slug>`)
- ✅ Regex patterns (`re_path` support)
- ✅ Automatic prefix management
- ✅ Dynamic module discovery

---

## Basic Usage

### Single Router (Flat)

```python
from django_router import Router
from django.http import JsonResponse

router = Router()

@router.route("users/")
def list_users(request):
    return JsonResponse({"users": []})

@router.route("users/<int:id>/")
def user_detail(request, id):
    return JsonResponse({"id": id})
```

In `urls.py`:
```python
from django.urls import path
from .views import router

urlpatterns = router.get_patterns()
```

**Generated URLs:**
- `GET /users/`
- `GET /users/123/`

---

## Nested Routers (Subrouting)

### Structure

```python
# routers/users_router.py
from django_router import Router

users = Router(namespace="users")

@users.route("", name="list")
def list_users(request):
    return JsonResponse({"users": []})

@users.route("<int:id>/", name="detail")
def user_detail(request, id):
    return JsonResponse({"id": id})


# routers/posts_router.py
posts = Router(namespace="posts")

@posts.route("", name="list")
def list_posts(request):
    return JsonResponse({"posts": []})

@posts.route("<int:id>/", name="detail")
def post_detail(request, id):
    return JsonResponse({"id": id})


# main_router.py
from django_router import Router
from .routers.users_router import users
from .routers.posts_router import posts

api = Router(prefix="api/v1", namespace="api")
api.include(users, prefix="users")
api.include(posts, prefix="posts")

# Export for urls.py
urlpatterns = api.get_patterns()
```

**Generated URLs:**
- `GET /api/v1/users/`
- `GET /api/v1/users/123/`
- `GET /api/v1/posts/`
- `GET /api/v1/posts/456/`

**Reverse URL names:**
```python
reverse("api:users:list")      # /api/v1/users/
reverse("api:users:detail", args=[123])  # /api/v1/users/123/
reverse("api:posts:list")      # /api/v1/posts/
```

---

## Advanced: Multi-Level Nesting

```python
# Nested 3 levels deep

comments = Router(namespace="comments")

@comments.route("", name="list")
def list_comments(request):
    return JsonResponse({"comments": []})

# Posts with comments
posts = Router(namespace="posts")

@posts.route("", name="list")
def list_posts(request):
    return JsonResponse({"posts": []})

# Include comments under posts
posts.include(comments, prefix="<int:post_id>/comments")

# API includes posts
api = Router(prefix="api/v1", namespace="api")
api.include(posts, prefix="posts")
```

**Generated URLs:**
- `GET /api/v1/posts/`
- `GET /api/v1/posts/456/comments/` ← comments nested under posts

---

## Regex Patterns

The router auto-detects regex by looking for regex metacharacters:

```python
from django_router import Router

router = Router()

# Path converter (simple)
@router.route("users/<int:id>/")
def user_by_id(request, id):
    return JsonResponse({"id": id})

# Regex pattern (auto-detected)
@router.route(r"posts/(?P<slug>[\w-]+)/$")
def post_by_slug(request, slug):
    return JsonResponse({"slug": slug})

@router.route(r"profiles/(?P<username>\w+)/settings/$")
def user_settings(request, username):
    return JsonResponse({"username": username})
```

**Generated URLs:**
- `GET /users/123/`
- `GET /posts/my-awesome-post/`
- `GET /profiles/john_doe/settings/`

---

## Dynamic Module Discovery

Auto-import all views in a package:

```python
# api/views/__init__.py
from django_router import Router

router = Router(prefix="api", namespace="api")
router.discover("api.views")  # Imports all modules in api/views/

# api/views/users.py
from api import router as api_router

@api_router.route("users/")
def list_users(request):
    return JsonResponse({"users": []})

# api/views/posts.py
@api_router.route("posts/")
def list_posts(request):
    return JsonResponse({"posts": []})
```

When `discover()` is called, all modules are imported and decorators fire automatically.

---

## Project Structure Example

```
myproject/
├── urls.py                 # Main Django URLs
├── api/
│   ├── __init__.py
│   ├── router.py          # API router setup
│   └── views/
│       ├── __init__.py
│       ├── users.py       # User views
│       ├── posts.py       # Post views
│       └── comments.py    # Comment views
└── core/
    └── routers/
        ├── api_v1.py      # v1 API router
        └── api_v2.py      # v2 API router
```

**api/router.py:**
```python
from django_router import Router

api = Router(prefix="api", namespace="api")

# Discover all views in api/views/
api.discover("api.views")

# Export for urls.py
urlpatterns = api.get_patterns()
```

**urls.py:**
```python
from django.contrib import admin
from django.urls import path
from api.router import urlpatterns as api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
] + api_urls
```

---

## Router API Reference

### `Router(prefix="", namespace="")`

Initialize a router with optional prefix and namespace.

```python
# No prefix
router = Router()

# With prefix
api = Router(prefix="api/v1")

# With namespace (for reverse URL lookups)
users = Router(namespace="users")

# Both
api = Router(prefix="api", namespace="api")
```

---

### `@router.route(url_string, name=None, method=None)`

Decorator to register a view.

```python
@router.route("users/", name="list")
def list_users(request):
    pass

@router.route("users/<int:id>/", name="detail")
def user_detail(request, id):
    pass

# With regex
@router.route(r"posts/(?P<slug>[\w-]+)/$", name="by_slug")
def post_by_slug(request, slug):
    pass

# method param is for metadata (not enforced)
@router.route("users/", method="GET")
def list_users(request):
    pass
```

---

### `router.include(subrouter, prefix, namespace=None)`

Include a subrouter with a prefix.

```python
users = Router(namespace="users")
api = Router(prefix="api")

api.include(users, prefix="users", namespace="api")
# URLs: /api/users/...
# Names: api:users:...
```

---

### `router.discover(package_name)`

Auto-import all modules in a package.

```python
router = Router()
router.discover("api.views")  # Imports all .py files in api/views/
```

---

### `router.get_patterns()`

Get all URL patterns (call once in your `urls.py`).

```python
urlpatterns = api_router.get_patterns()
```

---

## HTTP Method Validation

Since you chose to keep the generic `@route()` approach, you handle method validation **outside** the router:

```python
from django.http import HttpResponseNotAllowed
from django_router import Router

router = Router()

@router.route("users/", method="GET")
def list_users(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return JsonResponse({"users": []})

# Or use a middleware for automatic enforcement
# Or check in the view logic
```

Alternatively, use a **view wrapper**:

```python
def enforce_method(*allowed_methods):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.method not in allowed_methods:
                return HttpResponseNotAllowed(allowed_methods)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@router.route("users/")
@enforce_method("GET")
def list_users(request):
    return JsonResponse({"users": []})
```

---

## Reverse URL Lookups

With namespaces, reverse URL lookups become predictable:

```python
from django.urls import reverse

# Single level
reverse("users:list")  # /users/

# Nested with api namespace
reverse("api:users:list")  # /api/users/
reverse("api:users:detail", args=[123])  # /api/users/123/

# Multiple levels
reverse("api:v1:posts:detail", args=[456])  # /api/v1/posts/456/
```

---

## Class-Based Views

The router automatically detects and handles CBVs:

```python
from django.views import View
from django.http import JsonResponse

class UserListView(View):
    def get(self, request):
        return JsonResponse({"users": []})
    
    def post(self, request):
        return JsonResponse({"created": True})

class UserDetailView(View):
    def get(self, request, id):
        return JsonResponse({"id": id})

# Register them
router = Router()

@router.route("users/")
def user_list(request):
    return UserListView.as_view()(request)

@router.route("users/<int:id>/")
def user_detail(request, id):
    return UserDetailView.as_view()(request, id)
```

Or pass the CBV directly (router calls `.as_view()` automatically):

```python
@router.route("users/")
class UserListView(View):
    def get(self, request):
        return JsonResponse({"users": []})
```

---

## Tips & Best Practices

1. **Use namespaces** for clarity and reverse URL lookups:
   ```python
   api = Router(prefix="api", namespace="api")
   users = Router(namespace="users")
   api.include(users, prefix="users")
   # Access via: reverse("api:users:list")
   ```

2. **Organize by domain**:
   ```
   api/views/
   ├── users.py
   ├── posts.py
   ├── comments.py
   ```

3. **Use discovery for large projects**:
   ```python
   api.discover("api.views")  # Auto-loads all views
   ```

4. **Version your APIs**:
   ```python
   api_v1 = Router(prefix="api/v1", namespace="v1")
   api_v2 = Router(prefix="api/v2", namespace="v2")
   ```

5. **Keep routers modular**:
   ```python
   # Each router is self-contained
   users_router.py
   posts_router.py
   comments_router.py
   # Then compose them in main router
   ```