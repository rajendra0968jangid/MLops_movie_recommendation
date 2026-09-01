document
  .getElementById("searchBtn")
  .addEventListener("click", getRecommendations);
document
  .getElementById("movieInput")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      getRecommendations();
    }
  });

async function getRecommendations() {
  const movieInput = document.getElementById("movieInput");
  const movieTitle = movieInput.value.trim();

  const loadingDiv = document.getElementById("loading");
  const errorDiv = document.getElementById("error");
  const resultsSection = document.getElementById("resultsSection");
  const cardsGrid = document.getElementById("cardsGrid");

  // UI Reset
  errorDiv.classList.add("hidden");
  resultsSection.classList.add("hidden");
  cardsGrid.innerHTML = "";

  if (!movieTitle) {
    showError("Please type a movie name first!");
    return;
  }

  loadingDiv.classList.remove("hidden");

  try {
    // Fetch recommendations directly from your Flask pipeline
    const response = await fetch("http://localhost:5001/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ movie_title: movieTitle }),
    });

    const data = await response.json();
    loadingDiv.classList.add("hidden");

    if (!response.ok) {
      showError(data.error || "Something went wrong processing your request.");
      return;
    }

    // Render clean layout metrics served directly from the server structure
    data.recommendations.forEach((movie) => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
                <div class="poster-container">
                    <img src="${movie.poster}" alt="${movie.title} Poster" class="movie-poster" loading="lazy">
                    <span class="rating-badge">⭐ ${movie.rating}</span>
                </div>
                <div class="card-content">
                    <h3>${movie.title}</h3>
                    <div class="meta">Released: ${movie.year}</div>
                </div>
            `;
      cardsGrid.appendChild(card);
    });

    resultsSection.classList.remove("hidden");
  } catch (err) {
    loadingDiv.classList.add("hidden");
    showError(
      "Unable to reach the server. Make sure your backend server.py is running on port 5000!",
    );
    console.error(err);
  }
}

function showError(message) {
  const errorDiv = document.getElementById("error");
  errorDiv.innerText = message;
  errorDiv.classList.remove("hidden");
}

// CINEMATIC FLOATING PARTICLE SIMULATOR

const canvas = document.getElementById("particleCanvas");
const ctx = canvas.getContext("2d");

let particlesArray = [];
const numberOfParticles = 45; // Keeps it clean and lightweight without overhead

// Set canvas bounds to match the hero header section perfectly
function resizeCanvas() {
  canvas.width = canvas.parentElement.offsetWidth;
  canvas.height = canvas.parentElement.offsetHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// Blueprint constructor for a single particle node
class Particle {
  constructor() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.size = Math.random() * 2.5 + 0.5; // Varied subtle particle weights
    this.speedX = Math.random() * 0.4 - 0.2; // Slow, drifting horizontal speed
    this.speedY = Math.random() * -0.5 - 0.1; // Gentle drifting upward movement
    // Netflix red tint styling accents
    this.color = `rgba(229, 9, 20, ${Math.random() * 0.35 + 0.15})`;
  }

  update() {
    this.x += this.speedX;
    this.y += this.speedY;

    // If particle floats past the top border, reset it back to the bottom
    if (this.y < 0) {
      this.y = canvas.height;
      this.x = Math.random() * canvas.width;
    }
    // Handle horizontal bounds deflection wrap
    if (this.x < 0 || this.x > canvas.width) {
      this.speedX = -this.speedX;
    }
  }

  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.shadowBlur = 10; // Adds an ambient cinematic neon glow effect
    ctx.shadowColor = "rgba(229, 9, 20, 0.5)";
    ctx.fill();
    ctx.shadowBlur = 0; // Reset blur for optimal canvas performance
  }
}

// Populate the vector particle array system
function initParticles() {
  particlesArray = [];
  for (let i = 0; i < numberOfParticles; i++) {
    particlesArray.push(new Particle());
  }
}
initParticles();

// Continuous animation render loop execution
function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < particlesArray.length; i++) {
    particlesArray[i].update();
    particlesArray[i].draw();
  }
  requestAnimationFrame(animateParticles);
}
animateParticles();
