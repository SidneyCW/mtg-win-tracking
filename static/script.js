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

    fetch("/start_game", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
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

                // PLEXUS BACKGROUND

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
                        onclick: { enable: true, mode: "push" },
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
                  