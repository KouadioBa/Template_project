# -*- encoding: utf-8 -*-

{
    'name': 'Thème Open Livreur',
    'category': 'Theme',
    'author': 'Willof-God Bassanti',
    'version': '1.0',
    'depends': ['website','website_theme_install','sale','pragmatic_odoo_delivery_boy'],
    'data': [
        'static/src/views/driver_job_list.xml',
        'static/src/views/header_footer.xml',
        # 'static/src/views/shipping_details.xml',
        # 'static/src/views/driver_calendar_menu.xml',
        # 'static/src/views/login.xml',
        'views/payment_mode.xml',
        'views/views.xml',
        'views/inherits.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
}
