from pydantic import BaseModel
from typing import Optional

from pyrasgo.schemas.organization import Organization


class DataSourceBase(BaseModel):
    id: int


class DataSourceCreate(BaseModel):
    name: str
    abbreviation: str
    organizationId: int


class DataSource(DataSourceBase):
    name: Optional[str]  # TODO: Should not be optional
    abbreviation: Optional[str]
    category: Optional[str] = None
    organizationId: Optional[int]
