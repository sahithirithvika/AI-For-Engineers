# 🧭 AI for Engineers - Navigation Guide

## 🚀 Quick Start
- **New to the project?** → [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Need detailed setup?** → [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)
- **Want to understand the system?** → [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)

## 📁 Directory Guide

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| [`/api/`](api/) | Backend API server | `app.py`, `demo_app.py` |
| [`/training/`](training/) | ML model & training | `model.py`, `train_model.py`, `inference.py` |
| [`/frontend/`](frontend/) | React web interface | `src/App.js`, `package.json` |
| [`/data/`](data/) | Training datasets | `processed/*.json`, `merge_datasets.py` |
| [`/models/`](models/) | Trained models | `saved_models/`, `checkpoints/` |
| [`/docs/`](docs/) | Documentation | All `.md` files |
| [`/examples/`](examples/) | Usage examples | `*.py`, `*.html` demos |
| [`/scripts/`](scripts/) | Utility scripts | `check_syntax.py`, `verify_structure.py` |
| [`/deployment/`](deployment/) | Docker configs | `Dockerfile`, `docker-compose.yml` |

## 📖 Documentation Map

### Getting Started
- [QUICKSTART.md](docs/QUICKSTART.md) - 5-minute setup
- [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Detailed installation
- [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) - Complete project guide

### Technical Details
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [CURRENT_STATUS.md](docs/CURRENT_STATUS.md) - Development status
- [IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md) - Technical summary

### Development
- [CHECKLIST.md](docs/CHECKLIST.md) - Development checklist
- [ENHANCEMENTS.md](docs/ENHANCEMENTS.md) - Future roadmap
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues

## 🎯 Common Tasks

### Run the Application
```bash
# Start API server
python api/app.py

# Start frontend (new terminal)
cd frontend && npm start
```

### Train the Model
```bash
python training/train_model.py
```

### Test the API
```bash
# Open in browser
open examples/test_api.html
```

### Check Code Quality
```bash
python scripts/check_syntax.py
```

### Verify Project Structure
```bash
python scripts/verify_structure.py
```

## 🆘 Need Help?

1. **Check documentation** in `/docs/` folder
2. **Try examples** in `/examples/` folder  
3. **Run troubleshooting** guide: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
4. **Create GitHub issue** for bugs or questions

---

*Happy coding! 🚀*