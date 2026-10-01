from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of property (e.g. House)"

    # fields
    name = fields.Char(required=True)
