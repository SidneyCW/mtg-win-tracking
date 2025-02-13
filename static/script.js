// Wait for the DOM to fully load before running scripts
document.addEventListener("DOMContentLoaded", function () {
    // Initialize player input fields
    updatePlayers();

    // Attach form submission event listener
    document.getElementById('gameForm').addEventListener('submit', handleFormSubmit);
});

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
        // Create player input field
        const playerDiv = document.createElement('div');
        playerDiv.className = 'player-input';
        playerDiv.innerHTML = `
            <label for="player${i}">Player ${i}:</label>
            <input type="text" id="player${i}" placeholder="Player ${i} Name" oninput="updateWinnerOptions()" required />
        `;
        playersContainer.appendChild(playerDiv);

        // Create deck input field
        const deckDiv = document.createElement('div');
        deckDiv.className = 'deck-input';
        deckDiv.innerHTML = `
            <label for="deck${i}">Player ${i}'s Deck:</label>
            <input type="text" id="deck${i}" placeholder="Deck Name" required />
        `;
        decksContainer.appendChild(deckDiv);
    }

    updateWinnerOptions(); // Ensure winner dropdown updates when new players are added
}

// Function to update the winner dropdown options based on player names
function updateWinnerOptions() {
    const numPlayers = document.getElementById('numPlayers').value;
    const winnerSelect = document.getElementById('winner');

    // Clear previous options
    winnerSelect.innerHTML = '<option value="">Select Winner</option>';

    for (let i = 1; i <= numPlayers; i++) {
        const playerInput = document.getElementById(`player${i}`);
        if (playerInput) {
            const playerName = playerInput.value.trim();
            if (playerName) {
                const option = document.createElement('option');
                option.value = playerName;
                option.textContent = playerName;
                winnerSelect.appendChild(option);
            }
        }
    }
}

// Function to handle form submission
function handleFormSubmit(event) {
    event.preventDefault();

    const numPlayers = document.getElementById('numPlayers').value;
    const players = [];
    const decks = [];

    for (let i = 1; i <= numPlayers; i++) {
        const playerName = document.getElementById(`player${i}`).value.trim();
        const deckName = document.getElementById(`deck${i}`).value.trim();
        
        if (!playerName || !deckName) {
            alert("Please fill in all player names and decks.");
            return;
        }

        players.push(playerName);
        decks.push(deckName);
    }

    const winner = document.getElementById('winner').value.trim();

    if (!winner) {
        alert("Please select a winner.");
        return;
    }

    const data = {
        people: players,
        decks: decks,
        winner: winner
    };

    fetch('/new_game', {  // Send data to Flask backend
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Game data saved successfully!');
        } else {
            alert('Error saving game data.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send data. Please check your internet connection or server.');
    });
}
