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


request_tab, engineer_tab = st.tabs([
    "📋 Report Request Form",
    "⚙️ Data Engineering"
])

with request_tab:

  
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
    
            # =====================================================
            # CREATE JIRA TICKET
            # =====================================================
    
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
    
            # =====================================================
            # SAVE TO GOOGLE SHEETS
            # =====================================================
    
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
                additional_notes,
                "New"
    
            ])
    
            st.success(
                "📄 Request Saved To Google Sheets"
            )
    
            # =====================================================
            # GOOGLE SHEET LINK
            # =====================================================
    
            sheet_link = (
                f"https://docs.google.com/spreadsheets/d/"
                f"{GOOGLE_SHEET_ID}"
            )
    
            st.markdown(
                f"### [📂 Open Google Sheet]({sheet_link})"
            )
    
            # =====================================================
            # SEND EMAIL
            # =====================================================
    
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
    
            # =====================================================
            # FINAL SUCCESS
            # =====================================================
    
            st.success(
                "✅ Request Submitted Successfully"
            )
    
        except Exception as e:
    
            st.error(
                f"Submission Error: {e}"
            )

# =====================================================
# DATA MODEL REQUIREMENTS TAB
# =====================================================

with model_tab:

    st.title(
        "⚙️ Data Model Requirements"
    )

    # =====================================================
    # GOOGLE SHEETS WORKSHEETS
    # =====================================================

    sheet = spreadsheet.worksheet(
        "Requests"
    )

    engineering_sheet = spreadsheet.worksheet(
        "Data_Engineering"
    )

    # =====================================================
    # REQUEST ID
    # =====================================================

    request_id = (
        f"ENG-{datetime.now().year}-"
        f"{str(uuid.uuid4())[:8]}"
    )

    # =====================================================
    # SOURCE SYSTEMS
    # =====================================================

    st.subheader(
        "📥 Source Systems"
    )

    available_source_systems = [

        "SAP",
        "SQL Server",
        "Oracle",
        "Snowflake",
        "Excel",
        "API",
        "SharePoint",
        "Google Sheets"

    ]

    selected_source_systems = st.multiselect(

        "Select Source Systems",

        available_source_systems

    )

    custom_source_system = st.text_input(
        "Add Custom Source System"
    )

    if custom_source_system:

        selected_source_systems.append(
            custom_source_system
        )

    database_name = st.text_input(
        "Database Name"
    )

    schema_name = st.text_input(
        "Schema Name"
    )

    source_tables = st.text_area(
        "Source Tables"
    )

    # =====================================================
    # FACT TABLE
    # =====================================================

    st.subheader(
        "📊 Fact Table Information"
    )

    fact_table = st.text_input(
        "Fact Table Name"
    )

    granularity = st.selectbox(

        "Granularity",

        [

            "One row per transaction",
            "One row per customer",
            "One row per product",
            "One row per invoice",
            "One row per store",
            "Other"

        ]
    )

    transaction_date_field = st.text_input(
        "Transaction Date Field"
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    st.subheader(
        "📚 Dimensions"
    )

    available_dimensions = [

        "Customer",
        "Product",
        "Calendar",
        "Retailer",
        "Store",
        "Region",
        "Employee",
        "Supplier",
        "Brand"

    ]

    selected_dimensions = st.multiselect(

        "Select Dimensions",

        available_dimensions

    )

    custom_dimension = st.text_input(
        "Add Custom Dimension"
    )

    if custom_dimension:

        selected_dimensions.append(
            custom_dimension
        )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    st.subheader(
        "🔗 Relationships"
    )

    primary_keys = st.text_area(
        "Primary Keys"
    )

    foreign_keys = st.text_area(
        "Foreign Keys"
    )

    join_logic = st.text_area(
        "Join Logic"
    )

    # =====================================================
    # KPIs
    # =====================================================

    st.subheader(
        "📈 KPIs / Measures"
    )

    available_kpis = [

        "Sales",
        "Volume",
        "Margin",
        "Profit",
        "CSL",
        "Fill Rate",
        "Stock",
        "Availability",
        "Market Share"

    ]

    selected_kpis = st.multiselect(

        "Select KPIs",

        available_kpis

    )

    custom_kpi = st.text_input(
        "Add Custom KPI"
    )

    if custom_kpi:

        selected_kpis.append(
            custom_kpi
        )

    calculations = st.text_area(
        "Calculation Logic"
    )

    # =====================================================
    # BUSINESS RULES
    # =====================================================

    st.subheader(
        "📜 Business Rules"
    )

    business_rules = st.text_area(
        "Business Rules"
    )

    exclusion_rules = st.text_area(
        "Exclusion Rules"
    )

    # =====================================================
    # REFRESH REQUIREMENTS
    # =====================================================

    st.subheader(
        "🔄 Refresh Requirements"
    )

    refresh_frequency = st.selectbox(

        "Refresh Frequency",

        [

            "Hourly",
            "Daily",
            "Weekly",
            "Monthly",
            "Real-Time"

        ]
    )

    load_type = st.selectbox(

        "Load Type",

        [

            "Full Load",
            "Incremental Load"

        ]
    )

    historical_data_required = st.selectbox(

        "Historical Data Required?",

        [

            "Yes",
            "No"

        ]
    )

    history_years = st.number_input(

        "Years of History",

        min_value=0,
        max_value=20,
        value=3

    )

    # =====================================================
    # SECURITY
    # =====================================================

    st.subheader(
        "🔐 Security Requirements"
    )

    row_level_security = st.selectbox(

        "Row Level Security Required?",

        [

            "Yes",
            "No"

        ]
    )

    security_rules = st.text_area(
        "Security Rules"
    )

    # =====================================================
    # OUTPUT REQUIREMENTS
    # =====================================================

    st.subheader(
        "📤 Output Requirements"
    )

    output_tools = st.multiselect(

        "Output Tools",

        [

            "Power BI",
            "Pyramid",
            "Excel",
            "API",
            "CSV",
            "Google Sheets"

        ]
    )

    export_required = st.selectbox(

        "Export Required?",

        [

            "Yes",
            "No"

        ]
    )

    # =====================================================
    # MODEL DESIGN
    # =====================================================

    st.subheader(
        "🏗️ Model Design"
    )

    model_type = st.selectbox(

        "Model Type",

        [

            "Star Schema",
            "Snowflake",
            "Flat Table",
            "Data Mart"

        ]
    )

    existing_model = st.selectbox(

        "Existing Model Available?",

        [

            "Yes",
            "No"

        ]
    )

    existing_model_name = st.text_input(
        "Existing Model Name"
    )

    # =====================================================
    # PERFORMANCE
    # =====================================================

    st.subheader(
        "⚡ Performance Requirements"
    )

    expected_users = st.number_input(

        "Expected Number of Users",

        min_value=1,
        value=10

    )

    estimated_dataset_size = st.selectbox(

        "Estimated Dataset Size",

        [

            "Small",
            "Medium",
            "Large",
            "Very Large"

        ]
    )

    performance_notes = st.text_area(
        "Performance Notes"
    )

    # =====================================================
    # STATUS
    # =====================================================

    st.subheader(
        "📌 Request Status"
    )

    status = st.selectbox(

        "Status",

        [

            "New",
            "In Progress",
            "Waiting for Business",
            "In Testing",
            "Completed",
            "Blocked"

        ]
    )

    # =====================================================
    # JIRA
    # =====================================================

    st.subheader(
        "🎫 Jira Tracking"
    )

    jira_ticket = st.text_input(
        "Jira Ticket"
    )

    jira_link = st.text_input(
        "Jira Link"
    )

    # =====================================================
    # ENGINEERING NOTES
    # =====================================================

    st.subheader(
        "📝 Engineering Notes"
    )

    engineering_notes = st.text_area(
        "Engineering Notes"
    )

    # =====================================================
    # SAVE BUTTON
    # =====================================================

    submit_engineering = st.button(
        "💾 Save Engineering Requirements"
    )

    # =====================================================
    # SAVE TO GOOGLE SHEETS
    # =====================================================

    if submit_engineering:

        engineering_sheet.append_row([

            request_id,
            ", ".join(selected_source_systems),
            database_name,
            schema_name,
            source_tables,
            fact_table,
            granularity,
            transaction_date_field,
            ", ".join(selected_dimensions),
            primary_keys,
            foreign_keys,
            join_logic,
            ", ".join(selected_kpis),
            calculations,
            business_rules,
            exclusion_rules,
            refresh_frequency,
            load_type,
            historical_data_required,
            history_years,
            row_level_security,
            security_rules,
            ", ".join(output_tools),
            export_required,
            model_type,
            existing_model,
            existing_model_name,
            expected_users,
            estimated_dataset_size,
            performance_notes,
            status,
            jira_ticket,
            jira_link,
            engineering_notes

        ])

        st.success(
            "✅ Engineering Requirements Saved Successfully"
        )

