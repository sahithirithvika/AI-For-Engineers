# Quick Start Guide - AI for Engineers Model

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Step 1: Test Model Architecture

Verify the model implementation works:

```bash
python training/test_model.py
```

Expected output:
```
Testing Positional Encoding...
✓ Positional encoding works correctly

Testing Transformer Block...
✓ Transformer block works correctly

Testing Full Model...
✓ Model forward pass works correctly
✓ Total trainable parameters: X,XXX,XXX

✅ All tests passed!
```

## Step 2: Train the Model

Train on the sample dataset:

```bash
python training/train_model.py
```

This will:
- Load training data from `data/processed/training_data.json`
- Train for 10 epochs (adjust in script)
- Save model to `models/saved_models/`
- Create checkpoints in `models/checkpoints/`

## Step 3: Test Inference

```python
from training.inference import EngineeringAssistant

# Load trained model
assistant = EngineeringAssistant()
assistant.load_model()

# Ask a question
result = assistant.get_explanation("What is a deterministic finite automaton?")

print(result['explanation'])
print("\nSteps:")
for step in result['steps']:
    print(f"  {step}")
```

## Step 4: Start API Server

```bash
python api/app.py
```

Server runs on http://localhost:5000

## Step 5: Test API

```bash
# Test health endpoint
curl http://localhost:5000/health

# Ask a question
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain the dot product of vectors"}'
```

## Step 6: Connect Frontend

The React frontend (already created) will connect to the API automatically.

```bash
cd frontend
npm start
```

Visit http://localhost:3000 to use the web interface.

## Adding Your Own Data

Edit `data/processed/training_data.json`:

```json
[
  {
    "question": "Your engineering question",
    "answer": "Step 1: First explanation. Step 2: Second point. Step 3: Conclusion."
  }
]
```

Then retrain:
```bash
python training/train_model.py
```

## Troubleshooting

### Out of Memory
- Reduce `BATCH_SIZE` in `train_model.py`
- Reduce `MAX_LENGTH` or `EMBED_DIM`

### Slow Training
- Use GPU: `pip install tensorflow-gpu`
- Reduce `NUM_LAYERS` or `NUM_HEADS`

### Poor Quality Answers
- Add more training data
- Train for more epochs
- Adjust `temperature` in inference (lower = more focused)

## Next Steps

1. Collect more engineering Q&A data
2. Fine-tune on specific domains (automata, algebra, etc.)
3. Implement web scraping (see `scraper/scraper.py`)
4. Add monitoring and metrics
5. Deploy to cloud (see `deployment/Dockerfile`)
