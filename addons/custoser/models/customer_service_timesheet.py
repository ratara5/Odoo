from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Datetime

class CustomerServiceTimesheet(models.Model):
    _name="customer.service.timesheet"
    _description="Customer Service Timesheet"

    #CONSTRAINS
    _sql_constraints = [
        ("check_duration", "CHECK(duration > 0)", "The duration must be strictly positive"),
    ]

    #FIELDS
    ##Basics
    date=fields.Date()
    description=fields.Char()
    duration=fields.Float()

    ##Reserved
    service_id=fields.Many2one("customer.service")
    employee=fields.Many2one("res.users", default=lambda self:self.env.user)

    ##Special
    state = fields.Selection(
        selection=[
            ("ok", "Ok"),
            ("standby", "Standby"),
        ],
        string="Status",
        copy=False,
        default=False,
    )

    #ACTION METHODS
    def action_ok(self):
        return self.write({"state": "ok"})

    def action_standby(self):
        return self.write({"state": "standby"})
        #TODO: service.state!='outstandings'
    

