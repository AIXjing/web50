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

Except for html element, `document.querySelector()` can also accept `#id` and `.class` like css as an arguement to select a particular element.

### 4. js file

In order to further seperate Javascript code from html, we can move all the Javascript code into a `.js` file and import this file to the html file as `<script src="counter.js"></script>`
