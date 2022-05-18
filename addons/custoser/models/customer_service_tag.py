from odoo import api, fields, models
from odoo.exceptions import UserError

class CustomerServiceTag(models.Model):
    _name="customer.service.tag"
    _description="Customer Service Tag"

    #CONSTRAINS
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique")
    ]

    #FIELDS
    ##Basic
    name=fields.Char()
    color = fields.Integer("Color Index")