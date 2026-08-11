from odoo import fields, models


class SalesWizard(models.TransientModel):

    _name = 'cancel.sale'

    reason = fields.Char(string='Reason')
    order_id = fields.Many2one(
        'sale.order',
        string='Sales Order'
    )

    def action_confirmed(self):
        order = self.env["sale.order"].browse(
            self.env.context.get("active_id")
        )
        order.write({
            'reason':self.reason,
        })