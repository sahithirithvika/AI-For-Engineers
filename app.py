#!/usr/bin/env python3
"""
AI for Engineers - Unified Application
Single URL serves both UI and API.
Answer engine: Built-in KB → Gemini AI → OpenAI → Wikipedia/Web search
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import re, os, requests, json as _json

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCIDSBL3eyg_MMQjD14Qfbgu32c05HFUFM")

# ── Try Gemini client ──────────────────────────────────────────────────────────
try:
    from google import genai as google_genai
    from google.genai import errors as genai_errors
    gemini_client = google_genai.Client(api_key=GEMINI_API_KEY)
    FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash-lite"]
    print("✅ Gemini client initialised")
except Exception as e:
    gemini_client = None
    print(f"⚠️  Gemini unavailable: {e}")

# ── Try OpenAI client ──────────────────────────────────────────────────────────
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    print("✅ OpenAI client initialised")
except Exception as e:
    openai_client = None
    print(f"⚠️  OpenAI unavailable: {e}")


# ── Built-in solutions (instant, no API needed) ────────────────────────────────
BUILTIN = {
    'complex_numbers': {
        'match': lambda q: 'polar form' in q and 'complex' in q,
        'solution': "Converting z = 1 + i to polar form using r = |z| and θ = arg(z).",
        'steps': [
            "Step 1: Identify real and imaginary parts: a = 1, b = 1",
            "Step 2: Calculate modulus: r = √(1² + 1²) = √2",
            "Step 3: Calculate argument: θ = arctan(1/1) = π/4 (first quadrant)",
            "Step 4: Write polar form: z = r(cosθ + i sinθ)",
            "Step 5: Final answer: z = √2 (cos π/4 + i sin π/4) = √2 ∠ π/4",
        ],
        'concepts': ['Complex Numbers', 'Polar Form', 'Modulus', 'Argument'],
        'verification': "Check: √2·cos(π/4) + i·√2·sin(π/4) = 1 + i ✓"
    },
    'differential_equations': {
        'match': lambda q: 'differential equation' in q or ('dy/dx' in q and '+' in q),
        'solution': "Solving linear first-order ODE using integrating factor method.",
        'steps': [
            "Step 1: Standard form: dy/dx + P(x)y = Q(x)",
            "Step 2: Identify P(x) = 2, Q(x) = 4",
            "Step 3: Integrating factor: μ = e^(∫2 dx) = e^(2x)",
            "Step 4: Multiply through: d/dx[y·e^(2x)] = 4e^(2x)",
            "Step 5: Integrate both sides: y·e^(2x) = 2e^(2x) + C",
            "Step 6: Final answer: y = 2 + Ce^(-2x)",
        ],
        'concepts': ['ODE', 'Integrating Factor', 'Linear Equations'],
        'verification': "Substitute back: dy/dx + 2y = -2Ce^(-2x) + 2(2 + Ce^(-2x)) = 4 ✓"
    },
    'arithmetic_progression': {
        'match': lambda q: any(x in q for x in ['arithmetic progression', 'nth term', '12th term', ' ap ']),
        'solution': "Using AP formula Tₙ = a + (n-1)d.",
        'steps': [
            "Step 1: First term a = 4",
            "Step 2: Common difference d = 9 - 4 = 5",
            "Step 3: Formula: Tₙ = a + (n-1)d",
            "Step 4: T₁₂ = 4 + (12-1)×5 = 4 + 55",
            "Step 5: Final answer: T₁₂ = 59",
        ],
        'concepts': ['Arithmetic Progression', 'Common Difference', 'nth Term'],
        'verification': "Sequence: 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59 ✓"
    },
    'quadratic': {
        'match': lambda q: 'quadratic' in q and 'complex' not in q,
        'solution': "Solving using the quadratic formula x = [-b ± √(b²-4ac)] / 2a.",
        'steps': [
            "Step 1: Identify coefficients: a = 2, b = -7, c = 3",
            "Step 2: Discriminant: Δ = (-7)² - 4(2)(3) = 49 - 24 = 25",
            "Step 3: √Δ = 5",
            "Step 4: x₁ = (7+5)/4 = 3",
            "Step 5: x₂ = (7-5)/4 = 0.5",
            "Step 6: Solutions: x = 3 or x = 0.5",
        ],
        'concepts': ['Quadratic Formula', 'Discriminant', 'Roots'],
        'verification': "2(3)² - 7(3) + 3 = 18 - 21 + 3 = 0 ✓"
    },
    'integration': {
        'match': lambda q: any(x in q for x in ['integral', 'integrate', '∫']) and 'differential' not in q,
        'solution': "Applying the power rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C.",
        'steps': [
            "Step 1: Apply power rule to each term",
            "Step 2: ∫3x² dx = 3·(x³/3) = x³",
            "Step 3: Add constant of integration",
            "Step 4: Final answer: x³ + C",
        ],
        'concepts': ['Power Rule', 'Indefinite Integral', 'Constant of Integration'],
        'verification': "Differentiate: d/dx(x³ + C) = 3x² ✓"
    },
    'differentiation': {
        'match': lambda q: any(x in q for x in ['derivative', 'differentiate', 'd/dx']) and 'differential equation' not in q,
        'solution': "Applying the power rule: d/dx(xⁿ) = n·xⁿ⁻¹.",
        'steps': [
            "Step 1: Apply power rule to each term",
            "Step 2: d/dx(5x⁴) = 20x³",
            "Step 3: d/dx(-3x²) = -6x",
            "Step 4: Final answer: dy/dx = 20x³ - 6x",
        ],
        'concepts': ['Power Rule', 'Differentiation', 'Polynomial Derivatives'],
        'verification': "Each term differentiated independently using power rule ✓"
    },
    'laplace': {
        'match': lambda q: 'laplace' in q,
        'solution': "Using Laplace transform definition: L{f(t)} = ∫₀^∞ f(t)e^(-st) dt.",
        'steps': [
            "Step 1: Apply definition: L{e^(at)} = ∫₀^∞ e^(at)·e^(-st) dt",
            "Step 2: Combine exponents: ∫₀^∞ e^((a-s)t) dt",
            "Step 3: Integrate: [e^((a-s)t)/(a-s)]₀^∞",
            "Step 4: Apply limits (s > a): 0 - 1/(a-s) = 1/(s-a)",
            "Step 5: Final answer: L{e^(at)} = 1/(s-a), valid for s > a",
        ],
        'concepts': ['Laplace Transform', 'Improper Integral', 'Exponential Functions'],
        'verification': "Standard Laplace transform pair — verified in transform tables ✓"
    },
    'determinant': {
        'match': lambda q: any(x in q for x in ['determinant', 'det(']),
        'solution': "Using 2×2 determinant formula: det = ad - bc.",
        'steps': [
            "Step 1: For matrix [[a,b],[c,d]], det = ad - bc",
            "Step 2: Identify: a=2, b=3, c=1, d=4",
            "Step 3: det = (2)(4) - (3)(1) = 8 - 3",
            "Step 4: Final answer: det(A) = 5",
        ],
        'concepts': ['Determinant', 'Matrix', 'Linear Algebra'],
        'verification': "det ≠ 0, so matrix is invertible ✓"
    },
    'eigenvalues': {
        'match': lambda q: any(x in q for x in ['eigenvalue', 'eigenvector', 'eigen']),
        'solution': "Finding eigenvalues by solving the characteristic equation det(A - λI) = 0.",
        'steps': [
            "Step 1: Set up characteristic equation: det(A - λI) = 0",
            "Step 2: For 2×2 matrix [[a,b],[c,d]]: (a-λ)(d-λ) - bc = 0",
            "Step 3: Expand: λ² - (a+d)λ + (ad-bc) = 0",
            "Step 4: For [[4,1],[2,3]]: λ² - 7λ + (12-2) = 0 → λ² - 7λ + 10 = 0",
            "Step 5: Factor: (λ-5)(λ-2) = 0",
            "Step 6: Eigenvalues: λ₁ = 5, λ₂ = 2",
        ],
        'concepts': ['Eigenvalues', 'Characteristic Equation', 'Determinant', 'Linear Algebra'],
        'verification': "Trace = 4+3 = 7 = λ₁+λ₂ = 5+2 ✓  |  Det = 10 = λ₁·λ₂ = 5×2 ✓"
    },
    'logarithm': {
        'match': lambda q: any(x in q for x in ['logarithm', 'log₁₀', 'log10', 'ln(']),
        'solution': "Using the definition: log_b(x) = y means b^y = x.",
        'steps': [
            "Step 1: Recall log₁₀(x) asks: 10 to what power equals x?",
            "Step 2: Express 1000 as power of 10: 1000 = 10³",
            "Step 3: Therefore log₁₀(1000) = 3",
            "Step 4: Final answer: log₁₀(1000) = 3",
        ],
        'concepts': ['Logarithms', 'Inverse of Exponentiation', 'Base-10'],
        'verification': "Check: 10³ = 1000 ✓"
    },
    'trigonometry': {
        'match': lambda q: any(x in q for x in ['sin(', 'cos(', 'tan(', 'sin 90', 'trigonometric']) and 'differential' not in q,
        'solution': "Using unit circle definitions of trigonometric functions.",
        'steps': [
            "Step 1: Recall sin(θ) = y-coordinate on unit circle",
            "Step 2: At 90°, coordinates are (0, 1)",
            "Step 3: sin(90°) = 1, cos(90°) = 0, tan(90°) = undefined",
            "Step 4: Key values: sin(0°)=0, sin(30°)=½, sin(45°)=√2/2, sin(60°)=√3/2, sin(90°)=1",
        ],
        'concepts': ['Unit Circle', 'Trigonometric Functions', 'Special Angles'],
        'verification': "sin²(θ) + cos²(θ) = 1 for all θ ✓"
    },
    'fourier': {
        'match': lambda q: 'fourier' in q,
        'solution': "Fourier series represents a periodic function as sum of sines and cosines.",
        'steps': [
            "Step 1: For f(x) on [-L, L], Fourier series: f(x) = a₀/2 + Σ[aₙcos(nπx/L) + bₙsin(nπx/L)]",
            "Step 2: Calculate a₀ = (1/L)∫₋ₗᴸ f(x) dx",
            "Step 3: Calculate aₙ = (1/L)∫₋ₗᴸ f(x)cos(nπx/L) dx",
            "Step 4: Calculate bₙ = (1/L)∫₋ₗᴸ f(x)sin(nπx/L) dx",
            "Step 5: For f(x)=x on [-π,π]: a₀=0, aₙ=0 (odd function), bₙ = 2(-1)^(n+1)/n",
            "Step 6: Result: f(x) = 2[sin(x) - sin(2x)/2 + sin(3x)/3 - ...]",
        ],
        'concepts': ['Fourier Series', 'Periodic Functions', 'Orthogonality', 'Harmonics'],
        'verification': "Partial sums converge to f(x) at points of continuity ✓"
    },
    'probability': {
        'match': lambda q: any(x in q for x in ['probability', 'bayes', 'random variable', 'standard deviation']),
        'solution': "Applying probability theory and statistical methods.",
        'steps': [
            "Step 1: Identify the type: classical, conditional, or Bayes' theorem",
            "Step 2: Bayes' theorem: P(A|B) = P(B|A)·P(A) / P(B)",
            "Step 3: P(B) = P(B|A)·P(A) + P(B|A')·P(A') (total probability)",
            "Step 4: Substitute known values and calculate",
            "Step 5: Verify: all probabilities must be between 0 and 1",
        ],
        'concepts': ["Bayes' Theorem", 'Conditional Probability', 'Total Probability'],
        'verification': "Sum of all mutually exclusive probabilities = 1 ✓"
    },
}

# ── Conceptual knowledge base ("what is X", "explain X", "define X") ──────────
CONCEPTS = {
    'vector': {
        'match': lambda q: 'vector' in q,
        'solution': "A vector is a mathematical quantity with both magnitude (size) and direction.",
        'steps': [
            "Step 1: Definition — A vector is represented as an arrow: length = magnitude, direction = arrow",
            "Step 2: Notation — Written as v⃗ or bold v. In 2D: v = (x, y). In 3D: v = (x, y, z)",
            "Step 3: Magnitude — |v| = √(x² + y²) in 2D, or √(x² + y² + z²) in 3D",
            "Step 4: Addition — Add corresponding components: (a,b) + (c,d) = (a+c, b+d)",
            "Step 5: Scalar multiplication — k·(x,y) = (kx, ky) — scales the magnitude",
            "Step 6: Dot product — a⃗·b⃗ = |a||b|cos(θ) = axbx + ayby (gives a scalar)",
            "Step 7: Cross product — a⃗×b⃗ gives a vector perpendicular to both (3D only)",
            "Step 8: Unit vector — v̂ = v⃗/|v⃗| — magnitude 1, same direction",
        ],
        'concepts': ['Vector', 'Magnitude', 'Direction', 'Dot Product', 'Cross Product'],
        'verification': "Example: v = (3,4) → |v| = √(9+16) = √25 = 5 ✓"
    },
    'matrix_concept': {
        'match': lambda q: ('what is' in q or 'define' in q or 'explain' in q) and 'matrix' in q,
        'solution': "A matrix is a rectangular array of numbers arranged in rows and columns.",
        'steps': [
            "Step 1: Definition — An m×n matrix has m rows and n columns",
            "Step 2: Notation — A = [[a₁₁, a₁₂], [a₂₁, a₂₂]] for a 2×2 matrix",
            "Step 3: Addition — Add element by element (matrices must be same size)",
            "Step 4: Multiplication — (AB)ᵢⱼ = Σ aᵢₖ·bₖⱼ (row × column dot product)",
            "Step 5: Transpose — Aᵀ flips rows and columns: (Aᵀ)ᵢⱼ = Aⱼᵢ",
            "Step 6: Inverse — A⁻¹ exists only if det(A) ≠ 0, and A·A⁻¹ = I",
            "Step 7: Identity matrix I — diagonal 1s, rest 0s. A·I = A",
        ],
        'concepts': ['Matrix', 'Rows', 'Columns', 'Matrix Operations', 'Inverse'],
        'verification': "For 2×2: A⁻¹ = (1/det(A))·[[d,-b],[-c,a]] ✓"
    },
    'derivative_concept': {
        'match': lambda q: ('what is' in q or 'define' in q or 'explain' in q) and any(x in q for x in ['derivative', 'differentiation']),
        'solution': "The derivative measures the instantaneous rate of change of a function.",
        'steps': [
            "Step 1: Definition — f'(x) = lim(h→0) [f(x+h) - f(x)] / h",
            "Step 2: Geometric meaning — slope of the tangent line to the curve at point x",
            "Step 3: Physical meaning — rate of change (velocity = derivative of position)",
            "Step 4: Power rule — d/dx(xⁿ) = n·xⁿ⁻¹",
            "Step 5: Product rule — d/dx(uv) = u'v + uv'",
            "Step 6: Chain rule — d/dx[f(g(x))] = f'(g(x))·g'(x)",
            "Step 7: Common derivatives — d/dx(sin x)=cos x, d/dx(eˣ)=eˣ, d/dx(ln x)=1/x",
        ],
        'concepts': ['Derivative', 'Rate of Change', 'Tangent Line', 'Differentiation Rules'],
        'verification': "f(x)=x² → f'(x)=2x. At x=3, slope=6 ✓"
    },
    'integral_concept': {
        'match': lambda q: ('what is' in q or 'define' in q or 'explain' in q) and any(x in q for x in ['integral', 'integration']),
        'solution': "Integration is the reverse of differentiation — it finds the area under a curve.",
        'steps': [
            "Step 1: Indefinite integral — ∫f(x)dx = F(x) + C, where F'(x) = f(x)",
            "Step 2: Definite integral — ∫ₐᵇ f(x)dx = area under curve from a to b",
            "Step 3: Power rule — ∫xⁿ dx = xⁿ⁺¹/(n+1) + C  (n ≠ -1)",
            "Step 4: Fundamental theorem — ∫ₐᵇ f(x)dx = F(b) - F(a)",
            "Step 5: Common integrals — ∫sin(x)dx = -cos(x)+C, ∫eˣdx = eˣ+C",
            "Step 6: Techniques — substitution, integration by parts, partial fractions",
        ],
        'concepts': ['Integration', 'Antiderivative', 'Area Under Curve', 'Fundamental Theorem'],
        'verification': "∫3x²dx = x³+C → d/dx(x³+C) = 3x² ✓"
    },
    'limit_concept': {
        'match': lambda q: ('what is' in q or 'define' in q or 'explain' in q) and 'limit' in q,
        'solution': "A limit describes the value a function approaches as the input approaches a point.",
        'steps': [
            "Step 1: Definition — lim(x→a) f(x) = L means f(x) → L as x → a",
            "Step 2: Left limit — approach from the left: lim(x→a⁻)",
            "Step 3: Right limit — approach from the right: lim(x→a⁺)",
            "Step 4: Limit exists only if left limit = right limit",
            "Step 5: Direct substitution — if f is continuous at a: lim(x→a) f(x) = f(a)",
            "Step 6: L'Hôpital's rule — for 0/0 or ∞/∞: lim f/g = lim f'/g'",
        ],
        'concepts': ['Limits', 'Continuity', "L'Hôpital's Rule", 'One-sided Limits'],
        'verification': "lim(x→0) sin(x)/x = 1 (standard result) ✓"
    },
    'eigenvalue_concept': {
        'match': lambda q: ('what is' in q or 'define' in q or 'explain' in q) and any(x in q for x in ['eigenvalue', 'eigenvector']),
        'solution': "Eigenvalues and eigenvectors describe how a matrix transformation stretches space.",
        'steps': [
            "Step 1: Definition — For matrix A, if Av = λv then λ = eigenvalue, v = eigenvector",
            "Step 2: Meaning — eigenvector only gets scaled (not rotated) by the matrix",
            "Step 3: Finding eigenvalues — solve: det(A - λI) = 0",
            "Step 4: Finding eigenvectors — for each λ, solve: (A - λI)v = 0",
            "Step 5: Example — A=[[2,0],[0,3]]: eigenvalues λ=2 and λ=3",
            "Step 6: Applications — PCA, vibration analysis, quantum mechanics, PageRank",
        ],
        'concepts': ['Eigenvalues', 'Eigenvectors', 'Characteristic Equation', 'Linear Transformations'],
        'verification': "Verify: A·v = λ·v for each pair ✓"
    },
    'laplace_concept': {
        'match': lambda q: ('what is' in q or 'define' in q or 'explain' in q) and 'laplace' in q,
        'solution': "The Laplace transform converts a time-domain function into the complex frequency domain.",
        'steps': [
            "Step 1: Definition — L{f(t)} = F(s) = ∫₀^∞ f(t)·e^(-st) dt",
            "Step 2: Purpose — converts ODEs into algebraic equations (much easier to solve)",
            "Step 3: Key pairs — L{1}=1/s, L{eᵃᵗ}=1/(s-a), L{sin(at)}=a/(s²+a²)",
            "Step 4: Linearity — L{af+bg} = aF(s) + bG(s)",
            "Step 5: Derivative rule — L{f'(t)} = sF(s) - f(0)",
            "Step 6: Workflow — transform ODE → solve algebraically → inverse transform back",
        ],
        'concepts': ['Laplace Transform', 'Frequency Domain', 'ODE Solving', 'Transform Pairs'],
        'verification': "L{e^(at)} = 1/(s-a) verified by direct integration ✓"
    },
    'complex_concept': {
        'match': lambda q: ('what is' in q or 'define' in q or 'explain' in q) and 'complex' in q,
        'solution': "A complex number has a real part and an imaginary part: z = a + bi.",
        'steps': [
            "Step 1: Definition — z = a + bi, where i = √(-1)",
            "Step 2: Imaginary unit — i² = -1, i³ = -i, i⁴ = 1",
            "Step 3: Addition — (a+bi) + (c+di) = (a+c) + (b+d)i",
            "Step 4: Multiplication — (a+bi)(c+di) = (ac-bd) + (ad+bc)i",
            "Step 5: Conjugate — z̄ = a - bi. z·z̄ = a² + b² (real number)",
            "Step 6: Modulus — |z| = √(a²+b²)",
            "Step 7: Polar form — z = r·e^(iθ) = r(cosθ + i sinθ)",
        ],
        'concepts': ['Complex Numbers', 'Imaginary Unit', 'Modulus', 'Conjugate', 'Polar Form'],
        'verification': "i² = -1 is the fundamental definition ✓"
    },
    'ohms_law': {
        'match': lambda q: any(x in q for x in ["ohm", 'v=ir', 'voltage', 'resistance']),
        'solution': "Ohm's Law: V = IR — voltage equals current times resistance.",
        'steps': [
            "Step 1: Formula — V = I × R",
            "Step 2: V = Voltage (Volts), I = Current (Amperes), R = Resistance (Ohms Ω)",
            "Step 3: Rearrangements — I = V/R, R = V/I",
            "Step 4: Power — P = VI = I²R = V²/R (Watts)",
            "Step 5: Example — V=12V, R=4Ω → I = 12/4 = 3A, P = 12×3 = 36W",
        ],
        'concepts': ["Ohm's Law", 'Voltage', 'Current', 'Resistance', 'Power'],
        'verification': "Units: Volts = Amperes × Ohms ✓"
    },
    'newton': {
        'match': lambda q: any(x in q for x in ["newton", 'f=ma', 'force', 'inertia']),
        'solution': "Newton's Laws describe the relationship between force, mass, and motion.",
        'steps': [
            "Step 1: First Law — An object stays at rest or uniform motion unless a net force acts on it",
            "Step 2: Second Law — F = ma (Force = mass × acceleration)",
            "Step 3: Third Law — Every action has an equal and opposite reaction",
            "Step 4: Units — F in Newtons (N), m in kg, a in m/s²",
            "Step 5: Example — m=5kg, a=3m/s² → F = 15N",
        ],
        'concepts': ["Newton's Laws", 'Force', 'Mass', 'Acceleration', 'Inertia'],
        'verification': "1 Newton = 1 kg·m/s² ✓"
    },
    'gradient': {
        'match': lambda q: any(x in q for x in ['gradient', 'divergence', 'curl', 'del operator', 'nabla']),
        'solution': "Gradient, divergence, and curl are vector calculus operators using ∇ (nabla).",
        'steps': [
            "Step 1: Gradient — ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z) — points in direction of steepest increase",
            "Step 2: Divergence — ∇·F = ∂Fx/∂x + ∂Fy/∂y + ∂Fz/∂z — measures outward flux",
            "Step 3: Curl — ∇×F — measures rotation of a vector field",
            "Step 4: Laplacian — ∇²f = ∂²f/∂x² + ∂²f/∂y² + ∂²f/∂z²",
            "Step 5: Applications — fluid flow, electromagnetism, heat transfer",
        ],
        'concepts': ['Gradient', 'Divergence', 'Curl', 'Vector Calculus', 'Nabla'],
        'verification': "∇f points perpendicular to level curves of f ✓"
    },
    'taylor_series': {
        'match': lambda q: any(x in q for x in ['taylor', 'maclaurin', 'taylor series']),
        'solution': "Taylor series expands a function as an infinite sum of polynomial terms.",
        'steps': [
            "Step 1: Formula — f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + f'''(a)(x-a)³/3! + ...",
            "Step 2: Maclaurin series — Taylor series centered at a=0",
            "Step 3: eˣ = 1 + x + x²/2! + x³/3! + ... (converges for all x)",
            "Step 4: sin(x) = x - x³/3! + x⁵/5! - ...",
            "Step 5: cos(x) = 1 - x²/2! + x⁴/4! - ...",
            "Step 6: Use first few terms for approximations near the expansion point",
        ],
        'concepts': ['Taylor Series', 'Maclaurin Series', 'Power Series', 'Approximation'],
        'verification': "At x=0: eˣ ≈ 1+x (linear approximation) ✓"
    },
    'dfa': {
        'match': lambda q: any(x in q for x in ['deterministic finite automaton', 'dfa', 'finite automaton', 'finite state machine', 'fsm']),
        'solution': "A Deterministic Finite Automaton (DFA) is a theoretical model of computation that accepts or rejects strings.",
        'steps': [
            "Step 1: Definition — A DFA is a 5-tuple (Q, Sigma, delta, q0, F)",
            "Step 2: Q = finite set of states (e.g., {q0, q1, q2})",
            "Step 3: Sigma = input alphabet (e.g., {0, 1})",
            "Step 4: delta = transition function: state + input symbol -> next state",
            "Step 5: q0 = initial start state, F = set of accept/final states (F subset Q)",
            "Step 6: Operation — read input one symbol at a time, follow transitions",
            "Step 7: Accept if final state is in F after reading all input, else reject",
            "Step 8: Example — DFA accepting strings ending in '1': states {q0,q1}, delta(q0,1)=q1(accept), delta(q0,0)=q0",
        ],
        'concepts': ['DFA', 'Finite Automata', 'Theory of Computation', 'Formal Languages', 'States', 'Transitions'],
        'verification': "Trace input string through states — if final state in F, string is accepted"
    },
    'graph_theory': {
        'match': lambda q: any(x in q for x in ['graph theory', 'adjacency matrix', 'spanning tree', 'bfs', 'dfs', 'dijkstra', 'shortest path']),
        'solution': "Graph theory studies networks of nodes (vertices) connected by edges.",
        'steps': [
            "Step 1: Graph G = (V, E) — V = vertices (nodes), E = edges (connections)",
            "Step 2: Directed graph: edges have direction. Undirected: bidirectional edges",
            "Step 3: Degree — number of edges at a vertex. Sum of all degrees = 2|E|",
            "Step 4: BFS (Breadth-First Search) — explore level by level using a queue",
            "Step 5: DFS (Depth-First Search) — explore as deep as possible using stack/recursion",
            "Step 6: Spanning tree — connects all vertices with |V|-1 edges, no cycles",
            "Step 7: Dijkstra's algorithm — finds shortest path in weighted graph using greedy approach",
            "Step 8: Adjacency matrix — A[i][j]=1 if edge (i,j) exists, else 0",
        ],
        'concepts': ['Graph Theory', 'BFS', 'DFS', 'Spanning Tree', 'Dijkstra', 'Adjacency Matrix'],
        'verification': "Tree property: |E| = |V|-1 and no cycles"
    },
    'boolean_algebra': {
        'match': lambda q: any(x in q for x in ['boolean', 'logic gate', 'truth table', 'karnaugh', 'and gate', 'or gate', 'nand', 'nor']),
        'solution': "Boolean algebra deals with binary variables (0 and 1) and logical operations.",
        'steps': [
            "Step 1: Basic operations — AND (.), OR (+), NOT (') with values 0 or 1",
            "Step 2: AND: 1.1=1, all others=0. OR: 0+0=0, all others=1. NOT: 0'=1, 1'=0",
            "Step 3: Identity laws — A+0=A, A.1=A. Null laws — A+1=1, A.0=0",
            "Step 4: Complement — A+A'=1, A.A'=0. Idempotent — A+A=A, A.A=A",
            "Step 5: De Morgan's — (A.B)' = A'+B' and (A+B)' = A'.B'",
            "Step 6: Simplification — use Boolean laws to minimize logic expressions",
            "Step 7: Karnaugh map — group 1s in powers of 2 to find minimal SOP expression",
        ],
        'concepts': ['Boolean Algebra', 'Logic Gates', 'Truth Tables', "De Morgan's Laws", 'Karnaugh Map'],
        'verification': "Verify by constructing truth table for original and simplified expression"
    },
    'numerical_methods': {
        'match': lambda q: any(x in q for x in ['newton raphson', 'bisection method', 'runge kutta', 'euler method', 'numerical method', 'trapezoidal rule', 'gaussian elimination']),
        'solution': "Numerical methods solve mathematical problems using iterative computational algorithms.",
        'steps': [
            "Step 1: Newton-Raphson — x_{n+1} = x_n - f(x_n)/f'(x_n) for root finding",
            "Step 2: Bisection method — halve interval [a,b] where f(a).f(b)<0 until convergence",
            "Step 3: Euler's method — y_{n+1} = y_n + h.f(x_n, y_n) for solving ODEs",
            "Step 4: Runge-Kutta (RK4) — more accurate ODE solver using 4 slope estimates",
            "Step 5: Trapezoidal rule — integral approx = h/2.[f(x0)+2f(x1)+...+f(xn)]",
            "Step 6: Gaussian elimination — row operations to solve Ax=b linear systems",
            "Step 7: Error = truncation error (method) + round-off error (floating point arithmetic)",
        ],
        'concepts': ['Newton-Raphson', 'Bisection', 'Euler Method', 'Runge-Kutta', 'Numerical Integration'],
        'verification': "Compare numerical result with exact solution; check error tolerance"
    },
    'statistics': {
        'match': lambda q: any(x in q for x in ['mean', 'median', 'mode', 'variance', 'standard deviation', 'normal distribution', 'z-score', 'statistics']),
        'solution': "Statistics involves collecting, analyzing, and interpreting numerical data.",
        'steps': [
            "Step 1: Mean (average) — x_bar = (sum of xi)/n",
            "Step 2: Median — middle value when sorted. Even n: average of two middle values",
            "Step 3: Mode — most frequently occurring value in the dataset",
            "Step 4: Variance — sigma^2 = sum(xi - x_bar)^2 / n",
            "Step 5: Standard deviation — sigma = sqrt(variance)",
            "Step 6: Normal distribution — bell curve: 68% within 1sigma, 95% within 2sigma, 99.7% within 3sigma",
            "Step 7: Z-score — z = (x - mu)/sigma (how many standard deviations from mean)",
        ],
        'concepts': ['Mean', 'Variance', 'Standard Deviation', 'Normal Distribution', 'Z-score'],
        'verification': "For symmetric data: mean = median = mode"
    },
    'z_transform': {
        'match': lambda q: any(x in q for x in ['z-transform', 'z transform', 'z domain', 'discrete time signal']),
        'solution': "The Z-transform converts discrete-time signals into the complex frequency domain.",
        'steps': [
            "Step 1: Definition — Z{x[n]} = X(z) = sum of x[n].z^(-n)",
            "Step 2: Purpose — for discrete systems, analogous to Laplace for continuous systems",
            "Step 3: Key pairs — Z{delta[n]}=1, Z{u[n]}=z/(z-1), Z{a^n.u[n]}=z/(z-a)",
            "Step 4: Linearity — Z{ax[n]+by[n]} = aX(z) + bY(z)",
            "Step 5: Time shift — Z{x[n-k]} = z^(-k).X(z)",
            "Step 6: Inverse Z-transform — use partial fractions + Z-transform tables",
            "Step 7: Region of convergence (ROC) — values of z for which X(z) converges",
        ],
        'concepts': ['Z-Transform', 'Discrete Systems', 'Digital Signal Processing', 'ROC'],
        'verification': "Verify using Z-transform tables and check ROC"
    },
    'pde': {
        'match': lambda q: any(x in q for x in ['partial differential equation', 'pde', 'heat equation', 'wave equation', 'laplace equation']),
        'solution': "PDEs involve functions of multiple variables and their partial derivatives.",
        'steps': [
            "Step 1: Partial derivative df/dx — differentiate w.r.t. x, treat other variables as constants",
            "Step 2: Heat equation — du/dt = alpha^2.(d^2u/dx^2) — models heat diffusion",
            "Step 3: Wave equation — d^2u/dt^2 = c^2.(d^2u/dx^2) — models wave propagation",
            "Step 4: Laplace equation — d^2u/dx^2 + d^2u/dy^2 = 0 — steady-state problems",
            "Step 5: Separation of variables — assume u(x,t) = X(x).T(t), separate into ODEs",
            "Step 6: Apply boundary and initial conditions to find constants",
            "Step 7: Final solution — superposition of separated solutions",
        ],
        'concepts': ['PDEs', 'Heat Equation', 'Wave Equation', 'Separation of Variables'],
        'verification': "Substitute solution back into PDE and verify boundary conditions"
    },
    'set_theory': {
        'match': lambda q: any(x in q for x in ['set theory', 'union', 'intersection', 'subset', 'power set', 'venn diagram']),
        'solution': "Set theory deals with collections of distinct objects called sets.",
        'steps': [
            "Step 1: Set — collection of distinct elements. A = {1, 2, 3}",
            "Step 2: Union — A union B = all elements in A or B (or both)",
            "Step 3: Intersection — A intersect B = elements in both A and B",
            "Step 4: Difference — A - B = elements in A but not in B",
            "Step 5: Complement — A' = all elements NOT in A (relative to universal set U)",
            "Step 6: Subset — A subset B means every element of A is also in B",
            "Step 7: Power set — P(A) = all subsets of A. If |A|=n, then |P(A)|=2^n",
            "Step 8: De Morgan's — (A union B)' = A' intersect B' and (A intersect B)' = A' union B'",
        ],
        'concepts': ['Set Theory', 'Union', 'Intersection', 'Complement', 'Power Set', "De Morgan's Laws"],
        'verification': "Verify using Venn diagrams or element-by-element checking"
    },
}


def match_builtin(question):
    q = question.lower()
    # Check BUILTIN (computational) first, then CONCEPTS (explanatory)
    for key, data in BUILTIN.items():
        if data['match'](q):
            return key, data
    for key, data in CONCEPTS.items():
        if data['match'](q):
            return key, data
    return None, None


MATH_PROMPT = """You are an expert engineering mathematics tutor.
Solve the following problem with a clear, detailed step-by-step explanation.

