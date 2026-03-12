"""
Enhanced Transformer-based Language Model for AI for Engineers
A domain-specific model for engineering education with improved architecture
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


def get_angles(pos, i, d_model):
    """Calculate angles for positional encoding"""
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))
    return pos * angle_rates


class PositionalEncoding(layers.Layer):
    """Add positional information to token embeddings using sine/cosine functions"""
    
    def __init__(self, max_length, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length
        self.embed_dim = embed_dim
        
        # Create positional encoding matrix in __init__ instead of build
        position = np.arange(self.max_length)[:, np.newaxis]
        div_term = np.exp(np.arange(0, self.embed_dim, 2) * -(np.log(10000.0) / self.embed_dim))
        
        pos_encoding = np.zeros((self.max_length, self.embed_dim))
        pos_encoding[:, 0::2] = np.sin(position * div_term)
        pos_encoding[:, 1::2] = np.cos(position * div_term)
        
        # Store as numpy array, convert in call
        self.pos_encoding_np = pos_encoding[np.newaxis, :, :].astype(np.float32)
        
    def call(self, x):
        seq_len = tf.shape(x)[1]
        # Convert numpy to tensor in call method
        pos_enc = tf.constant(self.pos_encoding_np, dtype=tf.float32)
        return x + pos_enc[:, :seq_len, :]
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'max_length': self.max_length,
            'embed_dim': self.embed_dim
        })
        return config


class TransformerBlock(layers.Layer):
    """Enhanced transformer block with multi-head attention and feed-forward network"""
    
    def __init__(self, embed_dim, num_heads, ff_dim, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.dropout_rate = dropout_rate
        
        # Multi-head attention
        self.attention = layers.MultiHeadAttention(
            num_heads=num_heads, 
            key_dim=embed_dim // num_heads,  # Proper key dimension
            dropout=dropout_rate
        )
        
        # Feed-forward network with GELU activation for better performance
        self.ffn = keras.Sequential([
            layers.Dense(ff_dim, activation='gelu'),
            layers.Dropout(dropout_rate),
            layers.Dense(embed_dim)
        ])
        
        # Layer normalization
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        
        # Dropout layers
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)
    
    def call(self, x, training=False, mask=None):
        # Multi-head attention with causal mask for autoregressive generation
        attn_output = self.attention(
            query=x,
            value=x,
            key=x,
            attention_mask=mask,
            training=training
        )
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(x + attn_output)  # Residual connection
        
        # Feed-forward network
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)  # Residual connection
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'embed_dim': self.embed_dim,
            'num_heads': self.num_heads,
            'ff_dim': self.ff_dim,
            'dropout_rate': self.dropout_rate
        })
        return config


class EngineeringLLM(keras.Model):
    """
    Enhanced domain-specific transformer model for engineering education
    Designed to generate clear, step-by-step explanations with improved architecture
    """
    
    def __init__(self, vocab_size, max_length=512, embed_dim=256, 
                 num_heads=8, ff_dim=512, num_layers=6, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        
        self.vocab_size = vocab_size
        self.max_length = max_length
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_layers = num_layers
        
        # Token embedding layer with proper initialization
        self.token_embedding = layers.Embedding(
            input_dim=vocab_size,
            output_dim=embed_dim,
            embeddings_initializer='glorot_uniform',
            mask_zero=True,
            name='token_embedding'
        )
        
        # Positional encoding
        self.pos_encoding = PositionalEncoding(max_length, embed_dim)
        
        # Transformer blocks
        self.transformer_blocks = [
            TransformerBlock(embed_dim, num_heads, ff_dim, dropout_rate, name=f'transformer_block_{i}')
            for i in range(num_layers)
        ]
        
        # Dropout for regularization
        self.dropout = layers.Dropout(dropout_rate)
        
        # Output layer for next token prediction
        self.output_layer = layers.Dense(vocab_size, name='output_layer')
    
    def create_causal_mask(self, seq_len):
        """Create causal mask for autoregressive generation"""
        mask = tf.linalg.band_part(tf.ones((seq_len, seq_len)), -1, 0)
        return mask[tf.newaxis, tf.newaxis, :, :]  # Add batch and head dimensions
    
    def call(self, x, training=False):
        seq_len = tf.shape(x)[1]
        
        # Create causal mask
        mask = self.create_causal_mask(seq_len)
        
        # Embed tokens and add positional encoding
        x = self.token_embedding(x)
        x = x * tf.math.sqrt(tf.cast(self.embed_dim, tf.float32))  # Scale embeddings
        x = self.pos_encoding(x)
        x = self.dropout(x, training=training)
        
        # Pass through transformer blocks
        for transformer_block in self.transformer_blocks:
            x = transformer_block(x, training=training, mask=mask)
        
        # Generate logits for next token prediction
        return self.output_layer(x)
    
    def get_config(self):
        return {
            'vocab_size': self.vocab_size,
            'max_length': self.max_length,
            'embed_dim': self.embed_dim,
            'num_heads': self.num_heads,
            'ff_dim': self.ff_dim,
            'num_layers': self.num_layers
        }
