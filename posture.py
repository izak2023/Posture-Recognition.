import cv2
import time
import math as m
import mediapipe as mp
import streamlit as st
import streamlit_authenticator as stauth
import os
from PIL import Image
import requests
import base64
import pandas as pd
from PIL import Image
import nltk
from nltk.chat.util import Chat, reflections
import io
import plotly.express as px
# Calculate distance
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

# Calculate angle
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

# Function to send alert
def sendWarning():
    st.warning("Alert: Bad posture detected for more than 3 minutes!")

# Streamlit app
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #00000;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Define sidebar menu options
menu_options = {
    "Welcome page": "Description of the app",
    "PDF File Upload": "Upload and display PDF files.",
    "X-ray/MRI Photo Upload": "Upload and display X-ray or MRI photos.",
    "Excel File Upload": "Upload and display Excel files.",
    "Local Videos": "Display local video files.",
    "Chatbot": "Interact with the chatbot.",
    "Posture Stream System": "Detect your posture using your webcam.",
    "Contact Us in Our Official Web Page": "This section contains contact information and links to our official website."
}

# Sidebar menu
st.sidebar.title("Menu")
selection = st.sidebar.radio("Choose an option", options=list(menu_options.keys()))

# Conditional content display
if selection == "Welcome page":
    st.title("Welcome to Physio.py")
    
    # Display the first image
    image_path1 = r"C:\Users\HP\OneDrive\Bureau\posture\3DP1.png"
    if os.path.isfile(image_path1):
        try:
            image = Image.open(image_path1)
            st.image(image, caption="copyright2024", use_column_width=True)
        except Exception as e:
            st.error(f"Error opening image: {e}")
    else:
        st.error("Image file does not exist")
    
    # Descriptive text
    st.title("Posture detection using Mediapipe and OpenCV")
    st.markdown(
        """
        Poor posture is a modern-day epidemic. Research has shown that children as young as 10 years of age are demonstrating spinal degeneration on x-ray. Certain postures, like forward head posture, have been linked to migraines, high blood pressure, and decreased lung capacity. In this work, this application aimed to detect posture using mediapipe. We are going to use side view samples to perform analysis and draw conclusion. Practical application would require a webcam.
        """
    )
    
    # Display the second image
    image_path2 = r"C:\\Users\\HP\\OneDrive\\Bureau\\posture\\PT+Posture.png"
    if os.path.isfile(image_path2):
        try:
            image = Image.open(image_path2)
            st.image(image, caption="This picture presents good and bad posture", use_column_width=True)
        except Exception as e:
            st.error(f"Error opening image: {e}")
    else:
        st.error("Image file does not exist")
    
    # Description of neck pain and physiotherapy exercises
    st.title("Description of Neck Pain Due to Bad Posture")
    st.markdown("""
    Neck pain caused by bad posture often results from prolonged periods of poor alignment, such as slouching or leaning forward. This can strain the muscles, ligaments, and other structures in the neck, leading to discomfort, stiffness, and pain. Common postural issues include forward head posture and rounded shoulders, which can exacerbate muscle tension and spinal misalignment.
    """)
    
    st.title("Categories of Neck Pain")
    st.markdown("""
    1. Acute Neck Pain: Sudden onset, often due to a specific incident like a poor sleeping position or muscle strain.
    2. Chronic Neck Pain: Long-term pain lasting more than three months, often due to ongoing poor posture or repetitive stress.
    3. Radicular Neck Pain: Pain radiating into the arm due to nerve root irritation, commonly from herniated discs or spinal stenosis.
    4. Referred Neck Pain: Pain originating from another part of the body, such as the shoulders or upper back, but felt in the neck area.
    """)
    
    st.title("Physiotherapy Exercises for Neck Pain")
    st.markdown("""
    1. Strengthening Exercises:
        - Isometric Neck Exercises: Press your forehead into your hands (or a wall) without moving your head, holding for a few seconds to strengthen neck muscles.
        - Shoulder Blade Squeezes: Pinch your shoulder blades together and hold for a few seconds to strengthen upper back muscles.
    2. Postural Exercises:
        - Wall Angels: Stand with your back against a wall, arms at 90 degrees, and slide them up and down to improve shoulder and neck alignment.
        - Thoracic Extension: Sit or stand up straight, place your hands behind your head, and gently arch your upper back to improve spinal mobility.
    3. Range of Motion Exercises:
        - Neck Rotations: Slowly turn your head to one side and then the other, holding each position for a few seconds to improve flexibility.
        - Neck Flexion and Extension: Tilt your head forward and backward slowly, holding each position briefly to enhance range of motion.
    """)

