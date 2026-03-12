"""
Example usage of the AI for Engineers model
Demonstrates training, inference, and API integration
"""

import sys
from pathlib import Path

# Add training to path
sys.path.append('training')

from data_pipeline import EngineeringDataPipeline
from model import EngineeringLLM
from train_model import ModelTrainer
from inference import EngineeringAssistant


def example_data_pipeline():
    """Example: Load and preprocess data"""
    print("=" * 60)
    print("EXAMPLE 1: Data Pipeline")
    print("=" * 60)
    
    pipeline = EngineeringDataPipeline(vocab_size=5000, max_length=256)
    
    # Load dataset
    questions, answers = pipeline.load_dataset('data/processed/training_data.json')
    print(f"\nLoaded {len(questions)} Q&A pairs")
    print(f"\nSample question: {questions[0]}")
    print(f"Sample answer: {answers[0][:100]}...")
    
    # Prepare training data
    sequences = pipeline.prepare_training_data(questions, answers)
    print(f"\nSequence shape: {sequences.shape}")
    print(f"Vocabulary size: {len(pipeline.tokenizer.word_index)}")


def example_model_creation():
    """Example: Create and inspect model"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Model Architecture")
    print("=" * 60)
    
    model = EngineeringLLM(
        vocab_size=5000,
        max_length=256,
        embed_dim=128,
        num_heads=4,
        ff_dim=256,
        num_layers=2
    )
    
    print("\nModel created successfully!")
    print(f"Vocabulary size: {model.vocab_size}")
    print(f"Max sequence length: {model.max_length}")
    print(f"Embedding dimension: {model.embed_dim}")


def example_inference():
    """Example: Generate answers (requires trained model)"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Inference")
    print("=" * 60)
    
    model_dir = Path('models/saved_models')
    
    if not model_dir.exists():
        print("\n⚠️  No trained model found. Please run training first:")
        print("   python training/train_model.py")
        return
    
    # Load model
    assistant = EngineeringAssistant(model_dir=str(model_dir))
    assistant.load_model()
    
    # Test questions
    questions = [
        "What is a deterministic finite automaton?",
        "Explain the dot product of vectors",
        "How do you solve linear equations?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        result = assistant.get_explanation(question)
        
        if result['success']:
            print(f"A: {result['explanation'][:200]}...")
        else:
            print(f"Error: {result['error']}")


def example_api_integration():
    """Example: How to use in Flask API"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: API Integration")
    print("=" * 60)
    
    print("\nFlask API code example:")
    print("""
from inference import get_answer_for_question

@app.route('/api/solve', methods=['POST'])
def solve():
    question = request.json['question']
    result = get_answer_for_question(question)
    return jsonify(result)
    """)
    
    print("\nTo start the API server:")
    print("  python api/app.py")
    
    print("\nTo test the API:")
    print("""  curl -X POST http://localhost:5000/api/solve \\
    -H "Content-Type: application/json" \\
    -d '{"question": "What is Big O notation?"}'""")


if __name__ == '__main__':
    print("\n🚀 AI for Engineers - Model Examples\n")
    
    # Run examples
    example_data_pipeline()
    example_model_creation()
    example_inference()
    example_api_integration()
    
    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Train the model: python training/train_model.py")
    print("2. Test inference: python training/test_model.py")
    print("3. Start API: python api/app.py")
    print("4. Start frontend: cd frontend && npm start")
