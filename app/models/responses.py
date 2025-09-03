"""
Response models for the Jagriti API endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

class CaseResponse(BaseModel):
    """Model for individual case response"""
    case_number: str = Field(..., description="Case number")
    case_stage: str = Field(..., description="Current stage of the case")
    filing_date: str = Field(..., description="Case filing date in YYYY-MM-DD format")
    complainant: str = Field(..., description="Complainant name")
    complainant_advocate: Optional[str] = Field(None, description="Complainant advocate name")
    respondent: str = Field(..., description="Respondent name")
    respondent_advocate: Optional[str] = Field(None, description="Respondent advocate name")
    document_link: Optional[str] = Field(None, description="Link to case documents")

class CaseSearchResponse(BaseModel):
    """Model for case search API response"""
    cases: List[CaseResponse] = Field(..., description="List of matching cases")
    total_count: int = Field(..., description="Total number of cases found")
    search_criteria: dict = Field(..., description="Search criteria used")

class StateCommission(BaseModel):
    """Model for state commission response"""
    commission_id: int = Field(..., description="Commission ID")
    name: str = Field(..., description="State/Commission name")
    active: bool = Field(..., description="Whether the commission is active")
    is_circuit_bench: bool = Field(False, description="Whether this is a circuit bench")

class StatesResponse(BaseModel):
    """Model for states API response"""
    states: List[StateCommission] = Field(..., description="List of states and their commissions")
    total_count: int = Field(..., description="Total number of states")

class DistrictCommission(BaseModel):
    """Model for district commission response"""
    commission_id: int = Field(..., description="District commission ID")
    name: str = Field(..., description="District commission name")
    active: bool = Field(..., description="Whether the commission is active")

class DistrictCommissionsResponse(BaseModel):
    """Model for district commissions API response"""
    commissions: List[DistrictCommission] = Field(..., description="List of district commissions")
    state_id: int = Field(..., description="State commission ID")
    state_name: str = Field(..., description="State name")
    total_count: int = Field(..., description="Total number of district commissions")

class ErrorResponse(BaseModel):
    """Model for error responses"""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: Optional[str] = Field(None, description="Error timestamp")
    path: Optional[str] = Field(None, description="Request path that caused the error")

class SuccessResponse(BaseModel):
    """Generic success response model"""
    message: str = Field(..., description="Success message")
    data: Union[dict, list] = Field(..., description="Response data")
    status: str = Field("success", description="Response status")

# Example response models for documentation
class ExampleCaseResponse(BaseModel):
    """Example case response for documentation"""
    case_number: str = Field("DC/AB4/525/CC/72/2025", description="Case number")
    case_stage: str = Field("ADMIT", description="Case stage")
    filing_date: str = Field("2025-05-23", description="Filing date")
    complainant: str = Field("MANJUNATHA REDDY S/o. venkataswamy", description="Complainant")
    complainant_advocate: str = Field("D Narase Gowda", description="Complainant advocate")
    respondent: str = Field("INTERGLOBE AVIATION LIMITED", description="Respondent")
    respondent_advocate: Optional[str] = Field(None, description="Respondent advocate")
    document_link: Optional[str] = Field(None, description="Document link")

class ExampleStatesResponse(BaseModel):
    """Example states response for documentation"""
    states: List[StateCommission] = Field([
        StateCommission(commission_id=11290000, name="KARNATAKA", active=True, is_circuit_bench=False),
        StateCommission(commission_id=11270000, name="MAHARASHTRA", active=True, is_circuit_bench=False)
    ], description="List of states")
    total_count: int = Field(2, description="Total count")

class ExampleDistrictCommissionsResponse(BaseModel):
    """Example district commissions response for documentation"""
    commissions: List[DistrictCommission] = Field([
        DistrictCommission(commission_id=15290525, name="Bangalore 1st & Rural Additional", active=True),
        DistrictCommission(commission_id=11290525, name="Bangalore Urban", active=True)
    ], description="List of district commissions")
    state_id: int = Field(11290000, description="State ID")
    state_name: str = Field("KARNATAKA", description="State name")
    total_count: int = Field(2, description="Total count")
