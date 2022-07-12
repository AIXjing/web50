document.addEventListener('DOMContentLoaded', function() {
    // console.log('DOM loaded')
    document.querySelector('#compose-form').onsubmit = compose_post;

    show_posts();
});

function compose_post(){
    
    const subject = document.querySelector('#post-subject').value;
    
    fetch('/posts/compose', {
        method: 'POST',
        body: JSON.stringify({
            subject: subject
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
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
        console.log(posts)
        posts.forEach(post => {
            load_post(post);
        });
    })
}


function load_post(post){
    const post_box = document.createElement('div');
    post_box.innerHTML = `${post.poster}: ${post.subject} \n ${post.timestamp}`
    document.querySelector('#post-view').append(post_box);
}