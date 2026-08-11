from odoo import fields, models , api
class RestaurantTable(models.Model):
    _name = 'restaurant.table'
    _description = 'Restaurant Table'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(required=True)
    number = fields.Integer()
    capacity = fields.Integer(required=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ], default='active', tracking=True)

    count_orders = fields.Integer(default=0, compute='_compute_count_orders')

    order_ids = fields.One2many(
        "restaurant.order",
        "table_id",
        string="Orders"
    )

    _sql_constraints = [
        ('table_number_uniq', 'unique(number)', "Should use only one table"),
    ]

    @api.depends('order_ids')
    def _compute_count_orders(self):
        for table in self:
            table.count_orders = len(table.order_ids)

    def action_view_orders_smart_button(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant.order',
            'view_mode': 'tree',
            'domain': [('table_id', '=' , self.id)]
        }

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            record.message_post(body=f"New Table Created: {record.name}")

        return records
