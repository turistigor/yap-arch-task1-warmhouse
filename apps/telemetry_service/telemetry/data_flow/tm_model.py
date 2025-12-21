from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _json_tm_to_model(field_name: str) -> str:
    match field_name:
        case 'sensor_id':
            return 'SensorID'
        case 'status':
            return 'Status'
        case 'timestamp':
            return 'Timestamp'
        case 'value':
            return 'Value'
        case _:
            raise ValueError


class TmMeasure(BaseModel):
    model_config = ConfigDict(extra='ignore', alias_generator=_json_tm_to_model)

    sensor_id: int = Field(..., description="Sensor ID как строка")
    status: str
    timestamp: datetime
    value: float
    
    @field_validator('sensor_id', mode='before')
    @classmethod
    def convert_sensor_id(cls, value: str):
        """Преобразует sensor_id из числа в строку"""
        if value is None:
            return 0
        return int(value)
