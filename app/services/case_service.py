"""
Case Search Service
Business logic for case search operations
"""

import logging
from typing import List, Optional
from app.config import settings
from app.services.jagriti_client import jagriti_client, JagritiAPIException
from app.models.requests import CaseSearchRequest
from app.models.responses import CaseResponse, CaseSearchResponse
from app.models.jagriti import JagritiCaseSearchRequest, JagritiCaseDetail

logger = logging.getLogger(__name__)

class CaseServiceException(Exception):
    """Custom exception for case service errors"""
    pass

class CaseService:
    """Service for handling case search operations"""
    
    def __init__(self):
        self.client = jagriti_client
    
    async def search_cases_by_type(self, request: CaseSearchRequest, search_type: int) -> CaseSearchResponse:
        """Search cases by the specified search type"""
        try:
            # Find state commission ID
            state_commission_id = await self.client.find_state_commission_id(request.state)
            if not state_commission_id:
                raise CaseServiceException(f"State '{request.state}' not found")
            
            # Find district commission ID
            district_commission_id = await self.client.find_district_commission_id(
                state_commission_id, request.commission
            )
            if not district_commission_id:
                raise CaseServiceException(f"Commission '{request.commission}' not found in state '{request.state}'")
            
            # Set default dates if not provided
            from_date = request.from_date or settings.DEFAULT_FROM_DATE
            to_date = request.to_date or settings.DEFAULT_TO_DATE
            
            # Create Jagriti API request
            jagriti_request = JagritiCaseSearchRequest(
                commissionId=district_commission_id,
                dateRequestType=settings.DATE_REQUEST_TYPE,
                fromDate=from_date,
                toDate=to_date,
                judgeId=settings.JUDGE_ID,
                orderType=settings.ORDER_TYPE,
                serchType=search_type,
                serchTypeValue=request.search_value
            )
            
            # Search cases
            jagriti_response = await self.client.search_cases(jagriti_request)
            
            # Transform response
            cases = [self._transform_case_detail(case_detail) for case_detail in jagriti_response.data]
            
            search_criteria = {
                "state": request.state,
                "commission": request.commission,
                "search_value": request.search_value,
                "search_type": search_type,
                "from_date": from_date,
                "to_date": to_date,
                "state_commission_id": state_commission_id,
                "district_commission_id": district_commission_id
            }
            
            return CaseSearchResponse(
                cases=cases,
                total_count=len(cases),
                search_criteria=search_criteria
            )
            
        except JagritiAPIException as e:
            logger.error(f"Jagriti API error in case search: {str(e)}")
            raise CaseServiceException(f"External API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in case search: {str(e)}")
            raise CaseServiceException(f"Case search failed: {str(e)}")
    
    def _transform_case_detail(self, jagriti_case: JagritiCaseDetail) -> CaseResponse:
        """Transform Jagriti case detail to our response format"""
        try:
            # Generate document link if orderDocumentPath exists
            document_link = None
            if jagriti_case.orderDocumentPath:
                document_link = f"{settings.JAGRITI_BASE_URL}{jagriti_case.orderDocumentPath}"
            
            return CaseResponse(
                case_number=jagriti_case.caseNumber,
                case_stage=jagriti_case.caseStageName,
                filing_date=jagriti_case.caseFilingDate,
                complainant=jagriti_case.complainantName,
                complainant_advocate=jagriti_case.complainantAdvocateName,
                respondent=jagriti_case.respondentName,
                respondent_advocate=jagriti_case.respondentAdvocateName,
                document_link=document_link
            )
        except Exception as e:
            logger.error(f"Error transforming case detail: {str(e)}")
            raise CaseServiceException(f"Failed to transform case data: {str(e)}")
    
    async def search_cases_by_case_number(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by case number"""
        return await self.search_cases_by_type(request, settings.SEARCH_TYPES["case_number"])
    
    async def search_cases_by_complainant(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by complainant name"""
        return await self.search_cases_by_type(request, settings.SEARCH_TYPES["complainant"])
    
    async def search_cases_by_respondent(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by respondent name"""
        return await self.search_cases_by_type(request, settings.SEARCH_TYPES["respondent"])
    
    async def search_cases_by_complainant_advocate(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by complainant advocate name"""
        return await self.search_cases_by_type(request, settings.SEARCH_TYPES["complainant_advocate"])
    
    async def search_cases_by_respondent_advocate(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by respondent advocate name"""
        return await self.search_cases_by_type(request, settings.SEARCH_TYPES["respondent_advocate"])
    
    async def search_cases_by_industry_type(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by industry type"""
        return await self.search_cases_by_type(request, settings.SEARCH_TYPES["industry_type"])
    
    async def search_cases_by_judge(self, request: CaseSearchRequest) -> CaseSearchResponse:
        """Search cases by judge name"""
        return await self.search_cases_by_type(request, settings.SEARCH_TYPES["judge"])

# Global service instance
case_service = CaseService()
