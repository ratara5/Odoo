from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order="name" #SPRINKLES: List order

    name = fields.Char(required=True,help="""
    Write a complete tag name""",string='Name')
    color = fields.Integer()

    #CONSTRAINS
    _sql_constraints = [
        ('tag', 'UNIQUE (name)',
         'The tag must be unique.'),
    ]