# 🌐 Web Application Links

Both challenges are now running as web applications on your local machine!

---

## 🎙 Challenge 1: The Empathy Engine

**Link:** http://localhost:8000

**What it does:**
- Enter emotional text
- Analyzes the emotion (joy, sadness, anger, fear, surprise, disgust, neutral)
- Generates emotionally expressive speech
- Play audio instantly in your browser

**Try these examples:**
- "I am so excited and happy about this amazing news!"
- "This is absolutely frustrating and unacceptable!"
- "I feel sad and disappointed about what happened."
- "Wow! I can't believe this is happening!"

---

## 🖼 Challenge 2: The Pitch Visualizer

**Link:** http://localhost:8001

**What it does:**
- Enter a narrative story
- Automatically segments into key scenes
- Generates a visual storyboard
- Download the storyboard image

**Try these examples:**
- "Sarah walked into the old abandoned warehouse, her flashlight cutting through the darkness. Suddenly, she heard a noise from the corner. Behind the dusty crates, she discovered an old journal. This journal belonged to her grandmother who had disappeared 20 years ago."

---

## 📌 Quick Access

| Challenge | Link | Port |
|-----------|------|------|
| **Challenge 1** - The Empathy Engine | http://localhost:8000 | 8000 |
| **Challenge 2** - The Pitch Visualizer | http://localhost:8001 | 8001 |

---

## 🛑 To Stop the Servers

If you need to stop the applications:

1. Open Task Manager (Ctrl + Shift + Esc)
2. Find "python.exe" processes
3. End the processes running on ports 8000 and 8001

Or run this PowerShell command:
```powershell
Get-Process python | Where-Object {$_.MainWindowTitle -like "*app.py*"} | Stop-Process
```

---

## 🔄 To Restart the Servers

If the servers stop, restart them with:

**Challenge 1:**
```bash
cd "C:\Users\asus\Desktop\Darwix AI assignment\challenge1_empathy_engine"
python app.py
```

**Challenge 2:**
```bash
cd "C:\Users\asus\Desktop\Darwix AI assignment\challenge2_pitch_visualizer"
python app.py
```

---

## ✨ Features

### Challenge 1 Interface:
- ✅ Text input area
- ✅ Real-time emotion detection
- ✅ Voice parameter display (rate, pitch, volume)
- ✅ Instant audio playback
- ✅ Example texts to try
- ✅ Beautiful gradient UI

### Challenge 2 Interface:
- ✅ Narrative text input
- ✅ Title and scene count customization
- ✅ Scene breakdown display
- ✅ Generated storyboard preview
- ✅ Download button for storyboard
- ✅ Example narratives to try
- ✅ Responsive design

---

## 📱 Access from Other Devices

To access from other devices on your network:

1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address"

2. Access from other devices using:
   - Challenge 1: `http://YOUR_IP:8000`
   - Challenge 2: `http://YOUR_IP:8001`

---

## 🎉 Enjoy Exploring!

Both applications are fully functional and ready to use. Click the links above to start!
