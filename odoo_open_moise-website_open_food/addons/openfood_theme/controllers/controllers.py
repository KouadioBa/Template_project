from odoo import http
import logging
from odoo.http import request
from datetime import datetime, date

_logger = logging.getLogger(__name__)


class WebsiteControler(http.Controller):
    @http.route('/website-restriction-country', type='http', auth='public', website=True, csrf=False)
    def get_website_restriction(self, **post):
        try:
            http.request.cr.execute(
                "SELECT country_group_id FROM website_country_group_rel WHERE website_id=%d" % (
                    int(post.get('website_id')))
            )
            wbst_country_groups = http.request.cr.fetchall()

            all_country_codes = ''

            for country_group in wbst_country_groups:
                group_ids = http.request.env['res.country.group'].sudo().browse(
                    country_group)
                country_codes = ''
                for country_id in group_ids.country_ids:
                    country_codes = country_codes + str(country_id.code) + ';'
                all_country_codes = all_country_codes + country_codes

            return all_country_codes

        except:
            return "Erreur!"

    @http.route('/partner-adress', type='http', auth='public', website=True, csrf=False)
    def get_partner_adress(self, **post):
        try:
            order = request.website.sale_get_order()

            redirection = self.checkout_redirection(order)
            if redirection:
                return redirection

            if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
                return request.redirect('/shop/address')

            for f in self._get_mandatory_billing_fields():
                if not order.partner_id[f]:
                    return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)

            values = self.checkout_values(**post)

            if post.get('express'):
                return request.redirect('/shop/confirm_order')

            values.update({'website_sale_order': order})
        except:
            return "Erreur!"
