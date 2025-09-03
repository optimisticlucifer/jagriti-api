"""
Request models for the Jagriti API endpoints
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date

class CaseSearchRequest(BaseModel):
    """Base model for case search requests"""
    state: str = Field(..., description="State name (e.g., 'KARNATAKA')", min_length=1)
    commission: str = Field(..., description="Commission name (e.g., 'Bangalore 1st & Rural Additional')", min_length=1)
    search_value: str = Field(..., description="Search value (case number, name, etc.)", min_length=1)
    from_date: Optional[str] = Field(None, description="Start date in YYYY-MM-DD format")
    to_date: Optional[str] = Field(None, description="End date in YYYY-MM-DD format")
    
    @validator('state')
    def state_must_be_uppercase(cls, v):
        return v.upper()
    
    @validator('from_date', 'to_date')
    def validate_date_format(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v
    
    @validator('to_date')
    def to_date_must_be_after_from_date(cls, v, values):
        if v is not None and values.get('from_date') is not None:
            from_date = datetime.strptime(values['from_date'], '%Y-%m-%d')
            to_date = datetime.strptime(v, '%Y-%m-%d')
            if to_date < from_date:
                raise ValueError('to_date must be after from_date')
        return v

class CaseNumberSearchRequest(CaseSearchRequest):
    """Request model for case number search"""
    search_value: str = Field(..., description="Case number to search for", min_length=1)

class ComplainantSearchRequest(CaseSearchRequest):
    """Request model for complainant search"""
    search_value: str = Field(..., description="Complainant name to search for", min_length=1)

class RespondentSearchRequest(CaseSearchRequest):
    """Request model for respondent search"""
    search_value: str = Field(..., description="Respondent name to search for", min_length=1)

class ComplainantAdvocateSearchRequest(CaseSearchRequest):
    """Request model for complainant advocate search"""
    search_value: str = Field(..., description="Complainant advocate name to search for", min_length=1)

class RespondentAdvocateSearchRequest(CaseSearchRequest):
    """Request model for respondent advocate search"""
    search_value: str = Field(..., description="Respondent advocate name to search for", min_length=1)

class IndustryTypeSearchRequest(CaseSearchRequest):
    """Request model for industry type search"""
    search_value: str = Field(..., description="Industry type to search for", min_length=1)

class JudgeSearchRequest(CaseSearchRequest):
    """Request model for judge search"""
    search_value: str = Field(..., description="Judge name to search for", min_length=1)

# Example usage models
class ExampleCaseSearchRequest(BaseModel):
    """Example request for documentation"""
    state: str = Field("KARNATAKA", description="State name")
    commission: str = Field("Bangalore 1st & Rural Additional", description="Commission name")
    search_value: str = Field("REDDY", description="Search value")
    from_date: Optional[str] = Field("2025-01-01", description="Start date (optional)")
    to_date: Optional[str] = Field("2025-09-03", description="End date (optional)")
