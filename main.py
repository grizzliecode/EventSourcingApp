import command_handler
from event import Event, EventType, AggregateType
from  store import EventStore
from aggregates import OrderBook, Account
import argparse
from replay import App

def main():
    parser = argparse.ArgumentParser(description='Event Sourcing Trading System CLI.')
    subparsers = parser.add_subparsers(dest='command')

    place_order_parser = subparsers.add_parser("place_order", help="Place an order")
    place_order_parser.add_argument("user_id", type=int, help="User ID placing the order")
    place_order_parser.add_argument("order_type", type=int, choices=[0, 1], help="Order type: 0 (sell), 1 (buy)")
    place_order_parser.add_argument("product_id", type=int, help="Product ID for the order")
    place_order_parser.add_argument("quantity", type=int, help="Quantity of the product")
    place_order_parser.add_argument("price", type=int, help="Price per unit")

    cancel_order_parser = subparsers.add_parser("cancel_order", help="Cancel an order")
    cancel_order_parser.add_argument("order_id", type=int, help="Order ID to cancel")
    cancel_order_parser.add_argument("product_id", type=int, help="Product ID for the order being cancelled")

    credit_funds_parser = subparsers.add_parser("credit_funds", help="Credit funds to a user account")
    credit_funds_parser.add_argument("user_id", type=int, help="User ID to credit funds to")
    credit_funds_parser.add_argument("amount", type=int, help="Amount to credit")

    debit_funds_parser = subparsers.add_parser("debit_funds", help="Debit funds from a user account")
    debit_funds_parser.add_argument("user_id", type=int, help="User ID to debit funds from")
    debit_funds_parser.add_argument("amount", type=int, help="Amount to debit")

    replay_parser = subparsers.add_parser("replay", help="Replay all the events.")

    args = parser.parse_args()

    if args.command == "place_order":
        response, order_id = command_handler.place_order(args.user_id, args.order_type, args.product_id, args.quantity, args.price)
        print(response)
        if order_id != -1:
            command_handler.transaction(order_id, args.product_id)
    elif args.command == "cancel_order":
        order_book = OrderBook(args.product_id)
        if args.order_id in order_book.active_orders:
            response = command_handler.cancell_order(args.order_id, args.product_id)
            print(response)
        else:
            print(f"Order {args.order_id} not found.")
    elif args.command == "credit_funds":
        response = command_handler.credit_funds(args.user_id, args.amount)
        print(response)
    elif args.command == "debit_funds":
        response = command_handler.debit_funds(args.user_id, args.amount)
        print(response)
    elif args.command == "replay":
        app = App()
        app.replay()
    else:
        print("Unknown command.")

if __name__ == '__main__':
    main()