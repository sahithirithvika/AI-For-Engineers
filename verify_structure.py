"""
Verify project structure without requiring dependencies
"""

from pathlib import Path
import json


def check_file_exists(filepath, description):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (MISSING)")
        return False


def verify_structure():
    """Verify all required files exist"""
    print("=" * 60)
    print("AI for Engineers - Project Structure Verification")
    print("=" * 60)
    
    files_to_check = [
        # Model files
        ("training/model.py", "Model architecture"),
        ("training/data_pipeline.py", "Data pipeline"),
        ("training/train_model.py", "Training script"),
        ("training/inference.py", "Inference module"),
        ("training/config.py", "Configuration"),
        ("training/test_model.py", "Test script"),
        
        # API
        ("api/app.py", "Flask API"),
        
        # Data
        ("data/processed/training_data.json", "Training data"),
        
        # Frontend
        ("frontend/src/App.js", "React App"),
        ("frontend/src/App.css", "App styles"),
        ("frontend/package.json", "Frontend config"),
        
        # Deployment
        ("deployment/Dockerfile", "Docker config"),
        ("deployment/docker-compose.yml", "Docker Compose"),
        
        # Documentation
        ("README.md", "Main README"),
        ("README_MODEL.md", "Model documentation"),
        ("QUICKSTART.md", "Quick start guide"),
        ("requirements.txt", "Python dependencies"),
    ]
    
    print("\nChecking files...")
    all_exist = all(check_file_exists(f, d) for f, d in files_to_check)
    
    # Check training data
    print("\n" + "=" * 60)
    print("Checking training data...")
    print("=" * 60)
    
    try:
        with open('data/processed/training_data.json', 'r') as f:
            data = json.load(f)
        print(f"✓ Training data loaded: {len(data)} examples")
        print(f"  Sample question: {data[0]['question'][:50]}...")
    except Exception as e:
        print(f"✗ Error loading training data: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    if all_exist:
        print("✅ All files present!")
    else:
        print("⚠️  Some files are missing")
    
    print("=" * 60)
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Test model: python training/test_model.py")
    print("3. Train model: python training/train_model.py")
    print("4. Start API: python api/app.py")
    print("5. Start frontend: cd frontend && npm start")
    print("\nFor detailed instructions, see QUICKSTART.md")


if __name__ == '__main__':
    verify_structure()
