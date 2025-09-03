"""
Application configuration settings
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Jagriti API Configuration
    JAGRITI_BASE_URL: str = "https://e-jagriti.gov.in"
    JAGRITI_TIMEOUT: int = 30
    
    # API Configuration
    API_TITLE: str = "Jagriti Consumer Court API"
    API_VERSION: str = "1.0.0"
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    
    # Request Configuration
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    # Date Configuration (default date range)
    DEFAULT_FROM_DATE: str = "2025-01-01"
    DEFAULT_TO_DATE: str = "2025-09-03"
    
    # Search Configuration
    DATE_REQUEST_TYPE: int = 1  # Case Filing Date
    ORDER_TYPE: int = 1  # Daily Orders only
    JUDGE_ID: str = ""  # Empty for all judges
    
    # Headers for Jagriti API requests
    @property
    def JAGRITI_HEADERS(self) -> dict:
        return {
            "Accept": "application/json",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DNT": "1",
            "Origin": self.JAGRITI_BASE_URL,
            "Referer": f"{self.JAGRITI_BASE_URL}/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"'
        }
    
    # Jagriti API Endpoints
    @property
    def ENDPOINTS(self) -> dict:
        return {
            "states_commissions": f"{self.JAGRITI_BASE_URL}/services/report/report/getStateCommissionAndCircuitBench",
            "district_commissions": f"{self.JAGRITI_BASE_URL}/services/report/report/getDistrictCommissionByCommissionId",
            "case_search": f"{self.JAGRITI_BASE_URL}/services/case/caseFilingService/v2/getCaseDetailsBySearchType"
        }
    
    # Search type mappings
    SEARCH_TYPES = {
        "case_number": 1,
        "complainant": 2,
        "respondent": 3,
        "complainant_advocate": 4,
        "respondent_advocate": 5,
        "industry_type": 6,
        "judge": 7
    }

# Global settings instance
settings = Settings()
