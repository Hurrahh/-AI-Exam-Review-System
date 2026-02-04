# 📝 Student Answer Sheet Analysis System

A comprehensive AI-powered system for analyzing student answer sheets using Google's Gemini AI. This system provides detailed performance analysis, topic-wise breakdowns, error detection, and personalized feedback.

## 🌟 Features

### Core Analysis Features
1. **Overall Score Dashboard**
   - Total questions and accuracy metrics
   - Marks obtained vs total marks
   - Visual progress indicators

2. **Topic-Wise Performance Analysis**
   - Identification of strong topics
   - Detailed breakdown of areas needing improvement
   - Specific recommendations for each topic

3. **Question-Wise Breakdown**
   - Grouping of correctly answered questions
   - Individual analysis of questions needing improvement
   - Expected vs actual answers comparison

4. **Error Analysis**
   - Conceptual errors detection
   - Calculation mistakes identification
   - Incomplete steps tracking
   - Poor explanation detection
   - Notation errors identification

5. **Strengths and Improvements**
   - Clear identification of student strengths
   - Actionable improvement suggestions

6. **Personalized Feedback**
   - Customized feedback based on performance
   - Action plan for improvement
   - Motivational messaging

7. **AI Tutor Chat**
   - Ask questions about your performance
   - Get clarifications on specific topics
   - Receive personalized guidance

### Customization Options

**Evaluation Settings:**
- **Checking Strictness**: Lenient, Moderate, Strict, Very Strict
- **Expected Answer Depth**: Basic, Intermediate, Advanced, Expert
- **Focus Areas**: Multiple areas including conceptual understanding, problem-solving, etc.

**Feedback Settings:**
- **Feedback Tone**: Highly Encouraging, Balanced, Direct, Critical
- **Explanation Level**: Brief, Moderate, Detailed, Very Detailed

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download the project files**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access the application**
   - The app will automatically open in your browser
   - Default URL: [Judex](https://judex-ai.streamlit.app/)

## 📖 Usage Guide

### Step 1: Configure API Key
1. Enter your Google Gemini API key in the sidebar
2. The key is required for the analysis to work

### Step 2: Upload Documents
- **Answer Sheet** (Required): The student's completed answer sheet (PDF/Image)
- **Question Paper** (Optional): The original question paper
- **Answer Key** (Optional): The marking scheme or answer key
- **Syllabus** (Optional): Course syllabus for context

### Step 3: Configure Evaluation Settings
1. **Checking Strictness**: Choose how strictly to evaluate answers
2. **Expected Answer Depth**: Set the expected level of detail
3. **Focus Areas**: Select which aspects to prioritize

### Step 4: Configure Feedback Settings
1. **Feedback Tone**: Choose the tone of feedback
2. **Explanation Level**: Set how detailed explanations should be

### Step 5: Analyze
1. Click "🚀 Analyze Answer Sheet"
2. Wait for the analysis to complete (may take 1-2 minutes)
3. View the comprehensive report

### Step 6: Interact
1. Navigate to the "Ask Questions" tab
2. Ask specific questions about performance
3. Get personalized guidance from the AI tutor

## 🎯 Use Cases

### For Students
- Understand mistakes and learning gaps
- Get personalized study recommendations
- Track performance across topics
- Prepare better for future exams

### For Teachers
- Quickly analyze multiple answer sheets
- Identify common errors across students
- Generate detailed feedback reports
- Save time on manual evaluation

### For Tutors
- Provide data-driven insights to students
- Create customized learning plans
- Track student progress over time
- Identify teaching effectiveness

## 🔧 Technical Details

### AI Model
- **Primary Model**: Google Gemini 1.5 Pro
  - Used for comprehensive analysis
  - Excellent OCR capabilities for diagrams and handwriting
  - Supports multi-modal inputs (text + images)

### Document Processing
- **PDF Support**: Extracts text from PDF documents
- **Image Support**: Processes PNG, JPG, JPEG formats
- **Multi-page Support**: Handles multi-page answer sheets

### Analysis Components

1. **OCR & Text Extraction**
   - Gemini's built-in OCR for handwritten text
   - Diagram and graph recognition
   - Mathematical notation understanding

2. **Evaluation Engine**
   - Contextual answer matching
   - Partial credit assessment
   - Topic classification

3. **Error Detection**
   - Pattern recognition for common mistakes
   - Severity assessment
   - Remediation suggestions

4. **Feedback Generation**
   - Personalized messaging
   - Tone-adaptive responses
   - Action-oriented recommendations

## 📊 Output Format

The system generates a comprehensive JSON report containing:
```json
{
  "personal_details": {...},
  "overall_score": {...},
  "topic_wise_performance": {...},
  "question_wise_breakdown": {...},
  "error_analysis": {...},
  "strengths": [...],
  "improvements_needed": [...],
  "personal_feedback": {...}
}
```

## 🔒 Privacy & Security

- API keys are never stored
- Uploaded documents are processed in memory
- No data is permanently saved
- Session-based analysis only

## 🛠️ Troubleshooting

### Common Issues

**Issue**: "API Key Invalid"
- **Solution**: Verify your Gemini API key is correct
- Check if the key has proper permissions

**Issue**: "Analysis Failed"
- **Solution**: Ensure documents are clear and readable
- Try with higher quality images
- Check file format compatibility

**Issue**: "OCR Not Working Well"
- **Solution**: Use higher resolution images
- Ensure good lighting in scanned documents
- Avoid blurry or skewed images

**Issue**: "Slow Analysis"
- **Solution**: This is normal for large documents
- Gemini processes images thoroughly
- Complex answer sheets take 1-2 minutes

## 📝 Best Practices

### For Best Results

1. **Upload Quality**
   - Use high-resolution scans (300 DPI minimum)
   - Ensure good lighting and contrast
   - Keep documents straight (not skewed)

2. **Document Preparation**
   - Include question paper for better context
   - Provide answer key for accurate marking
   - Add syllabus for topic classification

3. **Settings Configuration**
   - Match strictness to actual exam standards
   - Set depth based on student level
   - Choose appropriate feedback tone

4. **Using the Chat Feature**
   - Ask specific questions
   - Reference question numbers
   - Request clarification on feedback

## 🔄 Future Enhancements

Potential improvements:
- [ ] Batch processing for multiple students
- [ ] Comparative analysis across students
- [ ] Progress tracking over time
- [ ] Export to PDF/Word reports
- [ ] Integration with Learning Management Systems
- [ ] Support for more languages
- [ ] Custom rubric creation
- [ ] Video explanation generation

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues or questions:
- Check the troubleshooting section
- Review the usage guide
- Consult Gemini API documentation

## 🙏 Acknowledgments

- Google Gemini AI for powerful analysis capabilities
- Streamlit for the excellent web framework
- Open-source community for supporting libraries

---

**Note**: This system is designed to assist in educational assessment but should not replace human judgment in critical evaluation scenarios. Use it as a tool to enhance, not replace, teacher feedback.
