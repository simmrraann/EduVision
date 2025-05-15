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