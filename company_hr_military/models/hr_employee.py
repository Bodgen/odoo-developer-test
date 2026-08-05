import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_reserved = fields.Boolean(
        string="Бронювання",
        groups="hr.group_hr_user",
        help="Працівник має бронювання",
    )

    is_mobilized = fields.Boolean(
        string="Мобілізований",
        groups = "hr.group_hr_user",
    )

    tcc_id = fields.Many2one(
        comodel_name='company.hr.military.tcc',
        string="ТЦК та СП",
        ondelete='restrict',
        groups="hr.group_hr_user",
        help="ТЦК та СП у якому працівник перебуває на обліку",
    )

    registry_number = fields.Char(
        string="№ в ЄДРПВР",
        copy=False,
        groups="hr.group_hr_user",
        help="Номер працівника в ЄДРПВР"
    )

    _registry_number_unique = models.Constraint(
        "UNIQUE(registry_number)",
        "Співробітник із таким номером у ЄДРПВР вже існує.",
    )

    @api.constrains("is_reserved", "is_mobilized")
    def _check_military_status(self):
        for employee in self:
            if employee.is_reserved and employee.is_mobilized:
                raise ValidationError(
                    _(
                        "Співробітник не може бути одночасно "
                        "заброньованим і мобілізованим."
                    )
                )

    @api.constrains("military_registry_number")
    def _check_military_registry_number(self):
        for employee in self:
            number = employee.registry_number

            if number and not re.fullmatch(r"[0-9]+", number):
                raise ValidationError(
                    _("Номер у ЄДРПВР повинен містити лише цифри.")
                )