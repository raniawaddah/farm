# -*- coding: utf-8 -*-
{
    'name': "Farm System",

    'summary': """
       Farm System
    """,

    'description': """
        Farm Sysyem
    """,

    'author': "Rania",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/customer.xml',
        'views/products.xml',
        'reports/customer_report.xml',
        'reports/stock_picking.xml',
        'views/sale_inherit.xml',

    ],
    'installable':True,
    'application':True,
    'auto_install':False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
