from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..models.region import Region
from ..models.search_criteria import SearchCriteria
from ..models.facility_cost_estimate import FacilityCostEstimate
from ...domain.models.facility import Facility


class FacilitiesServicePort(ABC):
    """Port for facilities service."""

    @abstractmethod
    def search_region(self, query: str) -> Optional[Region]:
        """Search for a region by name query.

        Args:
            query: The search string for finding a region.

        Returns:
            A Region with id and name, or None if not found.
        """
        pass

    @abstractmethod
    def find_facilities_in_area(self, criteria: SearchCriteria) -> List[Facility]:
        """Find facilities matching search criteria."""
        pass

    @abstractmethod
    def get_cost_estimate(
        self,
        facility_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> FacilityCostEstimate:
        """Get cost estimate for a facility during a period."""
        pass
