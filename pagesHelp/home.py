import streamlit as st


def home_page():
    # Title
    st.title("Donna - A title and a name ")

    # First Paragraph - related to resume scanning
    st.subheader("Welcome to Donna's empire of personal assistance")
    st.markdown(
        """
    Hi there I'm donna I am a virtual HR assistant I can help yo with your day to day task of hiring like scheduling the interview, giving you candidate and indutry hiring insights I can communicate with your candidates
    and can solve any problems they are having, cause I'm donna I solve problems and I 'm empathetic and you can ask any number of time I won't feel bad No will.....wait I will 
    """
    )
    # Random Image
    # st.image("https://via.placeholder.com/500x300?text=Resume+Scanning+Image+1", caption="AI-Powered Resume Analysis")
    # usage video  link: https://youtu.be/QyavlbFy6Bc
    # Replace with your actual unlisted YouTube video ID
    video_id = "QyavlbFy6Bc"  # Change this to your video ID

    # YouTube embed URL format
    # embed_url = f"https://www.youtube.com/embed/{video_id}"

    # # Embed the video using an iframe
    # st.markdown(
    #     f'<iframe width="700" height="400" src="{embed_url}" frameborder="0" allowfullscreen></iframe>',
    #     unsafe_allow_html=True,
    # )

    # Second Paragraph - About the Create Jobnd navigation
    st.markdown(
        """
    As of now I can only help in scheduling your interview with the cnadidates through my cutting edge and affordable AI technology people are working hard really hard on me (oops) to build me
    """
    )

    st.subheader("User Instructions!!!")
    st.subheader("I can't provide chat functionality because of the resource constraints but if you really want to try it contact me on email the main idea behind chat is that you don't even have to remember any steps or literally anything Donna will reeachout to you every single time and you can ask whatever you want,the number of times you want")
    st.markdown("""
                * Fristly you need to make sure all the users are registered within the system so use the User Registration form for it.
                * Then create a job with the system using hte Create New Job form fill the details and wait for a while
                * Now the employee's in the Panel need to give the slots of their availability through the employeee availability slots
                * Then here's the link for a format of candidate sheet which you need to use to fill the name, contact, email of the candidates whom interview you want to schedule sheet - 
                * Then once you have your sheet ready in the desired format use the Insert Candidate Sheet to insert the cnadidate sheet with system so that system can start reaching out to candidates
                * This cycle will repeat mutliple times till you have completed you hiring employee availability -> calling candidates -> scheduling interivews
                """)
    # Third Paragraph - About the creators and why it was built
    st.markdown(
        """
    This tool was built with the goal of making the recruitment process more efficient, saving time and effort for HR professionals, recruiters, and hiring managers. 
    The idea was born from the need to process and analyze resumes quickly and accurately, without compromising on quality. We believe that technology can 
    bridge the gap between employers and job seekers, making it easier to match the right people to the right opportunities.
    
    FeedBack Form link: https://forms.gle/jd3D5vPn7ThBX5Uu8 \n
    Contact: yashtiwari.enigneer@gmail.com
    """
    )
    # Random Image
    # st.image("https://via.placeholder.com/500x300?text=Team+Image", caption="The Team Behind Donna's Resume Scanning")
