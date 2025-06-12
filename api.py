from email_helper import send_email
from geolocation_helper import clinician_out_of_range
import requests
import time

url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"
MAX_QUERIES = 100  # Maximum number of queries per second
NUM_CLINICIANS = 6  # Number of clinicians to ping

def ping_all_clinicians():
    while True:
        # We don't want more than 100 queries per second and we have 6 clinicians so each clinician can
        # ping ~16 times per minute which is every 3.75 seconds
        # We also want to make sure we are pinged within 5 minutes
        start = time.time()
        for clinician_id in range(1, 7):
            get_clinician_status(clinician_id)
        end = time.time()
        time_taken = end - start
        print(f"Time taken for all queries: {time_taken} seconds")
        interval = min(60 - time_taken, (60 - time_taken)/(MAX_QUERIES//NUM_CLINICIANS))
        print(f"interval: {interval} seconds")
        time.sleep(interval)  # Wait for time_interval seconds before checking again

def get_clinician_status(clinician_id):
    if (clinician_id < 1 or clinician_id > 7):
        print(f"Invalid clinician_id: {clinician_id}. The clinician_id must be between 1 and 6.")
        return
    try:
        response = requests.get(f"{url}/clinicianstatus/{clinician_id}")
        data = response.json()
        # print(f"Success: {data}")
        # if clinician_id out of range, send email
        if clinician_out_of_range(clinician_id, data):
            send_email(clinician_id, "out_of_range")
    except Exception as error:
        print(f"Error fetching clinician status: {error}")
        send_email(clinician_id, "error", error)

def __main__():
    try:
        ping_all_clinicians()
    except Exception as e:
        print(f"Error in pinging clinicians: {e}")
    
if __name__ == "__main__":
    __main__()