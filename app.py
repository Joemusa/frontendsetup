# import streamlit as st
# from datetime import datetime
# import uuid
# import smtplib

# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# from google.oauth2 import service_account
# from googleapiclient.discovery import build

import streamlit as st

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/drive'
]

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

drive_service = build(
    'drive',
    'v3',
    credentials=credentials
)

st.success("Authenticated")

folder_id = "1dlfdV-sfjC1n092FL1bNR3fbHtZ6fz-x"

document_title = "Test Document"

try:

    file_metadata = {
    'name': document_title,
    'mimeType': 'application/vnd.google-apps.document',
    'parents': [folder_id]
    }
    
    file = drive_service.files().create(
        body=file_metadata,
        supportsAllDrives=True
    ).execute()
    
    document_id = file.get('id')
    
    st.success("Google Doc Created")
    
    st.write(document_id)
# # =========================================================
# # PAGE CONFIG
# # =========================================================

# st.set_page_config(
#     page_title="Report Configuration Portal",
#     page_icon="📊",
#     layout="wide"
# )
# #st.write(st.secrets["gcp_service_account"]["frontendsetup@rentabuka.iam.gserviceaccount.com"])


# # =========================================================
# # GOOGLE CONFIG
# # =========================================================

# SCOPES = [
#     'https://www.googleapis.com/auth/documents',
#     'https://www.googleapis.com/auth/drive'
# ]


# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"],
#     scopes=SCOPES
# )

# docs_service = build(
#     'docs',
#     'v1',
#     credentials=credentials
# )

# drive_service = build(
#     'drive',
#     'v3',
#     credentials=credentials
# )

# # =========================================================
# # GOOGLE DRIVE FOLDER ID
# # =========================================================

# # REPLACE THIS WITH YOUR REAL FOLDER ID
# folder_id = "1dlfdV-sfjC1n092FL1bNR3fbHtZ6fz-x"

# #https://drive.google.com/drive/folders/1dlfdV-sfjC1n092FL1bNR3fbHtZ6fz-x?usp=sharing

# # =========================================================
# # DEVELOPERS
# # =========================================================

# developers = {
#     "Joseph Hlongwane": "josephhlongwane17@gmail.com",
#     "John Smith": "john@gmail.com",
#     "Sarah Johnson": "sarah@gmail.com",
#     "Michael Brown": "michael@gmail.com"
# }

# # =========================================================
# # MASTER LISTS
# # =========================================================

# filters = [
#     "Campaigns",
#     "Daily Sales and Stock",
#     "Date",
#     "Date Range",
#     "Dim Business Unit",
#     "Dim Calendar",
#     "Dim Categories",
#     "Dim Location",
#     "Dim Products",
#     "Dim Retailer",
#     "Employee",
#     "FactPhoto",
#     "Incremental Value",
#     "Locations MDM",
#     "LSU Adjusted",
#     "Macro Data"
# ]

# query_actions = [
#     "Drill-Up and Drill-Down",
#     "Drill To Level",
#     "Expand and Collapse",
#     "Dice",
#     "Swap",
#     "Add",
#     "Remove",
#     "Quick Sort",
#     "Quick Filter",
#     "Member Selection",
#     "Pivot",
#     "Totals",
#     "Interact",
#     "Explain",
#     "Show Empties"
# ]

# meta_actions = [
#     "Copy Content",
#     "Build New Alert",
#     "Change Visual",
#     "Conversations",
#     "Workflows",
#     "Lasso",
#     "Smart Insights",
#     "Chat",
#     "Actions",
#     "Conditional Formatting",
#     "Ratings",
#     "Metadata Info"
# ]

# presentation_actions = [
#     "Show Warnings",
#     "Ignore Query Cache",
#     "Edit Presentation",
#     "Print Or Export",
#     "Subscribe",
#     "Multi-Highlight Mode",
#     "Bookmarks",
#     "Full Screen"
# ]

# # =========================================================
# # CREATE GOOGLE DOC
# # =========================================================

# def create_google_doc(
#     request_id,
#     report_name,
#     client_name,
#     business_unit,
#     requested_by,
#     developer_name,
#     priority,
#     date_required,
#     report_purpose,
#     visible_filters,
#     hidden_filters,
#     analyze_further_required,
#     query_actions_selected,
#     meta_actions_selected,
#     presentation_actions_selected,
#     additional_notes
# ):

#     document_title = (
#         f"{request_id} - {report_name}"
#     )

#     # CREATE GOOGLE DOC
#     doc = docs_service.documents().create(
#         body={"title": document_title}
#     ).execute()

#     document_id = doc.get('documentId')

#     content = f"""
# REPORT CONFIGURATION REQUEST

# ====================================================

