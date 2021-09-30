from odoo import http
import logging
import pprint
import werkzeug
from odoo import http
from odoo.http import request
import json
from datetime import datetime
from datetime import date

_logger = logging.getLogger(__name__)


class DriverControler(http.Controller):
    # accepter ou refuser un bon de livraison
    @http.route('/driver-assignment-action', type='http', auth='public', website=True, csrf=False)
    def accept_refuse_assignment(self, **post):
        action_type = post.get('action_type')
        picking_order = http.request.env['picking.order'].sudo().browse(
            int(post.get('picking_id')))

        try:
            if action_type == 'accept':
                picking_order.update({'state': 'accepted'})
                return "accepted"
            elif action_type == 'collect':
                picking_order.update({'state': 'collected'})
                return "collected"
            elif action_type == 'deliver':
                picking_order.write({'state': 'delivered'})
                return "delivered"
            elif action_type == 'reject':
                picking_order.update({'state': 'rejected'})
                return "rejected"
            elif action_type == 'checkstate':
                return picking_order.state
        except:
            return "Erreur!"

    @http.route('/confirm-delivery-step', type='http', auth='public', website=True, csrf=False)
    def confirm_delivery_step(self, **post):
        sale_order = http.request.env['sale.order'].sudo().browse(
            int(post.get('order_id')))
        try:
            if sale_order.delivery_state == 'accepted':
                sale_order.update({'delivery_state': 'taken'})
                return "Commande recupérée !"

            elif sale_order.delivery_state == 'taken':
                sale_order.update({'delivery_state': 'delivered'})
                return "Commande livré !"
            else:
                return sale_order.delivery_state
        except:
            return "Erreur!"

    @http.route('/confirm-delivery-step', type='http', auth='public', website=True, csrf=False)
    def confirm_delivery_step(self, **post):
        sale_order = http.request.env['sale.order'].sudo().browse(
            int(post.get('order_id')))
        try:
            if sale_order.delivery_state == 'accepted':
                sale_order.update({'delivery_state': 'taken'})
                return "Commande recupérée !"

            elif sale_order.delivery_state == 'taken':
                sale_order.update({'delivery_state': 'delivered'})
                return "Commande livré !"
            else:
                return sale_order.delivery_state
        except:
            return "Erreur!"
