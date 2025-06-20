# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.account.tools.certificate import load_key_and_certificates
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class HotelManagement(models.Model):
    _name = 'hotel.management'
    _description = 'Hotel Management'

    name = fields.Char(string='Hotel Name', required=True)

class HotelAccessories(models.Model):
    _name = 'hotel.accessories'

    name = fields.Char(string='Accessories Name', required=True)
    color = fields.Char(string='Accessories Color', required=False)


# class ResUser(models.Model):
#     _inherit = 'res.user'
#
#     partner_access = fields.Boolean(default=False)


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _order = 'name asc, sequence desc, hotel_id asc'
    # _constraints = [
    #     'sequence', 'name',
    # ]

    user_access = fields.Boolean(default=False)
    company_id = fields.Many2one('res.company', string='Company', compute="_get_company_data", required=True)
    sequence = fields.Integer(string='Hotel Room Sequence', default=1, required=True)
    name = fields.Char(string='Hotel Room Name', required=True)
    description = fields.Char(string='Hotel Room Description', required=False)
    hotel_id = fields.Many2one('hotel.management', string='Hotel', required=False)
    booking_date = fields.Date(string='Hotel Booking Date', default=datetime.now(), required=False)
    checkin_date = fields.Date(string='Hotel Checkin Date', default=datetime.now(), required=False)
    checkout_date = fields.Date(string='Hotel Checkout Date', default=datetime.now(), required=False)
    status_booking = fields.Selection([('draft','Draft'),('booking','Booking'),
                                       ('checkin','Checkin'),('checkout','Checkout'),
                                       ('cancel','Cancel')], default='draft')

    accessories = fields.Many2many('hotel.accessories', column1='room_id', column2='accessories_id', string='Accessories')
    # category_id = fields.Many2many('res.partner.category', column1='partner_id',
    #                                column2='category_id', string='Tags', default=_default_category)

    def _get_report_lang(self):
        return self.env.lang

    def _get_company_data(self):
        return self.env.company

    def action_print(self):
        return (self.env.ref('bis_hotel_management.action_report_room_pdf_report').report_action(self))

    # def check_user_access(self):
    #     partner_access = self.env.user.partner_access
    #     if partner_access:
    #         self.user_access = partner_access

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

    def _auto_delete(self):
        room = self.env['hotel.room'].search([('status_booking', '=', 'draft'),
                                              ('booking_date', '<', (datetime.now() - timedelta(days=7)))])
        room.sudo().unlink()

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

    note = fields.Text(string='Note', required=False)
    casher_id = fields.Many2one('res.partner', string='Casher', required=False)


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
