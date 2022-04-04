from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order="price desc" #SPRINKLES: List order

    price=fields.Float()
    status=fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one('res.partner', required=True) #this is in estate_property.py too
    


    validity=fields.Integer(default=7)
    date_deadline=fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    property_id = fields.Many2one('estate.property', required=True)

    #SPRINKLES:Stat buttons
    property_type_id=fields.Many2one(related="property_id.property_type_id", store=True)

    #CONSTRAINS
    _sql_constraints = [
        ('price', 'CHECK(price > 0)',
         'The price must be strictly positive.'),
    ]

    #COMPUTED FIELDS AND ONCHANGE
    @api.depends("validity","create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date: 
                record.date_deadline=record.create_date+relativedelta(days=record.validity)
            else:
                record.date_deadline=fields.Datetime.today()+relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            validity=record.date_deadline-record.create_date.date()
            record.validity=validity.days


    #SOME ACTION
    def accepted(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda r: r.status=='accepted'):
                raise UserError('This property already has an accepted offer')
            record.status='accepted'
            record.property_id.write({
                'selling_price':record.price,
                'partner_id':record.partner_id.id,
                'state':'ofeacc'
            })
        
    def refused(self):
        for record in self:
            record.status='refused'

    #INHERIT:
    @api.model
    def create(self, vals):
        offers=self.search([('property_id','=',vals['property_id'])]) #offers que existan
        if not offers:
            property=self.env['estate.property'].browse(vals['property_id'])
            property.write({
                'state':'oferec'
            })
        else:
            if vals['price']<max(offers.mapped('price')):
                raise UserError('offer price must be a upper or equal amount than an existing max offer')
        return super().create(vals) 
    


    