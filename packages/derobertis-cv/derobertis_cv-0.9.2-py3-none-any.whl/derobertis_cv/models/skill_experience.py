from dataclasses import dataclass
import datetime
from typing import Union, Type

import pandas as pd

from derobertis_cv.models.experience_scale import SkillExperienceScale, HoursExperienceScale


@dataclass(unsafe_hash=True)
class SkillExperience:
    begin_date_inp: Union[str, datetime.date]
    hours_per_week: float = 0
    one_time_hours: float = 0
    experience_scale: Type[SkillExperienceScale] = HoursExperienceScale

    def __post_init__(self):
        self.begin_date = pd.to_datetime(self.begin_date_inp)

    @property
    def experience_length(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.begin_date

    @property
    def experience_length_str(self) -> str:
        months = self.months_elapsed
        if months < 1.5:
            return '1 month'
        if months < 10:
            return f'{months:.0f} months'
        years = months / 12
        if round(years, 0) == 1:
            return f'{years:.0f} year'
        return f'{years:.0f} years'

    @property
    def weeks_elapsed(self) -> float:
        seconds_elapsed = self.experience_length.total_seconds()
        return seconds_elapsed / (60 * 60 * 24 * 7)

    @property
    def months_elapsed(self) -> float:
        seconds_elapsed = self.experience_length.total_seconds()
        return seconds_elapsed / (60 * 60 * 24 * 30)

    @property
    def hours(self) -> float:
        num_hours = self.one_time_hours
        num_hours += self.weeks_elapsed * self.hours_per_week
        return num_hours

    @property
    def experience_level(self) -> int:
        return self.experience_scale.experience_to_level(self)
