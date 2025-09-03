"""
Utility API endpoints for states and commissions
"""

import logging
from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.services.jagriti_client import jagriti_client, JagritiAPIException
from app.models.responses import (
    StatesResponse, DistrictCommissionsResponse,
    StateCommission, DistrictCommission, ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/states",
    response_model=StatesResponse,
    summary="Get all states with their commission IDs",
    description="Retrieve a list of all states and their corresponding commission IDs from the Jagriti portal",
    responses={
        200: {"description": "Successfully retrieved states list"},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def get_states():
    """
    Get all states and their commission IDs.
    
    This endpoint fetches all available states and union territories with their
    corresponding commission IDs from the Jagriti portal. Only active states
    that are not circuit benches are returned.
    
    Returns:
        StatesResponse: List of states with their commission IDs and metadata
    """
    try:
        logger.info("Fetching states and commissions from Jagriti API")
        jagriti_response = await jagriti_client.get_states_and_commissions()
        
        # Filter to get only main states (not circuit benches)
        states = []
        for state_data in jagriti_response.data:
            if state_data.activeStatus and not state_data.circuitAdditionBenchStatus:
                states.append(StateCommission(
                    commission_id=state_data.commissionId,
                    name=state_data.commissionNameEn,
                    active=state_data.activeStatus,
                    is_circuit_bench=state_data.circuitAdditionBenchStatus
                ))
        
        # Sort by name for better usability
        states.sort(key=lambda x: x.name)
        
        logger.info(f"Successfully retrieved {len(states)} states")
        return StatesResponse(
            states=states,
            total_count=len(states)
        )
        
    except JagritiAPIException as e:
        logger.error(f"Jagriti API error in get_states: {str(e)}")
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"Failed to fetch states from external API: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_states: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get(
    "/commissions/{state_id}",
    response_model=DistrictCommissionsResponse,
    summary="Get district commissions for a state",
    description="Retrieve all district commissions (DCDRC) for a given state commission ID",
    responses={
        200: {"description": "Successfully retrieved district commissions"},
        404: {"description": "State not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def get_district_commissions(
    state_id: int = Path(..., description="State commission ID", example=11290000)
):
    """
    Get district commissions for a specific state.
    
    This endpoint fetches all district consumer dispute redressal commissions (DCDRC)
    for a given state commission ID from the Jagriti portal.
    
    Args:
        state_id: The commission ID of the state
        
    Returns:
        DistrictCommissionsResponse: List of district commissions for the state
    """
    try:
        logger.info(f"Fetching district commissions for state ID: {state_id}")
        
        # First verify state exists and get state name
        state_name = await jagriti_client.get_state_name_by_id(state_id)
        if not state_name:
            raise HTTPException(
                status_code=404,
                detail=f"State with commission ID {state_id} not found"
            )
        
        # Fetch district commissions
        jagriti_response = await jagriti_client.get_district_commissions(state_id)
        
        # Transform to our response format
        commissions = []
        for commission_data in jagriti_response.data:
            if commission_data.activeStatus:
                commissions.append(DistrictCommission(
                    commission_id=commission_data.commissionId,
                    name=commission_data.commissionNameEn,
                    active=commission_data.activeStatus
                ))
        
        # Sort by name for better usability
        commissions.sort(key=lambda x: x.name)
        
        logger.info(f"Successfully retrieved {len(commissions)} district commissions for state {state_name}")
        return DistrictCommissionsResponse(
            commissions=commissions,
            state_id=state_id,
            state_name=state_name,
            total_count=len(commissions)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except JagritiAPIException as e:
        logger.error(f"Jagriti API error in get_district_commissions: {str(e)}")
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"Failed to fetch district commissions from external API: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_district_commissions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
