# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class BISController(http.Controller):
    @http.route('/bis-hello', auth='public')
    def bis_hello(self, **kw):
        return "Hello, world"

    @http.route('/hotel/room', type='http', medthod=['GET'], auth='user', csrf=True)
    def get_hotel_room(self, **kw):
        room = []
        list_room = request.env['hotel.room'].sudo().search([])
        for r in list_room:
            r_list = {
                'id': r.id,
                'name': r.name,
                'description': r.description,
            }
            room.append(r_list)

        return request.make_json_response(data={
            'status': 200,
            'room': room,
            'message': 'Response 200 OK'
        }, status=200)


    @http.route('/hotel/room/create', type='http', medthod=['POST'], auth='public', csrf=False)
    def post_hotel_room(self, **kwargs):
        room = request.env['hotel.room'].sudo()
        request_data = request.get_json_data()
        create_room = room.create(request_data)
        return request.make_json_response(data={
            'status': 201,
            'room': create_room,
            'message': 'Response 201 Created'
        }, status=201)

    @http.route('/hotel/room/update', type='http', medthod=['PUT'], auth='user', csrf=False)
    def update_hotel_room(self, **kwargs):
        request_data = request.get_json_data()
        try:
            room = request.env['hotel.room'].sudo().search([('id', '=', request_data.get('id'))])
            if room:
                data = {
                    'sequence': request_data.get('sequence'),
                    'name': request_data.get('name'),
                    'description': request_data.get('description'),
                }
                room.update(data)
                return request.make_json_response(data={
                    'status': 200,
                    'room': room,
                    'message': 'Response 200 OK'
                })
            else:
                data = {
                    'sequence': request_data.get('sequence'),
                    'name': request_data.get('name'),
                    'description': request_data.get('description'),
                }
                create_room = room.create(data)

                return request.make_json_response(data={
                    'status': 201,
                    'room': create_room,
                    'message': 'Response 201 Created'
                }, status=201)

        except Exception as e:
            return request.make_json_response(data={'error': e}, status=500)

    @http.route('/hotel/room/delete', type='http', medthod=['DELETE'], auth='public', csrf=False)
    def post_hotel_room(self, **kwargs):
        request_data = request.get_json_data()
        room = request.env['hotel.room'].sudo().search([('id', '=', request_data.get('id'))])
        room.unlink()
        return request.make_json_response(data={
            'status': 204,
            'room': [],
            'message': 'Response 204 No Content'
        }, status=204)

    @http.route('/rooms', type='http', auth='public', website=True, csrf=False)
    def get_website_room(self, **kwargs):
        rooms = request.env['hotel.room'].sudo().search([], order='id asc')
        return request.render(
            'bis_hotel_management.website_hotel_room_list_page', {
            'rooms': rooms
        })

    @http.route('/rooms/<int:room_id>', type='http', auth='public', website=True, csrf=False)
    def get_website_room_by_id(self, room_id=1, **kwargs):
        rooms = request.env['hotel.room'].sudo().search([('id', '=', room_id)], order='id asc', limit=1)
        if rooms:
            return request.render(
                'bis_hotel_management.website_hotel_room_with_id_page', {
                'room_id': rooms.id,
                'sequence': rooms.sequence,
                'name': rooms.name,
                'description': rooms.description
            })
        else:
            return request.render('website.page_404', {})


    # @http.route('/report/<int:sale_id>', type='http', auth='public', csrf=False)
    # def get_hotel_room_by_id(self, sale_id, **kwargs):



    # Other API With Post JSON Data
    @http.route('/hotel/room/create', auth='none', type='json')
    def post_create_hotel_room(self, **post):
        request.session.db = 'bis_dev'
        request_data = request.get_json_data()
        try:
            room = request.env['hotel.room'].sudo()

            room.create(request_data)
            # return request.make_json_response(data={'message': 'Create Success'}, status=201)
            return {
                'message': 'Created',
                'id': room.id,
                'status': 201
            }
        except Exception as e:
            return request.make_json_response(data={'error': e}, status=500)
