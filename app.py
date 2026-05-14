import streamlit as st
import pandas as pd
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
# DEVELOPERS
# =========================================================

developers = {
    "Joseph Hlongwane": "josephhlongwane17@gmail.com",
    "John Smith": "john@gmail.com",
    "Sarah Johnson": "sarah@gmail.com",
    "Michael Brown": "michael@gmail.com"
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

    sender_email = "josephhlongwane17@gmail.com"

    # APP PASSWORD FROM GOOGLE
    sender_password = "pkwq iaqn udue tpvh"

    # UPDATE AFTER DEPLOYMENT
    link = f"http://localhost:8501/?request_id={request_id}"

    subject = f"New Report Request - {report_name}"

    body = f"""
Hi Team,

A new report configuration request has been submitted.

Report Name: {report_name}
Requested By: {requested_by}
Priority: {priority}

#Open Request:
#{link}
Open Google Requirements Document:
{doc_link}

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
# URL PARAMETERS
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
            "Visible Filters",
            "Hidden Filters",
            "Analyze Further",
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

        st.success("Request Loaded Successfully")

        st.dataframe(
            request_df,
            use_container_width=True
        )

        st.divider()

        st.subheader("Update Status")

        status = st.selectbox(
            "Select Status",
            [
                "New",
                "In Progress",
                "Testing",
                "Completed"
            ]
        )

        if st.button("Update Status"):

            cursor.execute("""
            UPDATE requests
            SET status = ?
            WHERE request_id = ?
            """, (
                status,
                request_id_from_url
            ))

            conn.commit()

            st.success("Status Updated")

    else:

        st.error("Request Not Found")

# =========================================================
# SUBMISSION PAGE
# =========================================================

else:

    st.title("📊 Report Configuration Request Portal")

    st.markdown(
        "Submit report requirements for the development team."
    )

    st.divider()

    # =====================================================
    # BASIC INFORMATION
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

    # =====================================================
    # REPORT PURPOSE
    # =====================================================

    report_purpose = st.text_area(
        "Report Purpose *"
    )

    # =====================================================
    # VISIBLE FILTERS
    # =====================================================

    st.subheader("📂 Visible Filters")

    visible_filters = st.multiselect(
        "Select Visible Filters *",
        filters,
        help="Filters visible to users"
    )

    # =====================================================
    # HIDDEN FILTERS
    # =====================================================

    st.subheader("🔒 Hidden Filters")

    hidden_filters = st.multiselect(
        "Select Hidden Filters",
        filters,
        help="Filters applied behind the scenes"
    )

    # =====================================================
    # ANALYZE FURTHER
    # =====================================================

    st.subheader("📈 Analyze Further")

    analyze_further_required = st.radio(
        "Enable Analyze Further?",
        ["Yes", "No"],
        horizontal=True
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
    # PRESENTATION OPTIONS
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
        len(visible_filters) > 0,
        len(selected_query_actions) > 0
    ])

    # =====================================================
    # SUBMIT BUTTON
    # =====================================================

    if submit_button:

    request_id = (
        f"RPT-{datetime.now().year}-"
        f"{str(uuid.uuid4())[:8]}"
    )

    # CREATE GOOGLE DOC
    doc_link = create_google_doc(
        request_id,
        report_name,
        requested_by,
        visible_filters,
        hidden_filters,
        analyze_further_required,
        selected_query_actions,
        selected_meta_actions,
        selected_presentation_actions,
        additional_notes
    )

    # SEND EMAIL
    email_sent = send_email(
        developer_email,
        request_id,
        report_name,
        requested_by,
        priority,
        doc_link
    )

    st.success(
        "✅ Request Submitted Successfully"
    )

    st.info(
        f"Request ID: {request_id}"
    )

    st.success(
        "📄 Google Requirements Document Created"
    )

    st.markdown(
        f"[Open Requirements Document]({doc_link})"
    )

    if email_sent:

        st.success(
            "📧 Developer notification sent successfully"
        )

    else:

        st.warning(
            "Document created but email failed"
        )

    # =====================================================
    # SAVE REQUEST
    # =====================================================

    if submit_button:

        request_id = (
            f"RPT-{datetime.now().year}-"
            f"{str(uuid.uuid4())[:8]}"
        )


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
                "📧 Developer notification sent successfully"
            )

        else:

            st.warning(
                "Request saved but email failed"
            )
from google.oauth2 import service_account
from googleapiclient.discovery import build

# =====================================================
# GOOGLE SETUP
# =====================================================

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

docs_service = build(
    'docs',
    'v1',
    credentials=credentials
)

drive_service = build(
    'drive',
    'v3',
    credentials=credentials
)

# =====================================================
# CREATE GOOGLE DOC
# =====================================================

def create_google_doc(
    request_id,
    report_name,
    requested_by,
    visible_filters,
    hidden_filters,
    analyze_further_required,
    query_actions,
    meta_actions,
    presentation_actions,
    additional_notes
):

    document_title = (
        f"{request_id} - {report_name}"
    )

    # CREATE DOC
    doc = docs_service.documents().create(
        body={"title": document_title}
    ).execute()

    document_id = doc.get('documentId')

    content = f"""
Report Configuration Request

Request ID:
{request_id}

Report Name:
{report_name}

Requested By:
{requested_by}

VISIBLE FILTERS:
{', '.join(visible_filters)}

HIDDEN FILTERS:
{', '.join(hidden_filters)}

ANALYZE FURTHER:
{analyze_further_required}

QUERY ACTIONS:
{', '.join(query_actions)}

META ACTIONS:
{', '.join(meta_actions)}

PRESENTATION OPTIONS:
{', '.join(presentation_actions)}

ADDITIONAL NOTES:
{additional_notes}
"""

    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': content
            }
        }
    ]

    docs_service.documents().batchUpdate(
        documentId=document_id,
        body={'requests': requests}
    ).execute()

    # =================================================
    # MOVE FILE TO GOOGLE DRIVE FOLDER
    # =================================================

    folder_id = "1dlfdV-sfjC1n092FL1bNR3fbHtZ6fz-x"

    drive_service.files().update(
        fileId=document_id,
        addParents=folder_id,
        removeParents='root',
        fields='id, parents'
    ).execute()

    doc_link = (
        f"https://docs.google.com/document/d/"
        f"{document_id}/edit"
    )

    return doc_link
