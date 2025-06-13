# -*- coding: utf-8 -*-
{
    'name': "BIS Hotel Management",

    'summary': "BIS Hotel Management",

    'description': """
BIS Hotel Management
    """,

    'author': "BIS",
    'website': "https://www.bis.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Marketing',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/room_views.xml',
        'wizard/hotel_room_wizard.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

