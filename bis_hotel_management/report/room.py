# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class HotelRoomReport(models.Model):
    _name = 'hotel.room.report'

    name = fields.Char(string='Room Name', required=True)
    sequence = fields.Integer(string='Hotel Room Sequence', default=1, required=True)
    description = fields.Char(string='Hotel Room Description', required=False)
    hotel_id = fields.Many2one('hotel.management', string='Hotel', required=False)
    hotel_name = fields.Char(string='Hotel Room Name', required=True)
    booking_date = fields.Date(string='Hotel Booking Date', default=datetime.now(), required=False)
    checkin_date = fields.Date(string='Hotel Checkin Date', default=datetime.now(), required=False)
    checkout_date = fields.Date(string='Hotel Checkout Date', default=datetime.now(), required=False)
    status_booking = fields.Selection([('draft', 'Draft'), ('booking', 'Booking'),
                                       ('checkin', 'Checkin'), ('checkout', 'Checkout'),
                                       ('cancel', 'Cancel')], default='draft')

    def _select_room(self):
        select_ = f"""
            MIN(r.id) AS id,
            r.sequence AS sequence,
            r.name AS name,
            r.description AS description,
            r.hotel_id AS hotel_id,
            h.name AS hotel_name,
            r.booking_date AS booking_date,
            r.checkin_date AS checkin_date,
            r.checkout_date AS checkout_date,
            r.status_booking AS status_booking
        """

        return select_

    def _from_room(self):
        return """
            hotel_room r
            LEFT JOIN hotel h ON h.id = r.hotel_id
        """

    def _where_room(self):
        return """
            1=1
        """

    def _group_by_room(self):
        return """
            r.sequence,
            r.name,
            r.description,
            r.hotel_id,
            h.name,
            r.booking_date,
            r.checkin_date,
            r.checkout_date,
            r.status_booking
        """

    def _query(self):
        return f"""
            SELECT {self._select_room()}
            FROM {self._from_room()}
            WHERE {self._where_room()}
            GROUP BY {self._group_by_room()}
        """

    @property
    def _table_query(self):
        return self._query()