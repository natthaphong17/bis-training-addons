# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.account.tools.certificate import load_key_and_certificates
from datetime import datetime
from odoo.exceptions import AccessError, UserError, ValidationError

class HotelManagement(models.Model):
    _name = 'hotel.management'
    _description = 'Hotel Management'

    name = fields.Char(string='Hotel Name', required=True)


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _order = 'name asc, sequence desc, hotel_id asc'
    # _constraints = [
    #     'sequence', 'name',
    # ]

    sequence = fields.Integer(string='Hotel Room Sequence', default=1, required=True)
    name = fields.Char(string='Hotel Room Name', required=True)
    description = fields.Char(string='Hotel Room Description', required=False)
    hotel_id = fields.Many2one('hotel.management', string='Hotel', required=True)
    booking_date = fields.Date(string='Hotel Booking Date', default=datetime.now(), required=True)
    checkin_date = fields.Date(string='Hotel Checkin Date', default=datetime.now(), required=True)
    checkout_date = fields.Date(string='Hotel Checkout Date', default=datetime.now(), required=True)
    status_booking = fields.Selection([('draft','Draft'),('booking','Booking'),
                                       ('checkin','Checkin'),('checkout','Checkout'),
                                       ('cancel','Cancel')], default='draft')


    # @api.onchange('hotel_id')
    # def _onchange_hotel_id(self):
    #     sequence = self.env['hotel.room'].search([('sequence', '>=', 1)])
    #     print(sequence)
    #
    #     # select phone from user where phone like '%7260%' like
    #     # select constant(phone) from user where phone like '%7260%' ilike
    #
    #     # select id from hotel_room where (name = 'room1' or name = 'room2' or sequence != False)
    #     for room in self:
    #         if room.hotel_id:
    #             room.sequence = len(sequence) + 9

    def generate_sequence(self):
        sequence = self.env['hotel.room'].search([('sequence', '>=', 1)])
        print(sequence)

        # select phone from user where phone like '%7260%' like
        # select constant(phone) from user where phone like '%7260%' ilike

        # select id from hotel_room where (name = 'room1' or name = 'room2' or sequence != False)
        for room in self:
            if room.hotel_id:
                room.sequence = len(sequence) + 9


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


class HotelOrder(models.Model):
    _name = 'hotel.order'
    _inherit = 'hotel.room'
    # _description = 'Sale Order'

    order_name = fields.Char(string='Order Name', required=True)
    customer_id = fields.Many2one('customer.management', string='Customer', required=True)


class HotelRoomInherit(models.Model):
    _inherit = 'hotel.room'

    note = fields.Text(string='Note', required=True)
    casher_id = fields.Many2one('res.partner', string='Casher', required=True)


    def generate_sequence(self):
        res = super(HotelRoomInherit, self).generate_sequence()
        print('Hello Customer')
        sequence = self.env['hotel.room'].search([('sequence', '=', 1)])
        if len(sequence) == 1:
            print('Inherit: ',len(sequence))
            for room in self:
                room.sequence = len(sequence) + 1
                # return False
        else:
            return res

    # def sql_query(self):
    #     query = f"""
    #                 SELECT id, sequence, name
    #                 FROM hotel_room
    #                 WHERE sequence > {self.sequence}
    #             """
    #     print(query)
    #
    #     vals = ["id", "sequence", "name"]
    #
    #     self.env.cr.execute(query, vals)
    #     print(vals)
    #
    #     room = self.env.cr.fetchall()
    #     for r in room:
    #         print("======================================================")
    #         print("ID: %s" % r[0])
    #         print("Sequence: %s" % r[1])
    #         print("Name: %s" % r[2])
    #         print("======================================================")
    #
    #     if len(room) == 1:
    #         raise ValidationError(_("room: %s" % room))
    #     if len(room) > 1:
    #         raise ValidationError(_("room: %s" % room))
    #     else:
    #         raise ValidationError(_("No room"))

    # @api.onchange('hotel_id')
    # def _onchange_hotel_id(self):
    #     if self.hotel_id:
    #         if self.booking_date:
    #             raise ValidationError(_("booking_date: %s" % self.booking_date))
    #         else:
    #             raise ValidationError(_("booking_date: %s" % self.booking_date))
            # raise ValidationError(_("โรงแรมที่คุณเลือกคือ: %s" % self.hotel_id.name))

    def open_wizard(self):
        wizard = self.env.ref('bis_hotel_management.hotel_room_wizard')
        return {
            'name': _('Room Wizard'),
            'res_model': 'hotel.room.wizard',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'context': {'default_hotel_id': self.hotel_id.id,'default_name': self.name},
            'target': 'new',
        }
