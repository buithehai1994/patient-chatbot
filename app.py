import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch Gemini API key from environment variables
api_key= os.getenv("gemini_api")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# App Title
st.title("🌟 Gemini Medical Assistant")
st.markdown(
    """
    Welcome to **Gemini**, your AI-powered healthcare companion. 
    Input patient details and select a topic to generate personalized advice!
    """
)

# Sidebar for Prompt Selection
st.sidebar.header("Select a Topic")
prompts = [
    "General health advice",
    "Treatment options for hypertension",
    "Lifestyle recommendations for obesity",
    "Guidelines for chronic diabetes management",
    "Drug interaction concerns",
    "Recommended diagnostic tests",
    "Interpreting test results",
    "Action plan for next follow-up visit",
]
selected_prompt = st.sidebar.selectbox("Choose a topic:", prompts)

# Display Selected Topic in Main Section
st.header("📌 Selected Topic")
st.markdown(f"**You have chosen:** {selected_prompt}")

# Section: Search and Select Patient
st.header("🩺 Select a Predefined Patient")

# Predefined patient records
patients = {
    "John Doe": {
        "age": 45, "weight": 70.0, "height": 170.0, "blood_pressure": "130/85", "glucose_level": 110.0,
        "medications": "Lisinopril, Metformin", "smoking_status": "Non-Smoker", "family_history": "Hypertension, Heart Disease"
    },
    "Peter Parker": {
        "age": 32, "weight": 75.0, "height": 175.0, "blood_pressure": "125/80", "glucose_level": 90.0,
        "medications": "None", "smoking_status": "Former Smoker", "family_history": "Diabetes, High Cholesterol"
    },
    "Jane Smith": {
        "age": 28, "weight": 60.0, "height": 160.0, "blood_pressure": "110/70", "glucose_level": 95.0,
        "medications": "None", "smoking_status": "Non-Smoker", "family_history": "None"
    }
}

# Searchable patient list using a text input
search_query = st.text_input("Search Patient by Name:", "")
filtered_patients = {name: data for name, data in patients.items() if search_query.lower() in name.lower()}

# If no patients match the search, inform the user
if len(filtered_patients) == 0:
    st.warning("No patients found with the search term. Please try again.")

# If there are filtered patients, display them in a selectbox
if len(filtered_patients) > 0:
    selected_patient = st.selectbox("Select a patient:", list(filtered_patients.keys()))

    # Fill the patient form based on the selection
    patient_data = filtered_patients[selected_patient]

    # Patient Input Form
    with st.form("patient_details"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name (or part of it):", value=selected_patient)
            age = st.number_input("Age", min_value=0, max_value=120, value=patient_data["age"])
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=200.0, value=patient_data["weight"])
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)", value=patient_data["blood_pressure"])
            smoking_status = st.selectbox("Smoking Status", ["Non-Smoker", "Former Smoker", "Current Smoker"], index=["Non-Smoker", "Former Smoker", "Current Smoker"].index(patient_data["smoking_status"]))
        
        with col2:
            height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=patient_data["height"])
            glucose_level = st.number_input("Fasting Glucose Level (mg/dL)", min_value=0.0, max_value=500.0, value=patient_data["glucose_level"])
            medications = st.text_area("Current Medications", value=patient_data["medications"])
            family_history = st.text_area("Family History (e.g., Hypertension, Diabetes)", value=patient_data["family_history"])
        
        submit = st.form_submit_button("Generate Advice")

    # Patient Summary Section
    if submit:
        # Calculate BMI
        bmi = round(weight / ((height / 100) ** 2), 2)
        
        # Display Patient Summary
        st.header("📋 Patient Summary")
        st.markdown(
            f"""
            **Name:** {patient_name}  
            **Age:** {age}  
            **Weight:** {weight} kg  
            **Height:** {height} cm  
            **BMI:** {bmi}  
            **Blood Pressure:** {blood_pressure}  
            **Fasting Glucose Level:** {glucose_level} mg/dL  
            **Current Medications:** {medications}  
            **Smoking Status:** {smoking_status}  
            **Family History:** {family_history}  
            **Selected Topic:** {selected_prompt}  
            """
        )

        # Prepare Patient Context for AI
        patient_context = f"""
        Patient Name: {patient_name}
        Age: {age}
        Weight: {weight} kg
        Height: {height} cm
        BMI: {bmi}
        Blood Pressure: {blood_pressure}
        Fasting Glucose Level: {glucose_level} mg/dL
        Current Medications: {medications}
        Smoking Status: {smoking_status}
        Family History: {family_history}
        """
        
        # Construct Prompt
        prompt = f"""
        Based on the following patient details and the selected topic, provide detailed, personalized medical advice.

        Patient Details:
        {patient_context}

        Selected Topic: {selected_prompt}

        Provide a comprehensive, user-friendly response.
        """
        
        # Call Gemini API
        try:
            with st.spinner("Generating advice..."):
                response = model.generate_content(prompt)
            
            # Display Gemini's Advice
            st.header("💡 Gemini's Medical Advice")
            st.markdown("Here is the personalized advice based on the patient's details:")
            st.markdown(f"**Topic:** {selected_prompt}")
            st.info(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer Section
st.markdown(
    """
    --- 
    🛠 Powered by **Gemini AI** | Built with ❤️ using Streamlit
    """
)
