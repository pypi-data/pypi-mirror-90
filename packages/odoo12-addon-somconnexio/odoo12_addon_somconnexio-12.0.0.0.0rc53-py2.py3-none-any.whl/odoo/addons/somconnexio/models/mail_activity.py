from odoo import models, fields, api


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    reference = fields.Char(
        string='Reference',
        compute='_compute_reference',
        readonly=True,
        store=False
    )
    activity_type_name = fields.Char(
        related="activity_type_id.name"
    )
    date_done = fields.Date(readonly=False)

    @api.depends('res_model', 'res_id')
    def _compute_reference(self):
        for res in self:
            res.reference = "%s,%s" % (res.res_model, res.res_id)
