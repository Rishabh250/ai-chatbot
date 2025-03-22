import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_API = os.getenv("BASE_API")

class LeadDataCollector:
    def __init__(self):
        self.lead_data = {}
        self.lead_id = None

    def update_data(self, new_data: dict):
        """
        Update in-memory lead data with new values, if not already set.
        """
        for k, v in new_data.items():
            if v and not self.lead_data.get(k):
                self.lead_data[k] = v.strip() if isinstance(v, str) else v

    def is_ready(self):
        """
        Check if all required fields are present and not empty.
        """
        required_fields = ['firstName', 'lastName', 'email', 'phone', 'leadSource']
        return all(self.lead_data.get(field) for field in required_fields)

    def get_missing_fields(self):
        """
        Return a list of missing required fields.
        """
        required_fields = ['firstName', 'lastName', 'email', 'phone', 'leadSource']
        return [field for field in required_fields if not self.lead_data.get(field)]


    def submit(self):
        """
        Submit lead data to the backend once all required fields are collected.
        Returns the leadId if successful, None otherwise.
        """
        if not self.is_ready():
            print("[LeadDataCollector] Cannot submit - missing fields:", self.get_missing_fields())
            return None

        try:
            print("[LeadDataCollector] Submitting lead data:", self.lead_data)
            response = requests.post(f"{BASE_API}/admin/message", json=self.lead_data, timeout=50)
            response.raise_for_status()

            if (response.status_code == 201):
                lead_id = response.headers.get("public-id")
                print(f"[LeadDataCollector] Lead created with ID: {lead_id}")
                return lead_id
            else:
                print(f"[LeadDataCollector] Failed to submit lead: {response.json()}")
                return None

        except requests.RequestException as e:
            print(f"[LeadDataCollector] Failed to submit lead: {e}")
            return None
