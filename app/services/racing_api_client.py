# app/services/

import os
import time

import requests
from dotenv import load_dotenv
from app.core.logging import logger
from requests.auth import HTTPBasicAuth

load_dotenv()


class RacingAPIClient:
    def __init__(self):
        self.username = os.environ.get("RACING_API_USERNAME")
        self.password = os.environ.get("RACING_API_PASSWORD")
        self.base_url = os.environ.get("RACING_API_BASE_URL", "https://api.theracingapi.com/v1")
        
        if not all([self.username, self.password, self.base_url]):
            raise ValueError("Missing required Racing API credentials or base URL.")
        
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.username, self.password)
        self.session.headers.update({"Accept": "application/json"})
        
        self.request_delay = 0.5  # seconds

    def _request_get(self, endpoint: str, params: dict = None, retries: int = 3):
        """Generic GET request with basic retry logic and rate limiting."""
        url = f"{self.base_url}{endpoint}"
        attempt = 0

        while attempt < retries:
            try:
                logger.info(f"Requesting URL: {url} with params: {params}")
                response = self.session.get(url, params=params, timeout=10)
                if response.status_code == 429:
                    # Too Many Requests: wait and retry
                    wait_time = int(response.headers.get("Retry-After", 1))
                    logger.warning(f"Rate limit hit. Sleeping for {wait_time} seconds.")
                    time.sleep(wait_time)
                    attempt += 1
                    continue

                response.raise_for_status()
                time.sleep(self.request_delay)  # simple rate limiting
                return response.json()

            except requests.RequestException as e:
                logger.error(f"Request error on {url}: {e}")
                attempt += 1
                time.sleep(1)
        raise Exception(f"Failed to GET {url} after {retries} attempts.")

    # -------------------------------
    # Courses & Regions Endpoints
    # -------------------------------
    def list_courses(self, params: dict = None):
        return self._request_get("/courses", params)

    def list_regions(self, params: dict = None):
        return self._request_get("/courses/regions", params)

    # -------------------------------
    # Dams Endpoints
    # -------------------------------
    def search_dams(self, name: str, params: dict = None):
        params = params or {}
        params['name'] = name
        return self._request_get("/dams/search", params)

    def dam_results(self, dam_id: str, params: dict = None):
        endpoint = f"/dams/{dam_id}/results"
        return self._request_get(endpoint, params)

    def dam_class_analysis(self, dam_id: str, params: dict = None):
        endpoint = f"/dams/{dam_id}/analysis/classes"
        return self._request_get(endpoint, params)

    def dam_distance_analysis(self, dam_id: str, params: dict = None):
        endpoint = f"/dams/{dam_id}/analysis/distances"
        return self._request_get(endpoint, params)

    # -------------------------------
    # Damsires Endpoints
    # -------------------------------
    def search_damsires(self, name: str, params: dict = None):
        params = params or {}
        params['name'] = name
        return self._request_get("/damsires/search", params)

    def damsire_results(self, damsire_id: str, params: dict = None):
        endpoint = f"/damsires/{damsire_id}/results"
        return self._request_get(endpoint, params)

    def damsire_class_analysis(self, damsire_id: str, params: dict = None):
        endpoint = f"/damsires/{damsire_id}/analysis/classes"
        return self._request_get(endpoint, params)

    def damsire_distance_analysis(self, damsire_id: str, params: dict = None):
        endpoint = f"/damsires/{damsire_id}/analysis/distances"
        return self._request_get(endpoint, params)

    # -------------------------------
    # Horses Endpoints
    # -------------------------------
    def search_horses(self, name: str, params: dict = None):
        params = params or {}
        params['name'] = name
        return self._request_get("/horses/search", params)

    def horse_results(self, horse_id: str, params: dict = None):
        endpoint = f"/horses/{horse_id}/results"
        return self._request_get(endpoint, params)

    def horse_distance_time_analysis(self, horse_id: str, params: dict = None):
        endpoint = f"/horses/{horse_id}/analysis/distance-times"
        return self._request_get(endpoint, params)

    def horse_standard(self, horse_id: str):
        endpoint = f"/horses/{horse_id}/standard"
        return self._request_get(endpoint)

    def horse_pro(self, horse_id: str):
        endpoint = f"/horses/{horse_id}/pro"
        return self._request_get(endpoint)

    # -------------------------------
    # Jockeys Endpoints
    # -------------------------------
    def search_jockeys(self, name: str, params: dict = None):
        params = params or {}
        params['name'] = name
        return self._request_get("/jockeys/search", params)

    def jockey_results(self, jockey_id: str, params: dict = None):
        endpoint = f"/jockeys/{jockey_id}/results"
        return self._request_get(endpoint, params)

    def jockey_course_analysis(self, jockey_id: str, params: dict = None):
        endpoint = f"/jockeys/{jockey_id}/analysis/courses"
        return self._request_get(endpoint, params)

    def jockey_distance_analysis(self, jockey_id: str, params: dict = None):
        endpoint = f"/jockeys/{jockey_id}/analysis/distances"
        return self._request_get(endpoint, params)

    def jockey_owner_analysis(self, jockey_id: str, params: dict = None):
        endpoint = f"/jockeys/{jockey_id}/analysis/owners"
        return self._request_get(endpoint, params)

    def jockey_trainer_analysis(self, jockey_id: str, params: dict = None):
        endpoint = f"/jockeys/{jockey_id}/analysis/trainers"
        return self._request_get(endpoint, params)

    # -------------------------------
    # Owners Endpoints
    # -------------------------------
    def search_owners(self, name: str, params: dict = None):
        params = params or {}
        params['name'] = name
        return self._request_get("/owners/search", params)

    def owner_results(self, owner_id: str, params: dict = None):
        endpoint = f"/owners/{owner_id}/results"
        return self._request_get(endpoint, params)

    def owner_course_analysis(self, owner_id: str, params: dict = None):
        endpoint = f"/owners/{owner_id}/analysis/courses"
        return self._request_get(endpoint, params)

    def owner_distance_analysis(self, owner_id: str, params: dict = None):
        endpoint = f"/owners/{owner_id}/analysis/distances"
        return self._request_get(endpoint, params)

    def owner_jockey_analysis(self, owner_id: str, params: dict = None):
        endpoint = f"/owners/{owner_id}/analysis/jockeys"
        return self._request_get(endpoint, params)

    def owner_trainer_analysis(self, owner_id: str, params: dict = None):
        endpoint = f"/owners/{owner_id}/analysis/trainers"
        return self._request_get(endpoint, params)

    # -------------------------------
    # Sires Endpoints
    # -------------------------------
    def search_sires(self, name: str, params: dict = None):
        params = params or {}
        params['name'] = name
        return self._request_get("/sires/search", params)

    def sire_results(self, sire_id: str, params: dict = None):
        endpoint = f"/sires/{sire_id}/results"
        return self._request_get(endpoint, params)

    def sire_class_analysis(self, sire_id: str, params: dict = None):
        endpoint = f"/sires/{sire_id}/analysis/classes"
        return self._request_get(endpoint, params)

    def sire_distance_analysis(self, sire_id: str, params: dict = None):
        endpoint = f"/sires/{sire_id}/analysis/distances"
        return self._request_get(endpoint, params)

    # -------------------------------
    # Trainers Endpoints
    # -------------------------------
    def search_trainers(self, name: str, params: dict = None):
        params = params or {}
        params['name'] = name
        return self._request_get("/trainers/search", params)

    def trainer_results(self, trainer_id: str, params: dict = None):
        endpoint = f"/trainers/{trainer_id}/results"
        return self._request_get(endpoint, params)

    def trainer_horse_age_analysis(self, trainer_id: str, params: dict = None):
        endpoint = f"/trainers/{trainer_id}/analysis/horse-age"
        return self._request_get(endpoint, params)

    def trainer_course_analysis(self, trainer_id: str, params: dict = None):
        endpoint = f"/trainers/{trainer_id}/analysis/courses"
        return self._request_get(endpoint, params)

    def trainer_distance_analysis(self, trainer_id: str, params: dict = None):
        endpoint = f"/trainers/{trainer_id}/analysis/distances"
        return self._request_get(endpoint, params)

    def trainer_jockey_analysis(self, trainer_id: str, params: dict = None):
        endpoint = f"/trainers/{trainer_id}/analysis/jockeys"
        return self._request_get(endpoint, params)

    def trainer_owner_analysis(self, trainer_id: str, params: dict = None):
        endpoint = f"/trainers/{trainer_id}/analysis/owners"
        return self._request_get(endpoint, params)

    # -------------------------------
    # Racecards Endpoints
    # -------------------------------
    def racecards_free(self, params: dict = None):
        return self._request_get("/racecards/free", params)

    def racecards_basic(self, params: dict = None):
        return self._request_get("/racecards/basic", params)

    def racecards_standard(self, params: dict = None):
        return self._request_get("/racecards/standard", params)

    def racecards_pro(self, params: dict = None):
        return self._request_get("/racecards/pro", params)

    def racecards_big_races(self, params: dict = None):
        return self._request_get("/racecards/big-races", params)

    def racecards_summaries(self, params: dict = None):
        return self._request_get("/racecards/summaries", params)

    def racecard_horse_results(self, horse_id: str, params: dict = None):
        endpoint = f"/racecards/{horse_id}/results"
        return self._request_get(endpoint, params)

    def race_standard(self, race_id: str):
        endpoint = f"/racecards/{race_id}/standard"
        return self._request_get(endpoint)

    def race_pro(self, race_id: str):
        endpoint = f"/racecards/{race_id}/pro"
        return self._request_get(endpoint)

    # -------------------------------
    # Results Endpoints
    # -------------------------------
    def list_results(self, params: dict = None):
        return self._request_get("/results", params)

    def results_today(self, params: dict = None):
        return self._request_get("/results/today", params)

    def result(self, race_id: str):
        endpoint = f"/results/{race_id}"
        return self._request_get(endpoint)

    # -------------------------------
    # North America Regional Endpoints
    # -------------------------------
    def list_north_america_meets(self, params: dict = None):
        return self._request_get("/north-america/meets", params)

    def meet_entries(self, meet_id: str):
        endpoint = f"/north-america/meets/{meet_id}/entries"
        return self._request_get(endpoint)

    def meet_results(self, meet_id: str):
        endpoint = f"/north-america/meets/{meet_id}/results"
        return self._request_get(endpoint)