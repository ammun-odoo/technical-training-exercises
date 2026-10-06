from odoo import _, fields, models


class Property(models.Model):
    _name = "estate.property"
    _inherit = "estate.property"

    def action_mark_sold(self):
        self.ensure_one()

        for record in self:
            # Create a customer invoice for the buyer when a property is marked sold
            self.env["account.move"].create({
                "partner_id": record.buyer.id, 
                "move_type": "out_invoice",
                "name": _('%s Invoice', record.name),
                # Create line items
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

        return super().action_mark_sold()
