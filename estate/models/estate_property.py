from odoo import api, fields, models


class Property(models.Model):
    # No _description will result in warning
    _name = "estate.property"
    _description = "The estate.property module."

    # Shorter text, can be length limited
    # Text is used for multiline text
    # Attributes go in the ()
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    # Could be Datetime too, but Date is more relevant for this model
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
