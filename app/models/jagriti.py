"""
Models for Jagriti API data structures
These models represent the data structures used by the Jagriti portal API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class JagritiStateCommission(BaseModel):
    """Model for Jagriti state commission data"""
    commissionId: int = Field(..., description="Commission ID")
    commissionNameEn: str = Field(..., description="Commission name in English")
    circuitAdditionBenchStatus: bool = Field(..., description="Circuit bench status")
    activeStatus: bool = Field(..., description="Active status")

class JagritiStatesResponse(BaseModel):
    """Model for Jagriti states API response"""
    data: List[JagritiStateCommission] = Field(..., description="List of state commissions")
    message: str = Field(..., description="Response message")
    error: str = Field(..., description="Error status")
    status: int = Field(..., description="HTTP status code")

class JagritiDistrictCommission(BaseModel):
    """Model for Jagriti district commission data"""
    commissionId: int = Field(..., description="District commission ID")
    commissionNameEn: str = Field(..., description="District commission name in English")
    circuitAdditionBenchStatus: bool = Field(..., description="Circuit bench status")
    activeStatus: bool = Field(..., description="Active status")

class JagritiDistrictCommissionsResponse(BaseModel):
    """Model for Jagriti district commissions API response"""
    data: List[JagritiDistrictCommission] = Field(..., description="List of district commissions")
    message: str = Field(..., description="Response message")
    error: str = Field(..., description="Error status")
    status: int = Field(..., description="HTTP status code")

class JagritiAdditionalComplainant(BaseModel):
    """Model for additional complainant data"""
    additional_complainant_name: str = Field(..., description="Additional complainant name")

class JagritiAdditionalRespondent(BaseModel):
    """Model for additional respondent data"""
    additional_respondent_name: str = Field(..., description="Additional respondent name")

class JagritiCaseDetail(BaseModel):
    """Model for individual case detail from Jagriti API"""
    caseNumber: str = Field(..., description="Case number")
    complainantName: str = Field(..., description="Complainant name")
    complainantAdvocateName: Optional[str] = Field(None, description="Complainant advocate name")
    respondentName: str = Field(..., description="Respondent name")
    respondentAdvocateName: Optional[str] = Field(None, description="Respondent advocate name")
    caseFilingDate: str = Field(..., description="Case filing date")
    orderDocumentPath: Optional[str] = Field(None, description="Order document path")
    orderDate: Optional[str] = Field(None, description="Order date")
    dateOfDisposal: Optional[str] = Field(None, description="Date of disposal")
    caseStageName: str = Field(..., description="Case stage name")
    additionalComplainantList: Optional[List[JagritiAdditionalComplainant]] = Field(None, description="Additional complainants")
    additionalRespondantList: Optional[List[JagritiAdditionalRespondent]] = Field(None, description="Additional respondents")
    additionalComplainant: Optional[str] = Field(None, description="Additional complainant")
    additionalRespondant: Optional[str] = Field(None, description="Additional respondent")
    orderDocumentBytea: Optional[Any] = Field(None, description="Order document bytes")
    dailyOrderStatus: bool = Field(..., description="Daily order status")
    judgemtmentDocumentPath: Optional[str] = Field(None, description="Judgment document path")
    judgemtmentDocumentBytea: Optional[Any] = Field(None, description="Judgment document bytes")
    judgemtmentDate: Optional[str] = Field(None, description="Judgment date")
    judgmentOrderDocumentBase64: Optional[str] = Field(None, description="Judgment order document base64")

class JagritiCaseSearchResponse(BaseModel):
    """Model for Jagriti case search API response"""
    message: str = Field(..., description="Response message")
    status: int = Field(..., description="HTTP status code")
    data: List[JagritiCaseDetail] = Field(..., description="List of case details")
    error: str = Field(..., description="Error status")

class JagritiCaseSearchRequest(BaseModel):
    """Model for Jagriti case search request payload"""
    commissionId: int = Field(..., description="Commission ID")
    dateRequestType: int = Field(1, description="Date request type (1 for filing date)")
    fromDate: str = Field(..., description="From date in YYYY-MM-DD format")
    toDate: str = Field(..., description="To date in YYYY-MM-DD format")
    judgeId: str = Field("", description="Judge ID (empty for all judges)")
    orderType: int = Field(1, description="Order type (1 for daily orders)")
    serchType: int = Field(..., description="Search type (1-7)")
    serchTypeValue: str = Field(..., description="Search value")

# Mapping constants
SEARCH_TYPE_NAMES = {
    1: "Case Number",
    2: "Complainant",
    3: "Respondent", 
    4: "Complainant Advocate",
    5: "Respondent Advocate",
    6: "Industry Type",
    7: "Judge"
}
