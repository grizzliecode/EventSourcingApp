from event import Event, EventType, AggregateType
from store import EventStore

class OrderBook:
    def __init__(self, aggregate_id):
        self.aggregate_id = aggregate_id
        self.active_orders = {}
        self.cancelled_orders = {}
        self.successful_transactions = []
        self.event_store = EventStore()
        self.replay()

    def apply(self, event: Event) -> None:
        if event.event_type == EventType.OrderPlaced:
            self.active_orders.update(
                {event.data.get("order_id", 0):{
                    "user_id": event.data.get("user_id", 0),
                    "type": event.data.get("type", 0),
                    "product_id": event.aggregate_id,
                    "quantity": event.data.get("quantity", 0),
                    "price": event.data.get("price", 0),
                }}
            )
        elif event.event_type == EventType.OrderCancelled:
            order = self.active_orders.pop(event.data.get("order_id", 0), None)
            self.cancelled_orders.update({event.data.get("order_id", 0):order})
        elif event.event_type == EventType.TradeExecuted:
            self.successful_transactions.append((event.data.get("order1_id", 0), event.data.get("order2_id", 0)))
            x = self.active_orders.pop(event.data.get("order1_id",0), None)
            y = self.active_orders.pop(event.data.get("order2_id",0), None)

    def replay(self):
        events = self.event_store.get_specific_events(AggregateType.OrderBook, aggregate_id=self.aggregate_id)
        for event in events:
            self.apply(event)

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0
        self.event_store = EventStore()
        self.replay()

    def apply(self, event: Event) -> None:
        if event.event_type == EventType.FundsDebited:
            self.balance -= event.data.get("amount", 0)
        elif event.event_type == EventType.FundsCredited:
            self.balance += event.data.get("amount", 0)

    def replay(self):
        events = self.event_store.get_specific_events(AggregateType.Account, self.account_id)
        for event in events:
            self.apply(event)