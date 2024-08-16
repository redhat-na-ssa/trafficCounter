window.onload = function() {
    const imageElement = document.getElementById("image");
    const frameElement = document.getElementById("frame");
    const secondsElement = document.getElementById("seconds");
    const losElement = document.getElementById("los");

    async function updateData() {
        const response = await fetch("/latest-data");
        const data = await response.json();
        
        imageElement.src = data.image;
        frameElement.textContent = data.frame;
        secondsElement.textContent = data.seconds;
        losElement.textContent = data.los;
    }

    setInterval(updateData, 5000);  // Fetch the latest data every 5 seconds
};
