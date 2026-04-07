"""
Demo Flask API for AI for Engineers (without TensorFlow dependency)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Demo responses for different question types
DEMO_RESPONSES = {
    "vector": {
        "explanation": "A vector is a mathematical object that has both magnitude and direction. Step 1: Vectors can be represented as arrows in space. Step 2: They have components in each coordinate direction. Step 3: Vector operations include addition, subtraction, and scalar multiplication.",
        "steps": [
            "Step 1: A vector is defined by magnitude and direction",
            "Step 2: Vectors can be represented as ordered pairs or triples",
            "Step 3: Common operations include dot product and cross product"
        ]
    },
    "dfa": {
        "explanation": "A Deterministic Finite Automaton (DFA) is a theoretical model of computation. Step 1: It consists of states, transitions, and acceptance conditions. Step 2: For each state and input symbol, there is exactly one transition. Step 3: It accepts or rejects input strings based on final states.",
        "steps": [
            "Step 1: DFA has finite set of states",
            "Step 2: Transition function maps (state, symbol) to new state",
            "Step 3: Has start state and set of accepting states"
        ]
    },
    "integration": {
        "explanation": "Integration is the reverse process of differentiation. Step 1: It finds the area under a curve. Step 2: The fundamental theorem connects derivatives and integrals. Step 3: Common techniques include substitution and integration by parts.",
        "steps": [
            "Step 1: Integration finds antiderivatives",
            "Step 2: Definite integrals calculate area under curves",
            "Step 3: Use substitution method for complex functions"
        ]
    },
    "default": {
        "explanation": "This is a demo response showing the system architecture. Step 1: The question is processed by the frontend. Step 2: It's sent to the Flask API backend. Step 3: The model (when fully loaded) would generate a step-by-step explanation.",
        "steps": [
            "Step 1: Question received by API",
            "Step 2: Text processing and tokenization",
            "Step 3: Model inference and response generation"
        ]
    }
}

def get_demo_response(question):
    """Generate a demo response based on question keywords"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["vector", "dot product", "cross product"]):
        return DEMO_RESPONSES["vector"]
    elif any(word in question_lower for word in ["dfa", "automata", "finite"]):
        return DEMO_RESPONSES["dfa"]
    elif any(word in question_lower for word in ["integration", "integral", "antiderivative"]):
        return DEMO_RESPONSES["integration"]
    else:
        return DEMO_RESPONSES["default"]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'AI for Engineers Demo API'})

@app.route('/api/solve', methods=['POST'])
def solve_question():
    """
    Demo endpoint for solving engineering questions
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
        
        # Simulate processing time
        time.sleep(2)
        
        # Get demo response
        response_data = get_demo_response(question)
        
        result = {
            'success': True,
            'question': question,
            'explanation': response_data['explanation'],
            'steps': response_data['steps']
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("Starting AI for Engineers Demo API...")
    print("Demo API loaded successfully!")
    print("Note: This is a demo version with pre-written responses")
    print("The full model requires TensorFlow installation")
    
    app.run(host='0.0.0.0', port=5001, debug=True)