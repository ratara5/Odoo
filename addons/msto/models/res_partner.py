from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit='res.partner'

    is_technical=fields.Boolean(String="Is technical?")

    @api.model
    def create(self, vals):
        part= super().create(vals)
        if part.is_technical:
            city=part.city[0:2].upper()
            location = self.env["stock.location"].search([("name", "=", city)], limit=1)

            stock_loc=self.env["stock.location"].search([("name", "=", "Stock"),("location_id","=",location.id)], limit=1)

            list_name=part.name.split()
            name='_'.join(list_name)
            self.env["stock.location"].create(
                {
                    "location_id":stock_loc.id,
                    "name":name.upper(), # TODO: Unique number, civil identification number?
                    "partner_id":part.id
                }
            )
        return part
        # TODO: At delete Location and Warehouses, what happens?