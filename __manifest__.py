{
    'name': 'Restaurant App',
    'author': 'Yousef Ibrahim',
    'version': '17.0.0.1.0',
    'category': 'Services/Restaurant',
    'depends': [
        'base', 'mail' , 'sale_management'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/cancel_order.xml',
        'wizard/sales_order.xml',
        'views/base_menu.xml',
        'views/restaurant_table.xml',
        'views/restaurant_menu.xml',
        'views/restaurant_order.xml',
        'views/sales_inhert.xml',
        'reports/order_report.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
