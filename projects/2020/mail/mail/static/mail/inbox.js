document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  // By default, load the inbox
  load_mailbox('inbox');

  // Add event listener to the form
  document.querySelector('#compose-form').onsubmit = send_email;

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(){
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;
  // console.log(recipients);

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log("result", result);
  })
  .catch(error => {
    alert("Error", error);
  });
  // refer to: https://cs50.stackexchange.com/questions/39316/cs50w-2020-project3-mail-does-not-show-new-sent-mail-after-sending/41032#41032?newreg=2663463db11c461bbc518e0140e5aae2
  setTimeout(function(){ load_mailbox('sent'); }, 100);
  return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      console.log(emails);
      emails.forEach(show_email);
  })
  
}

function show_email(email) {
  const element = document.createElement('div');
  element.className = 'mail-view-box';
  element.innerHTML = `${email.sender}:    ${email.subject}  <div class="timestamp"> ${email.timestamp} </div>`;
  // when mouse hover on an email, change the email box format
  element.addEventListener('mouseover', function(){
    this.style.background = "white";
    element.addEventListener('click', function(){load_email(email.id)});
  })
  element.addEventListener('mouseout', function(){
    this.style.background = "rgba(188, 186, 186, 0.727)";
  })
  document.querySelector('#emails-view').append(element);
}


function load_email(email_id) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    let arch = '';
    if (email.archived === true) {arch = 'Archived'}
    else {arch = 'Archive'}

    document.querySelector('#emails-view').innerHTML = 
    `<b>From:</b> ${email.sender} </br>
      <b>To:</b> ${email.recipients} </br>
      <b>Subject:</b> ${email.subject} </br>
      <b>Timestamp:</b> ${email.timestamp} </div>  </br>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <button class="btn btn-sm btn-outline-primary" id="read">${email.read}</button>
      <button class="btn btn-sm btn-outline-primary" id="archive-button">${arch}</button>
      <hr>
      ${email.body} </br>
      <hr> </br>
      For check: 
      Is read? : ${email.read} </br>
      Is archived? : ${email.archived} </br> 
    `
    console.log(email)
    // document.querySelector('#reply-button').onclick = function(){reply_email(email)};
    // document.querySelector('#read-button').onclick = function(){read_email(email) };
    // if (request.user === email.sender) {
    //   document.querySelector('#archive-button').style.display = 'invisible';
    // } else {
    //   document.querySelector('#archive-button').addEventListener('click', () => archive_email(email));
    // }
  })
}

function archive_email(email) {
  const email_id = email.id;
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  // console.log("isArchived: " + email.archived)
  load_mailbox('inbox')
}

    

