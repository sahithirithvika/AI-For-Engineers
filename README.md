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

### Adaptive Learning Features
- Dynamic flashcards and personalized quizzes
- Spaced-repetition learning algorithms
- Multi-profile skill analytics and progress tracking
- Continuous retraining with user feedback

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
├── 📁 api/                      # Backend API server
│   ├── app.py                   # Main Flask API server
│   └── demo_app.py              # Demo API implementation
├── 📁 data/                     # Training datasets
│   ├── processed/               # Processed training data
│   │   ├── training_data.json
│   │   ├── engineering_math_dataset.json
│   │   ├── calculus_problems.json
│   │   ├── linear_algebra_problems.json
│   │   └── merged_training_data.json
│   └── merge_datasets.py        # Dataset merging utility
├── 📁 training/                 # ML model training pipeline
│   ├── model.py                 # Transformer model architecture
│   ├── data_pipeline.py         # Data loading and preprocessing
│   ├── train_model.py           # Training script with callbacks
│   ├── inference.py             # Inference engine
│   ├── config.py                # Model configuration
│   └── test_model.py            # Model testing utilities
├── 📁 models/                   # Trained models and checkpoints
│   ├── saved_models/            # Final trained model weights
│   └── checkpoints/             # Training checkpoints
├── 📁 frontend/                 # React web application
│   ├── src/                     # React source code
│   │   ├── App.js               # Main React component
│   │   ├── App.css              # Styling
│   │   └── index.js             # Entry point
│   ├── public/                  # Static assets
│   │   └── index.html           # HTML template
│   └── package.json             # Node.js dependencies
├── 📁 deployment/               # Container and deployment configs
│   ├── Dockerfile               # Container configuration
│   └── docker-compose.yml       # Multi-service orchestration
├── 📁 docs/                     # Project documentation
│   ├── ARCHITECTURE.md          # System architecture overview
│   ├── SETUP_GUIDE.md           # Detailed setup instructions
│   ├── QUICKSTART.md            # Quick start guide
│   ├── TROUBLESHOOTING.md       # Common issues and solutions
│   ├── ENHANCEMENTS.md          # Future enhancement plans
│   ├── CURRENT_STATUS.md        # Current project status
│   ├── CHECKLIST.md             # Development checklist
│   ├── IMPLEMENTATION_SUMMARY.md # Implementation details
│   └── FILES_CREATED.md         # File creation log
├── 📁 scripts/                  # Utility scripts
│   ├── check_syntax.py          # Code syntax checker
│   └── verify_structure.py      # Project structure validator
├── 📁 examples/                 # Example implementations
│   ├── demo_model_structure.py  # Model structure demo
│   ├── example_usage.py         # Usage examples
│   ├── test_api.html            # API testing interface
│   └── ui.html                  # Alternative UI demo
├── 📁 logs/                     # Training and application logs
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Main project documentation
├── 📄 LICENSE                   # MIT license
└── 📄 .gitignore                # Git ignore rules
```

## Getting Started

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ESpoorthy/AI-For-Engineers.git
   cd AI-For-Engineers
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the API server**
   ```bash
   python api/app.py
   ```
   Wait for "Model loaded successfully!" message. API runs on http://localhost:5001

4. **Start the frontend (new terminal)**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   Frontend runs on http://localhost:3000

5. **Access the application**
   Open http://localhost:3000 in your browser

### Alternative: Docker Deployment

```bash
docker-compose up --build
```

## Usage

### Web Interface
1. Navigate to http://localhost:3000
2. Enter engineering questions like:
   - "What is a deterministic finite automaton?"
   - "Explain the dot product of vectors"
   - "How do you solve linear equations?"
3. Click "Get Solution" and wait 5-10 seconds
4. View step-by-step explanations

### API Endpoints

**POST /api/solve** - Solve a single question
```bash
curl -X POST http://localhost:5001/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a vector?"}'
```

**GET /health** - Health check
```bash
curl http://localhost:5001/health
```

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

## Current Limitations

The model currently produces outputs with many unknown tokens because:
1. **Limited Training Data**: Only 22 Q&A examples (needs 1000+ for quality)
2. **Small Vocabulary**: 594 tokens (many engineering terms missing)
3. **Insufficient Training**: 10 epochs (needs 50-100+ with more data)

This demonstrates the complete ML pipeline - the model needs more training data to produce meaningful outputs.

## Development Workflow

1. Create feature branches with descriptive names
2. Keep commits small and meaningful
3. Open pull requests for code review
4. Ensure tests pass before merging
5. Avoid pushing directly to main branch

## Future Enhancements

### Short Term
1. Expand training dataset to 1000+ examples
2. Increase vocabulary size to 5000+ tokens
3. Implement beam search for better generation
4. Add temperature tuning for response quality

### Long Term
1. Fine-tune pre-trained models (GPT-2, BERT)
2. Implement retrieval-augmented generation (RAG)
3. Add support for mathematical notation rendering
4. Multi-modal support for diagrams and equations
5. Mobile-friendly interface and offline mode
6. OCR pipeline to support scanned or handwritten problems
7. Voice-based query input and spoken explanations
8. Dashboard for analytics, dataset drift detection and retraining triggers

## Team

1. **Sai Spoorthy Eturu** - Team lead, MLOps and deployment  
2. **Sahithi Rithvika Katakam** - Data engineer, scraping and dataset management  
3. **Shivani Edigi** - ML engineer, model design and evaluation  
4. **Hari Hansika Kommera** - Backend and frontend development

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
