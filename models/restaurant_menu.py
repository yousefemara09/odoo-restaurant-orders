from odoo import fields, models


class RestaurantMenu(models.Model):
    _name = 'restaurant.menu'
    _description = 'Restaurant Menu'

    name = fields.Char(required=True)
    price = fields.Float(required=True)
    description = fields.Text(required=True)
    active = fields.Boolean(default=True)