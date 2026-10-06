from odoo import _, api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of property (e.g. House)"
    # Model ordering
    # _order = "name"
    # Manual ordering
    _order = "sequence"

    # fields
    name = fields.Char(required=True)

    # SQL Constraints
    _unique_property_type = models.Constraint(
        'UNIQUE(name)',
        'Property type must have a unique name.'
    )

    # One2many properties
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    # Manual Ordering
    sequence = fields.Integer(default=1)

    # Counter for one2many
    offer_count = fields.Integer(compute="_compute_property_type_offers")

    @api.depends("offer_ids")
    def _compute_property_type_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # Public stat button method
    def action_open_offer_ids(self):
        return {
            "name": _("Offers"),
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "estate.property.offer",
            "target": "current",
            "domain": [('property_type_id', '=', self.id)],
            "context": {'default_property_type_id': self.id},
        }
