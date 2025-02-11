import os
import json
from fastapi import APIRouter, HTTPException
from app.pydantic_models.format import FormatConfig

router = APIRouter()

# Define the path to the formatting configuration file
FORMAT_CONFIG_PATH = os.path.join(os.getcwd(), "format_config.json")

def load_format_config() -> dict:
    """
    Load the formatting configuration from a JSON file.
    If the file does not exist, create it with default values.
    """
    if not os.path.exists(FORMAT_CONFIG_PATH):
        default_config = {
            "response_format": "table",
            "table_headers": ["Horse Name", "Odds", "Additional Info"],
            "format_instructions": (
                "When presenting lists of horses with odds, output the data in a table "
                "with headers 'Horse Name', 'Odds', and 'Additional Info'."
            )
        }
        with open(FORMAT_CONFIG_PATH, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    with open(FORMAT_CONFIG_PATH, "r") as f:
        return json.load(f)

def save_format_config(config: dict) -> None:
    """Save the provided configuration dictionary to the JSON file."""
    with open(FORMAT_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

@router.get("/", response_model=FormatConfig, summary="Get current formatting configuration")
def get_format_config():
    try:
        config = load_format_config()
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/", response_model=FormatConfig, summary="Update formatting configuration")
def update_format_config(new_config: FormatConfig):
    try:
        config = new_config.dict()
        save_format_config(config)
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
