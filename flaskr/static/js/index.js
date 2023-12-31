function handleSubmit(event) {
  // Prevent default submit event
  event.preventDefault();

  // Select HTML elements
  const usersList = document.querySelector(".users-list");
  const form = event.target;
  const submitBtn = form.querySelector("button[type='submit']");
  const buttons = usersList.querySelectorAll("button[type='submit']");

  // Create loading spinner to the button
  const div = document.createElement('div');
  div.classList.add("spinner-border");
  div.role = "status";
  const span = document.createElement('span');
  span.classList.add("visually-hidden");
  span.appendChild(document.createTextNode("Loading..."));
  div.appendChild(span);
  submitBtn.appendChild(div);

  // Disable the buttons
  for (let btn of buttons)
  {
    btn.disabled = true;
  }

  // Submit the form
  form.submit();
}