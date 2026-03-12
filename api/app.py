"""
Flask API for AI for Engineers
Serves the trained model for question answering
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add training directory to path
sys.path.append(str(Path(__file__).parent.parent / 'training'))

from inference import EngineeringAssistant

app = Flask(__name__)
# Enable CORS with explicit configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize model
assistant = None


def get_assistant():
    """Lazy load the model"""
    global assistant
    if assistant is None:
        assistant = EngineeringAssistant(model_dir='models/saved_models')
        assistant.load_model()
    return assistant


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'AI for Engineers API'})


@app.route('/api/solve', methods=['POST'])
def solve_question():
    """
    Main endpoint for solving engineering questions
    
    Request body:
        {
            "question": "Your engineering question here"
        }
    
    Response:
        {
            "success": true,
            "question": "...",
            "explanation": "...",
            "steps": [...]
        }
    """
    try:
        # Get question from request
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'No question provided'
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty'
            }), 400
        
        # Get model assistant
        model = get_assistant()
        
        # Generate explanation
        result = model.get_explanation(question)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/batch', methods=['POST'])
def batch_solve():
    """
    Batch endpoint for multiple questions
    
    Request body:
        {
            "questions": ["question1", "question2", ...]
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'questions' not in data:
            return jsonify({
                'success': False,
                'error': 'No questions provided'
            }), 400
        
        questions = data['questions']
        model = get_assistant()
        
        results = []
        for question in questions:
            result = model.get_explanation(question)
            results.append(result)
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("Starting AI for Engineers API...")
    print("Loading model...")
    
    # Preload model for faster first request
    try:
        get_assistant()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Warning: Could not preload model: {e}")
        print("Model will be loaded on first request")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
