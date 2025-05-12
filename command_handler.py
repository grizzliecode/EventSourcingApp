from store import EventStore
from aggregates import OrderBook, Account
from typing import Dict
from event import Event, EventType, AggregateType


def place_order(user_id: int, _type: int, product_id: int, quantity:int, price:int) -> (Dict[str, str], int):
    orderBook = OrderBook(product_id)
    order_id = len(orderBook.active_orders) + len(orderBook.cancelled_orders) + 2 * len(orderBook.successful_transactions) + 1
    account = Account(user_id)
    store = EventStore()
    if price > account.balance and _type == 1:
        return {"status": "Fail. Insufficient funds."}, -1
    if _type == 1:
        conf = False
        while conf == False:
            event = Event(event_type=EventType.FundsDebited, aggregate_type=AggregateType.Account, aggregate_id=user_id
                          , version=store.get_last_version(AggregateType.Account, aggregate_id=user_id) + 1,
                          data={"user_id": user_id, "amount": price})
            conf = store.append(event)
        if conf == False:
            return {"status": "Fail."} , -1
    conf = False
    while conf == False:
        event = Event(event_type=EventType.OrderPlaced, aggregate_type=AggregateType.OrderBook, aggregate_id=product_id,
                      version= store.get_last_version(AggregateType.OrderBook, aggregate_id = product_id) + 1,
                      data={"order_id": order_id,"user_id" : user_id, "type": _type,"product_id":product_id,"quantity":quantity ,"price": price})
        conf = store.append(event)
    if conf == False:
        return {"status": "Fail."}, -1
    return {"status": f"Success. Order {order_id} placed."}, order_id

def transaction(order_id: int, product_id: int):
    store = EventStore()
    orderBook = OrderBook(product_id)
    my_order = orderBook.active_orders.get(order_id)
    for orderID, order in orderBook.active_orders.items():
        if order_id != orderID:
            if my_order.get("type") != order.get("type") and order.get("quantity") == my_order.get("quantity") and order.get("price") == my_order.get("price"):
                conf = False
                while conf == False:
                    event = Event(event_type=EventType.TradeExecuted, aggregate_type=AggregateType.OrderBook, aggregate_id=product_id,
                                  version= store.get_last_version(AggregateType.OrderBook, aggregate_id = product_id) + 1,
                                  data={"product_id":product_id,"order1_id":order_id, "order2_id": orderID})
                    conf = store.append(event)
                if conf == False:
                    pass
                seller = 0
                if my_order.get("type") == 1:
                    seller = order.get("user_id")
                else:
                    seller = my_order.get("user_id")
                conf = False
                while conf == False:
                    event = Event(event_type=EventType.FundsCredited, aggregate_type=AggregateType.Account, aggregate_id=seller,
                                  version=store.get_last_version(AggregateType.Account, aggregate_id = seller) + 1,
                                  data={"user_id":seller, "amount":my_order.get("price")})
                    conf = store.append(event)
                if conf == False:
                    pass
                break

def cancell_order(order_id: int, product_id: int):
    store = EventStore()
    orderBook = OrderBook(product_id)
    order = orderBook.active_orders.get(order_id)
    if order is None:
        return {"status": "Fail. Order not found."}
    account = Account(order.get("user_id"))
    if order.get("type") == 1:
        seller = order.get("user_id")
        conf = False
        while conf == False:
            event = Event(event_type=EventType.FundsCredited, aggregate_type=AggregateType.Account, aggregate_id=seller,
                          version=store.get_last_version(AggregateType.Account, aggregate_id=seller) + 1,
                          data={"user_id": seller, "amount": order.get("price")})
            conf = store.append(event)
        if conf == False:
            pass
    conf = False
    while conf == False:
        event = Event(event_type=EventType.OrderCancelled, aggregate_type=AggregateType.OrderBook, aggregate_id=product_id,
                      version=store.get_last_version(AggregateType.OrderBook, aggregate_id=product_id) + 1,
                      data={"order_id": order_id, "user_id": account.account_id, "type": order.get("type"),
                            "product_id": product_id,
                            "quantity": order.get("quantity"), "price": order.get("price")})
        conf = store.append(event)
    if conf == False:
        return {"status": "Fail."}
    return {"status": "Success. Order cancelled."}


def debit_funds(user_id: int, amount: int) -> Dict[str, str]:
    account = Account(user_id)
    store = EventStore()
    if account.balance < amount:
        return {"status": "Fail. Insufficient funds."}
    conf = False
    while conf == False:
        event = Event(event_type=EventType.FundsDebited, aggregate_type=AggregateType.Account, aggregate_id=user_id,
                      version=store.get_last_version(AggregateType.Account, aggregate_id=user_id) + 1,
                      data={"user_id": user_id, "amount": amount})
        conf = store.append(event)
    if not conf:
        return {"status": "Fail. Unable to debit funds."}
    return {"status": "Success. Funds debited."}


def credit_funds(user_id: int, amount: int) -> Dict[str, str]:
    account = Account(user_id)
    store = EventStore()
    conf = False
    while conf == False:
        event = Event(event_type=EventType.FundsCredited, aggregate_type=AggregateType.Account, aggregate_id=user_id,
                      version=store.get_last_version(AggregateType.Account, aggregate_id=user_id) + 1,
                      data={"user_id": user_id, "amount": amount})
        conf = store.append(event)
    if not conf:
        return {"status": "Fail. Unable to credit funds."}
    return {"status": "Success. Funds credited."}