import streamlit as st
import requests

# Title for the app
st.title("Personalized Health Tracker")

# Tabs for navigation
tab1, tab2 = st.tabs(["Quick BMI Check", "User Profiles"])

# Update service URLs to point to the Kubernetes services
USER_SERVICE_URL = "http://user-service:5001"
BMI_SERVICE_URL = "http://bmi-service:5002/calculate_bmi"
EXERCISE_SERVICE_URL = "http://exercise-service:5003/recommend_exercises"

#BMI_SERVICE_URL = f"http://localhost:5002/calculate_bmi"
#USER_SERVICE_URL = f"http://localhost:5001/"
#EXERCISE_SERVICE_URL = f"http://10.99.211.41:31286/recommend_exercises"

# Tab 1: Quick BMI Check
with tab1:
    st.header("Quick BMI Check")
    weight = st.number_input("Enter your weight (in kg):", min_value=0.1, step=0.1, key="quick_weight")
    height = st.number_input("Enter your height (in m):", min_value=0.1, step=0.1, key="quick_height")

    if st.button("Check BMI", key="quick_bmi"):
        if weight > 0 and height > 0:
            try:
                # Calculate BMI
                #bmi_response = requests.post("http://bmi-service:5002/calculate_bmi", json={
                bmi_response = requests.post(BMI_SERVICE_URL, json={
                    "weight": weight,
                    "height": height
                })

                if bmi_response.status_code == 200:
                    bmi_data = bmi_response.json()
                    bmi = bmi_data.get("bmi")
                    advice = bmi_data.get("advice")

                    st.success(f"Your BMI is {bmi:.2f} ({advice})")

                    # Fetch Exercise Recommendations
                    #exercise_response = requests.post("http://exercise-service:5003/recommend_exercises", json={"bmi": bmi})
                    exercise_response = requests.post(EXERCISE_SERVICE_URL, json={"bmi": bmi})
                    if exercise_response.status_code == 200:
                        exercise_data = exercise_response.json()
                        st.write("Exercise Recommendations:")
                        for key, value in exercise_data.items():
                            st.write(f"{key.replace('_', ' ').title()}: {value}")
                    else:
                        st.error("Failed to fetch exercise recommendations.")
                else:
                    st.error("Failed to calculate BMI.")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter valid weight and height!")

# Tab 2: User Profiles
with tab2:
    st.header("Create and View Profiles")

    # Create Profile Section
    st.subheader("Create Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1, format="%d")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="profile_gender")
    weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1, key="profile_weight")
    height = st.number_input("Height (m)", min_value=0.1, step=0.1, key="profile_height")

    if st.button("Save Profile"):
        if name and age > 0 and weight > 0 and height > 0:
            try:
                # Save the user profile
                response = requests.post(USER_SERVICE_URL + "/add_user", json={
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "weight": weight,
                    "height": height
                })

                if response.status_code == 201:
                    result = response.json()
                    st.success("Profile saved successfully!")
                    st.write(f"Calculated BMI: {result['bmi']}")
                    st.write("Exercise Recommendations:")
                    for key, value in result['exercise_recommendations'].items():
                        st.write(f"{key.replace('_', ' ').title()}: {value}")
                else:
                    st.error(f"Error: {response.json().get('error')}")
            except Exception as e:
                st.error(f"Could not connect to the User Profile service: {e}")
        else:
            st.warning("Please fill in all fields!")

    # View Profiles Section
    st.subheader("View Profiles")
    try:
        response = requests.get(USER_SERVICE_URL + "/get_users")
        if response.status_code == 200:
            profiles = response.json()
            for profile in profiles:
                st.write("---")
                st.subheader(profile["name"])
                st.write(f"Age: {profile['age']}")
                st.write(f"Gender: {profile['gender']}")
                st.write(f"Weight: {profile['weight']} kg")
                st.write(f"Height: {profile['height']} m")
                st.write(f"BMI: {profile['bmi']}")
                st.write("Exercise Recommendations:")
                for key, value in profile["exercise_recommendations"].items():
                    st.write(f"{key.replace('_', ' ').title()}: {value}")
                
                # Delete Profile Button
                if st.button(f"Delete Profile: {profile['name']}"):
                    try:
                        delete_response = requests.delete(USER_SERVICE_URL + "/delete_user", json={"name": profile["name"]})
                        if delete_response.status_code == 200:
                            st.success(f"Profile {profile['name']} deleted successfully.")
                        else:
                            st.error(f"Error: {delete_response.json().get('error')}")
                    except Exception as e:
                        st.error(f"Failed to delete profile: {e}")
        else:
            st.error("Failed to fetch user profiles.")
    except Exception as e:
        st.error(f"Error: {e}")
