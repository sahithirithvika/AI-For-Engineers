import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnswer(null);
    
    try {
      // Create abort controller for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout
      
      // Call API directly (not through proxy)
      const apiUrl = 'http://localhost:5001/api/solve';
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      const data = await response.json();
      setAnswer(data);
    } catch (error) {
      if (error.name === 'AbortError') {
        setAnswer({ 
          error: 'Request timed out. The model is still learning and may take a while to respond. Please try again with a simpler question.' 
        });
      } else {
        setAnswer({ 
          error: `Failed to get answer: ${error.message}. Make sure the backend API is running on port 5001.` 
        });
      }
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <header>
        <h1>AI for Engineers</h1>
        <p>Your intelligent learning assistant</p>
      </header>
      
      <main>
        <form onSubmit={handleSubmit}>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask your engineering question..."
            rows="4"
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Solving...' : 'Get Solution'}
          </button>
        </form>

        {answer && (
          <div className="answer-box">
            <h2>Solution</h2>
            {answer.error ? (
              <p className="error">{answer.error}</p>
            ) : (
              <div className="solution">
                <div className="note" style={{
                  background: '#fff3cd',
                  border: '1px solid #ffc107',
                  borderRadius: '4px',
                  padding: '10px',
                  marginBottom: '15px',
                  fontSize: '14px'
                }}>
                  <strong>Note:</strong> The model is currently trained on limited data (22 examples) 
                  and may produce low-quality outputs. This demonstrates the complete ML pipeline - 
                  the model needs more training data to produce meaningful answers.
                </div>
                <p><strong>Question:</strong> {answer.question}</p>
                <p><strong>Answer:</strong> {answer.explanation}</p>
                {answer.steps && answer.steps.length > 0 && (
                  <div>
                    <strong>Steps:</strong>
                    <ul>
                      {answer.steps.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
