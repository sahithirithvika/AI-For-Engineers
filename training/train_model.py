"""
Enhanced training script for the Engineering LLM with improved error handling
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from pathlib import Path
import json
import sys
from datetime import datetime

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Note: Install tqdm for progress bars: pip install tqdm")

from model import EngineeringLLM
from data_pipeline import EngineeringDataPipeline


class ModelTrainer:
    """Handle model training and validation with enhanced features"""
    
    def __init__(self, model, data_pipeline):
        self.model = model
        self.data_pipeline = data_pipeline
        self.history = None
        
    def compile_model(self, learning_rate=0.001):
        """Compile model with optimizer and loss function"""
        # Use AdamW optimizer for better weight decay
        optimizer = keras.optimizers.Adam(
            learning_rate=learning_rate,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-7,
            clipnorm=1.0  # Gradient clipping
        )
        
        # Sparse categorical crossentropy for next token prediction
        loss_fn = keras.losses.SparseCategoricalCrossentropy(
            from_logits=True,
            reduction='none'
        )
        
        def masked_loss(y_true, y_pred):
            """Loss function that ignores padding tokens"""
            loss = loss_fn(y_true, y_pred)
            mask = tf.cast(tf.not_equal(y_true, 0), tf.float32)
            loss = loss * mask
            return tf.reduce_sum(loss) / tf.reduce_sum(mask)
        
        def masked_accuracy(y_true, y_pred):
            """Accuracy metric that ignores padding tokens"""
            y_pred = tf.argmax(y_pred, axis=-1)
            y_pred = tf.cast(y_pred, y_true.dtype)
            match = tf.cast(tf.equal(y_true, y_pred), tf.float32)
            mask = tf.cast(tf.not_equal(y_true, 0), tf.float32)
            return tf.reduce_sum(match * mask) / tf.reduce_sum(mask)
        
        self.model.compile(
            optimizer=optimizer,
            loss=masked_loss,
            metrics=[masked_accuracy]
        )
        
        print("✓ Model compiled successfully")
        print(f"  Optimizer: Adam (lr={learning_rate})")
        print(f"  Loss: Masked Sparse Categorical Crossentropy")
        print(f"  Metrics: Masked Accuracy")
    
    def train(self, train_dataset, val_dataset=None, epochs=10, 
              checkpoint_dir='models/checkpoints'):
        """Train the model with enhanced callbacks and logging"""
        
        # Create checkpoint directory
        checkpoint_dir = Path(checkpoint_dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logs directory
        log_dir = Path('logs') / datetime.now().strftime('%Y%m%d-%H%M%S')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print("Starting Training")
        print(f"{'='*60}")
        print(f"Epochs: {epochs}")
        print(f"Checkpoint dir: {checkpoint_dir}")
        print(f"Log dir: {log_dir}")
        print(f"{'='*60}\n")
        
        # Callbacks
        callbacks = [
            keras.callbacks.ModelCheckpoint(
                filepath=str(checkpoint_dir / 'model_epoch_{epoch:02d}_loss_{loss:.4f}.weights.h5'),
                save_weights_only=True,
                save_best_only=True,
                monitor='val_loss' if val_dataset else 'loss',
                mode='min',
                verbose=1
            ),
            keras.callbacks.EarlyStopping(
                monitor='val_loss' if val_dataset else 'loss',
                patience=3,
                restore_best_weights=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss' if val_dataset else 'loss',
                factor=0.5,
                patience=2,
                min_lr=1e-7,
                verbose=1
            ),
            keras.callbacks.TensorBoard(
                log_dir=str(log_dir),
                histogram_freq=1,
                write_graph=True,
                update_freq='epoch'
            ),
            keras.callbacks.CSVLogger(
                str(log_dir / 'training_log.csv'),
                append=True
            )
        ]
        
        # Train model
        try:
            self.history = self.model.fit(
                train_dataset,
                validation_data=val_dataset,
                epochs=epochs,
                callbacks=callbacks,
                verbose=1
            )
            
            print(f"\n{'='*60}")
            print("Training Complete!")
            print(f"{'='*60}")
            
            # Print final metrics
            if self.history:
                final_loss = self.history.history['loss'][-1]
                print(f"Final training loss: {final_loss:.4f}")
                
                if val_dataset:
                    final_val_loss = self.history.history['val_loss'][-1]
                    print(f"Final validation loss: {final_val_loss:.4f}")
            
            return self.history
            
        except KeyboardInterrupt:
            print("\n\nTraining interrupted by user!")
            print("Saving current model state...")
            return self.history
        
        except Exception as e:
            print(f"\n\nError during training: {e}")
            print("Attempting to save model...")
            raise
    
    def save_model(self, save_dir='models/saved_models'):
        """Save trained model, tokenizer, and training history"""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print("Saving Model")
        print(f"{'='*60}")
        
        try:
            # Save model weights
            weights_path = save_dir / 'model_weights.weights.h5'
            self.model.save_weights(str(weights_path))
            print(f"✓ Model weights saved: {weights_path}")
            
            # Save model config
            config = {
                'vocab_size': self.model.vocab_size,
                'max_length': self.model.max_length,
                'embed_dim': self.model.embed_dim,
                'num_heads': self.model.num_heads,
                'ff_dim': self.model.ff_dim,
                'num_layers': self.model.num_layers,
                'timestamp': datetime.now().isoformat()
            }
            
            config_path = save_dir / 'model_config.json'
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✓ Model config saved: {config_path}")
            
            # Save tokenizer
            tokenizer_path = save_dir / 'tokenizer.pkl'
            self.data_pipeline.save_tokenizer(tokenizer_path)
            print(f"✓ Tokenizer saved: {tokenizer_path}")
            
            # Save training history if available
            if self.history:
                history_path = save_dir / 'training_history.json'
                history_dict = {k: [float(v) for v in vals] for k, vals in self.history.history.items()}
                with open(history_path, 'w') as f:
                    json.dump(history_dict, f, indent=2)
                print(f"✓ Training history saved: {history_path}")
            
            print(f"{'='*60}")
            print(f"All files saved to: {save_dir}")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"✗ Error saving model: {e}")
            raise


def main():
    """Main training pipeline with comprehensive error handling"""
    
    print("\n" + "="*60)
    print("AI FOR ENGINEERS - MODEL TRAINING")
    print("="*60 + "\n")
    
    # Configuration
    VOCAB_SIZE = 10000
    MAX_LENGTH = 512
    EMBED_DIM = 256
    NUM_HEADS = 8
    FF_DIM = 512
    NUM_LAYERS = 6
    BATCH_SIZE = 32
    EPOCHS = 10
    LEARNING_RATE = 0.0001
    
    try:
        print("Step 1: Initializing data pipeline...")
        data_pipeline = EngineeringDataPipeline(
            vocab_size=VOCAB_SIZE,
            max_length=MAX_LENGTH
        )
        print("✓ Data pipeline initialized\n")
        
        # Load dataset
        print("Step 2: Loading dataset...")
        try:
            # Try to load merged dataset first
            questions, answers = data_pipeline.load_dataset('data/processed/merged_training_data.json')
            print(f"✓ Loaded {len(questions)} Q&A pairs from merged dataset\n")
        except FileNotFoundError:
            try:
                # Fall back to original dataset
                questions, answers = data_pipeline.load_dataset('data/processed/training_data.json')
                print(f"✓ Loaded {len(questions)} Q&A pairs\n")
            except FileNotFoundError:
                print("⚠ No dataset found. Creating sample dataset...")
                # Create sample data for demonstration
                sample_data = [
                    {
                        "question": "What is a deterministic finite automaton?",
                        "answer": "Step 1: A DFA is a theoretical model of computation. Step 2: It consists of states, transitions, and accepts/rejects strings. Step 3: It has exactly one transition per symbol from each state."
                    },
                    {
                        "question": "Explain the dot product of two vectors",
                        "answer": "Step 1: The dot product multiplies corresponding components. Step 2: Formula is a·b = a1*b1 + a2*b2 + ... Step 3: Result is a scalar value."
                    }
                ]
                
                Path('data/processed').mkdir(parents=True, exist_ok=True)
                with open('data/processed/training_data.json', 'w') as f:
                    json.dump(sample_data, f, indent=2)
                
                questions, answers = data_pipeline.load_dataset('data/processed/training_data.json')
                print(f"✓ Created and loaded {len(questions)} sample Q&A pairs\n")
        
        if len(questions) < 2:
            print("✗ Error: Need at least 2 examples for training")
            sys.exit(1)
        
        # Prepare training data
        print("Step 3: Preparing training data...")
        sequences = data_pipeline.prepare_training_data(questions, answers)
        print(f"✓ Prepared {len(sequences)} sequences")
        print(f"  Sequence shape: {sequences.shape}")
        print(f"  Vocabulary size: {len(data_pipeline.tokenizer.word_index)}\n")
        
        # Split into train and validation
        split_idx = max(1, int(0.9 * len(sequences)))
        train_sequences = sequences[:split_idx]
        val_sequences = sequences[split_idx:]
        
        print(f"  Training samples: {len(train_sequences)}")
        print(f"  Validation samples: {len(val_sequences)}\n")
        
        train_dataset = data_pipeline.create_training_dataset(train_sequences, BATCH_SIZE)
        val_dataset = data_pipeline.create_training_dataset(val_sequences, BATCH_SIZE) if len(val_sequences) > 0 else None
        
        # Create model
        print("Step 4: Building model...")
        model = EngineeringLLM(
            vocab_size=VOCAB_SIZE,
            max_length=MAX_LENGTH,
            embed_dim=EMBED_DIM,
            num_heads=NUM_HEADS,
            ff_dim=FF_DIM,
            num_layers=NUM_LAYERS
        )
        print("✓ Model architecture created")
        
        # Build model by calling it once
        dummy_input = tf.ones((1, 10), dtype=tf.int32)
        _ = model(dummy_input)
        
        # Count parameters
        total_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
        print(f"  Total parameters: {total_params:,}\n")
        
        # Initialize trainer
        print("Step 5: Compiling model...")
        trainer = ModelTrainer(model, data_pipeline)
        trainer.compile_model(learning_rate=LEARNING_RATE)
        print()
        
        # Train model
        print("Step 6: Training model...")
        trainer.train(
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            epochs=EPOCHS
        )
        
        # Save model
        print("\nStep 7: Saving model...")
        trainer.save_model()
        
        print("\n" + "="*60)
        print("✅ TRAINING COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Test inference: python training/inference.py")
        print("2. Start API: python api/app.py")
        print("3. Start frontend: cd frontend && npm start")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n\n✗ Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