# REQUEST ID:
# {request_id}

# REPORT NAME:
# {report_name}

# CLIENT NAME:
# {client_name}

# BUSINESS UNIT:
# {business_unit}

# REQUESTED BY:
# {requested_by}

# ASSIGNED DEVELOPER:
# {developer_name}

# PRIORITY:
# {priority}

# DATE REQUIRED:
# {date_required}

# ====================================================

# REPORT PURPOSE

# {report_purpose}

# ====================================================

# VISIBLE FILTERS

# {', '.join(visible_filters)}

# ====================================================

# HIDDEN FILTERS

# {', '.join(hidden_filters)}

# ====================================================

# ANALYZE FURTHER REQUIRED

# {analyze_further_required}

# ====================================================

# QUERY CONTEXT ACTIONS

# {', '.join(query_actions_selected)}

# ====================================================

# REPORT META ACTIONS

# {', '.join(meta_actions_selected)}

# ====================================================

# PRESENTATION OPTIONS

# {', '.join(presentation_actions_selected)}

# ====================================================

# ADDITIONAL NOTES

# {additional_notes}

# ====================================================
# """

#     requests = [
#         {
#             'insertText': {
#                 'location': {
#                     'index': 1
#                 },
#                 'text': content
#             }
#         }
#     ]

#     docs_service.documents().batchUpdate(
#         documentId=document_id,
#         body={'requests': requests}
#     ).execute()

#     # MOVE FILE TO DRIVE FOLDER
#     drive_service.files().update(
#     fileId=document_id,
#     addParents=folder_id,
#     fields='id, parents'
#     ).execute()

#     doc_link = (
#         f"https://docs.google.com/document/d/"
#         f"{document_id}/edit"
#     )

#     return doc_link

# # =========================================================
# # SEND EMAIL
# # =========================================================

# def send_email(
#     developer_email,
#     request_id,
#     report_name,
#     requested_by,
#     priority,
#     doc_link
# ):

#     sender_email = "josephhlongwane17@gmail.com"

#     # GOOGLE APP PASSWORD
#     sender_password = "pkwq iaqn udue tpvh"

#     subject = f"New Report Request - {report_name}"

#     body = f"""
# Hi Team,

# A new report configuration request has been submitted.

# ====================================================

# REQUEST ID:
# {request_id}

# REPORT NAME:
# {report_name}

# REQUESTED BY:
# {requested_by}

# PRIORITY:
# {priority}

# ====================================================

# OPEN REQUIREMENTS DOCUMENT:

# {doc_link}

# ====================================================

# Regards,
# Report Configuration Portal
# """

#     msg = MIMEMultipart()

#     msg["From"] = sender_email
#     msg["To"] = developer_email
#     msg["Subject"] = subject

#     msg.attach(
#         MIMEText(body, "plain")
#     )

#     try:

#         server = smtplib.SMTP(
#             "smtp.gmail.com",
#             587
#         )

#         server.starttls()

#         server.login(
#             sender_email,
#             sender_password
#         )

#         server.send_message(msg)

#         server.quit()

#         return True

#     except Exception as e:

#         st.error(f"Email Error: {e}")

#         return False

# # =========================================================
# # PAGE TITLE
# # =========================================================

# st.title("📊 Report Configuration Portal")

# st.markdown(
#     "Submit report setup requirements for the development team."
# )

# st.divider()

# # =========================================================
# # BASIC INFORMATION
# # =========================================================

# col1, col2, col3 = st.columns(3)

# with col1:

#     report_name = st.text_input(
#         "Report Name *"
#     )

#     client_name = st.text_input(
#         "Client Name *"
#     )

#     business_unit = st.text_input(
#         "Business Unit *"
#     )

# with col2:

#     requested_by = st.text_input(
#         "Requested By *"
#     )

#     priority = st.selectbox(
#         "Priority *",
#         ["High", "Medium", "Low"]
#     )

#     date_required = st.date_input(
#         "Date Required *"
#     )

# with col3:

#     developer_name = st.selectbox(
#         "Assign Developer *",
#         list(developers.keys())
#     )

#     developer_email = developers[
#         developer_name
#     ]

#     st.text_input(
#         "Developer Email",
#         value=developer_email,
#         disabled=True
#     )

# st.divider()

# # =========================================================
# # REPORT PURPOSE
# # =========================================================

# report_purpose = st.text_area(
#     "Report Purpose *"
# )

# # =========================================================
# # VISIBLE FILTERS
# # =========================================================

# st.subheader("📂 Visible Filters")

# visible_filters = st.multiselect(
#     "Select Visible Filters *",
#     filters,
#     help="Filters visible to end users"
# )

