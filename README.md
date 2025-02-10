**Personalized Health Recommendation System**

The Personalized Health Recommendation System is a Flask-based web application that provides AI-driven, tailored health insights based on user data. By analyzing inputs such as age, gender, height, weight, sleep habits, physical activity, and lifestyle choices, the system delivers actionable health recommendations for sleep, diet, exercise, weight management, and risk prediction.

**Features**
*Personalized Health Questionnaire: Collects detailed health information from users.
*AI-Powered Recommendations: Provides customized advice on sleep, diet, exercise, and lifestyle improvements.
*Risk Prediction: Identifies potential health risks based on user data.
*Interactive Dashboard: Displays personalized health insights in an easy-to-understand format.
*Responsive Design: User-friendly interface with mobile support.

**Technologies Used**
Backend: Flask, Python
Frontend: HTML, CSS (Bootstrap), JavaScript
AI Integration: Mistral API for generating personalized recommendations
(No Database for now)

**Project Structure**
/static           - Contains CSS, JavaScript, and images  
/templates        - HTML templates for the web pages  
app.py            - Main Flask application file  
main.js           - Handles form validation and AJAX requests  
style.css         - Custom CSS for styling  
questionnaire.html - Health questionnaire form  
dashboard.html    - Dashboard displaying health recommendations  

**How to Run the Project**
1.Clone the repository:

>git clone <repository-url>

run the above command in bash

2.Navigate to the project directory and install the required packages

>pip install -r requirements.txt

run the above command

3.Set up your Mistral API key in app.py:
Replace mistral_api_key with your actual API key.

4.Run the Flask application:

>python app.py

run the above command in the terminal

5.Access the web application:
Open your browser and navigate to http://127.0.0.1:5000/

**Future Enhancements**
1.Profile creation and account maintainance
2.Integration with database with regular monitoring and tracking of user's health.
3.Expanding coverage to include mental health blogs , AI health chat bot and chronic disease management.






