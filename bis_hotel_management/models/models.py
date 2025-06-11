# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.account.tools.certificate import load_key_and_certificates


class HotelManagement(models.Model):
    _name = 'hotel.management'
    _description = 'Hotel Management'

    name = fields.Char(string='Hotel Name', required=True)


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    _order = 'name asc, sequence desc, hotel_id asc'
    # _constraints = [
    #     'sequence', 'name',
    # ]

    sequence = fields.Integer(string='Hotel Room Sequence', required=True)
    name = fields.Char(string='Hotel Room Name', required=True)
    hotel_id = fields.Many2one('hotel.management', string='Hotel', required=True)

    @api.onchange('hotel_id')
    def _onchange_hotel_id(self):
        sequence = self.env['hotel.room'].search(['|',('name','=', 'room1'),('name','=', 'room2'),('sequence', '!=', False)])
        print(sequence)

        # select phone from user where phone like '%7260%' like
        # select constant(phone) from user where phone like '%7260%' ilike

        # select id from hotel_room where (name = 'room1' or name = 'room2' or sequence != False)
        for room in self:
            if room.hotel_id:
                room.sequence = len(sequence) + 3


class CustomerManagement(models.Model):
    _name = 'customer.management'
    _description = 'Customer Management'

    # customer = fields.Many2one(string='Customer', co_model='res.partner', domain=[('is_customer', '=', True)], required=True)
    rooms = fields.Many2many('hotel.room', string='Rooms', required=True)
    address = fields.Char(string='Address', required=True)
    sub_district = fields.Char(string='Sub District', required=True)
    district = fields.Char(string='District', required=True)
    province = fields.Char(string='Province', required=True)
    zipcode = fields.Char(string='Zip Code', required=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # _description = 'Sale Order'

    new_name = fields.Char(string='Sale Order Name', required=True)

# class HotelRoom(models.Model):
#     _name = 'hotel.room'
#     _description = 'Hotel Room'
#
#     name = fields.Char(string='Sale Order Name', required=True)
#     new_name = fields.Char(string='Sale Order Name', required=True)