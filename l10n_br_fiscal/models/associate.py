from odoo import _, fields, models


class Associate(models.Model):
    _name = "l10n_br_fiscal.associate"
    _description = "Associate"

    name = fields.Char(string="Nome")
    qualification = fields.Char(string="Qualificação")
    partner_id = fields.Many2one(comodel_name="res.partner")
