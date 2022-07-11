document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded')
    document.querySelector('#compose-form').onsubmit = compose_post;

    // show_posts();
});

function compose_post(){
    
    const subject = document.querySelector('#post-subject').value;
    console.log('ready to submit the form!')
    
    fetch('/posts/compose', {
        method: 'POST',
        body: JSON.stringify({
            subject: subject
        })
    })
    .then(res => res.json())
    .then(res => {
        setTimeout(console.log('response: ', res), 100)
    })
    .catch(error => {
        alert("Error", error);
    });
    // refer to: https://cs50.stackexchange.com/questions/39316/cs50w-2020-project3-mail-does-not-show-new-sent-mail-after-sending/41032#41032?newreg=2663463db11c461bbc518e0140e5aae2
    // setTimeout(function(){ load_mailbox('inbox'); }, 100);
}


function show_posts(){
    fetch('/posts')
    .then(res => res.json())
    .then(posts => {
        console.log(posts);
        // show emails depending on clicked mailbox
        // posts.forEach(post => {
        //     load_post(post);
        // });
    })
}


function load_post(post){
    pass
}