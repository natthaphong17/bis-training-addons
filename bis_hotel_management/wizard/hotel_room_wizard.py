# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from datetime import datetime

class HotelRoomWizard(models.TransientModel):
    _name = 'hotel.room.wizard'
    _description = 'hotel.room.wizard'

    name = fields.Char(string='Hotel Room Name', required=True)
    hotel_id = fields.Many2one('hotel.management', string='Hotel', required=True)

    def checkin(self):
        print('checkin')
        print(self.hotel_id)
        hotel_room = self.env['hotel.room'].search([('hotel_id', '=', self.hotel_id.id)])
        for room in hotel_room:
            if room.name == self.name:
                room.status_booking = 'checkin'