from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Dict
import pandas as pd
from uuid import uuid4

T = TypeVar('T')

class IDataService(ABC, Generic[T]):
    def __init__(self):
        self.id = str(uuid4())

    def __hash__(self):
        return hash(self.id)

    @abstractmethod
    def add_or_update(self, obj_identifier: str, objs: List[T], **kwargs) -> List[T]:
        pass

    @abstractmethod
    def retrieve_objs(self, obj_identifier: str, ids: List[str] = None) -> List[T]:
        pass

    @abstractmethod
    def delete(self, obj_identifier: str, ids: List[str]) -> Dict[str, bool]:
        pass

    @abstractmethod
    def translate_from_data_rows(self, df: pd.DataFrame) -> List[T]:
        pass

    @abstractmethod
    def retrieve_as_df(self, obj_identifier: str, ids: List[str] = None) -> pd.DataFrame:
        pass