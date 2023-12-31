const socket = io({autoConnect: false});

socket.connect();

// Select HTML elements
const textareaInput = document.querySelector("#message-textarea");
const ul = document.querySelector("#chat-messages");

// Chat messages - convert UTC time to local time
for (let listElement of ul.children)
{
  let smallElement = listElement.querySelector("small");
  if (smallElement)
  {
    let localDate = new Date(smallElement.textContent).toLocaleString();
    smallElement.textContent = localDate;
  }
}

// Handle the form submission with Enter - create new message
textareaInput.addEventListener("keyup", function(event) {
  if (event.key == "Enter")
  {
    // Select HTML element
    const recipient = document.querySelector(".recipient-name")

    // Remove whitespaces
    let message = textareaInput.value.trim();

    // Emit the message, if there is not blank
    if (message.length > 0) 
    {
      // Get the resourceId from tha pathname
      let pathSegments = window.location.pathname.split("/")
      let resourceId = pathSegments[pathSegments.length - 1];

      socket.emit("private_message", {
        chatResourceId: resourceId,
        recipient: recipient.textContent,
        date: new Date().toISOString(),
        message: message,
      });
    }

    // Delete the textarea content and focus the textarea input
    textareaInput.value = "";
    textareaInput.focus();
  }
});

// Handle receiving a message from socket io server side code
socket.on("receive_message", function(data) {
  // Select HTML elements
  const ul = document.querySelector("#chat-messages");
  const noMessages = document.querySelector(".no-messages");
  const chatHeader = document.querySelector(".chat-header");
  const recipient = chatHeader.querySelector("span");

  // Create HTML elements
  let li = document.createElement("li");
  let usernameSpan = document.createElement("span");
  let messageSpan = document.createElement("span");
  let small = document.createElement("small");

  // Add texts to the message
  usernameSpan.appendChild(document.createTextNode(data["message_author"]))
  messageSpan.appendChild(document.createTextNode(data["message"]));

  // Add classes
  usernameSpan.classList.add("author");
  messageSpan.classList.add("message");
  small.classList.add("date");

  // Convert UTC time to local time
  let localDate = new Date(data["createdAt"]).toLocaleString();
  small.appendChild(document.createTextNode(localDate));

  // Add the parts of the message to the list element
  li.appendChild(usernameSpan);
  li.appendChild(messageSpan);
  li.appendChild(small);

  // Add sender or recipient classes
  if (recipient.textContent && data["message_author"] == recipient.textContent)
  {
    li.classList.add("recipient")
  }
  else
  {
    li.classList.add("sender", "bg-primary")
  }

  // Remove no messages text
  if (noMessages)
  {
    ul.removeChild(noMessages)
  }

  // Add new message to the proper place
  ul.prepend(li);
});
