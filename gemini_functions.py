import google.genai as genai
from google.genai import types
import os
import streamlit as st
import json
from dotenv import load_dotenv
from datetime import datetime
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload
# from google.oauth2 import service_account
# import io
from github import Github


load_dotenv()

def get_gemini_client():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in environment variables!")
        st.stop()
    return genai.Client(api_key=api_key)


# def sync_to_drive_by_timestamp(file, category):
#
#     try:
#         creds_info = st.secrets["gcp_service_account"]
#         # creds_info = os.getenv("gcp_service_account")
#         creds = service_account.Credentials.from_service_account_info(
#             creds_info,
#             scopes=['https://www.googleapis.com/auth/drive']
#         )
#         service = build('drive', 'v3', credentials=creds)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         drive_file_name = f"{timestamp}_{category}_{file.name}"
#         folder_id = st.secrets["GDRIVE_FOLDER_ID"]
#         # folder_id = os.getenv("GDRIVE_FOLDER_ID")
#
#         file_metadata = {
#             'name': drive_file_name,
#             'parents': [folder_id]
#         }
#
#         fh = io.BytesIO(file.getbuffer())
#         media = MediaIoBaseUpload(
#             fh,
#             mimetype=file.type,
#             resumable=True
#         )
#
#         uploaded_file = service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id',
#             supportsAllDrives=True
#         ).execute()
#
#         return uploaded_file.get('id')
#     except Exception as e:
#         st.error(f"Failed to sync to Drive: {e}")
#         return None


def sync_to_github(file, category,session_folder):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"].strip())
        repo = g.get_repo(st.secrets["GITHUB_REPO"].strip())

        file_path = f"database/{session_folder}/{category}_{file.name}"

        content = file.getbuffer().tobytes()

        repo.create_file(
            path=file_path,
            message=f"Archive Session: {session_folder}",
            content=content,
            branch="main"
        )
        return True
    except Exception as e:
        st.error(f"❌ GitHub Archive Failed: {e}")
        return False

def upload_to_gemini(client, file):
    try:
        temp_path = f"./{file.name}"
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        uploaded_file = client.files.upload(file=temp_path)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return uploaded_file
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return None


