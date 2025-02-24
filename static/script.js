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


















document.addEventListener("DOMContentLoaded", function () {
    console.log("Initializing Plexus background...");
    
    setTimeout(() => {
        if (typeof particlesJS !== "undefined") {
            initPlexusBackground();
            console.log("Plexus background initialized!");
        } else {
            console.error("❌ particles.js is not loaded.");
        }
    }, 500); // Ensures the script loads first
});



// Function to initialize the Plexus background
function initPlexusBackground() {
  particlesJS("particles-js", {
      particles: {
          number: { value: 80, density: { enable: true, value_area: 200 } },
          color: { value: "#ffffff" },
          shape: {
              type: "circle",
              stroke: { width: 0, color: "#000000" },
              polygon: { nb_sides: 4 },
              image: { src: "img/github.svg", width: 50, height: 50 }
          },
          opacity: {
              value: 0.5,
              random: false,
              anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false }
          },
          size: {
              value: 3,
              random: true,
              anim: { enable: false, speed: 40, size_min: 0.1, sync: false }
          },
          line_linked: {
              enable: true,
              distance: 120,
              color: "#ffffff",
              opacity: 0.4,
              width: 1
          },
          move: {
              enable: true,
              speed: 2.5,
              direction: "none",
              random: false,
              straight: false,
              out_mode: "out",
              bounce: false,
              attract: { enable: false, rotateX: 300, rotateY: 600 }
          }
      },
      interactivity: {
          detect_on: "window",
          events: {
              onhover: { enable: true, mode: "grab" },
              resize: true
          },
          modes: {
              grab: { distance: 150, line_linked: { opacity: 1 } },
              bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
              repulse: { distance: 80, duration: 0.4 },
              push: { particles_nb: 4 },
              remove: { particles_nb: 2 }
          }
      },
      retina_detect: true
  });

  var count_particles, stats, update;
  stats = new Stats();
  stats.setMode(0);
  stats.domElement.style.position = "absolute";
  stats.domElement.style.left = "0px";
  stats.domElement.style.top = "0px";
  document.body.appendChild(stats.domElement);
  count_particles = document.querySelector(".js-count-particles");
  update = function() {
      stats.begin();
      stats.end();
      if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {
          count_particles.innerText = window.pJSDom[0].pJS.particles.array.length;
      }
      requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}