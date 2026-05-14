import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Report Configuration Portal",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(
    "report_requests.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    request_id TEXT,
    submission_date TEXT,
    report_name TEXT,
    client_name TEXT,
    business_unit TEXT,
    requested_by TEXT,
    developer_name TEXT,
    developer_email TEXT,
    priority TEXT,
    date_required TEXT,
    report_purpose TEXT,
    filters TEXT,
    query_actions TEXT,
    meta_actions TEXT,
    presentation_actions TEXT,
    additional_notes TEXT,
    status TEXT
)
""")

conn.commit()

# =========================================================
# DEVELOPER LIST
# =========================================================

developers = {
    "John Smith": "john@gmail.com",
    "Sarah Johnson": "sarah@gmail.com",
    "Michael Brown": "michael@gmail.com",
    "Joseph Hlongwane": "joseph@gmail.com"
}

# =========================================================
# MASTER LISTS
# =========================================================

filters = [
    "Campaigns",
    "Daily Sales and Stock",
    "Date",
    "Date Range",
    "Dim Business Unit",
    "Dim Calendar",
    "Dim Categories",
    "Dim Location",
    "Dim Products",
    "Dim Retailer",
    "Employee",
    "FactPhoto",
    "Incremental Value",
    "Locations MDM",
    "LSU Adjusted",
    "Macro Data"
]

query_actions = [
    "Drill-Up and Drill-Down",
    "Drill To Level",
    "Expand and Collapse",
    "Dice",
    "Swap",
    "Add",
    "Remove",
    "Quick Sort",
    "Quick Filter",
    "Member Selection",
    "Pivot",
    "Totals",
    "Interact",
    "Explain",
    "Show Empties"
]

meta_actions = [
    "Copy Content",
    "Build New Alert",
    "Analyze Further",
    "Change Visual",
    "Conversations",
    "Workflows",
    "Lasso",
    "Smart Insights",
    "Chat",
    "Actions",
    "Conditional Formatting",
    "Ratings",
    "Metadata Info"
]

presentation_actions = [
    "Show Warnings",
    "Ignore Query Cache",
    "Edit Presentation",
    "Print Or Export",
    "Subscribe",
    "Multi-Highlight Mode",
    "Bookmarks",
    "Full Screen"
]

# =========================================================
# EMAIL FUNCTION
# =========================================================

def send_email(
    developer_email,
    request_id,
    report_name,
    requested_by,
    priority
):

    sender_email = "YOUR_EMAIL@gmail.com"
    sender_password = "YOUR_APP_PASSWORD"

    link = f"http://localhost:8501/?request_id={request_id}"

    subject = f"New Report Request - {report_name}"

    body = f"""
Hi Team,

A new report configuration request has been submitted.

Report Name: {report_name}
Requested By: {requested_by}
Priority: {priority}

Open Request:
{link}

