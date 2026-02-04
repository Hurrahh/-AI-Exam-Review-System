# Project Structure

## Overview
Student Answer Sheet Analysis System - A comprehensive AI-powered solution for analyzing student answer sheets using Google's Gemini AI.

## File Structure

```
student-analysis-system/
│
├── student_analysis_app.py      # Main Streamlit application
├── analysis_utils.py             # Enhanced utility functions
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
│
├── README.md                     # Complete documentation
├── QUICK_START.md               # Quick start guide
└── PROJECT_STRUCTURE.md         # This file
```

## File Descriptions

### Core Application Files

#### `student_analysis_app.py`
**Purpose:** Main Streamlit application
**Key Components:**
- Page configuration and styling
- Document upload handlers
- Gemini API integration
- Analysis display functions
- Chatbot interface
- Session state management

**Main Functions:**
- `configure_gemini(api_key)` - Initialize Gemini API
- `extract_text_from_pdf(pdf_file)` - Extract text from PDFs
- `process_image_for_gemini(image_file)` - Process images
- `analyze_answer_sheet(...)` - Main analysis function
- `display_analysis(analysis)` - Display results
- `chatbot_interface(model, analysis)` - Chat functionality
- `main()` - Application entry point

#### `analysis_utils.py`
**Purpose:** Enhanced analysis utilities and helper functions
**Key Classes:**
- `AnalysisEnhancer` - Performance calculations and study plans
- `ResponseFormatter` - Report formatting (Markdown, HTML)
- `QuestionAnalyzer` - Advanced question analysis
- `ChatbotEnhancer` - Enhanced chatbot capabilities

**Key Features:**
- Percentile calculations
- Study plan generation
- Pattern identification
- Report generation
- Resource suggestions
- Contextual prompts

#### `config.py`
**Purpose:** Configuration and settings management
**Configuration Sections:**
- `GEMINI_CONFIG` - Model and API settings
- `ANALYSIS_SETTINGS` - Evaluation parameters
- `UI_SETTINGS` - Interface customization
- `DOCUMENT_SETTINGS` - File processing settings
- `CHATBOT_SETTINGS` - Chat configuration
- `ANALYSIS_CATEGORIES` - Available options
- `PROMPT_TEMPLATES` - Prompt engineering
- `FEATURES` - Feature flags
- `PERFORMANCE` - Performance settings

### Documentation Files

#### `README.md`
Complete project documentation including:
- Feature overview
- Setup instructions
- Usage guide
- Technical details
- Troubleshooting
- Best practices

#### `QUICK_START.md`
Quick reference guide covering:
- 5-minute setup
- Common use cases
- Tips for best results
- Sample questions
- Quick fixes

#### `PROJECT_STRUCTURE.md`
This file - project organization and architecture

### Configuration Files

#### `requirements.txt`
Python dependencies:
- streamlit (Web framework)
- google-generativeai (Gemini API)
- Pillow (Image processing)
- PyPDF2 (PDF handling)
- python-dotenv (Environment variables)

#### `.env.example`
Template for environment variables:
- GEMINI_API_KEY
- Default settings

## Data Flow

```
┌─────────────────┐
│  User Uploads   │
│   Documents     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Document       │
│  Processing     │
│  (OCR/Extract)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini API     │
│  Analysis       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Response  │
│  Parsing        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  UI Display     │
│  & Formatting   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  User           │
│  Interaction    │
│  (Chat/Export)  │
└─────────────────┘
```

## Component Architecture

### 1. Frontend Layer (Streamlit)
- User interface
- File uploads
- Results display
- Chat interface
- Settings configuration

### 2. Processing Layer
- Document handling
- Text extraction
- Image processing
- Data validation

### 3. AI Layer (Gemini)
- Answer sheet analysis
- Error detection
- Feedback generation
- Chat responses

### 4. Presentation Layer
- Result formatting
- Report generation
- Data visualization
- Export functionality

## Session State Management

The application uses Streamlit's session state to maintain:
- `analysis_result` - Stored analysis data
- `chat_history` - Conversation history
- `documents` - Uploaded document references

## Customization Points

### Adding New Error Types
1. Update `ANALYSIS_CATEGORIES` in `config.py`
2. Modify prompt in `analyze_answer_sheet()`
3. Add display logic in `display_analysis()`

### Changing UI Theme
1. Update `UI_SETTINGS` in `config.py`
2. Modify CSS in `student_analysis_app.py`
3. Adjust color scheme

### Adding New Features
1. Set feature flag in `config.py`
2. Implement functionality
3. Update documentation

## Extension Ideas

### Planned Features
- [ ] Batch processing for multiple students
- [ ] Progress tracking over time
- [ ] Comparative analysis
- [ ] Custom rubric support
- [ ] LMS integration
- [ ] Multi-language support
- [ ] Video explanations

### Integration Possibilities
- Google Classroom
- Canvas LMS
- Moodle
- Microsoft Teams
- Slack notifications

## Development Workflow

### Testing Changes
1. Modify files
2. Run locally: `streamlit run student_analysis_app.py`
3. Test with sample documents
4. Verify analysis quality

### Adding Dependencies
1. Update `requirements.txt`
2. Install: `pip install -r requirements.txt`
3. Test imports

### Deployment Options
- Streamlit Cloud (Recommended)
- Heroku
- AWS/GCP/Azure
- Docker container
- Local server

## Performance Considerations

### Optimization Areas
1. **Image Processing**
   - Compress large images
   - Use appropriate resolution
   - Lazy loading

2. **API Calls**
   - Batch requests when possible
   - Cache responses
   - Handle rate limits

3. **UI Rendering**
   - Paginate large results
   - Progressive loading
   - Efficient state management

## Security Considerations

### Data Privacy
- API keys stored in session only
- No permanent data storage
- Documents processed in memory
- Secure file handling

### Best Practices
- Validate all inputs
- Sanitize user data
- Handle errors gracefully
- Use HTTPS in production

## Troubleshooting Guide

### Common Issues
1. **Import Errors**
   - Check `requirements.txt`
   - Verify Python version
   - Reinstall dependencies

2. **API Errors**
   - Verify API key
   - Check quota limits
   - Review error messages

3. **Processing Errors**
   - Validate file formats
   - Check file sizes
   - Ensure document quality

## Version History

### v1.0 (Current)
- Initial release
- Core analysis features
- Chat functionality
- Basic customization

### Future Versions
- v1.1: Batch processing
- v1.2: Progress tracking
- v2.0: LMS integration

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

See README.md for license information.

## Support

For issues or questions:
- Check documentation
- Review troubleshooting guide
- Consult Gemini API docs
- Contact maintainers

---

**Last Updated:** February 2026
**Version:** 1.0
