# -*- coding: utf-8 -*-
{
    'name': "custom_module",
    'version': '1.0',
    'author': 'Adham',
    'summary': "Custom Module",
    'description': 
    """
A custom module to extend some functionalities
    """,
    'website': "https://www.adham.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_attendance', 'hr_holidays', 'sale', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/multi_sale_order_views.xml',
        'views/hr_attendance_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_attendance_absence_views.xml',
        'views/account_move_line_views.xml',
        'views/purchase_order_discount_views.xml',
        'data/absence_cron.xml',
        'data/reset_cron.xml',
        'demo/attendance_absence_demo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

