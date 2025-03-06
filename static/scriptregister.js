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




document.addEventListener("DOMContentLoaded", function () {
    console.log("Initializing Plexus background...");

    setTimeout(() => {
        if (typeof particlesJS !== "undefined") {
            initPlexusBackground();
            console.log("Plexus background initialized!");
        } else {
            console.error("❌ particles.js is not loaded.");
        }
    }, 500); // Ensure the script loads first
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
}

if (window.innerWidth < 500) {
    particlesJS("particles-js", {
        particles: {
            number: { value: 30 }, // Reduce number of particles
            move: { speed: 1.5 }   // Slow down movement
        }
    });
}