if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
} 

function count(){
    // retrieve the counter in the storage first
    counter = localStorage.getItem('counter');
    counter++;
    document.querySelector('h1').innerHTML = counter;
    // update the counter in the local storage
    localStorage.setItem('counter', counter);
}

document.addEventListener('DOMContentLoaded', function(){
    // every time loading the page, give the h1 element the latest counter 
    document.querySelector('h1').innerHTML = localStorage.getItem('counter')
    document.querySelector('button').onclick=count

    // increase counter on the page automatically 
    // setInterval(count, 1000);
})