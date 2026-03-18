"""Fitness AI Coach - Main Application.

A Streamlit-based fitness coaching application that uses computer vision
to detect exercises, count repetitions, calculate BMR, and generate diet plans.

Features:
- BMR (Basal Metabolic Rate) Calculator
- Video Mode: Upload and analyze exercise videos
- WebCam Mode: Real-time exercise detection and rep counting
- Diet Plan Generator: Personalized nutrition plans using Gemini AI
"""

import streamlit as st
import cv2
import tempfile
import ExerciseAiTrainer as exercise
import os
import time
import mediapipe as mp
import logging
import warnings
from ExerciseAiTrainer import Exercise
from functools import lru_cache

# Suppress unnecessary warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEMO_VIDEO_PATH = 'demo.mp4'
FORM_VIDEO_PATHS = {
    'Bicep Curl': 'curl_form.mp4',
    'Push-Up': 'push_up_form.mp4',
    'Squat': 'squat_form.mp4',
    'Shoulder Press': 'shoulder_press_form.mp4'
}


def calculate_bmr(gender, age, weight, height):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.
    
    Args:
        gender (str): 'Male' or 'Female'
        age (int): Age in years
        weight (float): Weight in kg
        height (float): Height in cm
        
    Returns:
        float: BMR in calories/day
    """
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr


def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="Fitness AI Coach", layout="wide", initial_sidebar_state="expanded")
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main { padding-top: 0px; }
    .header-container { background: linear-gradient(to right, #FF6B6B, #4ECDC4); padding: 20px; border-radius: 10px; color: white; }
    .feature-card { background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #FF6B6B; }
    .success-message { background-color: #d4edda; padding: 10px; border-radius: 5px; }
    .warning-message { background-color: #fff3cd; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-container">
        <h1 style="margin: 0;">🏋️ Your Fitness AI Coach</h1>
        <p style="margin: 10px 0 0 0;">Powered by AI • Computer Vision • Personalized Plans</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("Welcome! Track exercises, get diet recommendations, and achieve your fitness goals! 💪")

    feature = st.sidebar.selectbox("Choose Feature", 
                                  ["BMR Calculator", "Video Mode", "WebCam Mode", "Diet Plan Generator"])

    if feature == "BMR Calculator":
        bmr_calculator()
    elif feature == "Video Mode":
        video_mode()
    elif feature == "WebCam Mode":
        webcam_mode()
    elif feature == "Diet Plan Generator":
        diet_plan_generator()
    
    # Display feature information in sidebar
    st.sidebar.divider()
    st.sidebar.markdown("### 📚 Features Guide")
    st.sidebar.markdown("""
    **🧮 BMR Calculator**
    - Calculate your basal metabolic rate
    - Get daily calorie recommendations
    
    **📹 Video Mode**
    - Upload exercise videos
    - AI analyzes your form
    - Get rep count
    
    **🎥 WebCam Mode**
    - Real-time exercise detection
    - Live rep counting
    - Instant feedback
    
    **🥗 Diet Plan**
    - AI-powered meal plans
    - Personalized nutrition
    - Shopping lists
    """)


def bmr_calculator():
    """BMR calculator feature with TDEE calculation."""
    st.subheader("📊 BMR (Basal Metabolic Rate) Calculator")
    st.write("Calculate your BMR and Total Daily Energy Expenditure (TDEE)")
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio("Select Gender", ['Male', 'Female'])
        age = st.number_input("Enter Age", min_value=10, max_value=100, value=25, step=1)
    with col2:
        weight = st.number_input("Enter Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
        height = st.number_input("Enter Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.5)

    activity_level = st.select_slider("Select Activity Level", 
                                     options=['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extremely Active'],
                                     value='Moderately Active')
    
    # Map activity levels to multipliers
    activity_multipliers = {
        'Sedentary': 1.2,
        'Lightly Active': 1.375,
        'Moderately Active': 1.55,
        'Very Active': 1.725,
        'Extremely Active': 1.9
    }

    if st.button("📈 Calculate", use_container_width=True):
        try:
            bmr = calculate_bmr(gender, age, weight, height)
            tdee = bmr * activity_multipliers[activity_level]
            
            # Create columns for metrics display
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric(label="BMR (cal/day)", value=f"{bmr:.0f}")
            with metric_col2:
                st.metric(label="TDEE (cal/day)", value=f"{tdee:.0f}")
            with metric_col3:
                st.metric(label="Weight Loss (cal/day)", value=f"{tdee * 0.85:.0f}")
            
            st.divider()
            st.success("✅ BMR calculation complete!")
            
            # Provide recommendations
            st.subheader("💡 Calorie Recommendations")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Weight Loss:** {tdee * 0.85:.0f} cal/day (-15%)")
            with col2:
                st.info(f"**Maintenance:** {tdee:.0f} cal/day")
            with col3:
                st.info(f"**Muscle Gain:** {tdee * 1.1:.0f} cal/day (+10%)")
            
            st.markdown("""
            **💪 Fitness Tips:**
            - Combine calorie tracking with regular exercise
            - Aim for 0.5-1 kg weight loss per week for healthy results
            - For muscle gain, prioritize protein intake (1.6-2.2g per kg of body weight)
            """)
        except Exception as e:
            st.error(f"❌ Error calculating BMR: {str(e)}")
            logger.error(f"BMR calculation error: {e}")


def video_mode():
    """Video upload and analysis feature."""
    st.subheader('📹 Upload Your Exercise Video')
    st.write("Upload a video of your exercise, and our AI will analyze your form and count your reps!")
    
    # Create two columns for file upload and exercise selection
    col1, col2 = st.columns([2, 1])
    with col1:
        video_file = st.file_uploader("📤 Upload a video", type=["mp4", "mov", "avi", "m4v"], 
                                     help="Supported formats: MP4, MOV, AVI, M4V (Max 500MB)")
    with col2:
        st.write("")
        st.write("")
        use_demo = st.button("Use Demo Video", use_container_width=True)
    
    if video_file is not None:
        try:
            # Check file size
            file_size = len(video_file.getvalue())
            if file_size > 500 * 1024 * 1024:  # 500MB limit
                st.error("❌ File size exceeds 500MB limit. Please upload a smaller video.")
                return
                
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                temp_file.write(video_file.read())
                temp_path = temp_file.name
            st.success("✅ Video uploaded successfully!")
        except Exception as e:
            st.error(f"❌ Error uploading video: {str(e)}")
            logger.error(f"Video upload error: {e}")
            return
    elif use_demo:
        if os.path.exists(DEMO_VIDEO_PATH):
            temp_path = DEMO_VIDEO_PATH
            st.info("📌 Using demo video")
        else:
            st.warning("⚠️ Demo video not found")
            st.info("Please upload a video file to proceed.")
            return
    else:
        # Default: Try to use demo video if available
        if os.path.exists(DEMO_VIDEO_PATH):
            temp_path = DEMO_VIDEO_PATH
            st.info("📌 No video selected. Using demo video.")
        else:
            st.warning("⚠️ No video provided")
            st.info("Please upload a video file to proceed.")
            return
    
    try:
        # Verify video file is readable
        cap = cv2.VideoCapture(temp_path)
        if not cap.isOpened():
            st.error("❌ Cannot open video file. Ensure it's a valid video format.")
            return
        
        # Get basic video info
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if total_frames == 0 or fps == 0:
            st.error("❌ Invalid video file. Please ensure the video is not corrupted.")
            cap.release()
            return

        # Display input video
        st.markdown("### 📥 Input Video Preview")
        st.video(temp_path)
        st.info(f"Video Info: {total_frames} frames @ {fps:.1f} FPS")

        # Select exercise with descriptions
        exercise_descriptions = {
            "Push-Up": "Arm and chest exercise",
            "Squat": "Leg and glute exercise",  
            "Bicep Curl": "Arm flexing exercise",
            "Shoulder Press": "Shoulder and arm exercise"
        }
        
        exercise_type = st.selectbox("🏋️ Select Exercise Type", 
                                    list(exercise_descriptions.keys()),
                                    format_func=lambda x: f"{x} - {exercise_descriptions[x]}")

        if st.button("🎬 Analyze Video", use_container_width=True):
            with st.spinner(f"⏳ Analyzing {exercise_type} in your video..."):
                try:
                    # Reset video capture for processing
                    cap = cv2.VideoCapture(temp_path)
                    
                    trainer = Exercise()
                    output_path = None
                    
                    # Call appropriate exercise method
                    if exercise_type == "Push-Up":
                        output_path = trainer.push_up(cap, mode='video')
                    elif exercise_type == "Squat":
                        output_path = trainer.squat(cap, mode='video')
                    elif exercise_type == "Bicep Curl":
                        output_path = trainer.bicep_curl(cap, mode='video')
                    elif exercise_type == "Shoulder Press":
                        output_path = trainer.shoulder_press(cap, mode='video')
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    
                    # Check if output was generated
                    if output_path and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        st.divider()
                        st.markdown("### ✅ Processed Output")
                        st.video(output_path)
                        st.success("🎉 Video analyzed successfully!")
                        
                        # Display file info
                        output_size = os.path.getsize(output_path) / (1024 * 1024)
                        st.info(f"Output video: {output_size:.2f} MB")
                        
                        # Display tips
                        with st.expander("📖 Exercise Tips for " + exercise_type):
                            tips = {
                                "Push-Up": "Keep your body in a straight line. Lower until chest almost touches ground. Full arm extension at top.",
                                "Squat": "Keep your chest up. Knees should track over toes. Go as low as comfortable.",
                                "Bicep Curl": "Keep elbows stationary at your sides. Only move forearms. Control the descent.",
                                "Shoulder Press": "Press directly overhead. Engage your core. Avoid arching your lower back."
                            }
                            st.write(tips.get(exercise_type, "Follow proper form for best results."))
                    else:
                        st.warning("⚠️ Video processing completed but output file is empty or not found.")
                        st.info("This might happen if no clear exercise movement was detected. Try:")
                        st.markdown("""
                        - Ensuring the video has clear lighting
                        - Making sure you're fully visible in the frame
                        - Using a higher resolution video
                        - Ensuring the exercise is performed clearly
                        """)
                except Exception as e:
                    st.error(f"❌ Error processing video: {str(e)}")
                    logger.error(f"Video processing error: {e}")
                    st.info("Try uploading a clearer video with better lighting.")
                finally:
                    cap.release()
                    cv2.destroyAllWindows()
    except Exception as e:
        st.error(f"❌ Error in video mode: {str(e)}")
        logger.error(f"Video mode error: {e}")


def webcam_mode():
    """Live webcam exercise detection feature."""
    st.subheader('📹 Live Webcam Exercise Detection')

    # Sidebar: Select Exercise and Set Goals
    st.sidebar.subheader("🎯 Set Your Exercise Goal")
    selected_exercise = st.sidebar.selectbox("Choose Exercise", 
                                            ["Push-Up", "Squat", "Bicep Curl", "Shoulder Press"])
    target_reps = st.sidebar.number_input("Target Reps", min_value=1, max_value=100, value=10)

    # Show correct form preview
    st.markdown("### 📖 Correct Form Preview")
    if selected_exercise in FORM_VIDEO_PATHS:
        form_video = FORM_VIDEO_PATHS[selected_exercise]
        if os.path.exists(form_video):
            st.video(form_video)
        else:
            st.info(f"Form video for {selected_exercise} not available")

    # Initialize session state
    if 'current_rep' not in st.session_state:
        st.session_state.current_rep = 0
    if 'goal_reached' not in st.session_state:
        st.session_state.goal_reached = False
    if 'webcam_running' not in st.session_state:
        st.session_state.webcam_running = False

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Cannot open webcam. Please check your camera permissions.")
            return

        stframe = st.empty()
        status_placeholder = st.empty()
        trainer = Exercise()
        detector = exercise.pm.posture_detector()
        counter = 0
        stage = None

        # Start button
        col1, col2 = st.columns(2)
        with col1:
            start_button = st.button("Start Exercise")
        with col2:
            stop_button = st.button("Stop Exercise")

        if start_button:
            st.session_state.webcam_running = True
            st.session_state.current_rep = 0
            st.session_state.goal_reached = False

        while st.session_state.webcam_running:
            if stop_button or st.session_state.goal_reached:
                st.session_state.webcam_running = False
                break

            ret, frame = cap.read()
            if not ret:
                st.error("Failed to read from webcam")
                break

            # Flip for mirror view
            frame = cv2.flip(frame, 1)

            # Run pose detection
            img = detector.find_person(frame)
            landmark_list = detector.find_landmarks(img, False)

            # Only process if landmarks detected
            if landmark_list is not None and len(landmark_list) != 0:
                # Exercise-specific angle detection
                if selected_exercise == "Push-Up":
                    right_shoulder = landmark_list[12][1:]
                    right_wrist = landmark_list[16][1:]
                    distance = exercise.distanceCalculate(right_shoulder, right_wrist)
                    if distance < 130:
                        stage = "down"
                    if distance > 250 and stage == "down":
                        stage = "up"
                        st.session_state.current_rep += 1
                        counter = st.session_state.current_rep

                elif selected_exercise == "Squat":
                    right_leg_angle = detector.find_angle(img, 24, 26, 28)
                    left_leg_angle = detector.find_angle(img, 23, 25, 27)
                    if right_leg_angle > 140 and left_leg_angle < 240:
                        stage = "down"
                    if right_leg_angle < 80 and left_leg_angle > 270 and stage == 'down':
                        stage = "up"
                        st.session_state.current_rep += 1
                        counter = st.session_state.current_rep

                elif selected_exercise == "Bicep Curl":
                    left_arm_angle = detector.find_angle(img, 11, 13, 15)
                    if left_arm_angle < 230:
                        stage = "down"
                    if left_arm_angle > 310 and stage == 'down':
                        stage = "up"
                        st.session_state.current_rep += 1
                        counter = st.session_state.current_rep

                elif selected_exercise == "Shoulder Press":
                    right_arm_angle = detector.find_angle(img, 12, 14, 16)
                    left_arm_angle = detector.find_angle(img, 11, 13, 15)
                    if right_arm_angle > 315 and left_arm_angle < 40:
                        stage = "down"
                    if right_arm_angle < 240 and left_arm_angle > 130 and stage == 'down':
                        stage = "up"
                        st.session_state.current_rep += 1
                        counter = st.session_state.current_rep

            # Display rep counter on image
            cv2.rectangle(img, (0, 0), (225, 73), (245, 117, 16), -1)
            cv2.putText(img, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Display frame
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            stframe.image(img_rgb, channels='RGB', use_column_width=True)

            # Display progress
            status_placeholder.markdown(f"""
            ### 🏋️ Exercise Progress:
            - **Exercise:** {selected_exercise}  
            - **Reps Completed:** {st.session_state.current_rep}/{target_reps}  
            - **Status:** {'✅ Goal Reached!' if st.session_state.current_rep >= target_reps else '🔄 In Progress'}
            """)

            # Check if workout goal is complete
            if st.session_state.current_rep >= target_reps:
                st.session_state.goal_reached = True
                st.balloons()
                st.success("🎯 Target reps reached! Great job!")
                st.warning("Click 'Stop Exercise' to finish")
                break

            time.sleep(0.1)  # Small delay to prevent excessive processing

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        st.error(f"Error in webcam mode: {str(e)}")
        logger.error(f"Webcam mode error: {e}")


def diet_plan_generator():
    """Personalized diet plan generator feature with AI-powered recommendations."""
    st.subheader("🥗 Personalized Diet Plan Generator")
    st.write("Get an AI-powered personalized diet plan based on your body metrics and preferences!")

    if genai is None:
        st.error("❌ Google Generative AI not installed. Please install: pip install google-generativeai")
        return

    # Configure Gemini API using Streamlit Secrets
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("❌ GEMINI_API_KEY not found in secrets. Please add it to .streamlit/secrets.toml")
            return
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"❌ API configuration error: {str(e)}")
        logger.error(f"API error: {e}")
        return

    # Collect user inputs
    col1, col2 = st.columns(2)
    with col1:
        st.write("**👤 Personal Information**")
        gender = st.selectbox("Gender", ["Male", "Female"], key="diet_gender")
        age = st.slider("Age", 10, 100, 25, key="diet_age")
        weight = st.slider("Weight (kg)", 30, 200, 70, key="diet_weight")
    with col2:
        st.write("**🎯 Fitness Goals**")
        height = st.slider("Height (cm)", 100, 250, 170, key="diet_height")
        activity = st.selectbox("Activity Level", 
                               ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"], 
                               key="diet_activity")
        goal = st.selectbox("Fitness Goal", 
                           ["Weight Loss", "Muscle Gain", "Maintenance", "Athletic Performance"],
                           key="diet_goal")

    st.divider()
    st.write("**🍽️ Diet Preferences**")
    
    col1, col2 = st.columns(2)
    with col1:
        diet_type = st.selectbox("Diet Type", 
                                ["Vegetarian", "Vegan", "Non-Vegetarian", "Keto", "High-Protein", "Mediterranean"],
                                key="diet_type")
    with col2:
        restrictions = st.multiselect("Dietary Restrictions", 
                                     ["None", "Gluten-Free", "Dairy-Free", "Nut-Free", "Sugar-Free"],
                                     default=["None"],
                                     key="diet_restrictions")

    if st.button("✨ Generate Personalized Diet Plan", use_container_width=True):
        try:
            with st.spinner("🔄 Generating your personalized diet plan using AI..."):
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Calculate BMR for context
                bmr = calculate_bmr(gender, age, weight, height)
                activity_multipliers = {
                    'Sedentary': 1.2,
                    'Lightly Active': 1.375,
                    'Moderately Active': 1.55,
                    'Very Active': 1.725,
                }
                tdee = bmr * activity_multipliers.get(activity, 1.55)
                
                restrictions_str = ", ".join([r for r in restrictions if r != "None"])
                restrictions_text = f"Dietary restrictions: {restrictions_str}" if restrictions_str else "No specific restrictions"
                
                prompt = f"""Create a {diet_type} diet plan for {age}yr old {gender}.