Regards,
Report Configuration Portal
"""

    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = developer_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:

        st.error(f"Email Error: {e}")

        return False

# =========================================================
# CHECK URL PARAMETERS
# =========================================================

query_params = st.query_params

request_id_from_url = query_params.get("request_id")

# =========================================================
# DEVELOPER VIEW
# =========================================================

if request_id_from_url:

    st.title("📋 Report Request Details")

    cursor.execute("""
    SELECT * FROM requests
    WHERE request_id = ?
    """, (request_id_from_url,))

    data = cursor.fetchone()

    if data:

        columns = [
            "Request ID",
            "Submission Date",
            "Report Name",
            "Client Name",
            "Business Unit",
            "Requested By",
            "Developer Name",
            "Developer Email",
            "Priority",
            "Date Required",
            "Report Purpose",
            "Filters",
            "Query Actions",
            "Meta Actions",
            "Presentation Actions",
            "Additional Notes",
            "Status"
        ]

        request_df = pd.DataFrame(
            [data],
            columns=columns
        )

        st.dataframe(
            request_df,
            use_container_width=True
        )

    else:

        st.error("Request Not Found")

# =========================================================
# SUBMISSION FORM
# =========================================================

else:

    st.title("📊 Report Configuration Request Portal")

    st.divider()

    # =====================================================
    # BASIC INFO
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        report_name = st.text_input(
            "Report Name *"
        )

        client_name = st.text_input(
            "Client Name *"
        )

        business_unit = st.text_input(
            "Business Unit *"
        )

    with col2:

        requested_by = st.text_input(
            "Requested By *"
        )

        priority = st.selectbox(
            "Priority *",
            ["High", "Medium", "Low"]
        )

        date_required = st.date_input(
            "Date Required *"
        )

    with col3:

        developer_name = st.selectbox(
            "Assign Developer *",
            list(developers.keys())
        )

        developer_email = developers[
            developer_name
        ]

        st.text_input(
            "Developer Email",
            value=developer_email,
            disabled=True
        )

    st.divider()

    report_purpose = st.text_area(
        "Report Purpose *"
    )

    # =====================================================
    # FILTERS
    # =====================================================

    st.subheader("📂 Filters")

    selected_filters = st.multiselect(
        "Select Filters *",
        filters
    )

    # =====================================================
    # QUERY ACTIONS
    # =====================================================

    st.subheader("⚙ Query Context Actions")

    selected_query_actions = []

    cols = st.columns(3)

    for i, action in enumerate(query_actions):

        if cols[i % 3].checkbox(
            action,
            key=f"q_{i}"
        ):
            selected_query_actions.append(action)

    # =====================================================
    # META ACTIONS
    # =====================================================

    st.subheader("📈 Report Meta Actions")

    selected_meta_actions = []

    cols = st.columns(3)

    for i, action in enumerate(meta_actions):

        if cols[i % 3].checkbox(
            action,
            key=f"m_{i}"
        ):
            selected_meta_actions.append(action)

    # =====================================================
    # PRESENTATION ACTIONS
    # =====================================================

    st.subheader("🖥 Presentation Options")

    selected_presentation_actions = []

    cols = st.columns(3)

    for i, action in enumerate(
        presentation_actions
    ):

        if cols[i % 3].checkbox(
            action,
            key=f"p_{i}"
        ):
            selected_presentation_actions.append(action)

    # =====================================================
    # NOTES
    # =====================================================

    st.subheader("📝 Additional Notes")

    additional_notes = st.text_area(
        "Additional Requirements"
    )

    # =====================================================
    # VALIDATION
    # =====================================================

    form_complete = all([
        report_name,
        client_name,
        business_unit,
        requested_by,
        report_purpose,
        len(selected_filters) > 0,
        len(selected_query_actions) > 0
    ])

    # =====================================================
    # SUBMIT BUTTON
    # =====================================================

    st.divider()

    if not form_complete:

        st.warning(
            "Please complete all required fields before submitting."
        )

    submit_button = st.button(
        "🚀 Submit Request",
        disabled=not form_complete,
        use_container_width=True
    )

    # =====================================================
    # SAVE REQUEST
    # =====================================================

    if submit_button:

        request_id = (
            f"RPT-{datetime.now().year}-"
            f"{str(uuid.uuid4())[:8]}"
        )

        cursor.execute("""
        INSERT INTO requests VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            request_id,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            report_name,
            client_name,
            business_unit,
            requested_by,
            developer_name,
            developer_email,
            priority,
            str(date_required),
            report_purpose,
            ", ".join(selected_filters),
            ", ".join(selected_query_actions),
            ", ".join(selected_meta_actions),
            ", ".join(selected_presentation_actions),
            additional_notes,
            "New"
        ))

        conn.commit()

        email_sent = send_email(
            developer_email,
            request_id,
            report_name,
            requested_by,
            priority
        )

        st.success(
            "✅ Request Submitted Successfully"
        )

        st.info(
            f"Request ID: {request_id}"
        )

        if email_sent:

            st.success(
                "📧 Developer notification sent"
            )

        else:

            st.warning(
                "Request saved but email failed"
            )
