"""
Inference module for generating step-by-step explanations
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
from pathlib import Path

from model import EngineeringLLM
from data_pipeline import EngineeringDataPipeline


class EngineeringAssistant:
    """Generate explanations for engineering questions"""
    
    def __init__(self, model_dir='models/saved_models'):
        self.model_dir = Path(model_dir)
        self.model = None
        self.data_pipeline = None
        self.tokenizer = None
        
    def load_model(self):
        """Load trained model and tokenizer"""
        
        # Load model config
        with open(self.model_dir / 'model_config.json', 'r') as f:
            config = json.load(f)
        
        # Initialize model
        self.model = EngineeringLLM(
            vocab_size=config['vocab_size'],
            max_length=config['max_length'],
            embed_dim=config['embed_dim']
        )
        
        # Build model by calling it once
        dummy_input = tf.ones((1, 10), dtype=tf.int32)
        _ = self.model(dummy_input)
        
        # Load weights - try both filenames
        weights_path = self.model_dir / 'model_weights.weights.h5'
        if not weights_path.exists():
            weights_path = self.model_dir / 'model_weights.h5'
        
        self.model.load_weights(str(weights_path))
        
        # Load tokenizer
        self.data_pipeline = EngineeringDataPipeline(
            vocab_size=config['vocab_size'],
            max_length=config['max_length']
        )
        self.tokenizer = self.data_pipeline.load_tokenizer(
            self.model_dir / 'tokenizer.pkl'
        )
        
        print("Model loaded successfully")
    
    def preprocess_question(self, question):
        """Preprocess input question"""
        # Format question
        formatted = f"question: {self.data_pipeline.clean_text(question)} answer:"
        
        # Tokenize
        sequence = self.tokenizer.texts_to_sequences([formatted])[0]
        
        # Pad
        padded = keras.preprocessing.sequence.pad_sequences(
            [sequence],
            maxlen=self.data_pipeline.max_length,
            padding='post'
        )
        
        return padded
    
    def generate_answer(self, question, max_new_tokens=50, temperature=0.7, top_k=50):
        """
        Generate step-by-step answer for a question
        
        Args:
            question: Input engineering question
            max_new_tokens: Maximum tokens to generate (default: 50 for faster inference)
            temperature: Sampling temperature (higher = more random)
            top_k: Top-k sampling parameter
        
        Returns:
            Generated answer text
        """
        if not self.model:
            self.load_model()
        
        # Preprocess question
        input_ids = self.preprocess_question(question)
        
        # Generate tokens autoregressively
        generated_tokens = input_ids[0].tolist()
        
        for _ in range(max_new_tokens):
            # Prepare input (last max_length tokens)
            current_input = np.array([generated_tokens[-self.data_pipeline.max_length:]])
            
            # Get predictions
            predictions = self.model(current_input, training=False)
            
            # Get logits for next token (last position)
            next_token_logits = predictions[0, -1, :]
            
            # Apply temperature
            next_token_logits = next_token_logits / temperature
            
            # Top-k sampling
            top_k_indices = tf.math.top_k(next_token_logits, k=top_k).indices
            top_k_logits = tf.gather(next_token_logits, top_k_indices)
            
            # Sample from top-k
            probabilities = tf.nn.softmax(top_k_logits)
            next_token_idx = np.random.choice(top_k, p=probabilities.numpy())
            next_token = top_k_indices[next_token_idx].numpy()
            
            # Stop if end token or padding
            if next_token == 0:
                break
            
            generated_tokens.append(int(next_token))
        
        # Decode generated tokens
        generated_text = self.decode_tokens(generated_tokens)
        
        # Extract answer part
        if "answer:" in generated_text:
            answer = generated_text.split("answer:")[1].strip()
        else:
            answer = generated_text
        
        return answer
    
    def decode_tokens(self, tokens):
        """Convert token IDs back to text"""
        # Create reverse word index
        reverse_word_index = {v: k for k, v in self.tokenizer.word_index.items()}
        
        # Decode tokens
        words = []
        for token in tokens:
            if token != 0:  # Skip padding
                word = reverse_word_index.get(token, '<UNK>')
                words.append(word)
        
        return ' '.join(words)
    
    def get_explanation(self, question):
        """
        Main API function for getting explanations
        Returns structured response
        """
        try:
            answer = self.generate_answer(question)
            
            return {
                'success': True,
                'question': question,
                'explanation': answer,
                'steps': self.extract_steps(answer)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_steps(self, answer):
        """Extract step-by-step breakdown from answer"""
        steps = []
        lines = answer.split('.')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and len(line) > 10:
                if not line.lower().startswith('step'):
                    steps.append(f"Step {i}: {line}")
                else:
                    steps.append(line)
        
        return steps


# Convenience function for API integration
def get_answer_for_question(question, model_dir='models/saved_models'):
    """
    Simple function to get answer for a question
    Can be called directly from Flask/FastAPI
    """
    assistant = EngineeringAssistant(model_dir)
    return assistant.get_explanation(question)
