from odoo import api, fields, models

class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "offers on a property"

    # Standard fields
    price = fields.Float()
    status = fields.Selection(selection=[("accpeted", "Accepted"),("refused", "Refused")], copy=False)
    
    # Relational Fields
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
