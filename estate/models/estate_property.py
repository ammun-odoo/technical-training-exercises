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
    
    # Relational fields
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # res.partner and res.users are existing models
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    # Environment.user gets the current user
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    offer_ids = fields.One2many("estate.property.offer", "property_id")

    tag_ids = fields.Many2many("estate.property.tag")

    # Computed Fields
    
    # total_area = living_area + garden_area
    # compute function works out of the "", but only if defined AFTER the method. Putting it in quotes is more syntactically correct
    total_area = fields.Integer(compute="_get_total_area")

    # Make sure to import api from odoo
    @api.depends('living_area', 'garden_area')
    def _get_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_max_offer")

    @api.depends('offer_ids.price')
    def _max_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if (record.offer_ids) else 0
