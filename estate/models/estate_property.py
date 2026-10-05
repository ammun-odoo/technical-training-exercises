from odoo import _, api, exceptions, fields, models, tools


class Property(models.Model):
    # No _description will result in warning
    _name = "estate.property"
    _description = "The estate.property module."
    # Ordering. Supposed to be ID, but we don't have that field
    _order = "name desc"

    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Helper to calculate default availability date
    def _default_date(self):
        # relativedelta/timedelta: days=90
        return fields.Date.add(fields.Date.today(), days=90)

    # Shorter text, can be length limited
    # Text is used for multiline text
    # Attributes go in the ()
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

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
    state = fields.Selection(
        required=True,
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled")
        ],
        default="new",
        copy=False
    )

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
    total_area = fields.Integer(compute="_compute_total_area")

    # SQL Constraints
    _check_expected_price = models.Constraint('CHECK(expected_price > 0)', 'The expected price cannot be negative.')
    _check_positive_selling_price = models.Constraint('CHECK(selling_price >= 0)', 'The selling price cannot be negative.')

    # Make sure to import api from odoo
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_offer")

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if (record.offer_ids) else 0

    # Onchange methods for the garden
    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = None
            else:
                record.garden_area = 10
                record.garden_orientation = 'north'

    # Raise a warning for if date_availability is in the past
    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for record in self:
            if record.date_availability < fields.Date.today():
                return {
                    "warning": {
                        "title": "Availability in Past", 
                        "message": "The date available is set to prior to today and has already passed."
                    }
                }

    # Python Constraints
    @api.constrains('selling_price', 'expected_price')
    def _check_minimum_selling_price(self):
        for record in self:
            # Check that the selling price is actually set and we aren't resetting it to 0
            if not tools.float_is_zero(record.selling_price, 2):
                # Check that the selling price is at least 90% of the expected
                # returns -1 if a < b, 0 if ==, 1 if a > b
                if tools.float_compare(record.selling_price, (record.expected_price * 0.9), 2) < 0:
                    # Translate string
                    raise exceptions.ValidationError(_("This selling price is too low. It must be at least 90% of the selling price"))

    # CRUD/Inheritance Overrides
    # Cannot delete properties that aren't in new or canceled stated
    # requires at_uninstall, which determines if this is called when the module itself is being uninstalled. AKA if you want to check this condition then
    @api.ondelete(at_uninstall=False)
    def _unlink_estate_property(self):
        for record in self:
            if record.state not in {'new', 'canceled'}:
                raise exceptions.UserError(_("Cannot delete a property that is not new or canceled."))

    # Actions/Buttons
    def action_mark_sold(self):
        self.ensure_one()
        for record in self:
            # Check its state
            if record.state == 'canceled':
                # raise error
                raise exceptions.UserError("Cannot mark a canceled property as sold.")
            # mark the property sold
            record.state = 'sold'
        return True

    def action_mark_canceled(self):
        self.ensure_one()
        for record in self:
            # Check state
            if record.state == 'sold':
                raise exceptions.UserError("Cannot mark a sold property as canceled.")
            # mark canceled
            record.state = 'canceled'
        return True
