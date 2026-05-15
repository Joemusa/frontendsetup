import streamlit as st
import pandas as pd
import uuid
import smtplib
import gspread
from jira import JIRA

from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2 import service_account

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Report Configuration Portal",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# SESSION STATE DEFAULTS
# =========================================================

default_values = {

    "report_name": "",
    "client_name": "",
    "business_unit": "",
    "requested_by": "",
    "priority": "Medium",
    "report_purpose": "",
    "custom_visible_filters": "",
    "custom_hidden_filters": "",
    "analyze_further_required": "No",
    "exception_report_required": "No",
    "usage_report_required": "No",
    "additional_notes": ""

}

for key, value in default_values.items():

    if key not in st.session_state:

        st.session_state[key] = value

# =========================================================
# JIRA CONNECTION
# =========================================================

jira_options = {
    'server': st.secrets["jira"]["server"]
}

jira = JIRA(
    options=jira_options,
    basic_auth=(
        st.secrets["jira"]["email"],
        st.secrets["jira"]["api_token"]
    )
)

def create_jira_ticket(

    request_id,
    report_name,
    requested_by,
    priority,
    report_purpose,
    visible_filters,
    hidden_filters,
    developer_name

):

    issue_dict = {

        'project': {
            'key': st.secrets["jira"]["project_key"]
        },

        'summary': f"{request_id} - {report_name}",

        'description': f"""

REQUEST ID:
{request_id}

REQUESTED BY:
{requested_by}

PRIORITY:
{priority}

ASSIGNED DEVELOPER:
{developer_name}

====================================================

REPORT PURPOSE

{report_purpose}

====================================================

VISIBLE FILTERS

{visible_filters}

====================================================

HIDDEN FILTERS

{hidden_filters}

        """,

        'issuetype': {
            'name': 'Task'
        }
    }

    new_issue = jira.create_issue(
        fields=issue_dict
    )

    return new_issue.key
# =========================================================
# GOOGLE AUTH
# =========================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

# =========================================================
# GOOGLE SHEET
# =========================================================

GOOGLE_SHEET_ID = "1tqLkD_nXVt9YlMczTTVQY7pp8uHDrMMXi8YqdC4yGtA"

sheet = gc.open_by_key(
    GOOGLE_SHEET_ID
).sheet1

# =========================================================
# DEVELOPERS
# =========================================================

developers = {
    "Joseph Hlongwane": "josephhlongwane17@gmail.com",
    "John Smith": "john@gmail.com",
    "Sarah Johnson": "sarah@gmail.com",
    "Michael Brown": "michael@gmail.com"
}

# =========================================================
# FILTERS
# =========================================================

filters = [
    "Sub Location",
    "Brand",
    "Date",
    "SKU Format",
    "Buyability Points Category",
    "Principle",
    "CallID",
    "Facia",
    "PersonID",
    "VisitDate",
    "Region Name",
    "Period",
    "Segment",
    "Territory",
    "Date",
    "Facia",
    "Cycle",
    "Name"
]

# =========================================================
# QUERY ACTIONS
# =========================================================

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

# =========================================================
# META ACTIONS
# =========================================================

meta_actions = [
    "Copy Content",
    "Build New Alert",
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

# =========================================================
# PRESENTATION ACTIONS
# =========================================================

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

    sender_email = "josephhlongwane17@gmail.com"

    sender_password = "pkwq iaqn udue tpvh"

    sheet_link = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{GOOGLE_SHEET_ID}"
    )

    subject = f"New Report Request - {report_name}"

    body = f"""
Hi Team,

A new report request has been submitted.

====================================================

REQUEST ID:
{request_id}

REPORT NAME:
{report_name}

REQUESTED BY:
{requested_by}

PRIORITY:
{priority}

====================================================

OPEN GOOGLE SHEET:

{sheet_link}

====================================================

Regards,
Report Configuration Portal
"""

    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = developer_email
    msg["Subject"] = subject

    msg.attach(
        MIMEText(body, "plain")
    )

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
# PAGE TITLE
# =========================================================

st.title("📊 Report Configuration Portal")

st.markdown(
    "Submit report setup requirements for the development team."
)

st.divider()

# =========================================================
# BASIC INFORMATION
# =========================================================

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

# =========================================================
# REPORT PURPOSE
# =========================================================

report_purpose = st.text_area(
    "Report Purpose *"
)

# =========================================================
# VISIBLE FILTERS
# =========================================================

st.subheader("📂 Visible Filters")

visible_filters = st.multiselect(
    "Select Visible Filters *",
    filters
)

custom_visible_filters = st.text_area(
    "Add Custom Visible Filters",
    help="Separate filters using commas"
)

custom_visible_filters_list = [
    x.strip()
    for x in custom_visible_filters.split(",")
    if x.strip()
]

all_visible_filters = (
    visible_filters +
    custom_visible_filters_list
)

