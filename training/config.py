"""
Configuration file for model training and inference
Modify these parameters to customize the model
"""

# Model Architecture
MODEL_CONFIG = {
    'vocab_size': 10000,        # Size of vocabulary
    'max_length': 512,          # Maximum sequence length
    'embed_dim': 256,           # Embedding dimension
    'num_heads': 8,             # Number of attention heads
    'ff_dim': 512,              # Feed-forward network dimension
    'num_layers': 6,            # Number of transformer layers
    'dropout_rate': 0.1         # Dropout rate for regularization
}

# Training Configuration
TRAINING_CONFIG = {
    'batch_size': 32,           # Batch size for training
    'epochs': 10,               # Number of training epochs
    'learning_rate': 0.0001,    # Initial learning rate
    'validation_split': 0.1,    # Fraction of data for validation
    'early_stopping_patience': 3,  # Epochs to wait before early stopping
    'reduce_lr_patience': 2,    # Epochs to wait before reducing LR
    'reduce_lr_factor': 0.5     # Factor to reduce learning rate
}

# Data Configuration
DATA_CONFIG = {
    'train_data_path': 'data/processed/training_data.json',
    'raw_data_path': 'data/raw/',
    'processed_data_path': 'data/processed/'
}

# Model Saving
MODEL_PATHS = {
    'saved_models_dir': 'models/saved_models',
    'checkpoints_dir': 'models/checkpoints',
    'logs_dir': 'logs'
}

# Inference Configuration
INFERENCE_CONFIG = {
    'max_new_tokens': 200,      # Maximum tokens to generate
    'temperature': 0.7,         # Sampling temperature (0.1-1.0)
    'top_k': 50,                # Top-k sampling parameter
    'top_p': 0.9                # Nucleus sampling parameter (not implemented yet)
}

# API Configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'max_question_length': 500  # Maximum characters in question
}


def get_model_config():
    """Get model configuration"""
    return MODEL_CONFIG.copy()


def get_training_config():
    """Get training configuration"""
    return TRAINING_CONFIG.copy()


def get_inference_config():
    """Get inference configuration"""
    return INFERENCE_CONFIG.copy()
