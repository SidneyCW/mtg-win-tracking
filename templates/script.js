// Function to update the player input fields and decks dynamically
function updatePlayers() {
    const numPlayers = document.getElementById('numPlayers').value;
    const playersContainer = document.getElementById('playersContainer');
    const decksContainer = document.getElementById('decksContainer');
    const winnerSelect = document.getElementById('winner');

    // Clear existing content
    playersContainer.innerHTML = '';
    decksContainer.innerHTML = '';
    winnerSelect.innerHTML = '<option value="">Select Winner</option>';

    for (let i = 1; i <= numPlayers; i++) {
        // Create player input
        const playerDiv = document.createElement('div');
        playerDiv.className = 'player-input';
        playerDiv.innerHTML = `
            <label for="player${i}">Player ${i}:</label>
            <input type="text" name="player${i}" id="player${i}" placeholder="Player ${i} Name" onchange="updateWinnerOptions()" required />
        `;
        playersContainer.appendChild(playerDiv);

        // Create deck input
        const deckDiv = document.createElement('div');
        deckDiv.className = 'deck-input';
        deckDiv.innerHTML = `
            <label for="deck${i}">Player ${i}'s Deck:</label>
            <input type="text" name="deck${i}" id="deck${i}" placeholder="Deck Name" required />
        `;
        decksContainer.appendChild(deckDiv);

        // Add option to winner dropdown
        const option = document.createElement('option');
        option.value = `player${i}`;
        option.textContent = `Player ${i}`;
        winnerSelect.appendChild(option);
    }
}

// Function to update the winner dropdown options based on player names
function updateWinnerOptions() {
    const numPlayers = document.getElementById('numPlayers').value;
    const winnerSelect = document.getElementById('winner');

    // Clear and add default option
    winnerSelect.innerHTML = '<option value="">Select Winner</option>';

    for (let i = 1; i <= numPlayers; i++) {
        const playerName = document.getElementById(`player${i}`).value;
        const option = document.createElement('option');
        option.value = `player${i}`;
        option.textContent = playerName || `Player ${i}`;
        winnerSelect.appendChild(option);
    }
}

// Handle form submission and send data to the backend
document.getElementById('gameForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            alert('Data saved successfully!');
        } else {
            alert('Failed to save data.');
        }
    })
    .catch(error => console.error('Error:', error));
});
