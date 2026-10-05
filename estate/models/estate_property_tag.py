from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=0)

    # SQL Constraints
    _check_unique_property_tag = models.Constraint(
        'UNIQUE(name)',
        'Tag name must be unique.'
    )
