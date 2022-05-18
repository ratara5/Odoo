from odoo import api, fields, models
from odoo.exceptions import UserError

class CustomerServiceProject(models.Model):
    _name="customer.service.project"
    _description="Customer Service Project"

    #FIELDS
    ##Basic
    name=fields.Char()

    #Relational
    service_ids=fields.One2many("customer.service","project_id") #For inline view