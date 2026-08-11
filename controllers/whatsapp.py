from odoo import http
from odoo.http import request


class WhatsappController(http.Controller):

    @http.route('/whatsapp/webhook', methods=['POST'], type='http', auth='public', csrf=False)
    def whatsapp_webhook(self):

        vals = request.get_json_data()

        if not vals:
            return request.make_json_response({
                'status': 'error',
                'message': 'No data found'
            }, status=400)

        if not vals.get('name') or not vals.get('phone'):
            return request.make_json_response({
                'status': 'error',
                'message': 'Name or phone number not found'
            }, status=400)

        if not vals.get('items'):
            return request.make_json_response({
                'status': 'error',
                'message': 'No items found'
            }, status=400)

        menu_by_name = {}

        for line in vals['items']:

            menu_name = line.get('menu')
            quantity = line.get('quantity')

            if not menu_name:
                return request.make_json_response({
                    'status': 'error',
                    'message': 'Menu is required'
                }, status=400)

            if not quantity or quantity <= 0:
                return request.make_json_response({
                    'status': 'error',
                    'message': 'Quantity should be greater than 0'
                }, status=400)

            menu_food = request.env['restaurant.menu'].sudo().search(
                [('name', '=', menu_name)],
                limit=1
            )

            if not menu_food:
                return request.make_json_response({
                    'status': 'error',
                    'message': f'Food {menu_name} not found'
                }, status=404)

            menu_by_name[menu_name] = menu_food

        try:
            data_info = request.env['restaurant.order'].sudo().create({
                'name': vals['name'],
                'phone': vals['phone'],
            })

            ordered_items = []

            for line in vals['items']:
                menu_food = menu_by_name[line['menu']]
                request.env['restaurant.line'].sudo().create({
                    'order_id': data_info.id,
                    'menu_id': menu_food.id,
                    'quantity': line['quantity'],
                    'price': line['quantity'] * menu_food.price,
                })
                ordered_items.append(menu_food.name)

            # total is a stored computed field (depends on line_ids.price);
            # it recomputes automatically once the lines above are created.
            data_info.action_confirm()

            return request.make_json_response({
                'status': 'success',
                'data': data_info.id,
                'order_id': data_info.id,
                'items': ordered_items,
                'total': data_info.total,
            }, status=200)

        except Exception as e:
            return request.make_json_response({
                'status': 'error',
                'message': str(e),
            }, status=400)