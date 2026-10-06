from odoo import api, exceptions, fields, models


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "offers on a property"
    _order = "price desc"

    # Standard fields
    price = fields.Float()
    status = fields.Selection(selection=[
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ], copy=False)

    # Relational Fields
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Note that we are using property_id from above
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )

    # Computed and Inverse Fields
    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_compute_validity"
    )

    # SQL Constraints
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'An offer must have a positive price.'
    )

    # These will call creation date, which will default to day the record made
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if (fields.Date.to_date(record.create_date)):
                print(record.validity)
                record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)

    @api.depends('create_date', 'date_deadline')
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                if fields.Date.to_date(record.create_date):
                    # .days convertys this to an integer
                    print(record.date_deadline)
                    record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    # Inheritance and CRUD
    @api.model
    def create(self, vals):
        # For each new record
        for val in vals:
            # Val will return property_id, an int. Can access property.state as below
            curr_property = self.env['estate.property'].browse(val['property_id'])

            # The curr_property.offer_ids return the offer object, not just an int
            # Check that the offer is not lower than any others for this property
            if len(curr_property.offer_ids) > 0:
                min_price = min(curr_property.offer_ids.mapped('price'))
                if val['price'] < min_price:
                    raise exceptions.UserError("Cannot submit an offer lower than previous offers.")

            # Update the state for properties without any offers yet, but not those that already have them or are inactive
            if curr_property.state == 'new':
                curr_property.state = 'received'
        return super().create(vals)

    # Offer Actions/Buttons
    def action_mark_offer_accept(self):
        self.ensure_one()
        for record in self:
            if record.status != 'accepted':
                # Check if any other offers for this property have status=accepted
                if 'accepted' in self.property_id.offer_ids.mapped('status'):
                    raise exceptions.UserError("Cannot accept more than one offer at once.")
                record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
        return True


    def action_mark_offer_refuse(self):
        self.ensure_one()
        for record in self:
            # check if accepted so you can reset selling price
            if record.status == 'accepted':
                # Need to reference the property itself
                record.property_id.selling_price = 0
                record.property_id.buyer = None
            record.status = 'refused'
        return True
