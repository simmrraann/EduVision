# MindMorph - Your Smart Learning Companion 🧠✨

MindMorph is an AI-powered educational platform that transforms your learning materials into interactive study tools. Upload documents and instantly generate flashcards, mindmaps, MCQs, and more!

## 🌟 Features

### 📚 Core Learning Tools
- **Smart Flashcards**: AI-generated Q&A cards for effective memorization
- **Interactive Mindmaps**: Visual topic mapping with hierarchical structures
- **Multiple Choice Questions**: Test your knowledge with AI-generated quizzes
- **Fill-in-the-Blanks**: Practice with contextual completion exercises
- **Spaced Repetition**: Optimized study schedules for better retention
- **AI Summary**: Intelligent document summarization and key insights

### 🤖 AI Assistant
- **Document Chatbot**: Ask questions about your uploaded content
- **Context-Aware Responses**: AI understands your specific document content
- **Real-time Interaction**: Get instant answers to your learning questions

### 🎨 Modern UI/UX
- **Beautiful Snow Effect**: Animated particle background
- **Responsive Design**: Works perfectly on all devices
- **Modern Glassmorphism**: Sleek, modern interface design
- **Interactive Elements**: Hover effects, animations, and smooth transitions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (optional, for enhanced AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mindmorph.git
   cd mindmorph
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Usage Guide

### 1. Upload Your Document
- Supported formats: PDF, PNG, JPG, JPEG
- Drag and drop or click to upload
- The system will automatically extract text content

### 2. Generate Learning Materials
Click any of the feature buttons to generate:
- **Flashcards**: Perfect for memorization
- **Mindmaps**: Visual learning and concept mapping
- **MCQs**: Test your understanding
- **Fill-in-the-Blanks**: Practice active recall
- **Study Schedule**: Optimized spaced repetition plan
- **AI Summary**: Key insights and overview

### 3. Chat with AI Assistant
- Click the chat button (bottom right)
- Ask questions about your uploaded content
- Get instant, context-aware answers

## 🛠️ Technical Architecture

### Backend
- **Flask**: Web framework
- **OpenAI API**: Advanced AI capabilities
- **Transformers**: Local AI fallback
- **Pillow**: Image processing
- **PyPDF2**: PDF text extraction

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive features
- **tsParticles**: Animated background effects
- **Mermaid.js**: Mindmap visualization
- **Font Awesome**: Beautiful icons

### Key Components
```
mindmorph/
├── app.py                 # Main Flask application
├── llm_engine.py         # AI/LLM integration
├── utils/
│   ├── generator.py      # Content generation functions
│   ├── ocr.py           # Image text extraction
│   ├── parser.py        # PDF text extraction
│   ├── database.py      # Data persistence
│   ├── spaced.py        # Spaced repetition logic
│   └── emailer.py       # Email notifications
├── static/
│   ├── style.css        # Modern styling
│   └── script.js        # Interactive features
└── templates/
    └── index.html       # Main interface
```

## 🎯 Advanced Features

### Spaced Repetition System
- Intelligent review scheduling
- Email reminders (Gmail integration)
- Progress tracking
- Adaptive learning intervals

### Mindmap Visualization
- Interactive node-based diagrams
- Zoom and pan capabilities
- Color-coded topic branches
- Export functionality

### AI-Powered Content Generation
- Context-aware question generation
- Multiple difficulty levels
- Subject-specific adaptations
- Continuous learning improvements

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Customization
- Modify `static/style.css` for UI changes
- Update `utils/generator.py` for content generation logic
- Adjust `llm_engine.py` for different AI models

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t mindmorph .
docker run -p 5000:5000 mindmorph
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- The Flask community for the excellent web framework
- Font Awesome for beautiful icons
- tsParticles for the amazing particle effects

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mindmorph/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mindmorph/discussions)
- **Email**: support@mindmorph.ai

---

Made with ❤️ for students and lifelong learners everywhere!