Weight: {weight}kg, Height: {height}cm, Activity: {activity}, Goal: {goal}, {restrictions_text}, Calories: {tdee:.0f}/day.

Provide:
1. 7-day meal plan (breakfast, lunch, dinner, snacks)
2. Calories/macros per meal
3. Shopping list
4. 5 meal prep tips
5. Water intake
6. Supplement suggestions

Keep it practical and concise."""
                
                response = model.generate_content(prompt)
                
                st.divider()
                st.success("✅ Your personalized diet plan is ready!")
                st.markdown(response.text)
                
                # Add summary metrics
                st.divider()
                st.subheader("📊 Your Plan Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(label="Daily Calories (cal)", value=f"{tdee:.0f}")
                with col2:
                    st.metric(label="BMR (cal)", value=f"{bmr:.0f}")
                with col3:
                    st.metric(label="Goal", value=goal)
                with col4:
                    st.metric(label="Diet", value=diet_type)
                    
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower():
                st.error("""❌ API Quota Exceeded
                
Your free tier API limit has been reached. Options:
1. **Wait and Retry**: Free tier resets daily (24 hours)
2. **Upgrade Account**: Add billing to your Google Cloud account for higher limits
3. **Use a New API Key**: Create a new project with a fresh key

To upgrade: Visit https://ai.google.dev/pricing""")
            elif "404" in error_str or "not found" in error_str.lower():
                st.error("""❌ Model Not Available

This model is not available with your current API configuration. Please:
1. Check your API key is active
2. Ensure you're using the correct model name
3. Try again in a few moments

If the issue persists, create a new API key at https://ai.google.dev""")
            else:
                st.error(f"❌ Failed to generate diet plan: {error_str}")
            logger.error(f"Diet plan generation error: {e}")
            
    # Add helpful information
    with st.expander("ℹ️ How to use this tool"):
        st.write("""
        1. **Fill in your information:** Provide accurate personal metrics for better recommendations
        2. **Select your goal:** Choose what you want to achieve (weight loss, muscle gain, etc.)
        3. **Set preferences:** Include your diet type and any restrictions
        4. **Generate plan:** Click the button to get an AI-powered customized plan
        5. **Follow the plan:** Stick to the recommendations for best results
        6. **Adjust as needed:** You can regenerate different plans to explore options
        
        **Note:** This tool provides AI-generated recommendations. Consult a registered dietitian or healthcare provider 
        for personalized medical advice.
        """)


if __name__ == '__main__':
    main()
