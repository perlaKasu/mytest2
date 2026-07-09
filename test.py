import streamlit as st
import pandas as pd
import sqlite3

# ---------------- Database ----------------

conn = sqlite3.connect("job.db")
cursor = conn.cursor()

# Updated table schema to include a password field
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications(
    username TEXT,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    dob TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    qualification TEXT,
    college TEXT,
    graduation_year INTEGER,
    cgpa REAL,
    job_role TEXT,
    experience INTEGER,
    skills TEXT,
    expected_salary REAL
)
""")

conn.commit()

# ---------------- Streamlit Page ----------------

st.set_page_config(page_title="IT Job Registration Form", page_icon="💼")

st.title("💼 IT Job Registration Form")
st.write("Please fill in the details below to apply for an IT job.")

# ---------------- Form ----------------

with st.form("job_registration_form"):

    st.subheader("Personal Information")

    username = st.text_input("Username")
    # Added type="password" to mask the input for privacy
    password = st.text_input("Password", type="password", help="Create a secure password")
    
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    gender = st.radio(
        "Gender",
        ["Male", "Female", "Other"]
    )

    dob = st.date_input("Date of Birth")

    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")

    address = st.text_area("Address")

    st.subheader("Educational Details")

    qualification = st.selectbox(
        "Highest Qualification",
        [
            "B.Tech",
            "B.Sc",
            "BCA",
            "M.Tech",
            "MCA",
            "M.Sc",
            "Diploma",
            "Other"
        ]
    )

    college = st.text_input("College/University")

    graduation_year = st.number_input(
        "Graduation Year",
        min_value=2000,
        max_value=2035,
        step=1
    )

    cgpa = st.number_input(
        "CGPA / Percentage",
        min_value=0.0,
        max_value=100.0
    )

    st.subheader("Job Information")

    job_role = st.selectbox(
        "Preferred Job Role",
        [
            "Python Developer",
            "Data Analyst",
            "Data Scientist",
            "Web Developer",
            "Full Stack Developer",
            "Software Engineer",
            "UI/UX Designer",
            "DevOps Engineer"
        ]
    )

    experience = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=30,
        step=1
    )

    skills = st.multiselect(
        "Technical Skills",
        [
            "Python",
            "Java",
            "C++",
            "SQL",
            "Power BI",
            "Excel",
            "Machine Learning",
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Django",
            "Flask",
            "AWS"
        ]
    )

    expected_salary = st.number_input(
        "Expected Salary (LPA)",
        min_value=1.0,
        max_value=100.0
    )

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "doc", "docx"]
    )

    submit = st.form_submit_button("Submit Application")

# ---------------- Submit Action ----------------

if submit:
    if not username or not password:
        st.error("❌ Username and Password are required!")
    else:
        skills_str = ", ".join(skills)

        cursor.execute("""
        INSERT INTO applications
        (username, password, first_name, last_name, gender, dob, phone, email,
        address, qualification, college, graduation_year, cgpa,
        job_role, experience, skills, expected_salary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            password, # Stored in the database
            first_name,
            last_name,
            gender,
            str(dob),
            phone,
            email,
            address,
            qualification,
            college,
            graduation_year,
            cgpa,
            job_role,
            experience,
            skills_str,
            expected_salary
        ))

        conn.commit()

        # Excluded password from the summary display data dictionary for privacy
        data = {
            "Username": username,
            "First Name": first_name,
            "Last Name": last_name,
            "Gender": gender,
            "DOB": str(dob),
            "Phone": phone,
            "Email": email,
            "Address": address,
            "Qualification": qualification,
            "College": college,
            "Graduation Year": graduation_year,
            "CGPA": cgpa,
            "Job Role": job_role,
            "Experience": experience,
            "Skills": skills_str,
            "Expected Salary": expected_salary
        }

        st.success("✅ Application Submitted Successfully!")

        st.subheader("Submitted Details")
        st.json(data)

        df = pd.DataFrame([data])
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Application",
            csv,
            "job_application.csv",
            "text/csv"
        )

# ---------------- Admin View Database Section ----------------

st.markdown("---")
st.subheader("🔒 Admin Access: Saved Applications")

# Privacy Feature: Masked password verification field to see the database
admin_password_input = st.text_input("Enter Admin Password to view details", type="password")

if st.button("Show All Applications"):
    # Replace 'admin123' with your preferred secure password
    if admin_password_input == "l23cse207":
        df = pd.read_sql_query(
            "SELECT username, first_name, last_name, gender, dob, phone, email, address, qualification, college, graduation_year, cgpa, job_role, experience, skills, expected_salary FROM applications",
            conn
        )
        
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No applications found in the database.")
    else:
        st.error("❌ Invalid Admin Password. Access Denied.")

conn.close()
