from odoo import http
import logging
from odoo.http import request
from datetime import datetime, date
from odoo.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class OpenfoodHome(Website):
    @http.route(auth='public')
    def index(self, data={}, **kw):
        website_theme = ''
        try:
            website_id = request.session.force_website_id
            website = http.request.env['website'].sudo().browse(
                int(website_id))
            website_theme = website.theme_id.name
        except:
            pass

        if website_theme == 'openfood_theme':
            shippings = []
            if not request.env.user._is_public():
                order = request.website.sale_get_order(force_create=1)
                if order.partner_id != request.website.user_id.sudo().partner_id:
                    _logger.info("ONEEEEE")
                    Partner = order.partner_id.with_context(
                        show_address=1).sudo()
                    shippings = Partner.search([
                        ("id", "child_of", order.partner_id.commercial_partner_id.ids),
                        '|', ("type", "in", ["delivery", "other"]), ("id",
                                                                     "=", order.partner_id.commercial_partner_id.id)
                    ], order='id desc')
                    if shippings and not order.partner_shipping_id:
                        _logger.info("TWOO")
                        last_order = request.env['sale.order'].sudo().search(
                            [("partner_id", "=", order.partner_id.id)], order='id desc', limit=1)
                        order.partner_shipping_id.id = last_order and last_order.id
                data['order'] = order
                data['only_services'] = request.website.user_id.sudo().partner_id

            data['shippings'] = shippings
            data['cst_website'] = True

            super(OpenfoodHome, self).index(**kw)
            _logger.info(data)
            return request.render("website.openfood_homepage", data)

        return super(OpenfoodHome, self).index(**kw)

    @http.route('/openfood', type='http', auth='public', website=True)
    def indexof(self, data={}, **kw):
        data['is_public'] = request.env.user._is_public()

        data['cst_website'] = True

        OpenfoodHome.index(self, data={}, **kw)
        return request.render("website.openfood_homepage", data)
