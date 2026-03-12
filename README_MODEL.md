# AI for Engineers - Model Implementation

## Overview

This is a domain-specific transformer-based language model built with TensorFlow/Keras for engineering education. The model generates clear, step-by-step explanations for engineering questions.

## Architecture

### Model Components

1. **Token Embedding Layer**: Converts tokens to dense vectors (256 dimensions)
2. **Positional Encoding**: Adds position information using sine/cosine functions
3. **Transformer Blocks** (6 layers):
   - Multi-head attention (8 heads)
   - Feed-forward network (512 hidden units)
   - Layer normalization and residual connections
4. **Output Layer**: Projects to vocabulary size for next token prediction

### Model Parameters

- Vocabulary Size: 10,000 tokens
- Max Sequence Length: 512 tokens
- Embedding Dimension: 256
- Number of Attention Heads: 8
- Feed-Forward Dimension: 512
- Number of Transformer Layers: 6
- Dropout Rate: 0.1

## Usage

### 1. Training

```bash
# Install dependencies
pip install -r requirements.txt

# Prepare your dataset in data/processed/training_data.json
# Format: [{"question": "...", "answer": "..."}]

# Train the model
python training/train_model.py
```

### 2. Inference

```python
from training.inference import EngineeringAssistant

# Initialize assistant
assistant = EngineeringAssistant(model_dir='models/saved_models')
assistant.load_model()

# Get explanation
result = assistant.get_explanation("What is a deterministic finite automaton?")
print(result['explanation'])
```

### 3. API Integration

```bash
# Start Flask API
python api/app.py
```

```bash
# Test API
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain the dot product"}'
```

## Dataset Format

Training data should be in JSON format:

```json
[
  {
    "question": "What is a DFA?",
    "answer": "Step 1: ... Step 2: ... Step 3: ..."
  }
]
```

## File Structure

```
training/
  ├── model.py           # Model architecture
  ├── data_pipeline.py   # Data loading and preprocessing
  ├── train_model.py     # Training script
  └── inference.py       # Inference and generation

api/
  └── app.py            # Flask API

data/
  └── processed/
      └── training_data.json  # Training dataset

models/
  ├── saved_models/     # Trained model weights
  └── checkpoints/      # Training checkpoints
```

## Training Tips

1. **Data Quality**: Ensure answers follow a clear step-by-step format
2. **Batch Size**: Adjust based on GPU memory (default: 32)
3. **Learning Rate**: Start with 0.0001, reduce if loss plateaus
4. **Epochs**: Monitor validation loss to prevent overfitting
5. **Temperature**: Lower (0.5-0.7) for focused answers, higher (0.8-1.0) for creative

## API Endpoints

### POST /api/solve
Solve a single question

Request:
```json
{
  "question": "Your question here"
}
```

Response:
```json
{
  "success": true,
  "question": "...",
  "explanation": "...",
  "steps": ["Step 1: ...", "Step 2: ..."]
}
```

### POST /api/batch
Solve multiple questions

Request:
```json
{
  "questions": ["question1", "question2"]
}
```

### GET /health
Health check endpoint

## Model Customization

To modify the model architecture, edit `training/model.py`:

- Change `embed_dim` for embedding size
- Adjust `num_heads` for attention heads
- Modify `num_layers` for model depth
- Update `ff_dim` for feed-forward size

## Performance

- Training Time: ~2-3 hours on GPU for 10k samples
- Inference Speed: ~1-2 seconds per question
- Model Size: ~50MB (weights only)

## Future Improvements

1. Implement beam search for better generation
2. Add fine-tuning on specific engineering domains
3. Integrate retrieval-augmented generation (RAG)
4. Support for mathematical notation rendering
5. Multi-modal support (diagrams, equations)
