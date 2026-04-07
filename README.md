# AI for Engineers - MLOps-Based Problem Solver

AI for Engineers is an intelligent, MLOps-powered learning assistant built for engineering students and recent graduates. The system uses a custom transformer-based language model to provide step-by-step solutions for engineering problems, emphasizing conceptual understanding over rote memorization.

## The Challenge: Rote Memorization

Engineering mathematics demands profound foundational knowledge and conceptual clarity. Current AI tools frequently function as mere high-powered calculators, offering final answers devoid of context. This approach incentivizes rote memorization and restricts the development of genuine problem-solving capabilities.

## Our Solution: Conceptual Mastery

Our intelligent learning assistant serves as a virtual lecturer that:
- Deconstructs complex mathematical problems into manageable stages
- Guides students through the logical progression behind each equation
- Prioritizes methodology over the final output
- Cultivates rigorous analytical skills essential for real-world engineering

## Key Features

### Virtual Lecturer
Delivers step-by-step guidance that mirrors traditional university teaching, explaining the rationale behind every mathematical operation.

### Enhanced Mathematical Reasoning
- **Pattern Matching Engine**: Correctly identifies problem types (complex numbers, differential equations, etc.)
- **Step-by-Step Solutions**: Detailed breakdown of solution methodology
- **Concept Identification**: Explains underlying mathematical concepts
- **Verification Methods**: Shows how to verify solutions
- **Educational Tips**: Provides learning guidance and best practices

### Interactive Learning Games
- **🧩 Step Builder**: Arrange solution steps in correct order
- **🎯 Concept Matcher**: Match mathematical concepts with definitions
- **⚡ Formula Quest**: Complete mathematical formulas
- **📊 Visual Solver**: Interactive mathematical visualizations

### ChatGPT-like Interface
- **Persistent Chat History**: All conversations saved and accessible
- **Sidebar Navigation**: Easy access to games, settings, and chat history
- **Voice Input**: Speak questions naturally using speech recognition
- **Camera Integration**: Capture images for visual problem solving
- **Dark Theme**: Professional dark interface with glassmorphism effects

### Custom Transformer Model
Built from scratch using TensorFlow/Keras with:
- 6 transformer layers with 8 attention heads each
- 256 embedding dimensions, 512 feed-forward dimensions
- 8.2 million parameters optimized for engineering problems
- Causal masking for autoregressive text generation

### Complete ML Pipeline
- Data preprocessing and tokenization
- Model training with checkpointing and validation
- Inference engine for real-time question answering
- REST API for integration with web applications

### Modern Web Interface
- React-based frontend with responsive design
- Real-time communication with backend API
- Error handling and user feedback
- Multiple interface options (Enhanced UI, React, Demos)

## Technical Architecture

### Model Architecture
- Token Embedding Layer: Converts tokens to 256-dimensional vectors
- Positional Encoding: Sine/cosine position information
- 6 Transformer Blocks with multi-head attention and feed-forward networks
- Output Layer: Projects to vocabulary for next token prediction

### Backend
- Flask API server with CORS support
- Model loading and inference management
- Structured response formatting with step extraction

### Frontend
- React application with modern UI components
- Form handling for question submission
- Real-time answer display with error handling

### Data Pipeline
- JSON-based training data format
- Text preprocessing and tokenization
- Sequence padding and batch processing

## Competitive Advantage

| Feature | Conventional Solvers | Generic LLM Chatbots | AI for Engineers |
|---------|---------------------|---------------------|------------------|
| Provides Final Answers | ✓ Yes | ✓ Yes | ✓ Yes |
| Step-by-Step Methodology | ✗ No | Often Flawed | ✓ Mathematically Verified |
| Adaptive Revision & Flashcards | ✗ No | ✗ No | ✓ Core Feature |
| Multi-Profile Skill Analytics | ✗ No | ✗ No | ✓ Integrated Dashboard |

## Project Structure

