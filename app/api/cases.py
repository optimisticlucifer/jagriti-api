"""
Case search API endpoints
"""

import logging
from fastapi import APIRouter, HTTPException, Body
from app.services.case_service import case_service, CaseServiceException
from app.models.requests import (
    CaseSearchRequest, CaseNumberSearchRequest, ComplainantSearchRequest,
    RespondentSearchRequest, ComplainantAdvocateSearchRequest, 
    RespondentAdvocateSearchRequest, IndustryTypeSearchRequest,
    JudgeSearchRequest, ExampleCaseSearchRequest
)
from app.models.responses import CaseSearchResponse, ErrorResponse, ExampleCaseResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# Common error responses for all endpoints
common_responses = {
    400: {"description": "Bad request - validation error", "model": ErrorResponse},
    404: {"description": "State or commission not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
}

@router.post(
    "/by-case-number",
    response_model=CaseSearchResponse,
    summary="Search cases by case number",
    description="Search for cases using case number from District Consumer Courts",
    responses={**common_responses, 200: {"description": "Successfully retrieved cases"}}
)
async def search_cases_by_case_number(
    request: CaseNumberSearchRequest = Body(
        ...,
        example={
            "state": "KARNATAKA",
            "commission": "Bangalore 1st & Rural Additional",
            "search_value": "DC/AB4/525/CC/72/2025",
            "from_date": "2025-01-01",
            "to_date": "2025-09-03"
        }
    )
):
    """
    Search cases by case number.
    
    This endpoint searches for cases in District Consumer Courts using the case number.
    The search is performed across the specified state and district commission.
    
    Args:
        request: Case search request with case number
        
    Returns:
        CaseSearchResponse: List of matching cases with metadata
    """
    try:
        logger.info(f"Searching cases by case number: {request.search_value}")
        result = await case_service.search_cases_by_case_number(request)
        logger.info(f"Found {result.total_count} cases for case number search")
        return result
    except CaseServiceException as e:
        logger.error(f"Case service error in case number search: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in case number search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post(
    "/by-complainant",
    response_model=CaseSearchResponse,
    summary="Search cases by complainant name",
    description="Search for cases using complainant name from District Consumer Courts",
    responses={**common_responses, 200: {"description": "Successfully retrieved cases"}}
)
async def search_cases_by_complainant(
    request: ComplainantSearchRequest = Body(
        ...,
        example={
            "state": "KARNATAKA",
            "commission": "Bangalore 1st & Rural Additional",
            "search_value": "REDDY",
            "from_date": "2025-01-01",
            "to_date": "2025-09-03"
        }
    )
):
    """
    Search cases by complainant name.
    
    This endpoint searches for cases in District Consumer Courts using the complainant's name.
    Partial matches are supported - you can search for part of the complainant's name.
    
    Args:
        request: Case search request with complainant name
        
    Returns:
        CaseSearchResponse: List of matching cases with metadata
    """
    try:
        logger.info(f"Searching cases by complainant: {request.search_value}")
        result = await case_service.search_cases_by_complainant(request)
        logger.info(f"Found {result.total_count} cases for complainant search")
        return result
    except CaseServiceException as e:
        logger.error(f"Case service error in complainant search: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in complainant search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post(
    "/by-respondent",
    response_model=CaseSearchResponse,
    summary="Search cases by respondent name",
    description="Search for cases using respondent name from District Consumer Courts",
    responses={**common_responses, 200: {"description": "Successfully retrieved cases"}}
)
async def search_cases_by_respondent(
    request: RespondentSearchRequest = Body(
        ...,
        example={
            "state": "KARNATAKA",
            "commission": "Bangalore 1st & Rural Additional",
            "search_value": "INTERGLOBE",
            "from_date": "2025-01-01",
            "to_date": "2025-09-03"
        }
    )
):
    """
    Search cases by respondent name.
    
    This endpoint searches for cases in District Consumer Courts using the respondent's name.
    Partial matches are supported - you can search for part of the respondent's name.
    
    Args:
        request: Case search request with respondent name
        
    Returns:
        CaseSearchResponse: List of matching cases with metadata
    """
    try:
        logger.info(f"Searching cases by respondent: {request.search_value}")
        result = await case_service.search_cases_by_respondent(request)
        logger.info(f"Found {result.total_count} cases for respondent search")
        return result
    except CaseServiceException as e:
        logger.error(f"Case service error in respondent search: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in respondent search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post(
    "/by-complainant-advocate",
    response_model=CaseSearchResponse,
    summary="Search cases by complainant advocate name",
    description="Search for cases using complainant advocate name from District Consumer Courts",
    responses={**common_responses, 200: {"description": "Successfully retrieved cases"}}
)
async def search_cases_by_complainant_advocate(
    request: ComplainantAdvocateSearchRequest = Body(
        ...,
        example={
            "state": "KARNATAKA",
            "commission": "Bangalore 1st & Rural Additional",
            "search_value": "D Narase Gowda",
            "from_date": "2025-01-01",
            "to_date": "2025-09-03"
        }
    )
):
    """
    Search cases by complainant advocate name.
    
    This endpoint searches for cases in District Consumer Courts using the complainant's advocate name.
    Partial matches are supported - you can search for part of the advocate's name.
    
    Args:
        request: Case search request with complainant advocate name
        
    Returns:
        CaseSearchResponse: List of matching cases with metadata
    """
    try:
        logger.info(f"Searching cases by complainant advocate: {request.search_value}")
        result = await case_service.search_cases_by_complainant_advocate(request)
        logger.info(f"Found {result.total_count} cases for complainant advocate search")
        return result
    except CaseServiceException as e:
        logger.error(f"Case service error in complainant advocate search: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in complainant advocate search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post(
    "/by-respondent-advocate",
    response_model=CaseSearchResponse,
    summary="Search cases by respondent advocate name",
    description="Search for cases using respondent advocate name from District Consumer Courts",
    responses={**common_responses, 200: {"description": "Successfully retrieved cases"}}
)
async def search_cases_by_respondent_advocate(
    request: RespondentAdvocateSearchRequest = Body(
        ...,
        example={
            "state": "KARNATAKA",
            "commission": "Bangalore 1st & Rural Additional",
            "search_value": "SANTHOSH KUMAR",
            "from_date": "2025-01-01",
            "to_date": "2025-09-03"
        }
    )
):
    """
    Search cases by respondent advocate name.
    
    This endpoint searches for cases in District Consumer Courts using the respondent's advocate name.
    Partial matches are supported - you can search for part of the advocate's name.
    
    Args:
        request: Case search request with respondent advocate name
        
    Returns:
        CaseSearchResponse: List of matching cases with metadata
    """
    try:
        logger.info(f"Searching cases by respondent advocate: {request.search_value}")
        result = await case_service.search_cases_by_respondent_advocate(request)
        logger.info(f"Found {result.total_count} cases for respondent advocate search")
        return result
    except CaseServiceException as e:
        logger.error(f"Case service error in respondent advocate search: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in respondent advocate search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post(
    "/by-industry-type",
    response_model=CaseSearchResponse,
    summary="Search cases by industry type",
    description="Search for cases using industry type from District Consumer Courts",
    responses={**common_responses, 200: {"description": "Successfully retrieved cases"}}
)
async def search_cases_by_industry_type(
    request: IndustryTypeSearchRequest = Body(
        ...,
        example={
            "state": "KARNATAKA",
            "commission": "Bangalore 1st & Rural Additional",
            "search_value": "INSURANCE",
            "from_date": "2025-01-01",
            "to_date": "2025-09-03"
        }
    )
):
    """
    Search cases by industry type.
    
    This endpoint searches for cases in District Consumer Courts using the industry type.
    Common industry types include INSURANCE, BANKING, TELECOM, AIRLINES, etc.
    
    Args:
        request: Case search request with industry type
        
    Returns:
        CaseSearchResponse: List of matching cases with metadata
    """
    try:
        logger.info(f"Searching cases by industry type: {request.search_value}")
        result = await case_service.search_cases_by_industry_type(request)
        logger.info(f"Found {result.total_count} cases for industry type search")
        return result
    except CaseServiceException as e:
        logger.error(f"Case service error in industry type search: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in industry type search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post(
    "/by-judge",
    response_model=CaseSearchResponse,
    summary="Search cases by judge name",
    description="Search for cases using judge name from District Consumer Courts",
    responses={**common_responses, 200: {"description": "Successfully retrieved cases"}}
)
async def search_cases_by_judge(
    request: JudgeSearchRequest = Body(
        ...,
        example={
            "state": "KARNATAKA",
            "commission": "Bangalore 1st & Rural Additional",
            "search_value": "Judge Name",
            "from_date": "2025-01-01",
            "to_date": "2025-09-03"
        }
    )
):
    """
    Search cases by judge name.
    
    This endpoint searches for cases in District Consumer Courts using the judge's name.
    Partial matches are supported - you can search for part of the judge's name.
    
    Args:
        request: Case search request with judge name
        
    Returns:
        CaseSearchResponse: List of matching cases with metadata
    """
    try:
        logger.info(f"Searching cases by judge: {request.search_value}")
        result = await case_service.search_cases_by_judge(request)
        logger.info(f"Found {result.total_count} cases for judge search")
        return result
    except CaseServiceException as e:
        logger.error(f"Case service error in judge search: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in judge search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Health check endpoint for case search module
@router.get(
    "/health",
    summary="Health check for case search endpoints",
    description="Check if case search endpoints are operational"
)
async def case_search_health():
    """Health check endpoint for case search functionality"""
    return {
        "status": "healthy",
        "module": "case-search",
        "endpoints": [
            "/cases/by-case-number",
            "/cases/by-complainant", 
            "/cases/by-respondent",
            "/cases/by-complainant-advocate",
            "/cases/by-respondent-advocate",
            "/cases/by-industry-type",
            "/cases/by-judge"
        ]
    }
