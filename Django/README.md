### Install Django

`pip3 install Django`

### Create a project

`django-admin startproject PROJECT_NAME`

### Run web application

`python3 manage.py runserver`

Depending on which python you have installed on your PC, you probably need to use `python` instead of `python3` in the above command. If `manage.py` is not in your current directory, you also need to add path before the file.

After executing the above command, the output shows `starting development server at http://127.0.01:8000`. Copy the url to the browser and you will see a default Django web page.

### Create a Django app

#### General steps

First create an application by executing

`python3 manage.py startapp <app_name>`

Then add the app name to the `settings.py` file in the *Application definition*. Later, develop your application in the `views.py` file. For example,

```py
def index(request):
    return render(request, "hello/index.html")
```

*index.html* is the default url for an application.

Now create an `urls.py` file in the application folder, and define what urls are allowed in this application by typing the following codes. 

```py
urlpatterns = [
    path("", views.index, name="index")
]
```

Lastly, we need to go the project's ´urls.py´ file and add the application url by `path('hello/', include("hello.urls"))` to the project urls.

#### Parameterize request

Aside from *index.html*, we could also create other urls in the application. To do so, we can define functions like:

```py
def greet(request):
    return HttpResponse("Hello, world!")
```

To make it more *generic*, i.e., to greet whoever with a given name, we could pass another parameter to the function:

```py
def greet(request,name):
    return HttpResponse(f"Hello, {name}!")
```

In the curly brackets, we can also pass a method, e.g., `name.capitcalize()` to capitalize the give name.

In the application *urls.py* file, we need to add *greet* url accordingly `path("<str:name>", views.greet, name="greet")` with `name` passing as a variable.


#### render url

Aside from requesting a web page, we can also render the whole url in the application, which helps seperate python and html logic.

```py
def index(request):
    return render(request, "hello/index.html")
```

Then create a folder named *templates*. Under the *templates* folder, create a folder named as the same as the application name, e.g., *hello*; and under this folder, create a `index.html` file where we can write html.

Additionally, we can added the third arguement (a dict) to pass a variable to the html file in the `render()` method, e.g.,

```py
def greet(request, name):
    return render(request, "hello/greet.html", {
        "name" : name.capitalize()
    })
```

In the `templates/hello/index.html` file, we can pass the *name* variable by using {{ name }}. If we need to write python logic in the html file, use {% python code %} fomart. For example,

```html
    <body>
        {% if newyear %}
            <h1> YES </h1>
        {% else %}
            <h1> NO </h1>
        {% endif %}
    </body>
```

If using *for* loop, we can write a code like `{% for t in list %}`, with {% endfor %} to end the loop.

Moreover, we can refer to css file (static-type file, which does not require changes very often) in this html file by adding `<link href="{% static 'hello/style.css' %}" rel="stylesheet"`>, and adding `{% load static %}`. Meanwhile, we need to create a *static* folder under the folder of the applicaiton, and then create a folder with same name as the application, in which create a css file named `static`.


### Template inheritance

If many web pages in an application share a similar layout, we can build a basic layout, which can be inheritated by all of web pages in that application to avoid repetition. To do so, create a `layout.html` file under the `templates/<app_name>` folder, and write down the layout.

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Tasks</title>
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
</html>
```

And we can fill `{% block body %}` with the changes in each page. For example, in the `index.html` file, first we need to write `{% extends "tasks/layout.html" %}`, and in the body block section, we can write down the content.

```html
{% extends "tasks/layout.html" %}

{% block body %}
    <h1>Tasks</h1>
    <ul>
        {% for task in tasks %}
        <li>{{ task }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

We can also add a link in the body block by adding a line of code `<a href="{% url 'add' %}">Add a New Taks</a>`, where `add` in the name of the url that we want to link. Note that it may occur collision if the name of the url in this application is the same as that in other application. So here we could give it a name to the application by adding `app_name = "tasks"` in the application `urls.py` file and specify which application url to link by adding the name in the href, e.g. `'tasks:add'`.


