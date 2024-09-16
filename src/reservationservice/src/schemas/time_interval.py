from pydantic import BaseModel, model_validator


from datetime import datetime


class TimeInterval(BaseModel):
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def check_time_range(self):
        assert (
            self.start_time < self.end_time
        ), "start_time must be less than end_time"
        return self
