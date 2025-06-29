
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PromptRequest(BaseModel):
    prompt: str
    model_name: Optional[str] = "deepseek-r1"

class PromptResponse(BaseModel):
    response: str

class MultiModelRequest(BaseModel):
    prompt: str
    model_names: List[str]

class MultiModelResponse(BaseModel):
    responses: Dict[str, str]

class BatchTestRequest(BaseModel):
    test_case_ids: List[int]
    model_name: str
    prompts_per_case: Optional[int] = 3

class BatchTestResponse(BaseModel):
    results: List[Dict[str, Any]]

class TestResult(BaseModel):
    test_case_id: int
    test_case_title: str
    prompt: str
    model_name: str
    response: str
    status: Optional[str] = None
    timestamp: str

class ReportRequest(BaseModel):
    test_results: List[TestResult]
    report_title: str
