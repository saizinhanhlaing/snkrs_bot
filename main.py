from utils.session_check import is_session_valid
from monitor import fetch_snkrs_drops
from login import manual_login_and_save_session
from join_draw import simulate_join_draw

if __name__ == "__main__":
    #fetch_snkrs_drops()
    #manual_login_and_save_session()
    if is_session_valid():
        print("✅ Session is still valid!")
        simulate_join_draw("https://www.nike.com/launch/t/air-jordan-1-grey")
    else:
        print("❌ Session expired. Please re-login and export cookies again.")