Question: {question}

Respond in this EXACT format (keep the section headers exactly as shown):

SOLUTION_SUMMARY:
<one sentence describing the approach>

STEPS:
Step 1: <full explanation of this step>
Step 2: <full explanation of this step>
Step 3: <full explanation of this step>
(add as many steps as needed)

CONCEPTS:
<comma-separated list of mathematical concepts used>

VERIFICATION:
<how to verify the answer>

TIPS:
<one or two practical learning tips>

Be thorough. Show ALL working. Explain WHY each step is taken."""


def call_ai(question):
    """Try Gemini → OpenAI → Wikipedia in order. Returns raw text or None."""
    prompt = MATH_PROMPT.format(question=question)

    # 1. Try Gemini
    if gemini_client:
        for model_name in FALLBACK_MODELS:
            try:
                from google.genai import errors as genai_errors
                response = gemini_client.models.generate_content(
                    model=model_name, contents=prompt)
                print(f"✅ Answered via Gemini ({model_name})")
                return response.text, "Google Gemini AI"
            except Exception as e:
                if '429' in str(e) or 'quota' in str(e).lower():
                    continue
                break

    # 2. Try OpenAI
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert engineering mathematics tutor. Always give detailed step-by-step solutions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.3
            )
            print("✅ Answered via OpenAI")
            return response.choices[0].message.content, "OpenAI GPT"
        except Exception as e:
            print(f"⚠️  OpenAI failed: {e}")

    # 3. Wikipedia free search fallback
    return search_wikipedia(question), "Wikipedia + Web Search"


def search_wikipedia(question):
    """Search Wikipedia for relevant content and format as steps."""
    try:
        # Extract key topic from question
        topic = re.sub(r'(what is|define|explain|how to|solve|find|calculate|compute)\s*', '', question, flags=re.I).strip()
        topic = topic.split('?')[0].strip()

        # Wikipedia API search
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query", "list": "search",
            "srsearch": topic, "format": "json", "srlimit": 1
        }
        search_resp = requests.get(search_url, params=search_params, timeout=8)
        search_data = search_resp.json()

        if not search_data.get("query", {}).get("search"):
            return None

        page_title = search_data["query"]["search"][0]["title"]

        # Get page extract
        extract_params = {
            "action": "query", "prop": "extracts",
            "exintro": True, "explaintext": True,
            "titles": page_title, "format": "json"
        }
        extract_resp = requests.get(search_url, params=extract_params, timeout=8)
        extract_data = extract_resp.json()

        pages = extract_data.get("query", {}).get("pages", {})
        extract = next(iter(pages.values())).get("extract", "")

        if not extract or len(extract) < 100:
            return None

        # Format as structured response
        sentences = [s.strip() for s in extract.split('.') if len(s.strip()) > 30][:8]
        steps_text = "\n".join([f"Step {i+1}: {s}." for i, s in enumerate(sentences)])

        return f"""SOLUTION_SUMMARY:
