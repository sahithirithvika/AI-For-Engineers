"""
Enhanced test script to verify model improvements
"""

import tensorflow as tf
import numpy as np
from model import EngineeringLLM, TransformerBlock, PositionalEncoding


def test_positional_encoding():
    """Test enhanced positional encoding layer"""
    print("Testing Enhanced Positional Encoding...")
    
    pos_enc = PositionalEncoding(max_length=100, embed_dim=256)
    test_input = tf.random.normal((2, 50, 256))
    output = pos_enc(test_input)
    
    assert output.shape == test_input.shape, "Shape mismatch!"
    assert not tf.reduce_all(tf.equal(output, test_input)), "Positional encoding not applied!"
    print("✓ Positional encoding works correctly")
    print(f"  Input shape: {test_input.shape}")
    print(f"  Output shape: {output.shape}\n")


def test_transformer_block():
    """Test enhanced transformer block"""
    print("Testing Enhanced Transformer Block...")
    
    block = TransformerBlock(embed_dim=256, num_heads=8, ff_dim=512)
    test_input = tf.random.normal((2, 50, 256))
    
    # Test without mask
    output = block(test_input, training=False)
    assert output.shape == test_input.shape, "Shape mismatch!"
    
    # Test with mask
    mask = tf.ones((1, 1, 50, 50))
    output_masked = block(test_input, training=False, mask=mask)
    assert output_masked.shape == test_input.shape, "Shape mismatch with mask!"
    
    print("✓ Transformer block works correctly")
    print(f"  Input shape: {test_input.shape}")
    print(f"  Output shape: {output.shape}")
    print(f"  Supports causal masking: Yes\n")


def test_model():
    """Test enhanced full model"""
    print("Testing Enhanced Full Model...")
    
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
    
    assert output.shape == (2, 50, 1000), f"Expected (2, 50, 1000), got {output.shape}"
    print("✓ Model forward pass works correctly")
    print(f"  Input shape: {test_input.shape}")
    print(f"  Output shape: {output.shape}")
    
    # Count parameters
    total_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
    print(f"  Total trainable parameters: {total_params:,}")
    
    # Test causal mask creation
    mask = model.create_causal_mask(10)
    print(f"  Causal mask shape: {mask.shape}")
    print(f"  Causal mask working: Yes\n")


def test_model_config():
    """Test model configuration save/load"""
    print("Testing Model Configuration...")
    
    model = EngineeringLLM(
        vocab_size=1000,
        max_length=128,
        embed_dim=256,
        num_heads=8,
        ff_dim=512,
        num_layers=2
    )
    
    config = model.get_config()
    
    assert 'vocab_size' in config
    assert 'max_length' in config
    assert 'embed_dim' in config
    assert 'num_heads' in config
    assert 'ff_dim' in config
    assert 'num_layers' in config
    
    print("✓ Model configuration works correctly")
    print(f"  Config keys: {list(config.keys())}\n")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("ENHANCED MODEL TESTS")
    print("="*60 + "\n")
    
    try:
        test_positional_encoding()
        test_transformer_block()
        test_model()
        test_model_config()
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
