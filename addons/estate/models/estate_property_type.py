from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order="sequence, name" #SPRINKLES: List order

    name = fields.Char(required=True,help="""
    Write a complete type name""",string='Name')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    #CONSTRAINS
    _sql_constraints = [
            ('type', 'UNIQUE (name)',
            'The type must be unique.')
        ]

    #SPRINKLES
    property_ids=fields.One2many('estate.property','property_type_id')

    #SPRINKLES: Stat buttons
    offer_ids=fields.One2many('estate.property.offer','property_type_id')
    offer_count=fields.Integer(compute="_compute_count_offers")

    @api.depends("offer_ids")
    def _compute_count_offers(self):
        for record in self:
            record.offer_count=len(record.offer_ids)

    def stat_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_view_tree').id
        context = self._context.copy()
        return {
        'name':'Offers',
        'view_mode':'tree',
        'res_model':'estate.property.offer',
        'view_id':view_id,
        'type':'ir.actions.act_window',
        'target':'current',
        'domain':[('property_type_id', '=', self.id)],
        'context':context
        }