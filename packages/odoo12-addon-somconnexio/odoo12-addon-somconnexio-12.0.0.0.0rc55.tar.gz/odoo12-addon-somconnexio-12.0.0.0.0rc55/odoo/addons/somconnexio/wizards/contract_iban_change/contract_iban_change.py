from odoo import api, fields, models


class ContractIbanChangeWizard(models.TransientModel):
    _name = 'contract.iban.change.wizard'
    partner_id = fields.Many2one('res.partner')
    contract_ids = fields.Many2many('contract.contract', string='Contracts')
    account_banking_mandate_id = fields.Many2one(
        'account.banking.mandate', 'Banking mandate'
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['partner_id'] = self.env.context['active_id']
        return defaults

    @api.multi
    def button_change(self):
        self.ensure_one()
        self.contract_ids.write({'mandate_id': self.account_banking_mandate_id.id})
        return True
