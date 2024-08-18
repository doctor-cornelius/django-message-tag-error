# Django Message Tag Error

## TLDR;

If you override message tags in `settings.py`, it is difficult to know how to do it. Furthermore if you plan on generating `info` or `debug` message tags for the admin panel, they will not work because django admin does  not include styling for them. This repo shows how to achieve this, for vailla admin, and also if using `django-admin-interface`.

## The Problem

Let's say you're using Bootstrap and want to override message tag styles for your site. You might do this:

```python
from django.contrib.messages import constants as messages

MESSAGE_LEVEL = messages.DEBUG if DEBUG else messages.INFO

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-error",
}
```

The problem with this is that it won't work for admin. Every type of message (eg messages.INFO, messages.WARNING, etc) will be styled with the default green with a checkmark, because none of these classes are known to the `admin.contrib.admin.static.base.css` (whiich pays no attention to your styling of your main site).

So what you can do is use the classes that admin does expect, from its `DEFAULT TAGS`, as well as the classes you need for the front end:

```python
MESSAGE_TAGS = {
    messages.DEBUG: "debug alert-info",
    messages.INFO: "info alert-info",
    messages.SUCCESS: "success alert-success",
    messages.WARNING: "warning alert-warning",
    messages.ERROR: "error alert-error",
}
```

With this change, all your messages will be correctly styled for `SUCCESS`, `WARNING`, `ERROR`, and `INFO`. However, `DEBUG` and `INFO` messages will still be styled with the default green with a checkmark.

## The Solution

The solution is:

1. Include some suitable icons for `DEBUG` and `INFO` messages.
2. Override the `base_site.html` template to include the `DEBUG` and `INFO` classes; and

### Include some icons for `DEBUG` and `INFO` messages.

In `static/admin/img`, obtain some suitable files for `DEBUG` and `INFO` messages; I used:

- `icon-unknown.svg` (copied from `django.contrib.admin.static.img.icon-unknown.svg`)
- `icons8-info.svg` (from <a target="_blank" href="https://icons8.com/icon/77/info">Info</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>)

### Override `base_site.html`

You need to put this in `templates/admin/base_site.html`:

```html
{% extends "admin/base_site.html" %}

{% load static %}

{% block extrastyle %}{{ block.super }}
<style>
    html[data-theme="light"],
    :root {
        --message-debug-bg: #f116ede1;
        /* Blue background for info messages */
        --message-debug-text: #100f0f;
        /* White text for better contrast */
        --message-info-bg: #cfcfd769;
        /* Blue background for info messages */
        --message-info-text: #100f0f;
        /* White text for better contrast */
    }

    .messagelist .debug {
        background-color: var(--message-debug-bg);
        color: var(--message-info-text);
        background: var(--message-debug-bg) url({% static 'admin/img/icon-unknown.svg' %}) 40px 12px no-repeat;
        background-size: 16px auto;
    }

    .messagelist .info {
        background-color: var(--message-info-bg);
        color: var(--message-info-text);
        background: var(--message-info-bg) url({% static 'admin/img/icons8-info.svg' %}) 40px 12px no-repeat;
        background-size: 16px auto;
    }

</style>

</style>
{% endblock %}
```

You should run `python manage.py collectstatic` to copy the icons to your `staticfiles`. Then stop and restart the server, refresh your browser and any admin messages should be styled correctly.

## This Repo

This repo sets up a situation where it was easy to replicate the problem. This was done in the following ways.

### Project Structure

```
django_message_tag_error
├── LICENSE
├── README.md
├── db.sqlite3
├── demo
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── static
│   │   └── admin
│   │       └── img
│   │           ├── icon-unknown.svg
│   │           └── icons8-info.svg
│   ├── templates
│   │   ├── admin
│   │   │   └── base_site.html
│   │   └── demo
│   │       └── index.html
│   ├── tests.py
│   └── views.py
├── django_message_tag_error
│   ├── __init__.py
│   ├── __pycache__
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── poetry.lock
├── pyproject.toml
└── staticfiles
```

### Displaying Front End Messages

There is a home page template and a view to populate messages of different types.

The template uses bootstrap in this case (you can use whatever CSS framework you want, because the admin back end has nothing to do with the front end styling) and you can see that messages are displayed at the top.

`index.html`
```html
<!DOCTYPE html>
<html>

<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/custom.css' %}?v=1.0">

    <title>Message Demo</title>
</head>

<body>
    <div class="container">
        <!-- Bootstrap -->
        {% if messages %}
            {% for message in messages %}
                <div class="alert {{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}

        <h1>Welcome to the Message Demo</h1>
        <p>You should see formatted messages above</p>
        <br>
        <a href="{% url 'admin:index' %}" class="btn btn-primary">Go to Admin</a>
        <br>
        <p>There should be an image below:
            <img src="{% static 'admin/img/icon-no.svg' %}" alt="Test Image">
        </p>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
            crossorigin="anonymous"></script>

    </div>
</body>

</html>
```

The home page view is:

`views.py`
```python
from django.shortcuts import render
from django.contrib import messages

def index(request):
    messages.success(request, "This is a success message")
    messages.warning(request, "This is a warning message")
    messages.info(request, "This is an info message")
    messages.error(request, "This is an error message")
    return render(request, "demo/index.html")
```

### Admin Back End

The test for admin was when you click to manage `TestPerson` then messages are automatically displayed.

Created a very simple model:

`models.py`
```python
from django.db import models

# create a simple model called TestPerson with just name and age fields
class TestPerson(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

And generated the messages in `admin.py`:

`admin.py`
```python
from django.contrib import admin
from django.contrib import messages

from . import models

@admin.register(models.TestPerson)
class TestPersonAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        messages.debug(request, "This is a debug message")
        messages.info(request, "This is an info message")
        messages.success(request, "This is a success message")
        messages.warning(request, "This is a warning message")
        messages.error(request, "This is an error message")
        return super().changelist_view(request, extra_context)

    list_display = ("name", "age")
    search_fields = ("name", "age")
```

### Accommodating `django-admin-interface`

I am using `django-admin-interface` in another project so wanted to make sure this works ok. To do this you just need to:

1. Install `django-admin-interface` and `django-apptemplates`
2. Add `admin_interface` and `colorfields` to `INSTALLED_APPS` (before `django.contrib.admin`)
3. Change the `base_site.html` template to: `{% extends "admin_interface:admin/base_site.html" %}`

Settings are:

`settings.py`
```python
INSTALLED_APPS = [
    "demo",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
]
```

### Branches in This Repo

- `main` - the main branch, has the full setup including icons, etc
- `vanilla_admin_not_working`: the initial setup without the overrides. You can see the mis-styling of admin messages
- `vanilla_admin_working`: has the correct overrides as above. You can see the correct styling of admin messages
- `admin_interface_working`: same as main, but without the icons and the `README.md`

In the branches except for `main` you'll see that the info message includes `extra_tags="info"`, as below.  

```python
@admin.register(models.TestPerson)
class TestPersonAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        messages.success(request, "This is a success message")
        messages.warning(request, "This is a warning message")
        messages.info(request, "This is an info message", extra_tags="info")
        messages.error(request, "This is an error message")
        return super().changelist_view(request, extra_context)
```

That was an error. It should just be `messages.info(request, "This is an info message")` (which I corrected in `main` branch). It has no effect on the solution or problem, because the relevant tag is already `info`.