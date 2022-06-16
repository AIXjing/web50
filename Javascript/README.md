## Javascript

Javascript is a language allow user to manipulate *document object model(DOM)* on a brower (client), and the code can be directly run in the client.

To add Javascript code, we only need to add tag <script></script> in html file, and add the Javascript code between the tags. For example,

*example1*
```html
<script>
    alert("Hello, world!")
</script>
```

which will pop up a window shows "Hello, world". `alert` is Javascript build-in function.


Javascript can be quite powerful with *event-driven programming*. Event can be thought as an action from user, e.g., click, hover, etc. And we can add an event *listeners* or event handlers to "respond" these events. 

*example2*
```html
<script>
    function hello(){
        alert("Hello, world!")
    }
</script>

<button onclick="hello()">click</button>
```

In the above case, `onclick` inside the button tag is an event listener. Once the button is clicked, `hello()` function will be called. 

The following case shows that `h1` element will change to 'Goodbye!' once the button is clicked by using `document.querySelect('h1')` to retrieve the html element. 

*example3*
```html
<script>
    function hello(){
        const heading = document.querySelector('h1');
        if (heading.innerHTML === 'Hello!'){
            heading.innerHTML = 'Goodbye!';
        } else {
            heading.innerHTML = 'Hello!';
        } 
    }
</script>
<body>
    <h1>Hello!</h1>
    <button onclick="hello()">Click Here!</button>
</body>
```

### 1. Variables

Like Python and other programming languages, you can also assign a variable in Javascript.

*example4*
```html
<script>
    let counter = 0;
    function count(){
        counter++;
        document.querySelector('h1').innerHTML = counter;

        if (counter % 10 === 0) {
            alert(`Count is now ${counter}`);
        }
    }
</script>
<body>
    <h1>0</h1>
    <button onclick="count()">Click Here!</button>
</body>
```

Also see example in *example4*.

`let` is to define a normal variable.

`const` is to define a variable that cannot be changed.

### 2. Conditions

See example above.


### 3. addEventListener()

We could also seprate html and Javascript code by using Javascript functions. For example, instead of using `onclick` in the `button` tag, we can use `document.querySelector('button').onclick=count`, which is equivalent to `document.querySelector('button').addEventListener('click', count())`. Here, `count` function is passed to a variable instead of being called.

Note that we also need to nest this line of code inside the listner of the even `'DOMContentLoaded'` as the code would not be executed until the web page loaded.

```html
<script>
    document.addEventListener('DOMContentLoaded', function(){
        document.querySelector('button').onclick=count
    })
</script>   
```

Except for html element, `document.querySelector()` can also accept `#id` and `.class` like css as an arguement to select a particular element. Like that, using `document.querySelector()` can also change css of elements by using `.style.color` with the assigned color.

*example5*
```html
<script>
    document.addEventListener('DOMContentLoaded', function(){
        // change font color to red
        document.querySelector('#red').onclick = function () {
            document.querySelector('#hello').style.color = 'red'
        }
    })
</script>
<body>
    <h1>Hello!</h1>
    <button id="red">Red</button>
</body>
```
However, if we want to have three buttons in order to change the font with three colors, we can use `data-color` attribute in the tag instead of `id`. Here. to select all buttons, we could use `document.querySelector.All('button')`, which will return a *NodeList* like list in Python. To iterate each element in the NodeList, we can use NodeList method `.forEach()` where we can pass function of element to do something. 

Here we could also use a dropdown to change the color. This requires to use `.onchange` even, and the selected color can pass to the font by assigin `this.value` where `this` refer to whatever element the `select` recieved. In this case, the `function(){}` for event handler cannot be notated with `() =>  {}`

*example6*
```html
<script>
    document.addEventListener('DOMContentLoaded', function(){
        // change font color to red
        document.querySelector('select').onchange = function () {
            document.querySelector('#hello').style.color = this.value
        }
    })
</script>
<select>
    <option value="red">Red</option>
    <option value="green">Green</option>
    <option value="blue">Blue</option>
</select>
```

### 4. Javascript events

* onclick
* onchange
* onmouseover
* onkeydown
* onkeyup
* onsubmit
* ...

### 5. js file

In order to further seperate Javascript code from html, we can move all the Javascript code into a `.js` file and import this file to the html file as `<script src="counter.js"></script>`

### 6. Javascript notation

A shorthand of `function` is the notation `=>`. In the *example5*, we can also write it to:

```javascript
document.addEventListener('DOMContentLoaded', () => {
    // change font color dynamically
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            document.querySelector('#hello').style.color = button.dataset.color;
        }
    })
})
```

The left side of the `=>` is the argument is going to be passed into the function, and right side is the function body.

### Exercise notes

In order to print a value in console, we can use `console.log(variable)`, which also needs to include `return false` after to stop from further executing. 

Javascript can also create an element on event using `document.createElement('li')`. Then, we could assign a value to the element, and appened to the list by `document.querySelector('#tasks').append(li)`

### Local storage

* localStorage.getItem(key)

* localStorage.getItem(key,value)

* localStorage.setItem(varaible, value)


### Javascript object

Javascssript object is useful as it can be exchangeable through different services. Similar to Python dictionary, to define a Javascript object, 

```javascript
person = {
    first: 'Harry',
    last: 'Potter'
}
```

To extract the object property, we can either use `person.first` or `person['first']`. 

## APIs

It can be considered as a well-structured format that services use for communication with each other. The format often happens to be a particular format of data, known as *JSON (Javascript Object Notation)*. That is to transfer data through Javascript object. JSON data may look like below:

```json
{
    "origin": "New Yord",
    "destination": "London",
    "duration": 415
}

{
    "base": "USD",
    "rates": {
        "EUR": 0.907,
        "JRY": 109.716,
        "GBP": 0.766,
        "AUD": 1.479
    }
}
```

## Ajax

*Asynchronous Javascript*: allows Javascript to ask for additional request from external server even after page is loaded. *Asynchronous request* The following snippet shows how to fetch data from an api and print in console:

```javascript
fetch('https://api.exchangerate.host/latest?base=USD')
    // convert the retrieved data to json format
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.log("Error", error);
    })
```

We could also get a specific value by call its key.