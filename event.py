from enum import Enum
from dataclasses import dataclass, asdict
from typing import Dict, Any
class EventType(Enum):
    OrderedPlaced = 1
    OrderCancelled = 2
    TradeExecuted = 3
    FundsDebited = 4
    FundsCredited = 5

class AggregateType(Enum):
    OrderBook = 1
    Account = 2

@dataclass
class Event:
    aggregate_type : AggregateType
    aggregate_id : str
    event_type : EventType
    version : int
    data : Dict[str, Any]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Event":
        d["aggregate_type"] = AggregateType[d["aggregate_type"]]
        d["event_type"] = EventType[d["event_type"]]
        return Event(**d)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["aggregate_type"] = self.aggregate_type.name
        d["event_type"] = self.event_type.name
        return d