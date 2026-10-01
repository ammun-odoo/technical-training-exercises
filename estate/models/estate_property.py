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

    ### Helper to calculate default availability date ###
    def _default_date(self):
        # relativedelta/timedelta: days=90
        return fields.Date.add(fields.Date.today(), days=90)

    # Could be Datetime too, but Date is more relevant for this model
    date_availability = fields.Date(default=_default_date, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])

    # Invisible is not a valid field in Odoo.20.0
    # Active does determine behavior of the record still, but a visible checkbox.
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True,
        selection=[
            ("new", "New"), 
            ("received", "Offer Received"), 
            ("accepted", "Offer Accepted"), 
            ("sold", "Sold"), 
            ("canceled", "Canceled")
        ],
        default="new",
        copy=False)
