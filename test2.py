import streamlit as st
import json
import os
from gemini_functions import get_gemini_client, analyze_exam_with_gemini, chat_with_gemini
from datetime import datetime
import time

st.set_page_config(
    page_title="AI Exam Review System",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_class_metadata(class_num: str):
    try:
        filepath = f'metadata/class_{class_num}_metadata.json'
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading metadata: {e}")
    return None


def initialize_session_state():
    if 'metadata' not in st.session_state:
        st.session_state.metadata = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_class' not in st.session_state:
        st.session_state.selected_class = None


def render_metadata_form():
    st.markdown("### 📋 Exam Configuration")

    class_options = ["5", "6", "7", "8", "9", "10", "11", "12"]

    class_num = st.selectbox(
        "Select Class",
        options=class_options,
        key='class_selector'
    )

    if class_num != st.session_state.selected_class:
        st.session_state.selected_class = class_num
        class_metadata = load_class_metadata(class_num)

        if class_metadata:
            st.session_state.temp_metadata = class_metadata

    if 'temp_metadata' in st.session_state and st.session_state.temp_metadata:
        metadata = st.session_state.temp_metadata

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**📚 Academic Information**")

            subject = st.selectbox(
                "Subject",
                options=metadata.get('available_subjects', ["Mathematics"]),
                index=metadata.get('available_subjects', ["Mathematics"]).index(
                    metadata.get('default_subject', 'Mathematics')
                )
            )

            board = st.selectbox(
                "Board",
                options=metadata.get('boards', ["CBSE"]),
                index=metadata.get('boards', ["CBSE"]).index(
                    metadata.get('default_board', 'CBSE')
                )
            )

            exam_type = st.selectbox(
                "Exam Type",
                options=metadata.get('exam_types', ["Unit Test"]),
                index=metadata.get('exam_types', ["Unit Test"]).index(
                    metadata.get('default_exam_type', 'Unit Test')
                )
            )

        with col2:
            st.markdown("**⚙️ Evaluation Settings**")

            strictness_config = metadata.get('checking_strictness', {})
            strictness = st.select_slider(
                "Checking Strictness",
                options=strictness_config.get(
                    'options',
                    ['Lenient', 'Moderate', 'Strict', 'Very Strict']
                ),
                value=strictness_config.get('default', 'Moderate')
            )

            st.markdown(f"*{strictness_config.get('description', '')}*")

            answer_depth_config = metadata.get('answer_depth', {})
            answer_depth = st.select_slider(
                "Expected Answer Depth",
                options=answer_depth_config.get('options', ['Basic', 'Intermediate', 'Advanced', 'Expert']),
                value=answer_depth_config.get('default', 'Intermediate')
            )

            focus_areas = st.multiselect(
                "Focus Areas",
                ['Conceptual Understanding', 'Problem Solving', 'Written Communication',
                 'Calculation Accuracy', 'Diagram/Graph Quality', 'Time Management', 'Stepwise method'],
                default=['Conceptual Understanding', 'Stepwise method']
            )

        with col3:
            st.markdown("**💬 Feedback Settings**")

            tone_config = metadata.get('feedback_tone', {})
            feedback_tone = st.selectbox(
                "Feedback Tone",
                options=tone_config.get('options', ["Highly Encouraging", "Balanced", "Direct", "Critical"]),
                index=tone_config.get('options', ["Highly Encouraging", "Balanced", "Direct", "Critical"]).index(
                    tone_config.get('default', 'Balanced')
                )
            )

            explanation_config = metadata.get('explanation_level', {})
            explanation_level = st.selectbox(
                "Explanation Level",
                options=explanation_config.get('options', ["Simple", "Moderate", "Grade-appropriate", "Exam-Oriented"]),
                index=explanation_config.get('options',
                                             ["Simple", "Moderate", "Grade-appropriate", "Exam-Oriented"]).index(
                    explanation_config.get('default', 'Grade-appropriate')
                )
            )

        return {
            'class': class_num,
            'subject': subject,
            'board': board,
            'exam_type': exam_type,
            'strictness': strictness,
            'focus_areas': focus_areas,
            'answer_depth': answer_depth,
            'feedback_tone': feedback_tone,
            'explanation_level': explanation_level,
            'key_topics': metadata.get('key_topics', {}).get(subject, [])
        }

    return None


def render_upload_section():
    st.markdown("### 📤 Upload Examination Documents")

    col1, col2 = st.columns(2)

    files_data = {
        'syllabus': None,
        'question_paper': None,
        'answer_sheet': None,
        'answer_key': None
    }

    with col1:
        st.markdown("**📚 Syllabus (Optional)**")
        syllabus_file = st.file_uploader(
            "Upload syllabus to map topics accurately",
            type=['pdf', 'txt', 'png', 'jpg', 'jpeg'],
            key='syllabus'
        )
        if syllabus_file:
            files_data['syllabus'] = syllabus_file
            st.success(f"✓ {syllabus_file.name}")

        st.markdown("**📝 Question Paper**")
        question_file = st.file_uploader(
            "Upload question paper",
            type=['pdf', 'txt', 'png', 'jpg', 'jpeg'],
            key='questions'
        )
        if question_file:
            files_data['question_paper'] = question_file
            st.success(f"✓ {question_file.name}")

    with col2:
        st.markdown("**✍️ Student Answer Sheet**")
        answer_file = st.file_uploader(
            "Upload student's answer sheet",
            type=['pdf', 'txt', 'png', 'jpg', 'jpeg'],
            key='answers'
        )
        if answer_file:
            files_data['answer_sheet'] = answer_file
            st.success(f"✓ {answer_file.name}")

        st.markdown("**🔑 Answer Key (Optional)**")
        answer_key_file = st.file_uploader(
            "Upload answer key for accurate grading",
            type=['pdf', 'txt', 'png', 'jpg', 'jpeg'],
            key='answer_key'
        )
        if answer_key_file:
            files_data['answer_key'] = answer_key_file
            st.success(f"✓ {answer_key_file.name}")

    return files_data


def validate_inputs(metadata, files_data):
    errors = []

    if not metadata:
        errors.append("Please configure exam metadata")

    if not files_data['question_paper']:
        errors.append("Question paper is required")

    if not files_data['answer_sheet']:
        errors.append("Student answer sheet is required")

    return errors


def render_analysis_results(analysis, metadata):
    st.markdown("---")
    st.markdown("# 📊 Examination Analysis Report")

    personal_details = analysis.get('personal_details', {})

    if personal_details:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <h2 style='margin: 0; color: white;'>Student Performance Overview</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                {personal_details.get('student_name', 'Student')} • 
                Roll No: {personal_details.get('roll_number', 'N/A')} • 
                Class {personal_details.get('class', metadata['class'])} • 
                {personal_details.get('subject', metadata['subject'])}
            </p>
            <p style='margin: 0.3rem 0 0 0; opacity: 0.8; font-size: 0.9rem;'>
                {personal_details.get('exam_name', metadata['exam_type'])} • 
                {personal_details.get('date', 'Date not available')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <h2 style='margin: 0; color: white;'>Student Performance Overview</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Class {metadata['class']} • {metadata['subject']} • {metadata['exam_type']}</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    overall_score = analysis.get('overall_score', {})

    total_marks = overall_score.get('total_marks', 100)
    marks_obtained = overall_score.get('total_marks_obtained', 0)
    percentage = (marks_obtained / total_marks * 100) if total_marks > 0 else 0

    with col1:
        st.markdown(f"""
        <div style='background: #4CAF50; padding: 1.5rem; border-radius: 8px; text-align: center;'>
            <h3 style='margin: 0; color: white; font-size: 2.5rem;'>{percentage:.1f}%</h3>
            <p style='margin: 0.5rem 0 0 0; color: white; opacity: 0.9;'>Overall Score</p>
            <p style='margin: 0.3rem 0 0 0; color: white; opacity: 0.8; font-size: 0.9rem;'>{marks_obtained}/{total_marks} marks</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background: #2196F3; padding: 1.5rem; border-radius: 8px; text-align: center;'>
            <h3 style='margin: 0; color: white; font-size: 2.5rem;'>{overall_score.get('total_questions', 0)}</h3>
            <p style='margin: 0.5rem 0 0 0; color: white; opacity: 0.9;'>Total Questions</p>
            <p style='margin: 0.3rem 0 0 0; color: white; opacity: 0.8; font-size: 0.9rem;'>Attempted: {overall_score.get('attempted_questions', 0)}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background: #FF9800; padding: 1.5rem; border-radius: 8px; text-align: center;'>
            <h3 style='margin: 0; color: white; font-size: 2.5rem;'>{overall_score.get('correct_answers', 0)}</h3>
            <p style='margin: 0.5rem 0 0 0; color: white; opacity: 0.9;'>Correct Answers</p>
            <p style='margin: 0.3rem 0 0 0; color: white; opacity: 0.8; font-size: 0.9rem;'>Partial: {overall_score.get('partially_correct', 0)}</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        accuracy = overall_score.get('accuracy_percentage', 0)
        st.markdown(f"""
        <div style='background: #9C27B0; padding: 1.5rem; border-radius: 8px; text-align: center;'>
            <h3 style='margin: 0; color: white; font-size: 2.5rem;'>{accuracy:.0f}%</h3>
            <p style='margin: 0.5rem 0 0 0; color: white; opacity: 0.9;'>Accuracy</p>
            <p style='margin: 0.3rem 0 0 0; color: white; opacity: 0.8; font-size: 0.9rem;'>Incorrect: {overall_score.get('incorrect_answers', 0)}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 📚 Topic-Wise Performance Analysis")

    topic_analysis = analysis.get('topic_analysis', {})

    if topic_analysis:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Strong Topics")
            strong_topics = topic_analysis.get('strong_topics', [])
            if strong_topics:
                for topic in strong_topics:
                    st.markdown(f"""
                    <div style='background: #E8F5E9; padding: 1rem; border-left: 4px solid #4CAF50; margin-bottom: 0.5rem; border-radius: 4px;'>
                        <strong style='color: #2E7D32;'>{topic['name']}</strong><br>
                        <span style='color: #66BB6A;'>Score: {topic['score']}%</span><br>
                        <small style='color: #555;'>{topic['feedback']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No strong topics identified")

        with col2:
            st.markdown("### ⚠️ Areas for Improvement")
            weak_topics = topic_analysis.get('weak_topics', [])
            if weak_topics:
                for topic in weak_topics:
                    st.markdown(f"""
                    <div style='background: #FFF3E0; padding: 1rem; border-left: 4px solid #FF9800; margin-bottom: 0.5rem; border-radius: 4px;'>
                        <strong style='color: #E65100;'>{topic['name']}</strong><br>
                        <span style='color: #FB8C00;'>Score: {topic['score']}%</span><br>
                        <small style='color: #555;'>{topic['suggestion']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("All topics show good performance!")

        if topic_analysis.get('not_assessed'):
            with st.expander("📋 Topics Not Covered in This Exam"):
                st.info("These syllabus topics were not tested in this examination:")
                for topic in topic_analysis['not_assessed']:
                    st.write(f"• {topic}")

    st.markdown("---")
    st.markdown("## 📝 Question-Wise Detailed Breakdown")

    question_breakdown = analysis.get('question_wise_breakdown', {})

    highly_accurate = question_breakdown.get('highly_accurate_questions', [])
    if highly_accurate:
        for item in highly_accurate:
            question_nums = item.get('question_numbers', [])
            if question_nums:
                st.success(
                    f"✅ **Questions {', '.join(map(str, question_nums))}** ({item.get('topic', 'Topic')}): {item.get('summary', 'Perfectly answered')}")

    needs_improvement = question_breakdown.get('needs_improvement', [])
    if needs_improvement:
        st.markdown("### Questions Needing Attention")
        for q in needs_improvement:
            with st.expander(
                    f"❌ Question {q['question_number']}: {q.get('topic', 'Topic')} - {q['marks_obtained']}/{q['total_marks']} marks"):
                st.markdown(f"**Question:** {q.get('question_text', 'N/A')}")
                st.markdown(f"**Student's Answer:**")
                st.info(q.get('student_answer', 'N/A'))
                st.markdown(f"**Expected Answer:**")
                st.success(q.get('expected_answer', 'N/A'))

                if q.get('what_was_correct'):
                    st.markdown(f"✅ **What was correct:** {q['what_was_correct']}")

                if q.get('what_was_wrong'):
                    st.markdown(f"❌ **What was wrong:** {q['what_was_wrong']}")

                if q.get('issues'):
                    st.warning(f"**Issues identified:** {', '.join(q['issues'])}")

                st.markdown(f"**Feedback:** {q.get('feedback', 'N/A')}")

    st.markdown("---")
    st.markdown("## ❌ Error Analysis")

    error_analysis = analysis.get('error_analysis', {})
    if error_analysis:
        col1, col2, col3 = st.columns(3)

        conceptual_errors = error_analysis.get('conceptual_errors', [])
        calculation_mistakes = error_analysis.get('calculation_mistakes', [])
        incomplete_steps = error_analysis.get('incomplete_steps', [])
        poor_explanation = error_analysis.get('poor_explanation', [])
        notation_errors = error_analysis.get('notation_errors', [])
        time_management = error_analysis.get('time_management_issues', 0)

        conceptual_count = len(conceptual_errors) if isinstance(conceptual_errors, list) else conceptual_errors
        calculation_count = len(calculation_mistakes) if isinstance(calculation_mistakes,
                                                                    list) else calculation_mistakes
        incomplete_count = len(incomplete_steps) if isinstance(incomplete_steps, list) else incomplete_steps
        poor_exp_count = len(poor_explanation) if isinstance(poor_explanation, list) else poor_explanation
        notation_count = len(notation_errors) if isinstance(notation_errors, list) else notation_errors

        with col1:
            st.metric("Conceptual Errors", conceptual_count)
            st.metric("Calculation Mistakes", calculation_count)

        with col2:
            st.metric("Incomplete Steps", incomplete_count)
            st.metric("Poor Explanation", poor_exp_count)

        with col3:
            st.metric("Notation Errors", notation_count)
            st.metric("Time Management", time_management if isinstance(time_management, (int, float)) else 0)

        detailed_errors_found = False

        if isinstance(conceptual_errors, list) and conceptual_errors:
            detailed_errors_found = True
        if isinstance(calculation_mistakes, list) and calculation_mistakes:
            detailed_errors_found = True
        if isinstance(incomplete_steps, list) and incomplete_steps:
            detailed_errors_found = True
        if isinstance(poor_explanation, list) and poor_explanation:
            detailed_errors_found = True
        if isinstance(notation_errors, list) and notation_errors:
            detailed_errors_found = True

        if detailed_errors_found:
            with st.expander("📋 Detailed Error Breakdown"):
                if isinstance(conceptual_errors, list) and conceptual_errors:
                    st.markdown("### 🧠 Conceptual Errors")
                    for error in conceptual_errors:
                        st.markdown(f"""
                        <div style='background: #FFEBEE; padding: 1rem; border-left: 4px solid #F44336; margin-bottom: 0.5rem; border-radius: 4px;'>
                            <strong style='color: #C62828;'>Severity: {error.get('severity', 'Medium')}</strong><br>
                            <span style='color: #555;'><strong>Issue:</strong> {error.get('description', '')}</span><br>
                            <span style='color: #555;'><strong>Questions Affected:</strong> {', '.join(map(str, error.get('questions_affected', [])))}</span><br>
                            <span style='color: #555;'><strong>Example:</strong> {error.get('example', '')}</span><br>
                            <small style='color: #1976D2;'>💡 <strong>Remedy:</strong> {error.get('remedy', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)

                if isinstance(calculation_mistakes, list) and calculation_mistakes:
                    st.markdown("### 🔢 Calculation Mistakes")
                    for error in calculation_mistakes:
                        st.markdown(f"""
                        <div style='background: #FFF3E0; padding: 1rem; border-left: 4px solid #FF9800; margin-bottom: 0.5rem; border-radius: 4px;'>
                            <span style='color: #555;'><strong>Type:</strong> {error.get('description', '')}</span><br>
                            <span style='color: #555;'><strong>Questions Affected:</strong> {', '.join(map(str, error.get('questions_affected', [])))}</span><br>
                            <span style='color: #555;'><strong>Pattern:</strong> {error.get('pattern', '')}</span><br>
                            <small style='color: #1976D2;'>💡 <strong>Example:</strong> {error.get('example', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)

                if isinstance(incomplete_steps, list) and incomplete_steps:
                    st.markdown("### 📝 Incomplete Steps")
                    for error in incomplete_steps:
                        st.markdown(f"""
                        <div style='background: #E3F2FD; padding: 1rem; border-left: 4px solid #2196F3; margin-bottom: 0.5rem; border-radius: 4px;'>
                            <span style='color: #555;'><strong>Issue:</strong> {error.get('description', '')}</span><br>
                            <span style='color: #555;'><strong>Questions Affected:</strong> {', '.join(map(str, error.get('questions_affected', [])))}</span><br>
                            <span style='color: #555;'><strong>Missing Steps:</strong> {', '.join(error.get('missing_steps', []))}</span><br>
                            <small style='color: #1976D2;'>💡 <strong>Impact:</strong> {error.get('impact', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)

                if isinstance(poor_explanation, list) and poor_explanation:
                    st.markdown("### 💬 Poor Explanation")
                    for error in poor_explanation:
                        st.markdown(f"""
                        <div style='background: #F3E5F5; padding: 1rem; border-left: 4px solid #9C27B0; margin-bottom: 0.5rem; border-radius: 4px;'>
                            <span style='color: #555;'><strong>Issue:</strong> {error.get('description', '')}</span><br>
                            <span style='color: #555;'><strong>Questions Affected:</strong> {', '.join(map(str, error.get('questions_affected', [])))}</span><br>
                            <small style='color: #1976D2;'>💡 <strong>Suggestion:</strong> {error.get('suggestion', '')}</small><br>
                            <small style='color: #555;'><strong>Example:</strong> {error.get('example', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)

                if isinstance(notation_errors, list) and notation_errors:
                    st.markdown("### 🔤 Notation Errors")
                    for error in notation_errors:
                        st.markdown(f"""
                        <div style='background: #FCE4EC; padding: 1rem; border-left: 4px solid #E91E63; margin-bottom: 0.5rem; border-radius: 4px;'>
                            <span style='color: #555;'><strong>Issue:</strong> {error.get('description', '')}</span><br>
                            <span style='color: #555;'><strong>Questions Affected:</strong> {', '.join(map(str, error.get('questions_affected', [])))}</span><br>
                            <small style='color: #1976D2;'>💡 <strong>Correct Notation:</strong> {error.get('correct_notation', '')}</small><br>
                            <small style='color: #555;'><strong>Example:</strong> {error.get('example', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## ✅ Strengths Identified")
        strengths = analysis.get('strengths', [])
        for strength in strengths:
            st.markdown(f"""
            <div style='background: #E8F5E9; padding: 0.8rem; margin-bottom: 0.5rem; border-radius: 4px;'>
                <span style='color: #2E7D32;'>✓ {strength}</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("## 🎯 Improvement Recommendations")
        improvements = analysis.get('improvements', [])
        for improvement in improvements:
            st.markdown(f"""
            <div style='background: #FFF3E0; padding: 0.8rem; margin-bottom: 0.5rem; border-radius: 4px;'>
                <span style='color: #E65100;'>→ {improvement}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 💬 Personalized Feedback")

    personal_feedback = analysis.get('personal_feedback', {})

    if personal_feedback:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white;'>
            <h3 style='margin: 0 0 1rem 0; color: white;'>{personal_feedback.get('opening', 'Dear Student,')}</h3>
            <p style='margin: 0.5rem 0; line-height: 1.6;'><strong>Overall Impression:</strong> {personal_feedback.get('overall_impression', '')}</p>
            <p style='margin: 0.5rem 0; line-height: 1.6;'>{personal_feedback.get('detailed_analysis', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        if personal_feedback.get('key_takeaways'):
            st.markdown("### 🎯 Key Takeaways")
            for takeaway in personal_feedback['key_takeaways']:
                st.info(f"💡 {takeaway}")

        if personal_feedback.get('action_plan'):
            st.markdown("### 📋 Action Plan")
            for i, action in enumerate(personal_feedback['action_plan'], 1):
                st.success(f"**Step {i}:** {action}")

        if personal_feedback.get('motivation'):
            st.markdown(f"""
            <div style='background: #E8F5E9; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #4CAF50; margin-top: 1rem;'>
                <p style='margin: 0; color: #2E7D32; font-style: italic;'>"{personal_feedback['motivation']}"</p>
            </div>
            """, unsafe_allow_html=True)

        if personal_feedback.get('estimated_improvement_potential'):
            st.markdown(f"""
            <div style='background: #FFF3E0; padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
                <strong style='color: #E65100;'>📈 Improvement Potential:</strong><br>
                <span style='color: #555;'>{personal_feedback['estimated_improvement_potential']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        feedback = analysis.get('personalized_feedback', '')
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white;'>
            {feedback}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💬 Ask Questions About Your Performance", use_container_width=True, type="primary"):
            st.session_state.chat_mode = True
            st.rerun()


def render_chat_interface(analysis, metadata, client):
    st.markdown("---")
    st.markdown("# 💬 Performance Discussion Chat")

    if st.button("← Back to Results"):
        st.session_state.chat_mode = False
        st.rerun()

    st.markdown("Ask questions about your performance, feedback, or request study suggestions!")
    st.markdown("---")

    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.markdown(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message['content'])
    else:
        st.info(
            "👋 Hi! I'm your AI tutor. Ask me anything about your exam performance, specific mistakes, or how to improve!")

    st.markdown("---")
    st.markdown("**💡 Quick Questions:**")
    q_col1, q_col2, q_col3 = st.columns(3)

    quick_question = None
    if q_col1.button("📚 What should I study first?"):
        quick_question = "Based on my weak topics, what should I focus on first to improve?"
    if q_col2.button("🎯 How to avoid silly mistakes?"):
        quick_question = "I noticed some calculation errors. How can I improve my accuracy?"
    if q_col3.button("📈 Score improvement tips?"):
        quick_question = "What is a realistic score improvement I can achieve if I fix my errors?"

    user_question = st.chat_input("Type your question here...")

    if quick_question:
        user_question = quick_question

    if user_question:
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question
        })

        with st.spinner("🤔 Thinking..."):
            ai_response = chat_with_gemini(client, user_question, analysis, metadata)
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': ai_response
            })

        st.rerun()


def main():
    initialize_session_state()

    st.sidebar.title("🎓 AI Exam Review System")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")
    st.sidebar.info("Complete exam analysis with AI-powered insights")

    st.title("📝 AI-Powered Exam Analysis")

    try:
        client = get_gemini_client()
    except:
        st.error("Failed to initialize Gemini client. Please check GEMINI_API_KEY.")
        st.stop()

    if st.session_state.chat_mode and st.session_state.analysis_complete:
        render_chat_interface(st.session_state.analysis_results, st.session_state.metadata, client)
        return

    metadata = render_metadata_form()

    if metadata:
        st.session_state.metadata = metadata

    st.markdown("---")

    files_data = render_upload_section()

    st.markdown("---")

    errors = validate_inputs(metadata, files_data)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        analyze_button = st.button(
            "🚀 Analyze Exam Performance",
            type="primary",
            disabled=len(errors) > 0,
            use_container_width=True
        )

    if analyze_button:
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            analysis_results = analyze_exam_with_gemini(client, files_data, metadata)

            if analysis_results:
                st.session_state.analysis_results = analysis_results
                st.session_state.analysis_complete = True
                st.success("✅ Analysis Complete!")
                st.balloons()
            else:
                st.error("Analysis failed. Please try again.")

    if st.session_state.analysis_complete and st.session_state.analysis_results:
        render_analysis_results(st.session_state.analysis_results, st.session_state.metadata)


if __name__ == "__main__":
    main()