from odoo import http
import logging
import pprint
import werkzeug
from odoo import http
from odoo.http import request
import json
from datetime import datetime
from datetime import date
from odoo.addons.website.controllers.main import Website
from odoo.addons.web.controllers.main import Home
from odoo.addons.pragmatic_odoo_delivery_boy.controllers.main_driver import WebsiteDeliveryControlAppDriver


class OpenLivreurWebsite(Website):
    # page d'accueil
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

        if website_theme == 'open_livreur_theme':
            super(Website, self).index(**kw)
            if request.env.user._is_public():
                return request.render("pragmatic_odoo_delivery_boy.logged_in_template")

            if request.env.user.has_group('pragmatic_delivery_control_app.group_delivery_control_app_manager'):
                return request.redirect('/page/manage/delivery')

            elif request.env.user.has_group('pragmatic_delivery_control_app.group_delivery_control_app_user'):
                return request.redirect('/page/job/list')
        else:
            return super(OpenLivreurWebsite, self).index(**kw)


class OpenLivreurHome(Home):
    @http.route(auth='public')
    def web_login(self, redirect=None, **kw):
        website_theme = ''
        try:
            website_id = request.session.force_website_id
            website = http.request.env['website'].sudo().browse(
                int(website_id))
            website_theme = website.theme_id.name
        except:
            pass

        if website_theme == 'open_livreur_theme':
            super(OpenLivreurHome, self).web_login(**kw)
            data = {
                'wbst': "sucess"
            }
            return request.render("open_livreur_theme.login_page", data)
        else:
            return super(OpenLivreurHome, self).web_login(**kw)


class DeliveryAssignment(WebsiteDeliveryControlAppDriver):
    # administration des commandes
    @http.route(auth='public')
    def manage_sale_order_delivery(self, page=0, search='', opg=False, domain=None, **post):
        website_theme = ''
        try:
            website_id = request.session.force_website_id
            website = http.request.env['website'].sudo().browse(
                int(website_id))
            website_theme = website.theme_id.name
        except:
            pass

        if website_theme == 'open_livreur_theme':
            # super(DeliveryAssignment, self).manage_sale_order_delivery(**post)
            # data = {
            #     'wbst': "sucess"
            # }
            # return request.render("open_livreur_theme.login_page", data)
            return super(DeliveryAssignment, self).manage_sale_order_delivery(**post)
        else:
            return super(DeliveryAssignment, self).manage_sale_order_delivery(**post)

    # tableau de bord du livreur
    @http.route(auth='public')
    def job_list_website(self, page=0, search='', opg=False, domain=None, **kwargs):
        website_theme = ''
        try:
            website_id = request.session.force_website_id
            website = http.request.env['website'].sudo().browse(
                int(website_id))
            website_theme = website.theme_id.name
        except:
            pass

        if website_theme == 'open_livreur_theme':
            picking_orders = request.env['picking.order'].search([
                ('delivery_boy', '=', request.env.user.partner_id.id)
            ])
            assigned_pickings = request.env['picking.order'].search([
                ('delivery_boy', '=', request.env.user.partner_id.id),
                ('state', '=', 'assigned'),
            ])
            accepted_pickings = request.env['picking.order'].search([
                ('delivery_boy', '=', request.env.user.partner_id.id),
                ('state', '=', 'accepted')
            ])
            collected_pickings = request.env['picking.order'].search([
                ('delivery_boy', '=', request.env.user.partner_id.id),
                ('state', '=', 'collected'),
            ])
            delivered_pickings = request.env['picking.order'].search([
                ('delivery_boy', '=', request.env.user.partner_id.id),
                ('state', '=', 'delivered'),
            ])
            data = {
                'picking_orders': picking_orders,
                'assigned_pickings': assigned_pickings,
                'accepted_pickings': accepted_pickings,
                'collected_pickings': collected_pickings,
                'delivered_pickings': delivered_pickings
            }

            # clé d'api maps
            api_key = http.request.env['ir.config_parameter'].sudo().search(
                [('key', '=', 'google.api_key_geocode')]
            )
            if len(api_key) == 1:
                data['maps_script_url'] = "//maps.google.com/maps/api/js?key=" + \
                    api_key.value + "&amp;libraries=places&amp;language=en-AU"
            else:
                data['maps_script_url'] = "//maps.google.com/maps/api/js?key=&amp;libraries=places&amp;language=en-AU"

            return request.render("open_livreur_theme.joblist", data)

        else:
            return super(DeliveryAssignment, self).job_list_website(**kwargs)
