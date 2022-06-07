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

The `HttpResponse` can also take *html* elements, .e.g. `HttpResponse("<h1 style=\"color:blue\">Hello, World"</h1>")`. Although it is doable, it would be a bad design. The good practice is to seperate *html* and *css* files. This is where it would be better to use [Django templates](https://docs.djangoproject.com/en/4.0/topics/templates/).

### Django templates

Aside from requesting a web page, we can also render the whole url in the application, which helps seperate python and html logic.

```py
def index(request):
    return render(request, "hello/index.html")
```

Then create a folder named *templates*. Under the *templates* folder, create a folder named as the same as the application name, e.g., *hello*; and under this folder, create a `index.html` file where we can write html.

Additionally, we can added the third arguement (a dict) to pass a variable to the html file in the `render()` method to change the content of out *html* files based on the URL visited by using [Django's template language](https://docs.djangoproject.com/en/4.0/ref/templates/language/), e.g.,

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

Moreover, we can refer to css file (static-type file, which does not require changes very often) in this html file by using Django-specific syntax `<link href="{% static 'hello/style.css' %}" rel="stylesheet"`>, and adding `{% load static %}` on the top of the *html* file. Meanwhile, we need to create a *static* folder under the folder of the applicaiton, and then create a folder with same name as the application, in which create a css file named `static`.


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

To make a dynamic form, that is we can update the form every time pressing submit button in the page, we can add properties `method="post"` in the `form` tag in the html file. 

To return back to the previous page, we can add the property `action="{% url 'tasks:add' %}"` in the `form` tag.

When the request is the *POST* type, Django requires a token to prevent *Cross-Site Request Forgery (CSRF) Attack*. Thus, we need to add  `{% csrf_token %}` in the POST action. With this token, each session (can be considered as a user) is assinged an unique token. Every time a POST request is sent with that token so that the server can validate the POST request。

### Django Forms

Django also provides a *forms* class to help us easily deal with form, and we can create a class like below:

```py
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)
```

Then we can create a form by creating the *NewTaskForm* class. `forms.Form` in the parentheses after *NewTaskForm* indicates that the new form we are going to create inherits from a class called *Form* that is included in the *forms* module.

### Session and Migrate

At this point, we’ve successfully built an application that allows us to add tasks to a growing list. However, it may be a problem that we store these tasks as a global variable, as it means that all of the users who visit the page see the exact same list. In order to solve this problem we’re going to employ a tool known as **sessions**.

*Sessions* are a way to store unique data on the server side for each new visit to a website. To use sessions in our application, we’ll first delete our global `tasks` variable, then alter our `index` function, and finally make sure that anywhere else we had used the variable `tasks`, we replace it with `request.session["tasks"]`.

To create a table to store the data for each user, run `python3 manage.py migrate`

### Django model

Generally, each model maps to a single databse table. The basics:

- Each model is a Python class that subclasses `django.db.models.Model`

- Each attribute of the model represents a database field

- With all of this, Django gives you an automatically-generated database-access API.

To create *model*, we need to go to `models.py` writing a few lines of code:

```py
class Flight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
```

### Migration

To create a database from our models, run `python3 manage.py makemigrations` in the main directory.

To apply migration, run `python3 manage.py migrate`

To manipulate or execute sql, we can use Python through *Django Shell* by running `python3 manage.py shell`. Then, we could run python code in the console.

```py
# import newly-created class Flight
# flights are the app name and models is a folder in the app
from flights.models import Flight

f = Flight(origin="New York", destination="London", duration=415)
f.save()
```

To retrieve the data, use the syntax `Flight.objects.all()`, a query for all flights stored in the database. The output will be an object form like `<QuerySet [<Flight: Flight object (1)>]>`.

To explicitely show the object enties, we can define a `__str__` function that provides instructions for how to turn a Flight object into a string in the `Flight` class. For example,

```python
def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
```

To exit Django shell, press `control` + `D`

To build an application that can interact with this database, we can pass the object entries directly through response syntax. 
```python
# in views.py
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })
```

### Django Admin

To easily create new objects for developers, Django provides a *default admin interface*. First we need to create an adminstrative user by `python3 manage.py createsuperuser`. Then we must add our models to the admin application by entering `admin.py`, importing and registering our models. If we run server and go to `/admin` endpoint, we will see an administrative interface. 

We can also configurate display settings of the interface by defining class in `admin.py` e.g., 

```python
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")
```

Then, apply the class in the models `admin.site.register(Flight, FlightAdmin)`


### Authentification