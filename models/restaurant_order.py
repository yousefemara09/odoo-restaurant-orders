from odoo.exceptions import ValidationError
from odoo import fields, models , api

class RestaurantOrder(models.Model):
    _name = 'restaurant.order'
    _description = 'Restaurant Order'
    _inherit = ['mail.thread','mail.activity.mixin']


    ref = fields.Char(default='order', readonly=True)
    name = fields.Char(required=True)
    phone = fields.Char(string="Phone")
    order_date = fields.Datetime(string='Order Date',default=fields.Datetime.now)
    table_id = fields.Many2one("restaurant.table",string="Table")
    line_ids = fields.One2many("restaurant.line","order_id",string="Order Lines" )
    total = fields.Float(string="Total", compute="_compute_total",store=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('preparing', 'Preparing'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],default="draft", tracking=True)

    cancel_reason = fields.Selection([
        ('customer', 'Customer Request'),
        ('out_of_stock', 'Out of Stock'),
        ('other', 'Other'),
    ], string="Cancel Reason")

    cancel_note = fields.Text(string="Cancel Note")

    def action_draft(self):
        for record in self:
            record.state = 'draft'
            record.message_post(
                body=f"Order is {record.state}"
            )

    def action_preparing(self):
        for record in self:
            record.state = 'preparing'
            record.message_post(
                body=f"Order is {record.state}"
            )

    def action_done(self):
        for record in self:
            record.state = 'done'
            record.table_id.state = 'active'
            record.message_post(
                body=f"Order is {record.state}"
            )

    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Order',

            'res_model': 'cancel.order',
            'view_mode': 'form',
            'context': {
                'default_order_id': self.id
            },
            'target': 'new',
        }

    def action_confirm(self):
        for record in self:
            if record.table_id.state == 'occupied':
                raise ValidationError(
                    "You cannot confirm this order because the table is occupied."
                )
            record.state = 'confirmed'
            record.table_id.state = 'occupied'

            record.message_post(
                body=f"Order is {record.state}"
            )

            record.activity_schedule(
                'mail.mail_activity_data_todo',
                summary='Prepare Restaurant Order',
                note=f'Please prepare order {record.ref}.'
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'order') == 'order':
                vals['ref'] = self.env['ir.sequence'].next_by_code('restaurant_order')
        return super().create(vals_list)

    @api.onchange('table_id')
    def _onchange_table(self):
        if self.table_id:
            if self.table_id.state == 'occupied':
                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'This table is already occupied'
                    }
                }
    @api.depends('line_ids.price')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped('price'))

    @api.model
    def cron_actions(self):
        states = self.env['restaurant.order'].search([
            ('state', '=', 'confirmed')
        ])
        for order in states:
            order.action_preparing()

    def server_actions(self):
        for order in self.filtered(lambda o: o.state == 'draft'):
            order.action_confirm()

class RestaurantLine(models.Model):
    _name = 'restaurant.line'
    _description = 'Restaurant Line'

    order_id = fields.Many2one( "restaurant.order", string="Order")
    menu_id = fields.Many2one("restaurant.menu",string="Food")
    quantity = fields.Integer(default=1)
    price = fields.Float()

    @api.onchange("menu_id" , "quantity")
    def _onchange_price(self):
        self.price = self.menu_id.price * self.quantity

    @api.constrains('price')
    def positive_total(self):
       for record in self:
           if record.price <= 0:
               raise ValidationError("Price must be positive")


