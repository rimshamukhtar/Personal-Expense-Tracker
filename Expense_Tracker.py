import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# ✅ Move this line to the top (Fix for error)
st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="centered")

# Initialize session state for expenses if not exists
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Custom Styling
st.markdown("""
    <style>
        .main {
            background-color: #E4EFE7;
        }
        .stApp {
            background: linear-gradient(to right, #e6e9f0  ,  #5C7285);


;
;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
        .stSidebar {
            background: linear-gradient(to right, #e6e9f0  ,  #5C7285);
            padding: 15px;
            border-right: 2px solid #ddd;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        .stButton button {
            background-color: #213555 !important;
            color: white !important;
            border-radius: 5px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Expense Tracker App UI
st.title("💸 Personal Expense Tracker")

# Sidebar for adding expenses
st.sidebar.header("➕ Add New Expense")
date = st.sidebar.date_input("Select Date", datetime.date.today())
category = st.sidebar.selectbox("Category", ["Food", "Shopping", "Bills", "Travel", "Entertainment", "Other"])
amount = st.sidebar.number_input("Amount ($)", min_value=0.01, step=0.01)
description = st.sidebar.text_input("Description", "")

if st.sidebar.button("Add Expense"):
    if amount and description:
        st.session_state.expenses.append({"Date": date, "Category": category, "Amount": amount, "Description": description})
        st.sidebar.success("✅ Expense added successfully!")
    else:
        st.sidebar.error("❌ Please fill all fields.")

# Display expenses as a DataFrame
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.subheader("📋 Expense List")
    st.dataframe(df, use_container_width=True)

    # Expense Summary
    st.subheader("📊 Expense Summary")
    total_expense = df["Amount"].sum()
    st.metric("Total Expenses", f"${total_expense:.2f}")
    
    # Visualization
    fig = px.pie(df, values='Amount', names='Category', title='Category-wise Expense Distribution', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)
    
    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download CSV", data=csv, file_name="expenses.csv", mime="text/csv", key="download-csv")
else:
    st.info("ℹ️ No expenses added yet. Start by adding a new expense from the sidebar!")