# # CUSTOM VISIBLE FILTERS
# custom_visible_filters = st.text_area(
#     "Add Custom Visible Filters",
#     help="Enter filters separated by commas"
# )

# # CONVERT CUSTOM FILTERS TO LIST
# custom_visible_filters_list = [
#     x.strip()
#     for x in custom_visible_filters.split(",")
#     if x.strip()
# ]

# # FINAL VISIBLE FILTERS
# all_visible_filters = (
#     visible_filters +
#     custom_visible_filters_list
# )

# # =========================================================
# # HIDDEN FILTERS
# # =========================================================

# st.subheader("🔒 Hidden Filters")

# hidden_filters = st.multiselect(
#     "Select Hidden Filters",
#     filters,
#     help="Filters applied behind the scenes"
# )

# # CUSTOM HIDDEN FILTERS
# custom_hidden_filters = st.text_area(
#     "Add Custom Hidden Filters",
#     help="Enter filters separated by commas"
# )

# # CONVERT TO LIST
# custom_hidden_filters_list = [
#     x.strip()
#     for x in custom_hidden_filters.split(",")
#     if x.strip()
# ]

# # FINAL HIDDEN FILTERS
# all_hidden_filters = (
#     hidden_filters +
#     custom_hidden_filters_list
# )

# # =========================================================
# # ANALYZE FURTHER
# # =========================================================

# st.subheader("📈 Analyze Further")

# analyze_further_required = st.radio(
#     "Enable Analyze Further?",
#     ["Yes", "No"],
#     horizontal=True
# )

# # =========================================================
# # QUERY ACTIONS
# # =========================================================

# st.subheader("⚙ Query Context Actions")

# selected_query_actions = []

# cols = st.columns(3)

# for i, action in enumerate(query_actions):

#     if cols[i % 3].checkbox(
#         action,
#         key=f"q_{i}"
#     ):
#         selected_query_actions.append(action)

# # =========================================================
# # META ACTIONS
# # =========================================================

# st.subheader("📊 Report Meta Actions")

# selected_meta_actions = []

# cols = st.columns(3)

# for i, action in enumerate(meta_actions):

#     if cols[i % 3].checkbox(
#         action,
#         key=f"m_{i}"
#     ):
#         selected_meta_actions.append(action)

# # =========================================================
# # PRESENTATION OPTIONS
# # =========================================================

# st.subheader("🖥 Presentation Options")

# selected_presentation_actions = []

# cols = st.columns(3)

# for i, action in enumerate(
#     presentation_actions
# ):

#     if cols[i % 3].checkbox(
#         action,
#         key=f"p_{i}"
#     ):
#         selected_presentation_actions.append(action)

# # =========================================================
# # NOTES
# # =========================================================

# st.subheader("📝 Additional Notes")

# additional_notes = st.text_area(
#     "Additional Requirements"
# )

# # =========================================================
# # VALIDATION
# # =========================================================

# form_complete = all([
#     report_name,
#     client_name,
#     business_unit,
#     requested_by,
#     report_purpose,
#     len(all_visible_filters) > 0,
#     len(selected_query_actions) > 0
# ])

# # =========================================================
# # SUBMIT BUTTON
# # =========================================================

# st.divider()

# if not form_complete:

#     st.warning(
#         "Please complete all required fields before submitting."
#     )

# submit_button = st.button(
#     "🚀 Submit Request",
#     disabled=not form_complete,
#     use_container_width=True
# )

# # =========================================================
# # SUBMIT LOGIC
# # =========================================================

# if submit_button:

#     request_id = (
#         f"RPT-{datetime.now().year}-"
#         f"{str(uuid.uuid4())[:8]}"
#     )

#     # CREATE GOOGLE DOC
#     doc_link = create_google_doc(
#         request_id,
#         report_name,
#         client_name,
#         business_unit,
#         requested_by,
#         developer_name,
#         priority,
#         str(date_required),
#         report_purpose,
#         all_visible_filters,
#         all_hidden_filters,
#         analyze_further_required,
#         selected_query_actions,
#         selected_meta_actions,
#         selected_presentation_actions,
#         additional_notes
#     )

#     # SEND EMAIL
#     email_sent = send_email(
#         developer_email,
#         request_id,
#         report_name,
#         requested_by,
#         priority,
#         doc_link
#     )

#     st.success(
#         "✅ Request Submitted Successfully"
#     )

#     st.success(
#         "📄 Google Requirements Document Created"
#     )

#     st.markdown(
#         f"### [📂 Open Requirements Document]({doc_link})"
#     )

#     if email_sent:

#         st.success(
#             "📧 Developer notification email sent successfully"
#         )

#     else:

#         st.warning(
#             "Document created but email failed"
#        # )
