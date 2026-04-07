# Troubleshooting Guide

## System Status Check

### 1. Verify Both Services Are Running

**Backend API (Port 5001)**:
```bash
curl http://localhost:5001/health
```
Expected output: `{"status":"healthy","service":"AI for Engineers API"}`

**Frontend (Port 3000)**:
Open http://localhost:3000 in your browser

### 2. Test API Directly

```bash
curl -X POST http://localhost:5001/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question":"What is a vector?"}' \
  --max-time 30
```

This should return a JSON response with `explanation`, `question`, and `steps` fields.

## Common Issues

### Issue 1: "Failed to get answer: Server error: 403"

**Possible Causes**:
1. Browser cache or extensions blocking the request
2. CORS configuration issue
3. Proxy configuration problem

**Solutions**:
1. **Clear browser cache**: Hard refresh with Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
2. **Disable browser extensions**: Try in incognito/private mode
3. **Check CORS**: The API should allow requests from http://localhost:3000
4. **Restart both services**:
   ```bash
   # Stop and restart backend
   # Stop and restart frontend
   ```

### Issue 2: Request Timeout

**Cause**: Model inference is slow on CPU (5-10 seconds per request)

**Solutions**:
1. Be patient - wait at least 10-15 seconds
2. The frontend has a 60-second timeout
3. Try simpler questions first

### Issue 3: Poor Quality Output (lots of `<UNK>` tokens)

**This is expected!** The model was only trained on 22 examples for 10 epochs.

**To improve**:
1. Add more training data (1000+ examples)
2. Train for more epochs (50-100)
3. Use the ChatGPT dataset link provided earlier

### Issue 4: Port Already in Use

**Backend (5001)**:
```bash
lsof -ti:5001 | xargs kill -9
```

**Frontend (3000)**:
```bash
lsof -ti:3000 | xargs kill -9
```

## Testing the System

### Test 1: Health Check
```bash
curl http://localhost:5001/health
```

### Test 2: Simple Question
```bash
curl -X POST http://localhost:5001/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question":"test"}' \
  --max-time 30
```

### Test 3: Engineering Question
```bash
curl -X POST http://localhost:5001/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question":"Explain deterministic finite automata"}' \
  --max-time 30
```

### Test 4: Frontend Connection
Open `test_api.html` in your browser and click the test buttons.

## Browser Console Debugging

1. Open browser DevTools (F12 or Cmd+Option+I)
2. Go to Console tab
3. Submit a question
4. Look for errors (red text)
5. Check Network tab for failed requests

Common console errors:
- **CORS error**: Backend CORS not configured properly
- **Network error**: Backend not running
- **Timeout**: Request took too long

## Verify Services

### Check Backend Process
```bash
ps aux | grep "python api/app.py"
```

### Check Frontend Process
```bash
ps aux | grep "react-scripts start"
```

### Check Ports
```bash
lsof -i :5001  # Backend
lsof -i :3000  # Frontend
```

## Fresh Start

If nothing works, restart everything:

```bash
# 1. Kill all processes
lsof -ti:5001 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# 2. Start backend
python api/app.py

# 3. In another terminal, start frontend
cd frontend
npm start

# 4. Wait 10-15 seconds for both to start

# 5. Open http://localhost:3000
```

## Expected Behavior

1. **First request**: Takes 5-10 seconds (model inference on CPU)
2. **Response format**: JSON with `success`, `question`, `explanation`, `steps`
3. **Output quality**: Poor (many `<UNK>` tokens) - this is normal with limited training
4. **Frontend**: Shows question, answer, and steps with a note about model quality

## Still Not Working?

1. Check `CURRENT_STATUS.md` for system overview
2. Review API logs for errors
3. Check browser console for JavaScript errors
4. Verify Python dependencies are installed: `pip install -r requirements.txt`
5. Ensure model files exist in `models/saved_models/`

## Success Indicators

✓ Backend shows "Model loaded successfully!"
✓ Frontend shows "Compiled successfully!"
✓ Health endpoint returns 200 OK
✓ API responds to questions (even if output is poor quality)
✓ Frontend displays responses (even with `<UNK>` tokens)

The system is working if you get ANY response, even if it's low quality!
