function fetchLatestMessage() {
    fetch('/latest-message')
        .then(response => response.text())
        .then(data => {
            document.getElementById('message').innerText = data;
        });
}

// Fetch latest message every 1 second
setInterval(fetchLatestMessage, 1000);