```
AI-For-Engineers/
├── 📚 Core Application
│   ├── api/                     # Backend API services
│   │   ├── app.py              # Main Flask API
│   │   ├── demo_app.py         # Demo application
│   │   ├── demo_math_api.py    # Enhanced mathematical API
│   │   └── enhanced_math_api.py
│   │
│   ├── ui/                      # Main user interface
│   │   └── index.html          # ChatGPT-like interface with games
│   │
│   ├── frontend/               # React application
│   │   ├── src/                # React source code
│   │   │   ├── App.js          # Main React component
│   │   │   ├── App.css         # Styling
│   │   │   ├── EnhancedMathApp.js
│   │   │   ├── GameifiedLearning.js
│   │   │   └── index.jsx       # Entry point
│   │   ├── public/             # Static assets
│   │   │   └── index.html      # HTML template
│   │   ├── package.json        # Node.js dependencies
│   │   └── vite.config.js      # Vite configuration
│   │
│   └── servers/                # Server utilities
│       ├── serve_ui.py         # UI server (port 8080)
│       └── server.py           # Alternative server
│
├── 🧮 Machine Learning
│   ├── training/               # Model training
│   │   ├── enhanced_math_model.py
│   │   ├── train_model.py
│   │   ├── inference.py
│   │   ├── model.py            # Transformer model architecture
│   │   ├── data_pipeline.py    # Data loading and preprocessing
│   │   └── config.py           # Model configuration
│   │
│   ├── data/                   # Datasets
│   │   ├── processed/          # Processed datasets
│   │   │   ├── training_data.json
│   │   │   ├── engineering_math_dataset.json
│   │   │   ├── calculus_problems.json
│   │   │   ├── linear_algebra_problems.json
│   │   │   ├── comprehensive_math_dataset.json
│   │   │   └── merged_training_data.json
│   │   ├── enhanced_math_dataset.py
│   │   ├── engineering_curriculum_dataset.py
│   │   └── merge_datasets.py   # Dataset merging utility
│   │
│   └── models/                 # Trained models
│       ├── checkpoints/        # Model checkpoints
│       └── saved_models/       # Final models
│
├── 🔧 Development & Testing
│   ├── examples/               # Code examples
│   │   ├── demo_model_structure.py
│   │   ├── example_usage.py
│   │   └── test_api.html
│   │
│   ├── demos/                  # Demo applications
│   │   ├── app.html            # Single-page demo
│   │   ├── demo.html           # Basic demo
│   │   └── test_integration.html
│   │
│   ├── scripts/                # Utility scripts
│   │   ├── check_syntax.py
│   │   └── verify_structure.py
│   │
│   └── tests/                  # Test files
│
├── 📖 Documentation
│   ├── docs/                   # Project documentation
│   │   ├── ARCHITECTURE.md
│   │   ├── SETUP_GUIDE.md
│   │   ├── QUICKSTART.md
│   │   ├── TROUBLESHOOTING.md
│   │   ├── ENHANCED_MATH_SYSTEM.md
│   │   ├── GAMIFIED_LEARNING_SYSTEM.md
│   │   └── IMPLEMENTATION_SUMMARY.md
│   │
│   ├── PROJECT_STRUCTURE.md    # This file
│   ├── NAVIGATION.md           # Navigation guide
│   └── README.md               # Main documentation
│
├── 🚀 Deployment
│   ├── deployment/             # Deployment configurations
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   └── logs/                   # Application logs
│
└── 📋 Configuration
    ├── .gitignore              # Git ignore rules
    ├── LICENSE                 # Project license
    └── requirements.txt        # Python dependencies
```

## Getting Started

### Quick Start (Single Command)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ESpoorthy/AI-For-Engineers.git
   cd AI-For-Engineers
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the unified application**
   ```bash
   python3 app.py
   ```

4. **Access the application**
   Open http://localhost:8080 in your browser

That's it! The entire application (UI + API) runs on a single URL.

### Alternative: Docker Deployment

```bash
docker-compose up --build
```

## Application Interface

### 🎮 Unified Application
- **URL**: http://localhost:8080
- **Start**: `python3 app.py`
- **Features**: 
  - Complete application in single URL
  - ChatGPT-style sidebar with persistent chat history
  - Interactive learning games (Step Builder, Concept Matcher, etc.)
  - Voice input and camera functionality
  - Mathematical background patterns
  - User profile and settings
  - Dark theme with glassmorphism effects
  - Built-in API endpoints for mathematical reasoning

## Usage

### Unified Application Interface
1. Start the application: `python3 app.py`
2. Navigate to http://localhost:8080
3. Features available:
   - **Chat History**: All conversations saved in sidebar
   - **Learning Games**: Click games in sidebar (Step Builder, Concept Matcher, etc.)
   - **Voice Input**: Click microphone icon to speak questions
   - **Camera Input**: Click camera icon to capture images
   - **Settings**: Access user preferences and export options

### Example Questions
Enter engineering questions like:
- "Find the polar form of the complex number z = 1 + i"
- "Solve the differential equation dy/dx + 2y = 4"
- "Calculate the Laplace transform of e^(-2t)"
- "Find the 12th term of the AP: 4, 9, 14, ..."

Click "Send" and get step-by-step solutions with mathematical reasoning.

### Mathematical Capabilities
The system supports complete M1-M4 engineering mathematics curriculum:
- **M1**: Differential/Integral Calculus, Matrix Theory, Sequences & Series
- **M2**: Vector Calculus, ODEs, Complex Numbers, Laplace Transforms
- **M3**: Fourier Analysis, PDEs, Probability/Statistics, Z-Transforms  
- **M4**: Numerical Methods, Optimization, Discrete Mathematics

### API Endpoints

**POST /api/solve** - Solve a mathematical question
```bash
curl -X POST http://localhost:8080/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "Find the derivative of x^2 + 3x"}'
```

**GET /health** - Health check
```bash
curl http://localhost:8080/health
```

