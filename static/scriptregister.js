function registerDeck() {
    const playerName = document.getElementById("playerName").value.trim();
    const deckName = document.getElementById("deckName").value.trim();
    const responseMessage = document.getElementById("responseMessage");

    if (!playerName || !deckName) {
        responseMessage.textContent = "Please enter both player name and deck name.";
        responseMessage.style.color = "red";
        return;
    }

    fetch('/register_deck', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player: playerName, deck: deckName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            responseMessage.textContent = data.message;
            responseMessage.style.color = "green";
        } else {
            responseMessage.textContent = data.error;
            responseMessage.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        responseMessage.textContent = "Failed to register deck. Please try again.";
        responseMessage.style.color = "red";
    });
}
