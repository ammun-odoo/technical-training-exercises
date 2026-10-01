from odoo import api, fields, models

class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "offers on a property"

    # Standard fields
    price = fields.Float()
    status = fields.Selection(selection=[("accpeted", "Accepted"),("refused", "Refused")], copy=False)
    
    # Relational Fields
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Note that we are using property_id from above
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    # The creation date of the record
    # Although there is no more invisible, will leave off of custom views
    create_date = fields.Date(default=fields.Date.today())

    # Computed and Inverse Fields
    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute="_find_deadline",
        inverse="_find_validity"
    )

    # These will call creation date, which will default to the day the record is made
    @api.depends('create_date', 'validity')
    def _find_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    @api.depends('create_date', 'date_deadline')
    def _find_validity(self):
        for record in self:
            # .days convertys this to an integer
            record.validity = (record.date_deadline - record.create_date).days
    