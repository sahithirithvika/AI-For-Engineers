"""
Test script to verify model implementation
"""

import tensorflow as tf
import numpy as np
from model import EngineeringLLM, TransformerBlock, PositionalEncoding


def test_positional_encoding():
    """Test positional encoding layer"""
    print("Testing Positional Encoding...")
    
    pos_enc = PositionalEncoding(max_length=100, embed_dim=256)
    test_input = tf.random.normal((2, 50, 256))
    output = pos_enc(test_input)
    
    assert output.shape == test_input.shape
    print("✓ Positional encoding works correctly")


def test_transformer_block():
    """Test transformer block"""
    print("\nTesting Transformer Block...")
    
    block = TransformerBlock(embed_dim=256, num_heads=8, ff_dim=512)
    test_input = tf.random.normal((2, 50, 256))
    output = block(test_input, training=False)
    
    assert output.shape == test_input.shape
    print("✓ Transformer block works correctly")


def test_model():
    """Test full model"""
    print("\nTesting Full Model...")
    
    model = EngineeringLLM(
        vocab_size=1000,
        max_length=128,
        embed_dim=256,
        num_heads=8,
        ff_dim=512,
        num_layers=2
    )
    
    # Test forward pass
    test_input = tf.random.uniform((2, 50), minval=0, maxval=1000, dtype=tf.int32)
    output = model(test_input, training=False)
    
    assert output.shape == (2, 50, 1000)
    print("✓ Model forward pass works correctly")
    
    # Count parameters
    total_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
    print(f"✓ Total trainable parameters: {total_params:,}")


if __name__ == '__main__':
    print("Running model tests...\n")
    
    test_positional_encoding()
    test_transformer_block()
    test_model()
    
    print("\n✅ All tests passed!")