def create_analysis_prompt(metadata, has_answer_key, has_syllabus):
    subject = metadata.get('subject', 'Subject')
    class_num = metadata.get('class', '9')
    exam_type = metadata.get('exam_type', 'Exam')
    strictness = metadata.get('strictness', 0.5)
    answer_depth = metadata.get('answer_depth', 'Medium')
    feedback_tone = metadata.get('feedback_tone', 'Encouraging')
    explanation_level = metadata.get('explanation_level', 'Grade-appropriate')
    focus_areas = ', '.join(metadata.get('focus_areas', ['Conceptual understanding']))
    board = metadata.get('board', 'CBSE')

    prompt = f"""You are an expert educational evaluator. Analyze the student's answer sheet comprehensively and provide a detailed JSON response.

**EVALUATION SETTINGS:**
- Subject: {subject}
- Class Level: {class_num}
- Board: {board}
- Exam Type: {exam_type}
- Checking Strictness: {strictness} (0.3=very lenient, 0.5=balanced, 0.7=strict, 1.0=very strict)
- Expected Answer Depth: {answer_depth}
- Focus Areas: {focus_areas}

**FEEDBACK SETTINGS:**
- Feedback Tone: {feedback_tone}
- Explanation Level: {explanation_level}

**DOCUMENTS PROVIDED:**
- Answer Sheet: Provided (analyze the handwriting, diagrams, calculations directly from the image/PDF)
- Question Paper: Provided (analyze the question paper, diagrams, directly from the image/PDF)
- Answer Key: {"Provided - use for accurate marking" if has_answer_key else "Not Provided - evaluate based on your expertise"}
- Syllabus: {"Provided - map topics from syllabus" if has_syllabus else "Not Provided - identify topics from questions"}

**CRITICAL INSTRUCTIONS:**
1. Carefully read and analyze the answer sheet image/PDF directly
2. Extract all text, diagrams, calculations, and handwritten content
3. Match answers with questions from the question paper
4. Compare with answer key if provided
5. Identify errors by actually reading what the student wrote
6. Extract student's personal details from answer sheet (name, roll number, etc.)

**ANALYSIS REQUIREMENTS:**

Return a JSON object with this exact structure:

{{
    "personal_details": {{
        "student_name": "Extract from answer sheet if visible, otherwise 'Not found'",
        "exam_name": "Extract from documents if visible, otherwise use '{exam_type}'",
        "date": "Extract if visible, otherwise 'Not found'",
        "subject": "{subject}",
        "class": "{class_num}",
        "roll_number": "Extract if visible, otherwise 'Not found'",
        "school_name": "Extract if visible, otherwise 'Not found'"
    }},
    "overall_score": {{
        "total_questions": <count all questions from question paper>,
        "attempted_questions": <count attempted>,
        "correct_answers": <fully correct count>,
        "partially_correct": <partially correct count>,
        "incorrect_answers": <incorrect count>,
        "unattempted": <not attempted count>,
        "accuracy_percentage": <percentage of correct answers>,
        "total_marks_obtained": <actual marks earned>,
        "total_marks": <maximum possible marks>
    }},
    "topic_wise_performance": {{
        "strong_topics": [
            {{
                "topic": "{subject}-specific topic name",
                "questions": [<question numbers>],
                "score": "X/Y marks",
                "accuracy": <percentage>,
                "details": "Detailed explanation of strong performance with examples"
            }}
        ],
        "areas_for_improvement": [
            {{
                "topic": "{subject}-specific topic name",
                "questions": [<question numbers>],
                "score": "X/Y marks",
                "accuracy": <percentage>,
                "gaps": ["Specific conceptual gap 1", "Specific gap 2"],
                "recommendations": "Detailed, actionable recommendations specific to this topic"
            }}
        ]
    }},
    "question_wise_breakdown": {{
        "highly_accurate_questions": [
            {{
                "question_numbers": [<list all 100% correct questions>],
                "topic": "{subject} topic",
                "summary": "One-line summary: These questions were answered perfectly"
            }}
        ],
        "needs_improvement": [
            {{
                "question_number": <number>,
                "question_text": "The actual question text from question paper",
                "student_answer": "Exactly what the student wrote (transcribe from image accurately)",
                "expected_answer": "What was expected or from answer key",
                "marks_obtained": <marks>,
                "total_marks": <max marks>,
                "issues": ["Specific issue 1", "Specific issue 2"],
                "feedback": "Detailed constructive feedback explaining what went wrong",
                "what_was_correct": "What parts were right (if any)",
                "what_was_wrong": "What parts were wrong and why"
            }}
        ]
    }},
    "error_analysis": {{
        "conceptual_errors": [
            {{
                "description": "Clear description of the conceptual misunderstanding",
                "questions_affected": [<question numbers>],
                "severity": "High/Medium/Low",
                "remedy": "How to fix this conceptual gap",
                "example": "Example from their answer showing this error"
            }}
        ],
        "calculation_mistakes": [
            {{
                "description": "Type of calculation error",
                "questions_affected": [<question numbers>],
                "pattern": "Is this recurring? Describe pattern",
                "example": "Show the wrong calculation vs correct"
            }}
        ],
        "incomplete_steps": [
            {{
                "description": "What steps were missing",
                "questions_affected": [<question numbers>],
                "impact": "How this affected the grade",
                "missing_steps": ["Step 1 that was missing", "Step 2 that was missing"]
            }}
        ],
        "poor_explanation": [
            {{
                "description": "Communication issue identified",
                "questions_affected": [<question numbers>],
                "suggestion": "How to write clearer explanations",
                "example": "Show their explanation vs better one"
            }}
        ],
        "notation_errors": [
            {{
                "description": "Notation mistakes found",
                "questions_affected": [<question numbers>],
                "correct_notation": "What should be used",
                "example": "Wrong notation vs correct notation"
            }}
        ]
    }},
    "strengths": [
        "Specific strength 1 with evidence from answers",
        "Specific strength 2 with evidence from answers",
        "Specific strength 3 with evidence from answers"
    ],
    "improvements_needed": [
        "Specific improvement area 1 with actionable steps",
        "Specific improvement area 2 with actionable steps",
        "Specific improvement area 3 with actionable steps"
    ],
    "personal_feedback": {{
        "opening": "Warm, personalized greeting addressing the student by name if available",
        "overall_impression": "Balanced view of their performance in this {subject} {exam_type}",
        "detailed_analysis": "Very detailed 200-300 word paragraph covering: what they did well with examples, where they struggled with specific questions, patterns observed, overall assessment using {feedback_tone} tone",
        "key_takeaways": [
            "Important takeaway 1 from this exam",
            "Important takeaway 2 from this exam",
            "Important takeaway 3 from this exam"
        ],
        "action_plan": [
            "Specific, actionable step 1 with timeline (e.g., 'Practice 10 problems on topic X this week')",
            "Specific, actionable step 2 with timeline",
            "Specific, actionable step 3 with timeline"
        ],
        "motivation": "Encouraging closing message with realistic optimism suited to {feedback_tone}",
        "estimated_improvement_potential": "Realistic score improvement estimate with reasoning based on identified gaps"
    }}
}}

**GRADING STRICTNESS GUIDE ({strictness}):**
- 0.3-0.4: Very lenient - generous partial marks, overlook minor errors, focus on effort
- 0.5-0.6: Balanced - standard evaluation, fair partial marks, standard expectations
- 0.7-0.8: Strict - penalize incomplete work, require clear steps, limited partial marks
- 0.9-1.0: Very strict - demand perfection, mark every error, minimal partial marks

**IMPORTANT NOTES:**
1. For "highly_accurate_questions", list ALL question numbers that got 100% marks in one entry
2. For "needs_improvement", create individual entries for each question that was partially or fully incorrect
3. Actually READ the handwriting and diagrams from the uploaded images
4. Provide REAL analysis based on what you SEE in the documents, not generic feedback
5. Extract personal details carefully from the answer sheet header/top section

OUTPUT: Provide ONLY the JSON structure above with actual analysis data. No additional text."""

    return prompt