# =========================================================
# HIDDEN FILTERS
# =========================================================

st.subheader("🔒 Hidden Filters")

hidden_filters = st.multiselect(
    "Select Hidden Filters",
    filters
)

custom_hidden_filters = st.text_area(
    "Add Custom Hidden Filters",
    help="Separate filters using commas"
)

custom_hidden_filters_list = [
    x.strip()
    for x in custom_hidden_filters.split(",")
    if x.strip()
]

all_hidden_filters = (
    hidden_filters +
    custom_hidden_filters_list
)

# =========================================================
# ANALYZE FURTHER
# =========================================================

st.subheader("📈 Analyze Further")

analyze_further_required = st.radio(
    "Enable Analyze Further?",
    ["Yes", "No"],
    horizontal=True
)
# =========================================================
# PRODUCTION EXCEPTION REPORT
# =========================================================

st.subheader("📈 Production Exception Report")

exception_report_required = st.radio(
    "Enable Production Exception Report?",
    ["Yes", "No"],
    horizontal=True
)
# =========================================================
# USAGE REPORT
# =========================================================

st.subheader("📈 Usage Report")

usage_report_required = st.radio(
    "Enable Usage Report?",
    ["Yes", "No"],
    horizontal=True
)
# =========================================================
# QUERY ACTIONS
# =========================================================

st.subheader("⚙ Query Context Actions")

selected_query_actions = []

cols = st.columns(3)

for i, action in enumerate(query_actions):

    if cols[i % 3].checkbox(
        action,
        key=f"q_{i}"
    ):
        selected_query_actions.append(action)

# =========================================================
# META ACTIONS
# =========================================================

st.subheader("📊 Report Meta Actions")

selected_meta_actions = []

cols = st.columns(3)

for i, action in enumerate(meta_actions):

    if cols[i % 3].checkbox(
        action,
        key=f"m_{i}"
    ):
        selected_meta_actions.append(action)

# =========================================================
# PRESENTATION ACTIONS
# =========================================================

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

# =========================================================
# ADDITIONAL NOTES
# =========================================================

st.subheader("📝 Additional Notes")

additional_notes = st.text_area(
    "Additional Requirements"
)

# =========================================================
# VALIDATION
# =========================================================

form_complete = all([
    report_name,
    client_name,
    business_unit,
    requested_by,
    report_purpose,
    len(all_visible_filters) > 0
])

# =========================================================
# SUBMIT BUTTON
# =========================================================

st.divider()

if not form_complete:

    st.warning(
        "Please complete all required fields."
    )

submit_button = st.button(
    "🚀 Submit Request",
    disabled=not form_complete,
    use_container_width=True
)

# =========================================================
# SUBMIT LOGIC
# =========================================================

if submit_button:

    request_id = (
        f"RPT-{datetime.now().year}-"
        f"{str(uuid.uuid4())[:8]}"
    )

    try:

        sheet.append_row([

            request_id,
            jira_ticket,
            str(datetime.now()),
            report_name,
            client_name,
            business_unit,
            requested_by,
            developer_name,
            developer_email,
            priority,
            str(date_required),
            report_purpose,
            ", ".join(all_visible_filters),
            ", ".join(all_hidden_filters),
            analyze_further_required,
            ", ".join(selected_query_actions),
            ", ".join(selected_meta_actions),
            ", ".join(selected_presentation_actions),
            exception_report_required,
            exception_report_required, 
            additional_notes,
            "New"

        ])

        st.success(
            "✅ Request Submitted Successfully"
        )

        st.success(
            "📄 Request Saved To Google Sheets"
        )

        sheet_link = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{GOOGLE_SHEET_ID}"
        )

        st.markdown(
            f"### [📂 Open Google Sheet]({sheet_link})"
        )

        email_sent = send_email(
            developer_email,
            request_id,
            report_name,
            requested_by,
            priority
        )

        if email_sent:

            st.success(
                "📧 Developer notification sent"
            )

        else:

            st.warning(
                "Request saved but email failed"
            )

        try:

        jira_ticket = create_jira_ticket(
    
            request_id,
            report_name,
            requested_by,
            priority,
            report_purpose,
            ", ".join(all_visible_filters),
            ", ".join(all_hidden_filters),
            developer_name
    
        )
    
        st.success(
            f"✅ Jira Ticket Created: {jira_ticket}"
        )
    
    except Exception as e:
    
        st.error(
            f"Jira Error: {e}"
        )
        jira_link = (
        f"{st.secrets['jira']['server']}/browse/{jira_ticket}"
    )

    st.success(
    f"✅ Jira Ticket Created: {jira_ticket}"
    )
    
    st.link_button(
        "Open Jira Ticket",
        jira_link
    )
    JIRA LINK:

    {jira_link}

    except Exception as e:

        st.error(e)
