import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Report Configuration Request Portal",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("📊 Report Configuration Request Portal")
st.markdown("Capture report setup requirements for Report Developers.")

st.divider()

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
# SIDEBAR
# =========================================================

st.sidebar.header("📌 Request Information")

report_name = st.sidebar.text_input("Report Name")

client_name = st.sidebar.text_input("Client Name")

business_unit = st.sidebar.text_input("Business Unit")

requested_by = st.sidebar.text_input("Requested By")

priority = st.sidebar.selectbox(
    "Priority",
    ["High", "Medium", "Low"]
)

date_required = st.sidebar.date_input("Date Required")

report_purpose = st.sidebar.text_area(
    "Report Purpose"
)

# =========================================================
# MAIN TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Filters",
    "⚙ Runtime Actions",
    "🖥 Presentation",
    "📝 Notes & Attachments"
])

# =========================================================
# TAB 1 - FILTERS
# =========================================================

with tab1:

    st.subheader("Filters To Be Included")

    selected_filters = st.multiselect(
        "Select Filters",
        filters
    )

    st.markdown("### Selected Filters")

    if selected_filters:
        for item in selected_filters:
            st.success(item)
    else:
        st.info("No filters selected.")

# =========================================================
# TAB 2 - RUNTIME ACTIONS
# =========================================================

with tab2:

    st.subheader("Query Context Actions")

    selected_query_actions = []

    col1, col2, col3 = st.columns(3)

    for i, action in enumerate(query_actions):

        if i % 3 == 0:
            if col1.checkbox(action, key=f"query_{i}"):
                selected_query_actions.append(action)

        elif i % 3 == 1:
            if col2.checkbox(action, key=f"query_{i}"):
                selected_query_actions.append(action)

        else:
            if col3.checkbox(action, key=f"query_{i}"):
                selected_query_actions.append(action)

    st.divider()

    st.subheader("Report Meta Actions")

    selected_meta_actions = []

    col4, col5, col6 = st.columns(3)

    for i, action in enumerate(meta_actions):

        if i % 3 == 0:
            if col4.checkbox(action, key=f"meta_{i}"):
                selected_meta_actions.append(action)

        elif i % 3 == 1:
            if col5.checkbox(action, key=f"meta_{i}"):
                selected_meta_actions.append(action)

        else:
            if col6.checkbox(action, key=f"meta_{i}"):
                selected_meta_actions.append(action)

# =========================================================
# TAB 3 - PRESENTATION
# =========================================================

with tab3:

    st.subheader("Presentation Options")

    selected_presentation_actions = []

    col7, col8, col9 = st.columns(3)

    for i, action in enumerate(presentation_actions):

        if i % 3 == 0:
            if col7.checkbox(action, key=f"presentation_{i}"):
                selected_presentation_actions.append(action)

        elif i % 3 == 1:
            if col8.checkbox(action, key=f"presentation_{i}"):
                selected_presentation_actions.append(action)

        else:
            if col9.checkbox(action, key=f"presentation_{i}"):
                selected_presentation_actions.append(action)

# =========================================================
# TAB 4 - NOTES
# =========================================================

with tab4:

    st.subheader("Additional Requirements")

    additional_notes = st.text_area(
        "Business Rules / Calculations / Notes",
        height=200
    )

    uploaded_file = st.file_uploader(
        "Upload Supporting Documents",
        type=["xlsx", "csv", "png", "jpg", "pdf"]
    )

# =========================================================
# SUBMIT BUTTON
# =========================================================

st.divider()

if st.button("🚀 Submit Request", use_container_width=True):

    request_id = f"RPT-{datetime.now().year}-{str(uuid.uuid4())[:8]}"

    request_data = {
        "Request ID": request_id,
        "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Report Name": report_name,
        "Client Name": client_name,
        "Business Unit": business_unit,
        "Requested By": requested_by,
        "Priority": priority,
        "Date Required": str(date_required),
        "Report Purpose": report_purpose,
        "Filters": ", ".join(selected_filters),
        "Query Actions": ", ".join(selected_query_actions),
        "Meta Actions": ", ".join(selected_meta_actions),
        "Presentation Actions": ", ".join(selected_presentation_actions),
        "Additional Notes": additional_notes
    }

    df = pd.DataFrame([request_data])

    # SAVE TO CSV
    try:

        existing_df = pd.read_csv("report_requests.csv")

        updated_df = pd.concat([existing_df, df], ignore_index=True)

        updated_df.to_csv("report_requests.csv", index=False)

    except FileNotFoundError:

        df.to_csv("report_requests.csv", index=False)

    st.success("✅ Request Submitted Successfully!")

    st.info(f"Request ID: {request_id}")

    st.subheader("Submitted Information")

    st.dataframe(df, use_container_width=True)

    # OPTIONAL FILE SAVE
    if uploaded_file is not None:

        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("📎 Attachment Uploaded Successfully")