def analyze_exam_with_gemini(client, files_data, metadata):
    answer_sheet = files_data.get('answer_sheet')
    question_paper = files_data.get('question_paper')
    answer_key = files_data.get('answer_key')
    syllabus = files_data.get('syllabus')

    has_answer_key = answer_key is not None
    has_syllabus = syllabus is not None

    prompt = create_analysis_prompt(metadata, has_answer_key, has_syllabus)

    try:
        contents = [prompt]

        if answer_sheet:
            st.info("📄 Uploading answer sheet to Gemini cloud...")
            uploaded_answer = upload_to_gemini(client, answer_sheet)
            if uploaded_answer:
                contents.append(uploaded_answer)

        if question_paper:
            st.info("📄 Uploading question paper...")
            uploaded_question = upload_to_gemini(client, question_paper)
            if uploaded_question:
                contents.append(uploaded_question)

        if answer_key:
            st.info("📄 Uploading answer key...")
            uploaded_key = upload_to_gemini(client, answer_key)
            if uploaded_key:
                contents.append(uploaded_key)

        if syllabus:
            st.info("📄 Reading syllabus...")
            syllabus_text = syllabus.read().decode('utf-8')
            contents.append(f"\n\nSYLLABUS CONTENT:\n{syllabus_text}")

        # st.info("🤖 Analyzing with Gemini AI... This may take 30-60 seconds...")
        #
        # response = client.models.generate_content(
        #     model='gemini-2.5-flash',
        #     contents=contents,
        #     config=types.GenerateContentConfig(
        #         response_mime_type='application/json',
        #         temperature=0.3
        #     )
        # )
        #
        # if not response or not response.text:
        #     st.error("Empty response from AI.")
        #     return None
        #
        # response_text = response.text.strip()
        #
        # if "```" in response_text:
        #     response_text = response_text.replace("```json", "").replace("```", "").strip()
        #
        # try:
        #     analysis = json.loads(response_text)
        #     return analysis
        # except json.JSONDecodeError as je:
        #     st.error(f"Failed to parse AI output as JSON: {str(je)}")
        #     with st.expander("Show Raw Output"):
        #         st.code(response_text)
        #     return None
        st.info("🤖 Analyzing with Gemini AI... (Streaming mode active)")

        try:
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    temperature=0.1,
                )
            )

            full_response_text = ""
            progress_bar = st.progress(0, text="AI is thinking and grading...")

            for i, chunk in enumerate(response_stream):
                if chunk.text:
                    full_response_text += chunk.text
                    progress_bar.progress(min((i + 1) * 5, 100), text="📥 Receiving detailed analysis...")

            if not full_response_text:
                st.error("Empty response from AI.")
                return None

            clean_json = full_response_text.replace("```json", "").replace("```", "").strip()

            try:
                analysis = json.loads(clean_json)
                progress_bar.empty()
                return analysis
            except json.JSONDecodeError as je:
                st.error(f"Failed to parse AI output: {str(je)}")
                st.expander("View Raw Output").code(full_response_text)
                return None

        except Exception as e:
            st.error(f"Error during streaming analysis: {str(e)}")
            return None

    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        return None


def chat_with_gemini(client, user_question, analysis, metadata):
    context_prompt = f"""You are a supportive, expert AI tutor discussing exam performance with a student.

STUDENT DETAILS:
- Subject: {metadata.get('subject')}
- Class: {metadata.get('class')}
- Board: {metadata.get('board')}
- Exam Type: {metadata.get('exam_type')}
- Feedback Tone: {metadata.get('feedback_tone', 'Encouraging')}

COMPLETE EXAM ANALYSIS DATA:
{json.dumps(analysis, indent=2)}

STUDENT'S QUESTION:
{user_question}

INSTRUCTIONS FOR YOUR RESPONSE:
1. Answer based ONLY on the provided analysis data above
2. Be {metadata.get('feedback_tone', 'encouraging').lower()} but honest about areas needing work
3. If they ask about specific questions, refer to 'question_wise_breakdown' section
4. If they ask about topics, refer to 'topic_wise_performance' section
5. If they ask about mistakes, refer to 'error_analysis' section
6. Provide specific, actionable advice
7. Use {metadata.get('explanation_level', 'grade-appropriate').lower()} language
8. Keep response focused and conversational (150-250 words)
9. Reference actual question numbers and topics when relevant
10. Format with markdown for readability (use bullet points, bold, etc.)

Your response:"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=context_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"❌ Error getting response: {str(e)}"
