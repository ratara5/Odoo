from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class Product(models.Model):
    _inherit = "product.attribute"
