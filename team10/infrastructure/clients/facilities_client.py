from typing import List, Optional
from datetime import datetime

from ..ports.facilities_service_port import FacilitiesServicePort
from ..models.region import Region
from ..models.search_criteria import SearchCriteria
from ..models.facility_cost_estimate import FacilityCostEstimate
from ...domain.models.facility import Facility


class MockFacilitiesClient(FacilitiesServicePort):
    """Mock implementation of FacilitiesServicePort for development."""

    MOCK_REGIONS = [
        Region(id="1", name="Tehran"),
        Region(id="2", name="Isfahan"),
        Region(id="3", name="Shiraz"),
        Region(id="4", name="Mashhad"),
        Region(id="5", name="Tabriz"),
        Region(id="6", name="Yazd"),
        Region(id="7", name="Kerman"),
        Region(id="8", name="Rasht"),
        Region(id="9", name="Kish"),
        Region(id="10", name="Qeshm"),
        Region(id="11", name="Ahvaz"),
        Region(id="12", name="Bandar Abbas"),
        Region(id="13", name="Hamadan"),
        Region(id="14", name="Qom"),
        Region(id="15", name="Kashan"),
    ]

    # Mapping of Persian names and alternative spellings to region IDs
    NAME_ALIASES = {
        # Tehran
        "tehran": "1", "تهران": "1",
        # Isfahan
        "isfahan": "2", "esfahan": "2", "اصفهان": "2",
        # Shiraz
        "shiraz": "3", "شیراز": "3",
        # Mashhad
        "mashhad": "4", "mashad": "4", "مشهد": "4",
        # Tabriz
        "tabriz": "5", "تبریز": "5",
        # Yazd
        "yazd": "6", "یزد": "6",
        # Kerman
        "kerman": "7", "کرمان": "7",
        # Rasht
        "rasht": "8", "رشت": "8",
        # Kish
        "kish": "9", "کیش": "9",
        # Qeshm
        "qeshm": "10", "قشم": "10",
        # Ahvaz
        "ahvaz": "11", "اهواز": "11",
        # Bandar Abbas
        "bandar abbas": "12", "bandarabbas": "12", "بندرعباس": "12",
        # Hamadan
        "hamadan": "13", "hamedan": "13", "همدان": "13",
        # Qom
        "qom": "14", "قم": "14",
        # Kashan
        "kashan": "15", "کاشان": "15",
    }

    def search_region(self, query: str) -> Optional[Region]:
        normalized = query.strip().lower()

        # Exact match on aliases
        if normalized in self.NAME_ALIASES:
            region_id = self.NAME_ALIASES[normalized]
            return next(r for r in self.MOCK_REGIONS if r.id == region_id)

        # Partial match on aliases
        for alias, region_id in self.NAME_ALIASES.items():
            if alias in normalized or normalized in alias:
                return next(r for r in self.MOCK_REGIONS if r.id == region_id)

        # No match found
        return None

    def find_facilities_in_area(self, criteria: SearchCriteria) -> List[Facility]:
        return []

    def get_cost_estimate(
        self,
        facility_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> FacilityCostEstimate:
        return FacilityCostEstimate(
            facility_id=facility_id,
            estimated_cost=0.0,
            period_start=start_date,
            period_end=end_date
        )
