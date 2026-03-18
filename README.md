# 🏋️ Fitness AI Coach

A comprehensive Streamlit-based fitness coaching application powered by AI and computer vision. Track your exercises, get personalized diet plans, and achieve your fitness goals!

## ✨ Features

### 📊 BMR Calculator
- Calculate your Basal Metabolic Rate (BMR)
- Get Total Daily Energy Expenditure (TDEE) estimates
- Personalized calorie recommendations for your fitness goal
- Activity level-based calorie calculations

### 📹 Video Mode
- Upload exercise videos (MP4, MOV, AVI, M4V)
- AI-powered form analysis
- Automatic rep counting
- Support for multiple exercises:
  - Push-Ups
  - Squats
  - Bicep Curls
  - Shoulder Press

### 🎥 WebCam Mode
- Real-time exercise detection using your webcam
- Live rep counting
- Instant form feedback
- Set and track rep goals
- Celebration animations when targets reached

### 🥗 Diet Plan Generator
- AI-powered personalized meal plans
- Support for multiple diet types:
  - Vegetarian
  - Vegan
  - Non-Vegetarian
  - Keto
  - High-Protein
  - Mediterranean
- Dietary restriction options
- 7-day meal plans with:
  - Breakfast, lunch, dinner, and snacks
  - Calorie and macro information
  - Shopping lists
  - Meal prep tips

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Webcam (for webcam mode)
- Google Gemini API key (for diet plan generator)

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/fitness-coach-app.git
cd fitness-coach-app
```

2. Install dependencies
```bash
pip install -r requirement.txt
```

3. Set up your Google Gemini API key
   - Get your API key from [Google AI Studio](https://ai.google.dev)
   - Create `.streamlit/secrets.toml` with:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

4. Run the app
```bash
streamlit run main.py
```

### Access the App
Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies

- **streamlit** - Web app framework
- **opencv-python-headless** - Computer vision
- **mediapipe** - Pose detection
- **numpy** - Numerical computing
- **pandas** - Data manipulation
- **matplotlib** - Data visualization
- **google-generativeai** - AI diet plan generation

## 🎯 How to Use

### BMR Calculator
1. Select your gender, age, weight, and height
2. Choose your activity level
3. Click "Calculate" to see your BMR and TDEE
4. View personalized calorie recommendations

### Video Mode
1. Upload a video of your exercise (or use demo)
2. Select the exercise type
3. Click "Analyze Video"
4. View the processed video with rep count and form analysis

### WebCam Mode
1. Select your exercise and target reps
2. Click "Start Exercise"
3. Perform the exercise in front of your camera
4. See real-time rep counting
5. Celebrate when you reach your goal!

### Diet Plan Generator
1. Enter your personal information
2. Select your fitness goal
3. Choose your diet type and restrictions
4. Click "Generate Personalized Diet Plan"
5. View your AI-generated meal plan with shopping list

## 📋 File Structure

```
fitness-coach-app/
├── main.py                    # Main Streamlit application
├── ExerciseAiTrainer.py      # Exercise detection module
├── PoseModule2.py            # Pose detection utilities
├── AiTrainer_utils.py        # Helper utilities
├── requirement.txt           # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml         # API keys (not in repo)
└── README.md                # This file
```

## 🔧 Configuration

### Streamlit Config (`.streamlit/config.toml`)
- Custom theme colors
- Performance optimizations
- Error handling settings

### Secrets (`.streamlit/secrets.toml`)
- Google Gemini API key
- Keep this file private and out of version control

## 🌐 Deployment

### Deploy to Streamlit Community Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to `main.py`
6. Add your `GEMINI_API_KEY` in the "Advanced settings" → "Secrets"

### Other Deployment Options
- **Railway**: Easy deployment with automatic updates
- **Heroku**: Traditional Python app hosting
- **AWS**: Scalable cloud deployment

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests

## 📝 License

This project is released under the MIT License.

## 🙏 Acknowledgments

- MediaPipe for pose detection
- Google Gemini for AI-powered diet planning
- Streamlit for the amazing web framework

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## ⚠️ Disclaimer

This app provides fitness and health recommendations powered by AI. Always consult with healthcare professionals before making significant changes to your diet or exercise routine. This tool is meant to supplement, not replace, professional medical advice.

---

**Made with ❤️ for fitness enthusiasts everywhere!**
