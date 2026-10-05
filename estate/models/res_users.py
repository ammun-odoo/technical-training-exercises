from odoo import fields, models


class User(models.Model):
    _inherit = 'res.users'

    # Ensure that domain is not in quotes
    property_ids = fields.One2many(
        "estate.property",
        "salesperson",
        domain=['|', ('state', '=', 'new'), ('state', '=', 'received')]
    )
