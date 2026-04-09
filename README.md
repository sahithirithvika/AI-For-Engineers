# AI for Engineers

An intelligent learning assistant for engineering students with adaptive user interface, 30+ topic built-in knowledge base, Google Gemini AI, and interactive learning tools. Everything runs from a single unified Flask application.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/ESpoorthy/AI-For-Engineers.git
cd AI-For-Engineers

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API keys
# Create a .env file (see below)

# 4. Run
export $(cat .env | xargs) && python3 app.py
```

Open **http://localhost:8080** — one URL, one command, everything included.

---

## Setting Up API Keys

Create a `.env` file in the project root (never commit this file — it's gitignored):

```env
GEMINI_KEY_1=your_first_gemini_key
GEMINI_KEY_2=your_second_gemini_key
GEMINI_KEY_3=your_third_gemini_key
OPENAI_API_KEY=your_openai_key
```

- **Gemini keys**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **OpenAI key**: [platform.openai.com](https://platform.openai.com/api-keys)

Keys are loaded via environment variables only, never hardcoded in source files.

---

## How the Answer Engine Works

Questions are answered in priority order:

| Priority | Source | Speed | Notes |
|----------|--------|-------|-------|
| 1 | Built-in knowledge base | Instant | 30+ topics, no API call |
| 2 | Google Gemini AI (`gemini-2.5-flash`) | Fast | Rotates across 3 keys |
| 3 | OpenAI GPT-3.5 | Moderate | Fallback if Gemini fails |
| 4 | Structured fallback | Instant | Generic step-by-step response |

---

## Features

### Interface
- ChatGPT-like UI with collapsible sidebar
- Persistent chat history (localStorage)
- Rich visual answer cards:
  - Gradient banner with source + confidence badges
  - Question box (blue), summary box (green)
  - Collapsible step-by-step with numbered circles and emoji icons
  - Concept tags, verification box (yellow), learning tips (purple)
  - Slide-in animation
- MathJax rendering for math symbols (√, π, θ, ∫, etc.)
- Input box pinned to bottom
- Scrollable chat area
- "Built with ❤️ for Engineers" footer

### Input Methods
- Text input
- Voice input (speech recognition that works best in Chrome)
- Camera input

### Learning Tools
- **4 interactive games**: Step Builder, Concept Matcher, Formula Quest, Visual Solver
- Flashcards modal
- Multi-user profiles with progress tracking
- Weekly learning progress charts:
  - Bar chart: stock-market style (red → yellow → green)
  - Line chart: smooth curve with area fill
- Badges and achievement system

### Customization
- Theme switcher: dark / light / system
- Settings panel

---

## Built-in Knowledge Base (30+ Topics)

### Computational Problems
Complex numbers, differential equations, eigenvalues, quadratics, integration, differentiation, Laplace transforms, Fourier series, determinants, logarithms, trigonometry, probability, arithmetic progression, Z-transform, PDEs, numerical methods, statistics, set theory, boolean algebra, graph theory, DFA

### Conceptual Questions ("What is X?")
Vectors, matrices, derivatives, integrals, limits, eigenvalues, Laplace, complex numbers, Ohm's Law, Newton's Laws, gradient/curl, Taylor series, DFA, graph theory, boolean algebra, numerical methods, statistics, Z-transform, PDEs, set theory

---

## Mathematical Curriculum (M1–M4)

| Module | Topics |
|--------|--------|
| M1 | Differential & Integral Calculus, Matrix Theory, Sequences & Series |
| M2 | Vector Calculus, ODEs, Complex Numbers, Laplace Transforms |
| M3 | Fourier Analysis, PDEs, Probability & Statistics, Z-Transforms |
| M4 | Numerical Methods, Optimization, Discrete Mathematics |

---

## API Endpoints

All endpoints served from `http://localhost:8080`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the UI |
| `GET` | `/health` | Health check |
| `POST` | `/api/solve` | Solve a mathematical question |
| `GET` | `/api/problem-types` | List supported problem types |
| `GET` | `/api/examples` | Get example questions |
| `GET` | `/api/ai-status` | Check AI configuration |

### Example: Solve a Problem

```bash
curl -X POST http://localhost:8080/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "Find the polar form of z = 1 + i"}'
```

```json
{
  "success": true,
  "question": "Find the polar form of z = 1 + i",
  "problem_type": "complex_numbers",
  "solution": "Converting z = 1 + i to polar form using r = |z| and θ = arg(z).",
  "steps": [
    "Step 1: Identify real and imaginary parts: a = 1, b = 1",
    "Step 2: Calculate modulus: r = √(1² + 1²) = √2",
    "Step 3: Calculate argument: θ = arctan(1/1) = π/4",
    "Step 5: Final answer: z = √2 (cos π/4 + i sin π/4) = √2 ∠ π/4"
  ],
  "mathematical_concepts": ["Complex Numbers", "Polar Form", "Modulus", "Argument"],
  "verification": "Check: √2·cos(π/4) + i·√2·sin(π/4) = 1 + i ✓",
  "confidence": "high",
  "source": "Built-in expert solutions"
}
```

---

## Project Structure

```
AI-For-Engineers/
├── app.py                    # Unified Flask app — UI + API (start here)
├── .env                      # API keys (gitignored)
├── requirements.txt          # Python dependencies
│
├── ui/
│   └── index.html            # Main frontend (no build step needed)
│
├── training/                 # ML model training (research)
│   ├── model.py              # Transformer architecture (8.2M params)
│   ├── train_model.py        # Training loop
│   ├── inference.py          # Autoregressive generation
│   └── config.py             # Hyperparameters
│
├── data/processed/           # JSON training datasets
├── models/                   # Trained weights and checkpoints
│
├── deployment/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── docs/                     # Documentation
├── NAVIGATION.md             # Quick reference
└── PROJECT_STRUCTURE.md      # Directory layout
```

### Legacy Directories (not needed to run the app)
| Directory | Notes |
|-----------|-------|
| `api/` | Old standalone Flask API servers |
| `frontend/` | Old React app (Vite) |
| `servers/` | Old separate UI server scripts |
| `demos/` | Standalone HTML demo files |

---

## Docker Deployment

```bash
docker-compose -f deployment/docker-compose.yml up --build
```

---

## Example Questions to Try

- `Find the polar form of the complex number z = 1 + i`
- `Solve the differential equation dy/dx + 2y = 4`
- `What is a deterministic finite automaton?`
- `Explain eigenvalues`
- `Find the 12th term of the AP: 4, 9, 14, ...`
- `What is the Fourier series of f(x) = x?`
- `Solve x³ - 6x² + 11x - 6 = 0`

---

## Team

| Name | Role |
|------|------|
| Sai Spoorthy Eturu | Team lead |
| Sahithi Rithvika Katakam | Team Member |
| Shivani Edigi | Team Member |
| Hari Hansika Kommera | Team Member |

**Advisor**: A Naga Kalyani — Assistant Professor, Dept of CSE (AI&ML), BVRIT Hyderabad College of Engineering for Women

---

## License

MIT License — see [LICENSE](LICENSE) for details.

**GitHub**: https://github.com/ESpoorthy/AI-For-Engineers
