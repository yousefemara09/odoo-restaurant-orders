from odoo.tests.common import TransactionCase


class TestOrder(TransactionCase):

    def setUp(self):
        super().setUp()
        self.test_order = self.env['restaurant.order'].create({
            'name': 'Test Order',
            'phone': '010000',
        })

        self.test_table = self.env['restaurant.table'].create({
            'name': 'Test table',
            'capacity': 10,
            'state': 'active',
        })

    def test_order_table_create(self):
        self.assertRecordValues(
            self.test_order,
            [{
                'name': 'Test Order',
                'phone': '010000',
                'state': 'draft',
            }]
        )

        self.assertRecordValues(
            self.test_table,
            [{
                'name': 'Test table',
                'capacity': 10,
                'state': 'active',
            }]
        )

    def test_order_confirm(self):
        self.test_order.table_id = self.test_table
        self.test_order.action_confirm()

        self.assertRecordValues(
            self.test_order,
            [{
                'name': 'Test Order',
                'state': 'confirmed',
            }]
        )

    def test_order_preparing(self):
        self.test_order.table_id = self.test_table
        self.test_order.action_confirm()
        self.test_order.action_preparing()
        self.assertRecordValues(
            self.test_order,
            [{
                'name': 'Test Order',
                'state': 'preparing',
            }]
        )

    def test_order_done(self):
        self.test_order.table_id = self.test_table
        self.test_table.state = 'active'
        self.test_order.action_confirm()
        self.test_order.action_done()
        self.assertRecordValues( self.test_order,
            [{
                'name': 'Test Order',
                'state': 'done',
            }]
        )

        self.assertRecordValues(
            self.test_table,
            [{
                'name': 'Test table',
                'state': 'active',
            }]
        )