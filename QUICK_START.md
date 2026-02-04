# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Get Gemini API Key (2 minutes)
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with "AI...")

### Step 3: Run the Application (1 minute)
```bash
streamlit run app.py
```

### Step 4: Start Analyzing (1 minute)
1. Paste your API key in the sidebar
2. Upload answer sheet
3. Click "Analyze Answer Sheet"
4. View results!

## Common Use Cases

### Use Case 1: Quick Performance Check
**Upload:** Just the answer sheet
**Time:** ~1 minute
**Result:** Basic accuracy and error detection

### Use Case 2: Comprehensive Analysis
**Upload:** Answer sheet + Question paper + Answer key
**Time:** ~2 minutes
**Result:** Detailed topic-wise breakdown and personalized feedback

### Use Case 3: Study Plan Generation
**Upload:** Answer sheet + Question paper + Answer key + Syllabus
**Time:** ~2 minutes
**Result:** Complete analysis with curriculum-aligned recommendations

## Tips for Best Results

### Document Quality
✅ DO:
- Use 300 DPI or higher scans
- Ensure good lighting
- Keep documents flat and straight
- Use clear, readable handwriting

❌ DON'T:
- Use blurry photos
- Submit skewed documents
- Use very low resolution images
- Include multiple papers in one image

### Settings Configuration

**For Strict Evaluation:**
- Strictness: Very Strict
- Depth: Advanced/Expert
- Focus: All areas

**For Encouraging Feedback:**
- Tone: Highly Encouraging
- Explanation: Very Detailed

**For Quick Overview:**
- Depth: Basic/Intermediate
- Explanation: Brief/Moderate

## Sample Questions to Ask AI Tutor

After analysis, try asking:
- "What are my top 3 priority topics to study?"
- "How can I avoid the calculation mistakes I made?"
- "Can you explain why I got question 5 wrong?"
- "What's a realistic score improvement I can achieve?"
- "How should I structure my next 2 weeks of study?"

## Troubleshooting Quick Fixes

**Problem:** API Key Error
**Fix:** Make sure you copied the complete key including "AI" prefix

**Problem:** Slow Analysis
**Fix:** Normal for large files - wait 1-2 minutes

**Problem:** Poor OCR Results
**Fix:** Re-scan documents at higher resolution with better lighting

**Problem:** Missing Question Details
**Fix:** Upload the question paper for better context

## Advanced Features

### Export Report
After analysis, click "Download Detailed Report" to save results as JSON

### Multiple Focus Areas
Select multiple focus areas to get targeted analysis:
- Conceptual Understanding
- Problem Solving
- Written Communication
- Calculation Accuracy
- Diagram Quality

### Feedback Customization
Adjust tone and detail level based on:
- Student age/level
- Purpose (self-study vs teacher review)
- Sensitivity to criticism

## Next Steps After Analysis

1. **Review Overall Score** - Understand your current level
2. **Check Topic Performance** - Identify strong and weak areas
3. **Study Question Breakdown** - Learn from specific mistakes
4. **Read Error Analysis** - Understand error patterns
5. **Create Action Plan** - Use personalized feedback
6. **Ask Questions** - Clarify doubts with AI tutor
7. **Practice** - Work on weak areas
8. **Re-test** - Analyze again after practice

## Support Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **Streamlit Docs:** https://docs.streamlit.io
- **Issue Tracker:** Check README.md for support options

---

**Remember:** This tool is meant to supplement, not replace, teacher feedback. Use it as a learning aid!
