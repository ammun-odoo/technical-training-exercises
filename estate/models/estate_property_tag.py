from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char(required=True)
    
    # SQL Constraints
    _unique_property_tag = models.Constraint('UNIQUE(name)', 'Tag name must be unique.')

    color = fields.Integer(default=0)
