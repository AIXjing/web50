document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Add event listener to the form
  document.querySelector('#compose-form').onsubmit = send_email;

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}



function send_email(){
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value.replaceAll('\n', '</br>');

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
    setTimeout(console.log("result", result),100);
  })
  .catch(error => {
    alert("Error", error);
  });
  // refer to: https://cs50.stackexchange.com/questions/39316/cs50w-2020-project3-mail-does-not-show-new-sent-mail-after-sending/41032#41032?newreg=2663463db11c461bbc518e0140e5aae2
  setTimeout(function(){ load_mailbox('inbox'); }, 100);
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
      // console.log(emails);
      // show emails depending on clicked mailbox
      emails.forEach(email => {
        show_emails(email, mailbox);
      });
  })
}


// display maillist
function show_emails(email, mailbox) {
  const element = document.createElement('div');
  element.className = 'mail-view-box';
  element.innerHTML = `${email.sender}:    ${email.subject}  <div class="timestamp"> ${email.timestamp} </div>`;
  // if an email is read, the box show as grey, otherwise white
  if (email.read === true) {
    element.style.backgroundColor = 'rgba(188, 186, 186, 0.727)';
  } else {
    element.style.backgroundColor = 'white';
  }
  let bgcolor = element.style.backgroundColor;
  
  // when mouse hover on an email, change the email box format
  element.addEventListener('mouseenter', function(){
    this.style.backgroundColor = 'rgb(56,152,255)'; 
  })
  // once the email is open, it will be marked as read, i.e., the button will show 'Unread'.
  element.addEventListener('click', () => {
    const email_id = email.id;
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
    setTimeout(load_email, 100, email.id, mailbox);
  })
  element.addEventListener('mouseleave', function() {
    this.style.backgroundColor = bgcolor; 
  })
  document.querySelector('#emails-view').append(element);
}


// display a single email with details
function load_email(email_id, mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // hide all the mail view box
  document.querySelectorAll('.mail-view-box').forEach(function(box) {
    box.style.display = 'none';
  })

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Divide the email view into three parts
    // the 1st part: 
    const email_info = document.createElement('div');
    // pass email.read status to a string that can show in the button
    let read_state = '';
    if (email.read === true) {read_state = 'Unread'}
    else {read_state = 'Read'}
    console.log('read status: ', email.read);
    email_info.innerHTML = 
      `<b>From:</b> ${email.sender} </br>
      <b>To:</b> ${email.recipients} </br>
      <b>Subject:</b> ${email.subject} </br>
      <b>Timestamp:</b> ${email.timestamp} </div>  </br>
      <button class="btn btn-sm btn-outline-primary" id="reply_button">Reply</button>
      <button class="btn btn-sm btn-outline-primary" id="read_button">${read_state}</button>`
    document.querySelector('#emails-view').append(email_info);

    document.querySelector('#reply_button').addEventListener('click', () => reply_email(email));
    
    // click the read-button to change the 'read' status and return back to inbox
    document.querySelector('#read_button').addEventListener('click', () => {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: !read_state
        })
      })
      setTimeout(load_mailbox, 100, 'inbox');
      console.log("is_read: ", !read_state)
    })

    // the 2nd part: the Archive button
    // pass email.archived status to a string that can show in the button
    let arch = '';
    if (email.archived === true) {arch = 'Archived'}
    else {arch = 'Archive'}
    const archive_button = document.createElement('button');
    archive_button.innerHTML = ` ${arch}`;
    archive_button.classList = "btn btn-sm btn-outline-primary";
    archive_button.id = 'archive_button';
    archive_button.style.display = 'inline';
    if (mailbox !== 'sent') {
      email_info.append("  ");
      email_info.append(archive_button);
    } 
    // click the 'archive-button' to change 'archive' status and return back to inbox 
    archive_button.addEventListener('click', function() {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      setTimeout(load_mailbox, 100, 'inbox')
    })
    
    // the 3rd part: the body
    const email_body = document.createElement('div');
    email_body.innerHTML = 
      `<hr>
      ${email.body.replaceAll('\n', '</br>')} </br>`
    document.querySelector('#emails-view').append(email_body);
    // console.log(email)
  })
}
  


// reply to an email
function reply_email(email) {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    document.querySelector('#compose-recipients').value = email.sender;
    // check if subject is started with 'Re: ' already
    const old_subject = email.subject;
    console.log('old_subject: ', old_subject);
    if (old_subject.slice(0,3) !== 'Re:') {
      document.querySelector('#compose-subject').value = "Re: " + old_subject;
    } else {
      document.querySelector('#compose-subject').value = old_subject;
    }
    
    const pre_body = `\n ----------------------------- \n ${email.timestamp} ${email.sender}  wrote: \n \n ${email.body}`;
    document.querySelector('#compose-body').value = pre_body.replaceAll('</br>', '\n');

    // document.querySelector('#compose-form').onsubmit = send_email;
    document.querySelector('#compose-form').onsubmit = send_email;

    //TODO: Error message after submit despite succesfully submission
    //TODO: multi lines
}


    

