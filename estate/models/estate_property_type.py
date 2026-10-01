from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of property (e.g. House)"

    # fields
    name = fields.Char(required=True)

    # SQL Constraints
    _unique_property_type = models.Constraint('UNIQUE(name)', 'Property type must have a unique name.')
