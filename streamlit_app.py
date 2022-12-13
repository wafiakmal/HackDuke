import streamlit as st
import streamlit.components.v1 as components
from createdb import query


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        userquery = f"SELECT user_name, password FROM customers_db where user_name = '{st.session_state['username']}';"
        results = query(userquery)
        passwords = {eachLine[0]: eachLine[1] for eachLine in results}
        if (
            (st.session_state["username"] in passwords.keys())
            and (st.session_state["password"]
            == passwords[st.session_state["username"]])
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            # del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        with st.form("sign-in1"):
            # First run, show inputs for username + password.
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                password_entered()
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        with st.form("sign-in2"):
            # First run, show inputs for username + password.
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                password_entered()
    else:
        # Password correct.
        return True

st.title("Cup Adventure")
st.write(st.session_state)
if check_password():
    if "user info" not in st.session_state:
        userquery = f"SELECT customer_firstName, user_name, customer_status FROM customers_db where user_name = '{st.session_state['username']}';"
        results = query(userquery)
        userInfo = {'firstName': results[0][0], 'username': results[0][1], 'status': results[0][2]}
        st.session_state['user info'] = userInfo
    if "user info" in st.session_state:
        st.write(f"Welcome {st.session_state['user info']['firstName']}")
        while st.session_state['user info']['status'] != "Borrowed":
            if st.session_state['user info']['status'] == "Available":
            st.write("If you would like to rent a cup, please use the dropdown below.")
            with st.form("rental"):
                # First run, show inputs for username + password.
                st.selectbox("Please select a vendor", ["Starbucks", "Beyu"])
                st.selectbox("Please select a cup", ["Cup 1", "Cup 2"])
                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
                st.write(submitted)
                if submitted:
                    st.write("Thank you for renting your cup.")
            elif st.session_state['user info']['status'] == None:
                st.write("Use the dropdown below to rent your first cup.")
                with st.form("first_rental"):
                    # First run, show inputs for username + password.
                    st.selectbox("Please select a vendor", ["Starbucks", "Beyu"])
                    st.selectbox("Please select a cup", ["Cup 1", "Cup 2"])
                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    # st.write(submitted)
                    if submitted:
                        # cup_rental()
                        st.write("Thank you for renting your cup.")
            else:
                st.write("There has been an error tracking your last cup.  Please contact us for help.")
        if st.session_state['user info']['status'] == "Borrowed":
            st.write("You currently have a cup borrowed.  Please return your cup when you are finished with it.")

def cup_rental():
    st.write("Thank you for renting your cup.")



