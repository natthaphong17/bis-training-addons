# -*- coding: utf-8 -*-
# from odoo import http


# class ./custom-addons/bis-hotel-management(http.Controller):
#     @http.route('/./custom-addons/bis-hotel-management/./custom-addons/bis-hotel-management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./custom-addons/bis-hotel-management/./custom-addons/bis-hotel-management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./custom-addons/bis-hotel-management.listing', {
#             'root': '/./custom-addons/bis-hotel-management/./custom-addons/bis-hotel-management',
#             'objects': http.request.env['./custom-addons/bis-hotel-management../custom-addons/bis-hotel-management'].search([]),
#         })

#     @http.route('/./custom-addons/bis-hotel-management/./custom-addons/bis-hotel-management/objects/<model("./custom-addons/bis-hotel-management../custom-addons/bis-hotel-management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./custom-addons/bis-hotel-management.object', {
#             'object': obj
#         })

