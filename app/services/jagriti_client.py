"""
Jagriti API Client
Handles HTTP requests to the Jagriti portal API endpoints
"""

import logging
import asyncio
from typing import Dict, List, Optional
import httpx
from app.config import settings
from app.models.jagriti import (
    JagritiStatesResponse,
    JagritiDistrictCommissionsResponse, 
    JagritiCaseSearchResponse,
    JagritiCaseSearchRequest
)

logger = logging.getLogger(__name__)

class JagritiAPIException(Exception):
    """Custom exception for Jagriti API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class JagritiAPIClient:
    """Client for interacting with Jagriti API endpoints"""
    
    def __init__(self):
        self.base_url = settings.JAGRITI_BASE_URL
        self.timeout = settings.REQUEST_TIMEOUT
        self.max_retries = settings.MAX_RETRIES
        self.headers = settings.JAGRITI_HEADERS
        
    async def _make_request(self, method: str, url: str, data: Optional[dict] = None, params: Optional[dict] = None) -> dict:
        """Make HTTP request with retry logic and error handling"""
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    logger.info(f"Making {method} request to {url} (attempt {attempt + 1})")
                    
                    if method.upper() == "GET":
                        response = await client.get(url, headers=self.headers, params=params)
                    else:
                        response = await client.post(url, headers=self.headers, json=data)
                    
                    # Log response details
                    logger.info(f"Response status: {response.status_code}")
                    
                    # Check for HTTP errors
                    response.raise_for_status()
                    
                    # Parse JSON response
                    response_data = response.json()
                    logger.debug(f"Response data: {response_data}")
                    
                    return response_data
                    
                except httpx.TimeoutException as e:
                    logger.warning(f"Timeout on attempt {attempt + 1}: {str(e)}")
                    if attempt == self.max_retries - 1:
                        raise JagritiAPIException(f"Request timed out after {self.max_retries} attempts")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                    raise JagritiAPIException(
                        f"HTTP {e.response.status_code} error: {e.response.text}",
                        status_code=e.response.status_code,
                        response_data=e.response.json() if e.response.content else None
                    )
                    
                except httpx.RequestError as e:
                    logger.error(f"Request error on attempt {attempt + 1}: {str(e)}")
                    if attempt == self.max_retries - 1:
                        raise JagritiAPIException(f"Request failed after {self.max_retries} attempts: {str(e)}")
                    await asyncio.sleep(2 ** attempt)
                    
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")
                    raise JagritiAPIException(f"Unexpected error: {str(e)}")
    
    async def get_states_and_commissions(self) -> JagritiStatesResponse:
        """Get all states and their commission IDs"""
        try:
            url = settings.ENDPOINTS["states_commissions"]
            response_data = await self._make_request("GET", url)
            return JagritiStatesResponse(**response_data)
        except Exception as e:
            logger.error(f"Error fetching states and commissions: {str(e)}")
            raise JagritiAPIException(f"Failed to fetch states and commissions: {str(e)}")
    
    async def get_district_commissions(self, state_commission_id: int) -> JagritiDistrictCommissionsResponse:
        """Get district commissions for a given state commission ID"""
        try:
            url = settings.ENDPOINTS["district_commissions"]
            params = {"commissionId": state_commission_id}
            response_data = await self._make_request("GET", url, params=params)
            return JagritiDistrictCommissionsResponse(**response_data)
        except Exception as e:
            logger.error(f"Error fetching district commissions for state {state_commission_id}: {str(e)}")
            raise JagritiAPIException(f"Failed to fetch district commissions: {str(e)}")
    
    async def search_cases(self, search_request: JagritiCaseSearchRequest) -> JagritiCaseSearchResponse:
        """Search cases using the provided search criteria"""
        try:
            url = settings.ENDPOINTS["case_search"]
            request_data = search_request.dict()
            logger.info(f"Searching cases with criteria: {request_data}")
            response_data = await self._make_request("POST", url, data=request_data)
            return JagritiCaseSearchResponse(**response_data)
        except Exception as e:
            logger.error(f"Error searching cases: {str(e)}")
            raise JagritiAPIException(f"Failed to search cases: {str(e)}")
    
    async def find_state_commission_id(self, state_name: str) -> Optional[int]:
        """Find commission ID for a given state name"""
        try:
            states_response = await self.get_states_and_commissions()
            state_name_upper = state_name.upper()
            
            for state in states_response.data:
                if state.commissionNameEn.upper() == state_name_upper:
                    logger.info(f"Found commission ID {state.commissionId} for state {state_name}")
                    return state.commissionId
            
            logger.warning(f"State '{state_name}' not found")
            return None
            
        except Exception as e:
            logger.error(f"Error finding state commission ID for '{state_name}': {str(e)}")
            raise JagritiAPIException(f"Failed to find state commission ID: {str(e)}")
    
    async def find_district_commission_id(self, state_commission_id: int, district_name: str) -> Optional[int]:
        """Find district commission ID for a given state and district name"""
        try:
            districts_response = await self.get_district_commissions(state_commission_id)
            
            for district in districts_response.data:
                if district.commissionNameEn.lower() == district_name.lower():
                    logger.info(f"Found district commission ID {district.commissionId} for district {district_name}")
                    return district.commissionId
            
            logger.warning(f"District '{district_name}' not found in state commission {state_commission_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error finding district commission ID for '{district_name}': {str(e)}")
            raise JagritiAPIException(f"Failed to find district commission ID: {str(e)}")
    
    async def get_state_name_by_id(self, state_commission_id: int) -> Optional[str]:
        """Get state name by commission ID"""
        try:
            states_response = await self.get_states_and_commissions()
            
            for state in states_response.data:
                if state.commissionId == state_commission_id:
                    return state.commissionNameEn
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding state name for ID {state_commission_id}: {str(e)}")
            raise JagritiAPIException(f"Failed to find state name: {str(e)}")

# Global client instance
jagriti_client = JagritiAPIClient()
