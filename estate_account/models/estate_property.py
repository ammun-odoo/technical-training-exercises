from odoo import _, exceptions, fields, models

class Property(models.Model):
    _name = "estate.property"
    _inherit = "estate.property"

    def mark_sold(self):
        print("inherited")
        # Create a customer invoice for the buyer when a property is marked sold
        for record in self:
            try:
                self.env["account.move"].create({
                    "partner_id": record.buyer.id, 
                    "move_type": "out_invoice",
                    "name": _('%s Invoice', record.name),
                    "invoice_line_ids": [
                        fields.Command.create({
                            "name": "6% of Selling Price",
                            "quantity": 1,
                            "price_unit": (record.selling_price * 0.06),
                        }),
                        fields.Command.create({
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100,
                        })
                    ],
                })
            except:
                raise exceptions.UserError(_("Error creating invoice"))
        
        return super().mark_sold()