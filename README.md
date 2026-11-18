# Restaurant Order Management (Odoo 17)

An Odoo 17 module for restaurant tables, menu items, and orders, with a state workflow, automation, a WhatsApp webhook, and an extension of Odoo Sales.

> Technical module name: `restaurant_app`.

## Features

- **Tables, menu, and orders** (with order lines and computed totals).
- **Order workflow:** `Draft → Confirmed → Preparing → Done / Cancelled`, with chatter messages on every transition and table-status updates (a confirmed order marks its table occupied).
- **Cancellation wizard.**
- **Automation**
  - A daily scheduled action (`ir.cron`) moves confirmed orders to *Preparing*.
  - A bulk **Confirm** server action for draft orders.
- **WhatsApp webhook:** `POST /whatsapp/webhook` creates an order from JSON, removing manual entry.

  ```json
  { "name": "Ahmed", "phone": "01000000000",
    "items": [ { "menu": "Pizza", "quantity": 2 } ] }
  ```

  It validates the payload and returns `400` / `404` JSON errors for missing fields or unknown menu items.
- **Sales extension** (`sale.order`): adds a *Waiting Manager* state, a Customer PO number, and a cancellation wizard that stores the reason.
- **Security:** `Manager` and `Waiter` groups; waiters see only the orders they created (record rule).
- **QWeb PDF report** for orders.
- **Unit tests** (`TransactionCase`).

## Stack

Python · XML · PostgreSQL · `mail` · `sale_management` · QWeb

## Installation

1. Copy this folder into your Odoo `addons` directory as `restaurant_app`.
2. Update the apps list and install **Restaurant App**.

## Author

Yousef Ibrahim — [GitHub](https://github.com/yousefemara09) · [LinkedIn](https://www.linkedin.com/in/yousef-ibrahim-148b48240/)
