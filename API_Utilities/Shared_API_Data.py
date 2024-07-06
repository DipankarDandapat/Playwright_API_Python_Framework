from dataclasses import dataclass, field
from typing import Any, Dict
from API_Utilities import logger_utility

log = logger_utility.customLogger()

@dataclass
class SharedData:
    data: Dict[str, Any] = field(default_factory=dict)

    def set_data(self, key: str, value: Any):
        log.info(f"Setting data for key: {key} with value: {value}")
        self.data[key] = value
        log.info(f"Current data state: {self.data}")

    def get_data(self, key: str) -> Any:
        value = self.data.get(key)
        if value is not None:
            log.info(f"Retrieved data for key: {key} with value: {value}")
        else:
            log.info(f"No data found for key: {key}")
        return value


shared_data = SharedData()
