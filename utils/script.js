document.querySelectorAll('.menu-link').forEach(link => {
    link.addEventListener("click", function(event) {
        console.log(`Clicked: ${event.target.textContent}`);
    });
});


// Wait for the DOM to fully load before running scripts
document.addEventListener("DOMContentLoaded", function () {
  updatePlayers();
  fetchDecks(); // Load decks from MySQL when the page loads
  setTimeout(initPlexusBackground, 500); // Delay Plexus initialization to prevent conflicts
});

// Fetch available decks from MySQL and populate dropdowns
function fetchDecks(playerName) {
    console.log(`Fetching decks for: ${playerName}`);

    return fetch(`/get_decks?player=${encodeURIComponent(playerName)}`)
        .then(response => response.json())
        .then(data => {
            console.log("Decks received:", data);

            if (data.decks && data.decks.length > 0) {
                window.availableDecks = data.decks;
            } else {
                console.warn("No decks found for", playerName);
                window.availableDecks = [];
            }
        })
        .catch(error => {
            console.error("Error fetching decks:", error);
            window.availableDecks = [];
        });
}




// Function to update player input fields dynamically
function updatePlayers() {
    console.log("updatePlayers() is running");

    const numPlayers = document.getElementById("numPlayers").value;
    const playersContainer = document.getElementById("playersContainer");
    const decksContainer = document.getElementById("decksContainer");
    const winnerSelect = document.getElementById("winner");

    // Clear existing content
    playersContainer.innerHTML = "";
    decksContainer.innerHTML = "";
    winnerSelect.innerHTML = '<option value="">Select Winner</option>';

    for (let i = 1; i <= numPlayers; i++) {
        console.log(`Adding Player ${i}`);

        // Create player input field
        const playerDiv = document.createElement("div");
        playerDiv.className = "player-input";
        playerDiv.innerHTML = `
            <label for="player${i}">Player ${i}:</label>
            <input type="text" id="player${i}" placeholder="Enter Player Name" oninput="fetchDecksForPlayer(${i})" required />
        `;
        playersContainer.appendChild(playerDiv);

        // Create deck selection dropdown
        const deckDiv = document.createElement("div");
        deckDiv.className = "deck-input";
        deckDiv.innerHTML = `
            <label for="deck${i}">Player ${i}'s Deck:</label>
            <select id="deck${i}" required>
                <option value="">Select Deck</option>
            </select>
        `;
        decksContainer.appendChild(deckDiv);
    }

    console.log("updatePlayers() finished");

  
}

// Fetch decks based on player's name input
function fetchDecksForPlayer(playerIndex) {
    const playerName = document.getElementById(`player${playerIndex}`).value.trim();

    if (playerName) {
        fetchDecks(playerName).then(() => {
            // Populate deck dropdown once data is loaded
            const deckSelect = document.getElementById(`deck${playerIndex}`);
            deckSelect.innerHTML = '<option value="">Select Deck</option>';

            window.availableDecks.forEach(deck => {
                const option = document.createElement("option");
                option.value = deck;
                option.textContent = deck;
                deckSelect.appendChild(option);
            });
        });
    }

    updateWinnerOptions();
}






// Function to update the winner dropdown based on player names
function updateWinnerOptions() {
    const numPlayers = document.getElementById("numPlayers").value;
    const winnerSelect = document.getElementById("winner");

    // Clear previous options
    winnerSelect.innerHTML = '<option value="">Select Winner</option>';
    console.log("Updating Winner Dropdown...");

    for (let i = 1; i <= numPlayers; i++) {
        const playerInput = document.getElementById(`player${i}`);
        
        if (playerInput) {
            const playerName = playerInput.value.trim();
            console.log(`Checking Player ${i}: ${playerName}`);

            if (playerName) {
                const option = document.createElement("option");
                option.value = playerName;
                option.textContent = playerName;
                winnerSelect.appendChild(option);
                console.log(`✅ Added winner option: ${playerName}`);
            } else {
                console.warn(`⚠️ Player ${i} has no name yet.`);
            }
        } else {
            console.error(`❌ Player input field not found for Player ${i}`);
        }
    }
}



// Function to handle form submission
function submitGameData() {
  const numPlayers = document.getElementById("numPlayers").value;
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

  const winner = document.getElementById("winner").value.trim();

  if (!winner) {
      alert("Please select a winner.");
      return;
  }

  const data = {
      people: players,
      decks: decks,
      winner: winner
  };

  fetch('/start_game', {  // Corrected endpoint for MySQL submission
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