# from bdb import GENERATOR_AND_COROUTINE_FLAGS
# from gc import garbage
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class Property(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order="id desc" #SPRINKLES: List order

    name = fields.Char(required=True,help="""
    Write a complete name""",string='Name')
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(copy=False,default=lambda self: self.month_plus_3())
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage =fields.Boolean()
    garden=fields.Boolean(default=None)
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(selection=[('north','North'),('south','South'),('east','East'),('west','West')],default=None)
    state=fields.Selection(selection=[('new','New'),('oferec','Offer Received'),('ofeacc','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],copy=False,default='new')
    active=fields.Boolean(default=True)
    
    property_type_id=fields.Many2one('estate.property.type',string='Type')

    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    tag_ids=fields.Many2many('estate.property.tag',string='Tags')#SPRINKLES: Attributes and options

    offer_ids=fields.One2many('estate.property.offer','property_id')

    total_area=fields.Integer(compute="_compute_total_area")

    best_offer=fields.Float(compute="_compute_best_offer")

    #CONSTRAINS
    _sql_constraints = [
        ('selling_price', 'CHECK(selling_price > 0)',
         'The selling price must be strictly positive.'),
        ('expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.')
    ]

    @api.model
    def month_plus_3(self):
        return fields.Datetime.today()+relativedelta(months=3)

    # COMPUTED FIELDS AND ONCHANGE
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        if not self.offer_ids:
            self.best_offer = 0
        else:
            self.best_offer = max(self.offer_ids.mapped("price"))
        return self.best_offer

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation='north'
        else:
            self.garden_area=0
            self.garden_orientation=False

    #SOME ACTION
    def cancel(self):
        for record in self:
            if record.state!='sold':
                record.state='canceled'
            else:
                raise UserError('Sold properties cannot be canceled')
        return True

    def sold(self):
        for record in self:
            if record.state!='canceled':
                record.state='sold'
            else:
                raise UserError('Canceled properties cannot be sold')
        return True

#CONSTRAINS
    @api.constrains('selling_price')
    def _check_price(self):
        for record in self:
            if record.selling_price!=0 and record.selling_price<0.9*record.expected_price:
                raise ValidationError("The sellling price cannot be minor than 90% expected price".format())

#INHERIT
    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_canceled(self):
        for record in self:
            if record.state not in ('new','canceled'):
                raise UserError("It's not possible delete a property not New or not Cancelled")




