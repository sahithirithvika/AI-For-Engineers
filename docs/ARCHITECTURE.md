# AI for Engineers - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                      (React + CSS)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Question Input Form                                │  │
│  │  • Answer Display                                     │  │
│  │  • Loading States                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP POST /api/solve
                         │ {"question": "..."}
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Flask API Server                        │
│                      (api/app.py)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Request Validation                                 │  │
│  │  • Error Handling                                     │  │
│  │  • Response Formatting                                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ get_explanation(question)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Inference Engine                           │
│              (training/inference.py)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Question Preprocessing                             │  │
│  │  • Tokenization                                       │  │
│  │  • Autoregressive Generation                          │  │
│  │  • Answer Decoding                                    │  │
│  │  • Step Extraction                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ model(input_tokens)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Transformer Model                           │
│                 (training/model.py)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Input: Token IDs [batch, seq_len]                   │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Token Embedding (vocab_size → embed_dim)    │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                      ↓                                │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Positional Encoding (sin/cos)               │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                      ↓                                │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Transformer Block 1                         │   │  │
│  │  │    • Multi-Head Attention (8 heads)          │   │  │
│  │  │    • Layer Norm + Residual                   │   │  │
│  │  │    • Feed-Forward (512 units)                │   │  │
│  │  │    • Layer Norm + Residual                   │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                      ↓                                │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Transformer Blocks 2-6 (same structure)     │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                      ↓                                │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Output Layer (embed_dim → vocab_size)       │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                                                        │  │
│  │  Output: Logits [batch, seq_len, vocab_size]         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Training Pipeline

```
Raw Q&A Data (JSON)
        ↓
┌───────────────────────┐
│  Data Pipeline        │
│  • Load JSON          │
│  • Clean text         │
│  • Create tokenizer   │
│  • Generate sequences │
└───────────────────────┘
        ↓
Training Dataset (TF Dataset)
        ↓
┌───────────────────────┐
│  Model Training       │
│  • Forward pass       │
│  • Compute loss       │
│  • Backpropagation    │
│  • Update weights     │
└───────────────────────┘
        ↓
Saved Model + Tokenizer
```

### Inference Pipeline

```
User Question (Text)
        ↓
┌───────────────────────┐
│  Preprocessing        │
│  • Format question    │
│  • Tokenize           │
│  • Pad sequence       │
└───────────────────────┘
        ↓
Input Token IDs
        ↓
┌───────────────────────┐
│  Autoregressive Gen   │
│  Loop:                │
│  1. Model forward     │
│  2. Sample next token │
│  3. Append to input   │
│  4. Repeat            │
└───────────────────────┘
        ↓
Generated Token IDs
        ↓
┌───────────────────────┐
│  Postprocessing       │
│  • Decode tokens      │
│  • Extract answer     │
│  • Format steps       │
└───────────────────────┘
        ↓
Structured Answer (JSON)
```

## Model Architecture Details

### Transformer Block

```
Input [batch, seq_len, embed_dim]
        ↓
┌─────────────────────────────────┐
│  Multi-Head Attention           │
│  ┌───────────────────────────┐ │
│  │  Q, K, V = Linear(input)  │ │
│  │  Attention = softmax(QK/√d)│ │
│  │  Output = Attention × V    │ │
│  └───────────────────────────┘ │
└─────────────────────────────────┘
        ↓
    Dropout
        ↓
  Add & Norm (Residual)
        ↓
┌─────────────────────────────────┐
│  Feed-Forward Network           │
│  ┌───────────────────────────┐ │
│  │  Linear(embed_dim → 512)  │ │
│  │  ReLU                      │ │
│  │  Linear(512 → embed_dim)  │ │
│  └───────────────────────────┘ │
└─────────────────────────────────┘
        ↓
    Dropout
        ↓
  Add & Norm (Residual)
        ↓
Output [batch, seq_len, embed_dim]
```

## Component Interactions

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Flask API  │────▶│  Inference   │
│   (React)    │◀────│   (Python)   │◀────│   Engine     │
└──────────────┘     └──────────────┘     └──────────────┘
                                                   │
                                                   ▼
                                          ┌──────────────┐
                                          │ Transformer  │
                                          │    Model     │
                                          └──────────────┘
                                                   │
                                                   ▼
                                          ┌──────────────┐
                                          │  Tokenizer   │
                                          └──────────────┘
```

## File Organization

```
training/
├── model.py           → Defines model architecture
├── data_pipeline.py   → Handles data loading/preprocessing
├── train_model.py     → Training loop and optimization
├── inference.py       → Generation and decoding
└── config.py          → Hyperparameters

api/
└── app.py            → Flask endpoints

frontend/
└── src/
    ├── App.js        → React components
    └── App.css       → Styling

data/
└── processed/
    └── training_data.json → Q&A dataset

models/
├── saved_models/     → Trained weights
└── checkpoints/      → Training snapshots
```

## Key Design Decisions

1. **Transformer Architecture**: Self-attention for context understanding
2. **Autoregressive Generation**: Token-by-token prediction
3. **Masked Loss**: Ignore padding in loss calculation
4. **Top-k Sampling**: Balance between quality and diversity
5. **Step-by-Step Format**: Structured educational responses
6. **Modular Design**: Separate concerns for maintainability
7. **REST API**: Standard HTTP interface
8. **React Frontend**: Modern, responsive UI

## Scalability Considerations

- **Model Size**: Can scale up layers/dimensions for better performance
- **Batch Processing**: API supports batch endpoint
- **Caching**: Can add Redis for frequent questions
- **Load Balancing**: Multiple API instances behind load balancer
- **GPU Acceleration**: TensorFlow supports GPU out of the box
- **Distributed Training**: Can use tf.distribute for large datasets

## Security & Production

- CORS enabled for frontend
- Input validation on API
- Error handling throughout
- Docker containerization
- Environment-based configuration
- Health check endpoint
