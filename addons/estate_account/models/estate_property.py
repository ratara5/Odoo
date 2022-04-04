#INTERACT WITH OTHER MODULES
from odoo import models

class Property(models.Model):
    _inherit='estate.property'

    def sold(self):
        self.env["account.move"].create({
                "partner_id":self.partner_id.id,
                "move_type":"out_invoice",
                "journal_id":self.env["account.move"].
                    with_context(default_move_type="out_invoice").
                    _get_default_journal().id,
                "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name":self.name,
                        "quantity":1,               
                        "price_unit":self.selling_price,
                        "discount":6

                    }
                )
                ]
            })
        return super().sold()
