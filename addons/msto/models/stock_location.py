# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class Location(models.Model):
    _inherit = "stock.location"

    partner_id=fields.Many2one("res.partner","Technical")
 

#class Route(models.Model):
    #_inherit = 'stock.location.route'