**Response Format:**
```json
{
  "success": true,
  "question": "Find the derivative of x^2 + 3x",
  "solution": "The derivative is 2x + 3",
  "steps": [
    "Apply the power rule to each term",
    "d/dx(x²) = 2x", 
    "d/dx(3x) = 3",
    "Combine: 2x + 3"
  ],
  "confidence": "high",
  "api_version": "2.0"
}

### Training Custom Models

1. **Prepare training data** in JSON format:
   ```json
   [
     {
       "question": "What is a DFA?",
       "answer": "Step 1: A DFA is... Step 2: It consists of..."
     }
   ]
   ```

2. **Train the model**:
   ```bash
   python training/train_model.py
   ```

3. **Test inference**:
   ```bash
   python training/test_model.py
   ```

## Model Details

### Architecture Specifications
- **Model Type**: Transformer-based Language Model
- **Parameters**: 8,292,624 total parameters
- **Vocabulary Size**: 594 tokens (expandable to 10,000)
- **Max Sequence Length**: 512 tokens
- **Embedding Dimension**: 256
- **Attention Heads**: 8 per layer
- **Transformer Layers**: 6
- **Feed-Forward Dimension**: 512
- **Activation**: GELU
- **Dropout Rate**: 0.1

### Training Configuration
- **Optimizer**: Adam (learning rate: 0.0001)
- **Loss Function**: Sparse Categorical Crossentropy
- **Batch Size**: 8
- **Gradient Clipping**: 1.0
- **Callbacks**: ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

### Performance Metrics
- **Training Time**: ~2 minutes for 10 epochs (CPU)
- **Model Size**: 95MB
- **Inference Speed**: 5-10 seconds per question (CPU)
- **Current Accuracy**: 7.59% (limited by training data size)

## Current Status & Recent Improvements

### ✅ Completed Features
- **Unified Application**: Single URL (http://localhost:8080) runs entire application
- **Enhanced Mathematical API**: Supports M1-M4 engineering mathematics with pattern matching
- **ChatGPT-like Interface**: Sidebar with chat history, games, and user settings
- **Interactive Learning Games**: 4 different game types for concept reinforcement
- **Voice & Camera Input**: Speech recognition and image capture capabilities
- **Simplified Deployment**: One command starts everything (`python3 app.py`)

### 🔧 Recent Fixes
- **Single Application**: Combined UI and API into unified Flask application
- **Pattern Matching Bug**: Fixed issue where complex number problems were incorrectly identified
- **Simplified Architecture**: Eliminated need for multiple servers and ports
- **UI Enhancement**: Improved mathematical background patterns (larger size)
- **Chat Persistence**: Added localStorage for chat history across sessions

### 🎯 Current Capabilities
- Correctly solves complex numbers, differential equations, calculus problems
- Provides step-by-step solutions with mathematical reasoning
- Supports voice input and camera integration
- Maintains persistent chat history
- Offers interactive learning through games
- Single command deployment for entire application

## Development Workflow

1. Create feature branches with descriptive names
2. Keep commits small and meaningful
3. Open pull requests for code review
4. Ensure tests pass before merging
5. Avoid pushing directly to main branch

## Future Enhancements

### Short Term
1. **Model Improvements**
   - Expand training dataset to 1000+ examples
   - Increase vocabulary size to 5000+ tokens
   - Implement beam search for better generation
   - Add temperature tuning for response quality

2. **Interface Enhancements**
   - Export chat history functionality
   - Advanced user settings and preferences
   - Mobile app development
   - Offline mode capabilities

### Long Term
1. **Advanced AI Features**
   - Fine-tune pre-trained models (GPT-2, BERT)
   - Implement retrieval-augmented generation (RAG)
   - Multi-modal support for diagrams and equations
   - OCR pipeline for scanned/handwritten problems

2. **Educational Platform**
   - Adaptive learning algorithms
   - Progress tracking and analytics
   - Personalized learning paths
   - Integration with LMS platforms

3. **Production Features**
   - Voice-based query input and spoken explanations
   - Dashboard for analytics and dataset drift detection
   - Auto-retraining triggers
   - Scalable cloud deployment

### Current Limitations
- Model needs more training data for complex problems
- Limited to text-based mathematical notation
- Requires internet connection for full functionality
- Voice recognition works best in Chrome browser

## Team

1. **Sai Spoorthy Eturu** - Team lead 
2. **Sahithi Rithvika Katakam**  
3. **Shivani Edigi**  
4. **Hari Hansika Kommera** 

**Under the guidance of:**  
**A Naga Kalyani** - Assistant Professor, Dept of CSE (AI&ML)  
BVRIT Hyderabad College of Engineering for Women

## Development Workflow

1. Create a feature branch for each task using a descriptive name
2. Work locally and keep commits small and meaningful
3. Push the branch and open a pull request to main for review
4. Ensure tests run in CI and address review comments before merging
5. Avoid pushing directly to main

## License

This repository is published under the MIT License and is intended for academic and research purposes. Please include attribution if you reuse significant parts of the code or datasets.

## Support

Use the GitHub Issues section to report bugs, request features, or suggest new datasets. Include input examples and expected behavior to help reproduce issues.

## Repository

**GitHub**: https://github.com/ESpoorthy/AI-For-Engineers.git

---

## Building Better Engineers

Our ultimate goal is to shift the educational paradigm away from mere answer-finding towards profound conceptual understanding, equipping the next generation with genuine analytical capabilities.
