from odoo import fields, models


class SalesInheritance(models.Model):

    _inherit = 'sale.order'
    customer_po_number = fields.Char(string="Customer PO Number")
    reason = fields.Char(string="Reason")

    state = fields.Selection(
        selection_add = [
        ('waiting_manager', 'Waiting Manager')
    ])

    def action_send_to_manager(self):
        for order in self:
            order.state = 'waiting_manager'

    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Order',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'cancel.sale',
            'context': {
                'default_order_id':self.id
            }
        }