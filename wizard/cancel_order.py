from odoo import fields, models


class CancelOrder(models.TransientModel):
    _name = 'cancel.order'
    _description = 'Cancel Order'

    reason = fields.Selection([
        ('customer', 'Customer Request'),
        ('out_of_stock', 'Out of Stock'),
        ('other', 'Other'),
    ], string="Cancel Reason")

    note = fields.Text(string="Cancel Note")


    def action_confirm(self):
        order = self.env["restaurant.order"].browse(
            self.env.context.get("active_id")
        )
        order.write({
            'cancel_reason': self.reason,
            'cancel_note': self.note,
            'state':'cancel'
        })