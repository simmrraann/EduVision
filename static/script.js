// Enhanced Snow Effect
tsParticles.load("tsparticles", {
    background: {
      color: {
        value: "transparent"
      }
    },
    particles: {
      number: { 
        value: 150,
        density: {
          enable: true,
          value_area: 800
        }
      },
      color: { value: "#ffffff" },
      shape: { 
        type: "circle",
        stroke: {
          width: 0,
          color: "#000000"
        }
      },
      opacity: { 
        value: 0.8,
        random: true,
        anim: {
          enable: true,
          speed: 1,
          opacity_min: 0.1,
          sync: false
        }
      },
      size: { 
        value: 3,
        random: true,
        anim: {
          enable: true,
          speed: 2,
          size_min: 0.1,
          sync: false
        }
      },
      move: {
        enable: true,
        speed: 1.5,
        direction: "bottom",
        random: true,
        straight: false,
        out_mode: "out",
        bounce: false,
        attract: {
          enable: false,
          rotateX: 600,
          rotateY: 1200
        }
      }
    },
    interactivity: {
      detect_on: "canvas",
      events: {
        onhover: { 
          enable: true, 
          mode: "repulse" 
        },
        onclick: { 
          enable: true, 
          mode: "push" 
        },
        resize: true
      },
      modes: {
        repulse: { 
          distance: 100,
          duration: 0.4 
        },
        push: { 
          particles_nb: 4 
        }
      }
    },
    retina_detect: true
});

// Global variables
let currentText = "";
let isLoading = false;

// Feature testing functions
async function testFeature(featureType) {
    if (isLoading) return;
    
    const button = event.target;
    const originalText = button.textContent;
    
    // Show loading state
    button.textContent = "Generating...";
    button.disabled = true;
    isLoading = true;
    
    try {
        let endpoint = '';
        let data = {};
        
        switch(featureType) {
            case 'flashcards':
                endpoint = '/generate_flashcards';
                break;
            case 'mindmaps':
                endpoint = '/generate_mindmap';
                break;
            case 'fitb':
                endpoint = '/generate_fillups';
                break;
            case 'spaced':
                endpoint = '/generate_schedule';
                break;
            case 'mcq':
                endpoint = '/generate_mcqs';
                break;
            case 'summary':
                endpoint = '/generate_summary';
                break;
        }
        
        data = { text: currentText };
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.error) {
            showNotification(result.error, 'error');
        } else {
            displayOutput(result.output, featureType);
            showNotification(`${featureType.charAt(0).toUpperCase() + featureType.slice(1)} generated successfully!`, 'success');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error generating content. Please try again.', 'error');
    } finally {
        // Reset button
        button.textContent = originalText;
        button.disabled = false;
        isLoading = false;
    }
}

// Display output in a modal
function displayOutput(output, featureType) {
    // Remove existing modal
    const existingModal = document.getElementById('outputModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'outputModal';
    modal.className = 'modal';
    
    let formattedOutput = output;
    
    // Try to format JSON output
    try {
        const parsed = JSON.parse(output);
        if (Array.isArray(parsed)) {
            formattedOutput = parsed.map(item => {
                if (typeof item === 'object') {
                    return Object.entries(item).map(([key, value]) => 
                        `<strong>${key}:</strong> ${value}`
                    ).join('<br>');
                }
                return item;
            }).join('<br><br>');
        } else {
            formattedOutput = Object.entries(parsed).map(([key, value]) => 
                `<strong>${key}:</strong> ${value}`
            ).join('<br>');
        }
    } catch (e) {
        // If not JSON, display as is
        formattedOutput = output.replace(/\n/g, '<br>');
    }
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>${featureType.charAt(0).toUpperCase() + featureType.slice(1)} Output</h2>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-body">
                <div class="output-content">${formattedOutput}</div>
            </div>
            <div class="modal-footer">
                <button onclick="closeModal()">Close</button>
                <button onclick="copyToClipboard('${output.replace(/'/g, "\\'")}')">Copy</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    const modal = document.getElementById('outputModal');
    if (modal) {
        modal.remove();
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy to clipboard', 'error');
    });
}

// Show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Chatbot functionality
let chatHistory = [];

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addChatMessage('user', message);
    input.value = '';
    
    // Show typing indicator
    addChatMessage('bot', 'Thinking...', true);
    
    // Send to backend
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: message,
            context: currentText
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        
        if (data.error) {
            addChatMessage('bot', data.error);
        } else {
            addChatMessage('bot', data.response);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addChatMessage('bot', 'Sorry, I encountered an error. Please try again.');
    });
}

