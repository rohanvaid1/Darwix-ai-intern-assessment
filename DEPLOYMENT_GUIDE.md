# 🚀 GitHub Upload & Deployment Guide

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website (Easiest)

1. **Go to GitHub:** https://github.com/new

2. **Repository Settings:**
   - **Name:** `darwix-ai-intern-assessment`
   - **Description:** "AI Intern Assessment: Emotion-aware TTS & Narrative-to-Storyboard Generator"
   - **Visibility:** Public (recommended for portfolio) or Private
   - **Do NOT initialize with:** README, .gitignore, or license (we already have them!)

3. **Click:** "Create repository"

4. **Copy the repository URL** - You'll see something like:
   ```
   https://github.com/YOUR-USERNAME/darwix-ai-intern-assessment.git
   ```

---

## Step 2: Push to GitHub

Open PowerShell in your project folder and run:

```powershell
cd "C:\Users\asus\Desktop\Darwix AI assignment"

# Add your GitHub repository as remote (replace with YOUR URL)
git remote add origin https://github.com/YOUR-USERNAME/darwix-ai-intern-assessment.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**You'll be asked to login to GitHub** - use your credentials.

---

## Step 3: Verify Upload

1. Go to your GitHub repository URL
2. You should see all your files uploaded!
3. Update the main README:
   - Replace `README.md` with `README_GITHUB.md` content
   - Add your GitHub username and email

---

## 🌐 Deployment Options

### Option 1: Render (Recommended - Free & Easy)

#### Deploy Challenge 1 (Empathy Engine)

1. **Go to:** https://render.com
2. **Sign up/Login** (use GitHub account)
3. **New → Web Service**
4. **Connect GitHub repository**
5. **Settings:**
   - **Name:** `empathy-engine`
   - **Root Directory:** `challenge1_empathy_engine`
   - **Environment:** Python 3
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python -m textblob.download_corpora
     ```
   - **Start Command:** 
     ```
     uvicorn app:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** Free

6. **Click:** "Create Web Service"
7. **Wait 5-10 minutes** for deployment
8. **Your live URL:** `https://empathy-engine.onrender.com`

#### Deploy Challenge 2 (Pitch Visualizer)

Repeat the same steps but:
- **Name:** `pitch-visualizer`
- **Root Directory:** `challenge2_pitch_visualizer`
- **Build Command:** 
  ```
  pip install -r requirements.txt && python -m textblob.download_corpora && python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"
  ```
- **Start Command:** Same as Challenge 1

---

### Option 2: Railway (Alternative - Also Free)

1. **Go to:** https://railway.app
2. **Sign up with GitHub**
3. **New Project → Deploy from GitHub repo**
4. **Select your repository**
5. **Railway auto-detects Python** and deploys!
6. **Set environment variables** (if needed)
7. **Your live URL:** Will be provided by Railway

---

### Option 3: Vercel (For Static/API)

1. **Go to:** https://vercel.com
2. **Import Git Repository**
3. **Select your repo**
4. **Configure:**
   - Framework: Other
   - Build Command: `pip install -r requirements.txt`
5. **Deploy**

---

### Option 4: Hugging Face Spaces (Specialized)

1. **Go to:** https://huggingface.co/spaces
2. **Create new Space**
3. **Choose:** Gradio or Streamlit SDK
4. **Connect GitHub repo**
5. **Configure and deploy**

---

## 📝 After Deployment

### Update Your README

Replace these placeholders in your GitHub README:

```markdown
## 🚀 Live Demos

**Challenge 1:** [The Empathy Engine](https://empathy-engine.onrender.com)
**Challenge 2:** [The Pitch Visualizer](https://pitch-visualizer.onrender.com)
```

### Update Google Form Submission

If the form accepts GitHub links:
- **GitHub Repository:** `https://github.com/YOUR-USERNAME/darwix-ai-intern-assessment`
- **Live Demo 1:** `https://empathy-engine.onrender.com`
- **Live Demo 2:** `https://pitch-visualizer.onrender.com`

---

## 🎯 Quick Commands Reference

```powershell
# Check repository status
git status

# Add new changes
git add .
git commit -m "Update: description of changes"
git push

# View remote
git remote -v

# Create new branch
git checkout -b feature-name

# Pull latest changes
git pull origin main
```

---

## 🔧 Troubleshooting

### Issue: Git push asks for password

**Solution:** Use Personal Access Token
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Use token as password when pushing

### Issue: Deployment fails on Render

**Check:**
- Build logs for errors
- Ensure requirements.txt is correct
- Verify start command
- Check Python version compatibility

### Issue: Port already in use locally

**Solution:**
```powershell
# Find process using port
netstat -ano | findstr :8005

# Kill process (replace PID)
Stop-Process -Id <PID> -Force
```

---

## 🎉 Success Checklist

- [ ] Git repository initialized locally
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] README updated with your info
- [ ] Challenge 1 deployed on Render/Railway
- [ ] Challenge 2 deployed on Render/Railway
- [ ] Live URLs working
- [ ] Google Form updated with links
- [ ] Repository is public (for portfolio)

---

## 📧 Final Submission Info

**Include in Google Form:**

```
GitHub Repository: https://github.com/YOUR-USERNAME/darwix-ai-intern-assessment

Live Demos:
- Challenge 1 (Empathy Engine): https://empathy-engine.onrender.com
- Challenge 2 (Pitch Visualizer): https://pitch-visualizer.onrender.com

Technology Stack: Python, FastAPI, TextBlob, NLTK, Pillow, pyttsx3
Features: Web interfaces, emotion detection, storyboard generation
Documentation: Comprehensive README and setup guides
```

---

🎊 **You're ready to deploy!** Follow the steps above and your project will be live!
