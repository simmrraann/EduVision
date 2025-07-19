tsParticles.load("tsparticles", {
    background: {
      color: {
        value: "transparent"
      }
    },
    particles: {
      number: { value: 120 },
      color: { value: "#ffffff" },
      shape: { type: "circle" },
      opacity: { value: 0.6 },
      size: { value: 2 },
      move: {
        enable: true,
        speed: 1
      }
    },
    interactivity: {
      events: {
        onhover: { enable: true, mode: "repulse" }
      },
      modes: {
        repulse: { distance: 50 }
      }
    }
  });

document.getElementById("flashcard-btn").addEventListener("click", () => {
document.getElementById("flashcard-output").style.display = "block";
});

document.getElementById("mcq-btn").addEventListener("click", () => {
document.getElementById("mcq-output").style.display = "block";
});

document.getElementById("mindmap-btn").addEventListener("click", () => {
  document.getElementById("mondmap-output").style.display = "block";
});

document.getElementById("fill_in_the_blank-btn").addEventListener("click", () => {
  document.getElementById("fill_in_the_blank-output").style.display = "block";
});


// Repeat for FIB, Mindmap, etc.