"""
Data pipeline for loading and preprocessing engineering Q&A datasets
"""

import tensorflow as tf
from tensorflow import keras
import json
import re
from pathlib import Path


class EngineeringDataPipeline:
    """Handle data loading, preprocessing, and tokenization"""
    
    def __init__(self, vocab_size=10000, max_length=512):
        self.vocab_size = vocab_size
        self.max_length = max_length
        self.tokenizer = None
        
    def load_dataset(self, data_path):
        """
        Load engineering Q&A dataset from JSON file
        Expected format: [{"question": "...", "answer": "..."}]
        """
        data_path = Path(data_path)
        
        if not data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {data_path}")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = [item['question'] for item in data]
        answers = [item['answer'] for item in data]
        
        return questions, answers
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation for context
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        return text.strip()
    
    def create_tokenizer(self, texts):
        """Create and fit tokenizer on training texts"""
        self.tokenizer = keras.preprocessing.text.Tokenizer(
            num_words=self.vocab_size,
            oov_token='<OOV>',
            filters=''
        )
        
        # Clean texts before fitting
        cleaned_texts = [self.clean_text(text) for text in texts]
        self.tokenizer.fit_on_texts(cleaned_texts)
        
        return self.tokenizer
    
    def prepare_training_data(self, questions, answers):
        """
        Prepare training data by combining questions and answers
        Format: "Question: {q} Answer: {a}"
        """
        if not self.tokenizer:
            # Combine all texts for tokenizer training
            all_texts = questions + answers
            self.create_tokenizer(all_texts)
        
        # Create training examples
        training_texts = []
        for q, a in zip(questions, answers):
            # Format as instruction-following task
            text = f"question: {self.clean_text(q)} answer: {self.clean_text(a)}"
            training_texts.append(text)
        
        # Convert to sequences
        sequences = self.tokenizer.texts_to_sequences(training_texts)
        
        # Pad sequences
        padded_sequences = keras.preprocessing.sequence.pad_sequences(
            sequences,
            maxlen=self.max_length,
            padding='post',
            truncating='post'
        )
        
        return padded_sequences
    
    def create_training_dataset(self, sequences, batch_size=32):
        """
        Create TensorFlow dataset for training
        Input: sequence[:-1], Target: sequence[1:]
        """
        # Prepare input and target sequences
        input_sequences = sequences[:, :-1]
        target_sequences = sequences[:, 1:]
        
        # Create TF dataset
        dataset = tf.data.Dataset.from_tensor_slices((input_sequences, target_sequences))
        dataset = dataset.shuffle(10000).batch(batch_size).prefetch(tf.data.AUTOTUNE)
        
        return dataset

    
    def save_tokenizer(self, save_path):
        """Save tokenizer configuration"""
        import pickle
        
        tokenizer_config = {
            'word_index': self.tokenizer.word_index,
            'vocab_size': self.vocab_size,
            'max_length': self.max_length
        }
        
        with open(save_path, 'wb') as f:
            pickle.dump(tokenizer_config, f)
    
    def load_tokenizer(self, load_path):
        """Load tokenizer configuration"""
        import pickle
        
        with open(load_path, 'rb') as f:
            tokenizer_config = pickle.load(f)
        
        self.tokenizer = keras.preprocessing.text.Tokenizer(
            num_words=tokenizer_config['vocab_size'],
            oov_token='<OOV>'
        )
        self.tokenizer.word_index = tokenizer_config['word_index']
        self.vocab_size = tokenizer_config['vocab_size']
        self.max_length = tokenizer_config['max_length']
        
        return self.tokenizer
