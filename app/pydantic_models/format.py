from pydantic import BaseModel

class FormatConfig(BaseModel):
    response_format: str
    table_headers: list[str]
    format_instructions: str