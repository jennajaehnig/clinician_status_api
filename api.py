from email_helper import send_email
from geolocation_helper import clinician_out_of_range
import requests
import time
import threading

url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"
MAX_QUERIES = 100  # Maximum number of queries per second
NUM_CLINICIANS = 6  # Number of clinicians to ping

active_clinicians = set()

def ping_clinician(clinician_id):
    """
    This function pings the clinician every 3.75 seconds for the specified clinician_id.
    If the clinician is out of range, it sends an email notification and waits for 5 minutes before checking again.
    If the clinician is in range, it continues to ping every 3.75 seconds.
    """
    global active_clinicians
    while True:
        # We don't want more than 100 queries per second and we have 6 clinicians so each clinician can
        # ping ~16 times per minute which is every 3.75 seconds
        # We also want to make sure we are pinged within 5 minutes
        start = time.time()
        in_range = get_clinician_status(clinician_id)
        end = time.time()
        if not in_range:
            active_clinicians.remove(clinician_id)
            time.sleep(5 * 60)  # Wait for 5 minutes before checking again
            active_clinicians.add(clinician_id)
            continue
        time_taken = end - start
        # print(f"Time taken for all queries: {time_taken} seconds")
        # interval = 5 - time_taken
        # interval = min(5 * 60 - time_taken, (60 - time_taken)/(MAX_QUERIES//NUM_CLINICIANS))
        # print(f"interval: {interval} seconds")
        interval = 3.75
        time.sleep(interval)  # Wait for time_interval seconds before checking again

def get_clinician_status(clinician_id):
    """
    This function sends a GET request to the clinician status API for the specified clinician_id.
    If the clinician_id is out of range, it sends an email notification and returns False.
    If the clinician_id is valid and the API call is successful, it returns True.
    """
    if (clinician_id < 1 or clinician_id > 7):
        print(f"Invalid clinician_id: {clinician_id}. The clinician_id must be between 1 and 6.")
        return
    response = requests.get(f"{url}/clinicianstatus/{clinician_id}")
    if response.status_code == 200:
        data = response.json()
        # print(f"Success: {data}")
        # if clinician_id out of range, send email
        out_of_range = clinician_out_of_range(clinician_id, data)
        if out_of_range:
            send_email(clinician_id, "out_of_range")
            return False
        else:
            return True
    else:
        print(f"Error fetching clinician status for {clinician_id}: {response.status_code} - {response.text}")
        send_email(clinician_id, "error", response.text)
        return False


def __main__():
    for clinician_id in range(1, NUM_CLINICIANS + 1):
        active_clinicians.add(clinician_id)

    threads = []

    for clinician_id in range(1, NUM_CLINICIANS + 1):
        thread = threading.Thread(target=ping_clinician, args=(clinician_id,))
        threads.append(thread)
        thread.start()
    
if __name__ == "__main__":
    __main__()