from aggregates import OrderBook, Account
from store import EventStore
from event import AggregateType, EventType, Event


class App:
    def __init__(self):
        self.orderBooks = {}
        self.accounts = {}
        self.eventStore = EventStore()

    def replay(self):

        events = self.eventStore.get_all_events()
        for event in events:
            if event.aggregate_type == AggregateType.OrderBook:
                if self.orderBooks.get(event.aggregate_id, None) is None:
                    self.orderBooks[event.aggregate_id] = OrderBook(event.aggregate_id)
                self.orderBooks[event.aggregate_id].apply(event)
            else:
                if self.accounts.get(event.aggregate_id, None) is None:
                    self.accounts[event.aggregate_id] = Account(event.aggregate_id)
                self.accounts[event.aggregate_id].apply(event)
        print("ACCOUNTS")
        print()
        print()
        for account in self.accounts.values():
            print("Account of user : " + str(account.account_id) + "\n")
            print("Balance of user : " + str(account.balance) + "\n")
            print()
        print()
        print()
        print("ORDERBOOKS")
        print()
        print()
        for orderBook in self.orderBooks.values():
            print("OrderBook of product : " + str(orderBook.aggregate_id) + "\n")
            print("Active orders:")
            print(orderBook.active_orders)
            print("Cancelled orders:")
            print(orderBook.cancelled_orders)
            print("Successful transactions: ")
            print(orderBook.successful_transactions)
            print()