# Option to upload and display PDF file
if selection == "PDF File Upload":
    st.write("Upload and Display PDF File")

    def convert_to_base64(file):
        return base64.b64encode(file.read()).decode('utf-8')

    pdf_file = st.file_uploader("Upload your PDF file here", type="pdf")

    if pdf_file is not None:
        pdf_base64 = convert_to_base64(pdf_file)
        pdf_display = f'''
        <iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="900" type="application/pdf"></iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)

# Option to upload and display X-ray/MRI photo
elif selection == "X-ray/MRI Photo Upload":
    st.write("Upload and Display X-ray, MRI Photo")

    photo_file = st.file_uploader("Upload your photo here", type=["jpg", "jpeg", "png"])

    if photo_file is not None:
        image = Image.open(photo_file)
        st.image(image, caption="Uploaded Photo", use_column_width=True)

# Option to upload and display Excel file
elif selection == "Excel File Upload":
    st.write("Upload and Display Excel File")

    excel_file = st.file_uploader("Upload your Excel file here", type="xlsx")

    if excel_file is not None:
        df = pd.read_excel(excel_file)
        st.write("Displaying the contents of the uploaded Excel file:")
        st.dataframe(df)

        # Plot bar chart
        if st.checkbox('Show Bar Chart', key='bar_chart'):
            st.subheader('Bar Chart')
            num_cols = df.select_dtypes(include=['number']).columns
            if not num_cols.empty:
                df_bar = df[num_cols].copy()  # Ensure we don't modify the original DataFrame

                # Reset index to have a 'Categories' column
                df_bar_reset = df_bar.reset_index()
                df_bar_reset.columns = ['Categories'] + list(num_cols)  # Rename columns for clarity

                # Create bar chart using Plotly Express
                fig = px.bar(df_bar_reset, x='Categories', y=num_cols, title='Bar Chart', labels={'Categories': 'Categories', 'value': 'Values'})
                st.plotly_chart(fig)
            else:
                st.write("No numeric columns available for Bar Chart.")

        # Plot pie chart
        if st.checkbox('Show Pie Chart', key='pie_chart'):
            st.subheader('Pie Chart')
            num_cols = df.select_dtypes(include=['number']).columns
            if not num_cols.empty:
                df_pie = df[num_cols].sum()
                # Create pie chart using Plotly Express
                fig_pie = px.pie(names=df_pie.index, values=df_pie.values, title='Pie Chart', labels={'names': 'Categories', 'values': 'Values'})
                st.plotly_chart(fig_pie)
            else:
                st.write("No numeric columns available for Pie Chart.")

        # Plot line chart
        if st.checkbox('Show Line Chart', key='line_chart'):
            st.subheader('Line Chart')
            num_cols = df.select_dtypes(include=['number']).columns
            if not num_cols.empty:
                df_line = df[num_cols].sum().reset_index()
                df_line.columns = ['Categories', 'Values']  # Rename columns for clarity

                # Create line chart using Plotly Express
                fig_line = px.line(df_line, x='Categories', y='Values', title='Values Over Categories', labels={'Categories': 'Categories', 'Values': 'Values'})
                st.plotly_chart(fig_line)
            else:
                st.write("No numeric columns available for Line Chart.")

# Option to display local videos

# Option to display local videos
if selection == "Local Videos":
    st.write("Select a video to play:")

    video_options = {
        "Physical Therapy Session": "ssstik.io_@physicaltherapysession_1723331514902.mp4",
        "Health Tips": "ssstik.io_@whealth__1723331591355.mp4",
        # Add more video options here
    }

    selected_video = st.selectbox("Choose a video", options=list(video_options.keys()))

    if selected_video:
        video_path = video_options[selected_video]
        st.video(video_path)

# Option to interact with the chatbot
elif selection == "Chatbot":
    st.write("Chatbot Application")

    pairs = [
    (r'Hi|Hello|Hey', [
        'Hello! How can I assist you today? Feel free to ask me about neck pain and posture.',
        'Hi there! I am here to provide information about neck pain due to bad posture. How can I help you?'
    ]),
    (r'give me informations?', [
        'I am the Neck Pain Assistant chatbot, designed to provide helpful information about neck pain caused by poor posture, You can call me the Neck Pain and Posture Guide. I’m here to help you with any questions about neck pain and how to improve your posture.'
    ]),
    (r'need more informations?', [
        'I am just a chatbot, but I am fully operational and ready to provide you with information about neck pain and posture! I’m functioning well, thank you for asking, How can I assist you with your posture or neck pain today?'
    ]),
    (r'Give me information about neck pain', [
        'Neck pain is often caused by poor posture, which puts extra strain on your neck muscles and spine. Common issues include muscle tension, stiffness, and discomfort, Good posture involves keeping your head aligned with your spine and avoiding prolonged periods of sitting or looking down. Regular stretches and ergonomic adjustments can help alleviate and prevent neck pain. Bad posture, such as slouching or hunching over, can lead to neck pain by causing misalignment of the spine and increased stress on the neck muscles. To reduce neck pain, maintain a neutral spine position, take frequent breaks, and incorporate stretches and strengthening exercises into your routine. If you experience persistent pain, it’s advisable to consult a healthcare professional.'
    ]),
    (r'What causes bad posture?', [
        'Bad posture can be caused by various factors including prolonged sitting, improper ergonomics, muscle imbalances, and lack of physical activity, Activities such as working at a computer for extended periods without proper support, carrying heavy bags, and slouching can contribute to poor posture, Common causes of bad posture include poor ergonomics at your workstation, sedentary lifestyle, muscle weakness, and habitual slouching. Addressing these factors through ergonomic adjustments, regular exercise, and mindfulness about posture can help improve your alignment and reduce related discomfort.'
    ]),
    (r'How can I improve my posture?', [
        'To improve your posture, focus on exercises that strengthen your back and core muscles, maintain an ergonomic workstation setup, and practice good posture habits, Regular stretching, adjusting your sitting position, and using supportive chairs can also help, Being mindful of your posture throughout the day is crucial Improving posture involves strengthening your core and back muscles, adjusting your workstation to support proper alignment, and practicing good habits such as sitting up straight and keeping your shoulders back. Incorporating regular stretching and exercise into your routine can also support better posture.'
    ]),
    (r'What should I do if I have neck pain?', [
        'If you have neck pain, consider adjusting your posture, taking breaks from prolonged sitting, and performing gentle stretches. Applying heat or cold packs, maintaining good ergonomics, and staying hydrated can also help. If the pain persists or worsens, seek advice from a healthcare professional for a tailored treatment plan, To manage neck pain, try improving your posture, incorporating stretches and strengthening exercises, and using heat or cold therapy. Ensure your workstation is ergonomically designed and take regular breaks to avoid strain. Persistent or severe pain should be evaluated by a healthcare provider for appropriate diagnosis and treatment.'
    ]),
    (r'quit', [
        'Goodbye! If you have more questions about neck pain or posture in the future, don’t hesitate to reach out.',
        'See you later! Feel free to return if you have more questions about neck pain and improving your posture.'
    ]),
]


    chatbot = Chat(pairs, reflections)

    def get_chat_response(user_input):
        return chatbot.respond(user_input)

    user_input = st.text_input("You:", "")

    if st.button("Send"):
        if user_input:
            response = get_chat_response(user_input)
            st.write(f"**Chatbot:** {response}")
        else:
            st.write("**Chatbot:** Please enter a message.")

    # Add a button with an icon
    col1, col2 = st.columns([9, 1])
    with col1:
        st.write("")  # Placeholder for alignment
    with col2:
        if st.button("🔄 Chat"):
            st.write("Button clicked!")

# Option to display contact information
elif selection == "Contact Us in Our Official Web Page":
    st.write("For more information, visit our official website:")
    st.markdown("[Official Website](https://www.linkedin.com/in/izak-reeducation)")
    st.write("Check out our resources:")
    st.markdown("[YouTube Channel](https://www.youtube.com/watch?v=XtHfEI5DUE0)")
    st.markdown("[Physiopedia](https://www.physio-pedia.com/home/)")

# Option for webcam posture detection
elif selection == "Posture Stream System":
    st.write("This app detects your posture using your webcam.")

    # Initialize webcam control
    if 'webcam_running' not in st.session_state:
        st.session_state.webcam_running = False

    # Add buttons for webcam control
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Run"):
            st.session_state.webcam_running = True

    with col2:
        if st.button("Off"):
            st.session_state.webcam_running = False

    if st.session_state.webcam_running:
        st.write("Webcam is running...")  # Placeholder text for demonstration

        # Initialize MediaPipe and OpenCV
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        cap = cv2.VideoCapture(0)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        frame_window = st.image([])

        good_frames = 0
        bad_frames = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        blue = (255, 127, 0)
        red = (50, 50, 255)
        green = (127, 255, 0)
        light_green = (127, 233, 100)
        yellow = (0, 255, 255)
        pink = (255, 0, 255)

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                st.write("Null Frames")
                break

            # Convert the BGR image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image
            keypoints = pose.process(image)

            # Convert the image back to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            if lm:
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * width)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * height)
                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * width)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * height)
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * width)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * height)
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * width)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * height)

                offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

                if offset < 100:
                    cv2.putText(image, str(int(offset)) + ' Aligned', (width - 150, 30), font, 0.9, green, 2)
                else:
                    cv2.putText(image, str(int(offset)) + ' Not Aligned', (width - 150, 30), font, 0.9, red, 2)

                neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
                torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
                cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
                cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
                cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
                cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

                angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

                if neck_inclination < 40 and torso_inclination < 10:
                    bad_frames = 0
                    good_frames += 1
                    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                    cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                    cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)
                else:
                    good_frames = 0
                    bad_frames += 1
                    cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                    cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                    cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

                good_time = (1 / fps) * good_frames
                bad_time = (1 / fps) * bad_frames

                if good_time > 0:
                    time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
                    cv2.putText(image, time_string_good, (10, height - 20), font, 0.9, green, 2)
                else:
                    time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
                    cv2.putText(image, time_string_bad, (10, height - 20), font, 0.9, red, 2)

                if bad_time > 180:
                    st.write("Warning: Poor posture detected for more than 3 minutes!")
                    # Implement your sendWarning function if needed

            frame_window.image(image, channels="BGR")

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        st.write("Webcam is off.")

