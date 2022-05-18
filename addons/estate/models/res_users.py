# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.users"

    # --------------------------------------- Fields Declaration ----------------------------------
    #Basic
    is_technical=fields.Boolean(default=False)

    # Relational
    # This domain gives the opportunity to mention the evaluated and non-evaluated domains
    property_ids = fields.One2many(
        "estate.property", "user_id", string="Properties", domain=[("state", "in", ["new", "offer_received"])]
    )
