# Jagriti Consumer Court API

A FastAPI application that replicates the Jagriti portal's District Consumer Court case search functionality. This API provides REST endpoints to search consumer court cases by various criteria and retrieve state/commission data.

## Features

- **7 Case Search Types**: Search by case number, complainant, respondent, advocates, industry type, and judge
- **State & Commission Management**: Get lists of states and district commissions
- **Date Range Filtering**: Search cases within specific date ranges
- **Real-time Data**: Direct integration with Jagriti portal APIs
- **Comprehensive Documentation**: Auto-generated OpenAPI/Swagger docs
- **Error Handling**: Robust error handling and validation
- **Async Support**: High-performance async/await implementation

## Prerequisites

- Python 3.8 or higher
- Internet connection (for Jagriti portal API access)

## Installation

### Local Development Setup

1. **Clone or download the project**
```bash
cd jagriti-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints Overview

#### Utility Endpoints
- `GET /states` - Get all states with commission IDs
- `GET /commissions/{state_id}` - Get district commissions for a state
- `GET /health` - Health check
- `GET /` - API information

#### Case Search Endpoints
- `POST /cases/by-case-number` - Search by case number
- `POST /cases/by-complainant` - Search by complainant name
- `POST /cases/by-respondent` - Search by respondent name
- `POST /cases/by-complainant-advocate` - Search by complainant advocate
- `POST /cases/by-respondent-advocate` - Search by respondent advocate
- `POST /cases/by-industry-type` - Search by industry type
- `POST /cases/by-judge` - Search by judge name

### Request Format

All case search endpoints accept the following JSON payload:

```json
{
  "state": "KARNATAKA",
  "commission": "Bangalore 1st & Rural Additional",
  "search_value": "REDDY",
  "from_date": "2025-01-01",
  "to_date": "2025-09-03"
}
```

### Response Format

Case search endpoints return:

```json
{
  "cases": [
    {
      "case_number": "DC/AB4/525/CC/72/2025",
      "case_stage": "ADMIT",
      "filing_date": "2025-05-23",
      "complainant": "MANJUNATHA REDDY S/o. venkataswamy",
      "complainant_advocate": "D Narase Gowda",
      "respondent": "INTERGLOBE AVIATION LIMITED",
      "respondent_advocate": null,
      "document_link": null
    }
  ],
  "total_count": 1,
  "search_criteria": {
    "state": "KARNATAKA",
    "commission": "Bangalore 1st & Rural Additional",
    "search_value": "REDDY",
    "search_type": 2,
    "from_date": "2025-01-01",
    "to_date": "2025-09-03"
  }
}
```

## Usage Examples

### 1. Get States List

```bash
curl -X GET "http://localhost:8000/states"
```

### 2. Get District Commissions for Karnataka

```bash
curl -X GET "http://localhost:8000/commissions/11290000"
```

### 3. Search Cases by Complainant

```bash
curl -X POST "http://localhost:8000/cases/by-complainant" \
-H "Content-Type: application/json" \
-d '{
  "state": "KARNATAKA",
  "commission": "Bangalore 1st & Rural Additional",
  "search_value": "REDDY",
  "from_date": "2025-01-01",
  "to_date": "2025-09-03"
}'
```

### 4. Search Cases by Case Number

```bash
curl -X POST "http://localhost:8000/cases/by-case-number" \
-H "Content-Type: application/json" \
-d '{
  "state": "KARNATAKA",
  "commission": "Bangalore 1st & Rural Additional",
  "search_value": "DC/AB4/525/CC/72/2025"
}'
```

## Project Structure

```
jagriti-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic models
│   │   ├── requests.py      # Request models
│   │   ├── responses.py     # Response models
│   │   └── jagriti.py       # Jagriti API models
│   ├── services/            # Business logic
│   │   ├── jagriti_client.py # Jagriti API client
│   │   └── case_service.py   # Case search service
│   └── api/                 # API endpoints
│       ├── cases.py         # Case search endpoints
│       └── utilities.py     # Utility endpoints
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## Configuration

The application can be configured through environment variables:

- `API_HOST`: Host to bind to (default: 0.0.0.0)
- `API_PORT`: Port to bind to (default: 8000)

## Search Types Mapping

| Search Type | ID | Description |
|-------------|----|-----------| 
| Case Number | 1 | Search by exact case number |
| Complainant | 2 | Search by complainant name |
| Respondent | 3 | Search by respondent name |
| Complainant Advocate | 4 | Search by complainant's lawyer |
| Respondent Advocate | 5 | Search by respondent's lawyer |
| Industry Type | 6 | Search by business sector |
| Judge | 7 | Search by judge name |

## Key Features

### Date Filtering
- **Default Range**: 2025-01-01 to 2025-09-03
- **Customizable**: Specify your own date range
- **Filter Type**: Uses Case Filing Date

### State & Commission Resolution
- Automatically converts state names to internal IDs
- Maps commission names to district commission IDs
- Validates state and commission existence

### Error Handling
- **400**: Bad request/validation errors
- **404**: State or commission not found
- **500**: Internal server errors
- Detailed error messages for debugging

### Performance Features
- Async/await for high performance
- Connection pooling with httpx
- Retry logic with exponential backoff
- Request timeouts and error recovery

## Important Notes

### DCDRC Focus
This API focuses specifically on **District Consumer Dispute Redressal Commissions (DCDRC)** as specified in the requirements.

### Daily Orders Only
The API is configured to return only **Daily Orders** (`orderType: 1`) as per the requirements.

### Captcha Handling
For this implementation, captcha validation is bypassed as mentioned in the assignment requirements.

### External Dependencies
This API relies on the Jagriti portal's public APIs:
- State/Commission data: `https://e-jagriti.gov.in/services/report/report/getStateCommissionAndCircuitBench`
- District commissions: `https://e-jagriti.gov.in/services/report/report/getDistrictCommissionByCommissionId`
- Case search: `https://e-jagriti.gov.in/services/case/caseFilingService/v2/getCaseDetailsBySearchType`

## API Reference

For detailed API documentation with request/response schemas, visit the interactive documentation at `/docs` when the server is running.

---

**Note**: This API provides a clean REST interface to the Jagriti portal's case search functionality, making it easy to integrate consumer court case tracking into other applications.