function addChatMessage(sender, message, isTyping = false) {
    const chatContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message`;
    
    if (isTyping) {
        messageDiv.classList.add('typing-indicator');
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <span class="sender">${sender === 'user' ? 'You' : 'AI'}</span>
            <p>${message}</p>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// File upload handling
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        
        // Show loading
        showNotification('Processing file...', 'info');
        
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Update the page content
            document.documentElement.innerHTML = html;
            showNotification('File processed successfully!', 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error processing file', 'error');
        });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Show file info
                const fileInfo = document.getElementById('fileInfo');
                const fileName = document.getElementById('fileName');
                if (fileInfo && fileName) {
                    fileName.textContent = file.name;
                    fileInfo.style.display = 'block';
                }
                
                // Enable submit button
                const submitBtn = document.getElementById('submitBtn');
                if (submitBtn) {
                    submitBtn.disabled = false;
                }
            }
        });
    }
    
    // Handle form submission
    const uploadForm = document.querySelector('.upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = this.querySelector('input[type="file"]');
            if (!fileInput.files[0]) {
                e.preventDefault();
                showNotification('Please select a file first!', 'error');
                return;
            }
            
            // Show loading
            const submitBtn = document.getElementById('submitBtn');
            if (submitBtn) {
                submitBtn.value = 'Processing...';
                submitBtn.disabled = true;
            }
            
            showNotification('Processing your document...', 'info');
        });
    }
    
    // Chat input enter key
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('outputModal');
        if (event.target === modal) {
            closeModal();
        }
    });
});

// Mindmap visualization (using Mermaid.js)
function renderMindmap(data) {
    try {
        const parsed = JSON.parse(data);
        let mermaidCode = 'graph TD\n';
        
        // Convert JSON structure to Mermaid format
        function addNodes(obj, parentId = 'A') {
            let nodeId = parentId;
            Object.entries(obj).forEach(([key, value], index) => {
                const childId = `${parentId}${index + 1}`;
                mermaidCode += `    ${parentId}["${key}"] --> ${childId}["${value}"]\n`;
                if (typeof value === 'object' && value !== null) {
                    addNodes(value, childId);
                }
            });
        }
        
        addNodes(parsed);
        
        // Render with Mermaid
        mermaid.render('mindmap', mermaidCode).then(({svg}) => {
            const container = document.getElementById('mindmapContainer');
            container.innerHTML = svg;
        });
        
    } catch (e) {
        console.error('Error rendering mindmap:', e);
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 3000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            max-width: 400px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            background: ${type === 'success' ? 'linear-gradient(45deg, #28a745, #20c997)' : 
                         type === 'error' ? 'linear-gradient(45deg, #dc3545, #e74c3c)' : 
                         'linear-gradient(45deg, #17a2b8, #6f42c1)'};
        ">
            ${message}
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.querySelector('div').style.transform = 'translateX(0)';
    }, 100);
    
    // Hide notification after 3 seconds
    setTimeout(() => {
        notification.querySelector('div').style.transform = 'translateX(400px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Flashcard flip functionality (if on flashcards page)
function flipCard(button) {
    const card = button.closest('.flashcard-inner');
    const front = card.querySelector('.flashcard-front');
    const back = card.querySelector('.flashcard-back');
    
    if (front.style.display === 'none') {
        front.style.display = 'block';
        back.style.display = 'none';
    } else {
        front.style.display = 'none';
        back.style.display = 'block';
    }
}

// MCQ option selection (if on MCQs page)
function selectOption(element, selectedOption, correctAnswer) {
    // Remove previous selections from this question
    const card = element.closest('.mcq-card');
    const options = card.querySelectorAll('.mcq-option');
    options.forEach(opt => {
        opt.classList.remove('correct', 'incorrect');
    });
    
    // Add selection styling
    if (selectedOption === correctAnswer) {
        element.classList.add('correct');
    } else {
        element.classList.add('incorrect');
    }
    
    // Show result
    const result = card.querySelector('.mcq-result');
    const resultText = card.querySelector('.result-text');
    const correctAnswerText = card.querySelector('.correct-answer');
    
    if (selectedOption === correctAnswer) {
        result.style.background = 'rgba(0, 255, 0, 0.1)';
        result.style.border = '1px solid #00ff00';
        resultText.innerHTML = '<i class="fas fa-check-circle"></i> Correct!';
        resultText.style.color = '#00ff00';
    } else {
        result.style.background = 'rgba(255, 0, 0, 0.1)';
        result.style.border = '1px solid #ff0000';
        resultText.innerHTML = '<i class="fas fa-times-circle"></i> Incorrect!';
        resultText.style.color = '#ff0000';
        correctAnswerText.innerHTML = `Correct answer: ${correctAnswer}`;
    }
    
    result.style.display = 'block';
}

// Fill in the blanks answer checking (if on FIB page)
function checkAnswer(input) {
    const userAnswer = input.value.trim().toLowerCase();
    const correctAnswer = input.dataset.answer.toLowerCase();
    const card = input.closest('.fib-card');
    const result = card.querySelector('.fib-result');
    const resultText = card.querySelector('.result-text');
    const correctAnswerText = card.querySelector('.correct-answer');
    
    if (userAnswer === correctAnswer) {
        result.style.background = 'rgba(0, 255, 0, 0.1)';
        result.style.border = '1px solid #00ff00';
        resultText.innerHTML = '<i class="fas fa-check-circle"></i> Correct!';
        resultText.style.color = '#00ff00';
        input.style.borderColor = '#00ff00';
        input.style.background = 'rgba(0, 255, 0, 0.1)';
    } else if (userAnswer !== '') {
        result.style.background = 'rgba(255, 0, 0, 0.1)';
        result.style.border = '1px solid #ff0000';
        resultText.innerHTML = '<i class="fas fa-times-circle"></i> Incorrect!';
        resultText.style.color = '#ff0000';
        correctAnswerText.innerHTML = `Correct answer: ${input.dataset.answer}`;
        input.style.borderColor = '#ff0000';
        input.style.background = 'rgba(255, 0, 0, 0.1)';
    } else {
        result.style.display = 'none';
        input.style.borderColor = 'rgba(0, 255, 247, 0.3)';
        input.style.background = 'rgba(0, 0, 0, 0.3)';
        return;
    }
    
    result.style.display = 'block';
}