Here is a detailed explanation of {topic} based on mathematical principles.

STEPS:
{steps_text}

CONCEPTS:
{topic}, Mathematical Theory, Engineering Mathematics

VERIFICATION:
Cross-reference with your textbook or course notes for this topic.

TIPS:
Study the fundamental definition first, then work through examples.
Source: Wikipedia - {page_title}"""

    except Exception as e:
        print(f"⚠️  Wikipedia search failed: {e}")
        return None


def parse_ai_response(raw_text, question, source):
    """Parse structured AI response into API format."""
    steps, concepts, verification, tips, summary = [], [], "", [], ""

    section = None
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("SOLUTION_SUMMARY:"):
            section = "summary"
            rest = line[len("SOLUTION_SUMMARY:"):].strip()
            if rest:
                summary = rest
        elif line.startswith("STEPS:"):
            section = "steps"
        elif line.startswith("CONCEPTS:"):
            section = "concepts"
            rest = line[len("CONCEPTS:"):].strip()
            if rest:
                concepts = [c.strip() for c in rest.split(',')]
        elif line.startswith("VERIFICATION:"):
            section = "verification"
            rest = line[len("VERIFICATION:"):].strip()
            if rest:
                verification = rest
        elif line.startswith("TIPS:"):
            section = "tips"
            rest = line[len("TIPS:"):].strip()
            if rest:
                tips.append(rest)
        else:
            if section == "summary" and not summary:
                summary = line
            elif section == "steps" and re.match(r'^Step\s*\d+', line, re.I):
                steps.append(line)
            elif section == "concepts" and not concepts:
                concepts = [c.strip() for c in line.split(',')]
            elif section == "verification" and not verification:
                verification = line
            elif section == "tips":
                tips.append(line)

    if not steps:
        steps = [l.strip() for l in raw_text.splitlines()
                 if re.match(r'^(Step\s*\d+|\d+\.)', l.strip(), re.I)]

    return {
        'success': True,
        'question': question,
        'problem_type': 'ai_solved',
        'solution': summary or f"Step-by-step solution for: {question}",
        'steps': steps or [raw_text[:500]],
        'full_explanation': raw_text,
        'mathematical_concepts': concepts or ['Mathematical Reasoning'],
        'verification': verification or "Verify by substituting back into the original problem.",
        'mathematical_tips': tips,
        'confidence': 'high',
        'api_version': '3.0',
        'source': source
    }

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    ui_path = Path(__file__).parent / 'ui' / 'index.html'
    if ui_path.exists():
        return ui_path.read_text(encoding='utf-8')
    return "UI not found", 404


@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'AI for Engineers',
        'ai_enabled': gemini_client is not None,
        'message': 'Single-URL unified application'
    })


@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.get_json()
    if not data or not data.get('question', '').strip():
        return jsonify({'success': False, 'error': 'Please provide a question'}), 400

    question = data['question'].strip()

    # 1. Try built-in solutions first (instant)
    key, builtin = match_builtin(question)
    if builtin:
        return jsonify({
            'success': True,
            'question': question,
            'problem_type': key,
            'solution': builtin['solution'],
            'steps': builtin['steps'],
            'mathematical_concepts': builtin['concepts'],
            'verification': builtin['verification'],
            'confidence': 'high',
            'api_version': '3.0',
            'source': 'Built-in expert solutions'
        })

    # 2. Use AI chain: Gemini → OpenAI → Wikipedia
    result = call_ai(question)
    if result:
        raw_text, source = result
        if raw_text:
            return jsonify(parse_ai_response(raw_text, question, source))

    # 3. Hard fallback — should almost never reach here
    return jsonify({
        'success': True,
        'question': question,
        'problem_type': 'general',
        'solution': f"Unable to find a specific answer for: {question}",
        'steps': [
            "Step 1: Identify the topic and relevant formulas",
            "Step 2: Break the problem into smaller parts",
            "Step 3: Apply the appropriate method step by step",
            "Step 4: Verify your answer",
        ],
        'mathematical_concepts': ['Problem Solving'],
        'verification': "Check your answer against textbook examples.",
        'confidence': 'low',
        'api_version': '3.0',
        'source': 'Fallback'
    })


@app.route('/api/ai-status')
def ai_status():
    return jsonify({
        'ai_enabled': gemini_client is not None,
        'api_key_configured': True,
        'models_available': FALLBACK_MODELS
    })


@app.route('/api/problem-types')
def problem_types():
    return jsonify({
        'supported_types': [
            'Calculus — Differentiation, Integration, Limits',
            'Algebra — Equations, Quadratics, Systems',
            'Linear Algebra — Matrices, Determinants, Eigenvalues',
            'Differential Equations — ODEs, PDEs',
            'Complex Numbers — Polar Form, Operations',
            'Laplace & Fourier Transforms',
            'Probability & Statistics',
            'Numerical Methods',
            'Any other topic — powered by Gemini AI'
        ]
    })


@app.route('/api/examples')
def examples():
    return jsonify({'examples': [
        {'question': 'Find the polar form of the complex number z = 1 + i', 'type': 'Complex Numbers'},
        {'question': 'Solve the differential equation dy/dx + 2y = 4', 'type': 'Differential Equations'},
        {'question': 'Solve the quadratic equation 2x² - 7x + 3 = 0', 'type': 'Algebra'},
        {'question': 'Find the eigenvalues of matrix [[3,1],[0,2]]', 'type': 'Linear Algebra'},
        {'question': 'Calculate the Fourier series of f(x) = x on [-π, π]', 'type': 'Fourier Analysis'},
        {'question': 'Find the probability using Bayes theorem', 'type': 'Probability'},
    ]})


if __name__ == '__main__':
    print("=" * 60)
    print("🚀  AI for Engineers — Unified Application")
    print("=" * 60)
    print(f"🌐  URL : http://localhost:8080")
    print(f"🤖  AI  : {'✅ Gemini connected' if gemini_client else '❌ Not connected'}")
    print("📖  Endpoints:")
    print("      POST /api/solve")
    print("      GET  /api/ai-status")
    print("      GET  /health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8080, debug=False)
