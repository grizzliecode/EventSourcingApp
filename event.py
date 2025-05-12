from enum import Enum
from dataclasses import dataclass, asdict
from typing import Dict, Any
class EventType(Enum):
    OrderPlaced = 1
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
    aggregate_id : int
    event_type : EventType
    version : int
    data : Dict[str, Any]
    '''
        For:
            - OrderPlaced data = {
                                   order_id : int 
                                   user_id : int
                                   type : int (sell = 0, buy = 1)
                                   product_id : int (= aggregate_id)
                                   quantity : int
                                   price : int
                                    } 
            - OrderCancelled data = {
                                    order_id : int      
                                    user_id : int
                                    type : int (sell = 0, buy = 1)
                                    product_id : int (= aggregate_id)
                                    quantity : int
                                    price : int
                                    }
            - TradeExecuted data = {
                                    product_id : int (= aggregate_id)
                                    order1_id : int
                                    order2_id : int
                                    }
            - FundsDebited data = {
                                    user_id : int (= aggregate_id)
                                    amount : int
                                    }
            - FundsCredited data = {
                                    user_id : int (= aggregate_id)
                                    amount : int
                                    }
    '''

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