from lib2to3 import refactor
from odoo import api, fields, models
from odoo.fields import Date, Datetime
from odoo.exceptions import UserError

from datetime import datetime

class CustomerService(models.Model):
    _name="customer.service"
    _description="Customer Service"

    #CONSTRAINS
    _sql_constraints = [
        ("check_planned_duration", "CHECK(planned_duration > 0)", "The planned_duration must be strictly positive"),
    ] #TODO: Avoid: '-'
    #FIELDS
    ##Basics
    name=fields.Char(copy="False")
    description=fields.Char()
    planned_date=fields.Date(required=True, copy="False", default=Date.add(Date.today(),days=1))
    phone=fields.Char() #TODO: Partner's phone 
    planned_duration=fields.Float(string="Initially Planned Hours")

    ##Reserved
    state=fields.Selection(selection=[('new','New'),('on_going','On Going'),('on_site','On Site'),('done','Done'),('outstandings','Outstandings')], copy=False, default="new")
    active=fields.Boolean(default=True)

    ##Relational
    technical_id=fields.Many2one("res.users", string="Assigned to", copy=False, default=lambda self: self.env.user)
    customer_id=fields.Many2one("res.partner", copy=False)
    project_id=fields.Many2one("customer.service.project")
    tag_ids=fields.Many2many("customer.service.tag")
    timesheet_ids=fields.One2many("customer.service.timesheet","service_id")

    ##Computed and Onchange
    ###Technical planned time
    remaining_hours=fields.Float(String="Remaining hours [hh:mm]", compute="_compute_remaining_hours") #TODO: hh:mm
    progress=fields.Float()
    hours_spend=fields.Float(String="Hours spend [hh:mm]", readonly=True) #TODO: debug readonly=False
    ###Timer
    start_time=fields.Datetime()
    elapsed_time=fields.Float(readonly=True) #TODO: Refresh in view

    #ONCHANGE METHODS
    @api.onchange("timesheet_ids")
    def sum_total(self):
        self.hours_spend=sum(self.timesheet_ids.mapped("duration"))
    @api.onchange("customer_id")
    def show_phone(self):
        self.phone=self.customer_id.phone
    
    #COMPUTE METHODS
    @api.depends("hours_spend")
    def _compute_remaining_hours(self):
        timesheet_ok=self.timesheet_ids.filtered(lambda r: r.state=="ok")
        self.progress=sum(timesheet_ok.mapped('duration')) #TODO: The progressbar must be updated (onchange?)
        self.remaining_hours=self.hours_spend-self.progress
    
    #ACTION METHODS
    def action_start(self):
        self.start_time=Datetime.now()

    def action_stop(self):
        self.elapsed_time=(datetime.now()-Datetime.to_datetime(self.start_time)).total_seconds()/3600
        return self.write({"state": "done"})

    def action_pause(self):
        pass #TODO

    def action_sign_report(self):
        pass #TODO

    def action_onsite(self):
        return self.write({"state": "on_site"})