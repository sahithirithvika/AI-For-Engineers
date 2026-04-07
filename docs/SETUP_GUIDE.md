# Complete Setup Guide - AI for Engineers

## Prerequisites

- Python 3.8+ (3.10 recommended)
- Node.js 16+ and npm
- 8GB+ RAM (16GB recommended for training)
- GPU optional but recommended for training

## Step-by-Step Installation

### 1. Clone and Navigate

```bash
git clone https://github.com/Esssp/AI-For-Engineers.git
cd AI-For-Engineers
```

### 2. Verify Project Structure

```bash
python verify_structure.py
```

Expected output: "✅ All files present!"

### 3. Set Up Python Environment

#### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### Option B: Using conda

```bash
conda create -n ai-engineers python=3.10
conda activate ai-engineers
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- TensorFlow 2.13+
- Keras 2.13+
- Flask
- NumPy, Pandas, Matplotlib

**Note**: Installation may take 5-10 minutes.

### 5. Test Model Architecture

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

### 6. Train the Model

```bash
python training/train_model.py
```

This will:
- Load sample data (5 Q&A pairs)
- Train for 10 epochs (~5-10 minutes on CPU)
- Save model to `models/saved_models/`
- Create checkpoints in `models/checkpoints/`

**Training Output**:
```
Initializing data pipeline...
Loading dataset...
Loaded 5 Q&A pairs
Preparing training data...
Building model...
Compiling model...
Starting training...
Epoch 1/10
...
Training complete!
Model saved to models/saved_models
```

### 7. Test Inference

```bash
python -c "
from training.inference import EngineeringAssistant
assistant = EngineeringAssistant()
assistant.load_model()
result = assistant.get_explanation('What is a DFA?')
print(result['explanation'])
"
```

### 8. Set Up Frontend

```bash
cd frontend
npm install
```

This installs React and dependencies (~2-3 minutes).

### 9. Start the Backend API

In one terminal:

```bash
# From project root
python api/app.py
```

Expected output:
```
Starting AI for Engineers API...
Loading model...
Model loaded successfully!
 * Running on http://0.0.0.0:5000
```

### 10. Start the Frontend

In another terminal:

```bash
cd frontend
npm start
```

Expected output:
```
Compiled successfully!
You can now view ai-for-engineers-frontend in the browser.
  Local:            http://localhost:3000
```

### 11. Test the Complete System

Open browser to http://localhost:3000

Try asking:
- "What is a deterministic finite automaton?"
- "Explain the dot product of vectors"
- "How do you solve linear equations?"

## Troubleshooting

### Issue: TensorFlow Installation Fails

**Solution**:
```bash
# Try installing without GPU support
pip install tensorflow-cpu
```

### Issue: Out of Memory During Training

**Solution**: Edit `training/train_model.py`:
```python
BATCH_SIZE = 16  # Reduce from 32
EMBED_DIM = 128  # Reduce from 256
NUM_LAYERS = 4   # Reduce from 6
```

### Issue: Frontend Won't Connect to API

**Solution**: Check CORS and proxy settings in `frontend/package.json`:
```json
"proxy": "http://localhost:5000"
```

### Issue: Model Not Found

**Solution**: Ensure training completed successfully:
```bash
ls models/saved_models/
# Should show: model_weights.h5, model_config.json, tokenizer.pkl
```

### Issue: Port Already in Use

**Solution**: Change ports in code:
- API: Edit `api/app.py` → `app.run(port=5001)`
- Frontend: `PORT=3001 npm start`

## Docker Deployment (Alternative)

### Build and Run with Docker Compose

```bash
# From project root
docker-compose -f deployment/docker-compose.yml up --build
```

This starts both API and frontend in containers.

### Build API Container Only

```bash
docker build -f deployment/Dockerfile -t ai-engineers-api .
docker run -p 5000:5000 ai-engineers-api
```

## Adding Your Own Training Data

### 1. Create Dataset File

Edit `data/processed/training_data.json`:

```json
[
  {
    "question": "Your engineering question here",
    "answer": "Step 1: First point. Step 2: Second point. Step 3: Conclusion."
  },
  {
    "question": "Another question",
    "answer": "Step 1: Explanation. Step 2: Details. Step 3: Summary."
  }
]
```

### 2. Retrain Model

```bash
python training/train_model.py
```

### 3. Test New Model

```bash
python api/app.py
```

## Configuration Customization

Edit `training/config.py` to adjust:

```python
MODEL_CONFIG = {
    'vocab_size': 10000,    # Increase for larger vocabulary
    'max_length': 512,      # Increase for longer sequences
    'embed_dim': 256,       # Increase for more capacity
    'num_heads': 8,         # Must divide embed_dim
    'num_layers': 6,        # More layers = better but slower
}

TRAINING_CONFIG = {
    'batch_size': 32,       # Reduce if out of memory
    'epochs': 10,           # Increase for better training
    'learning_rate': 0.0001 # Adjust if loss plateaus
}

INFERENCE_CONFIG = {
    'temperature': 0.7,     # Lower = more focused, higher = more creative
    'max_new_tokens': 200   # Maximum answer length
}
```

## Performance Optimization

### For Training

1. **Use GPU**: Install `tensorflow-gpu`
2. **Increase Batch Size**: If you have enough memory
3. **Mixed Precision**: Add to training script:
   ```python
   from tensorflow.keras import mixed_precision
   mixed_precision.set_global_policy('mixed_float16')
   ```

### For Inference

1. **Model Quantization**: Reduce model size
2. **Caching**: Cache frequent questions
3. **Batch Requests**: Use `/api/batch` endpoint

## Monitoring and Logging

### View TensorBoard

```bash
tensorboard --logdir logs
```

Open http://localhost:6006

### Check API Logs

API logs are printed to console. For production, add:
```python
import logging
logging.basicConfig(filename='api.log', level=logging.INFO)
```

## Next Steps

1. **Collect More Data**: Scrape engineering Q&A sites
2. **Fine-tune Model**: Train on domain-specific data
3. **Add Features**: 
   - User feedback collection
   - Answer rating system
   - Question history
4. **Deploy to Cloud**: AWS, GCP, or Azure
5. **Add Monitoring**: Prometheus, Grafana
6. **Implement CI/CD**: GitHub Actions

## Useful Commands

```bash
# Verify installation
python verify_structure.py

# Run tests
python training/test_model.py

# Train model
python training/train_model.py

# Start API
python api/app.py

# Start frontend
cd frontend && npm start

# View logs
tail -f logs/training.log

# Check model size
du -sh models/saved_models/

# Clean up
rm -rf models/checkpoints/*
rm -rf logs/*
```

## Getting Help

- Check `README_MODEL.md` for model details
- See `ARCHITECTURE.md` for system design
- Review `QUICKSTART.md` for quick reference
- Open GitHub issue for bugs

## System Requirements

### Minimum
- CPU: 2 cores
- RAM: 8GB
- Storage: 2GB
- OS: macOS, Linux, Windows

### Recommended
- CPU: 4+ cores
- RAM: 16GB
- GPU: NVIDIA with 4GB+ VRAM
- Storage: 10GB
- OS: Linux (Ubuntu 20.04+)

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Model tests pass
- [ ] Training completes
- [ ] Model files saved
- [ ] API starts successfully
- [ ] Frontend builds
- [ ] Can ask questions via UI
- [ ] Receives answers

If all checked, you're ready to go! 🚀
