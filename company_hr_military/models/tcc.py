import re

from odoo import _, fields, models, api
from odoo.exceptions import ValidationError, UserError


def _is_valid_phone(phone):
    if not phone:
        return True

    normalized_phone = re.sub(r"[\s()-]", "", phone)
    return bool(
        re.fullmatch(r"(?:\+380\d{9}|0\d{9})", normalized_phone)
    )


class TccModel(models.Model):
    _name = 'company.hr.military.tcc'
    _description = 'ТЦК та СП'
    _order = 'name'

    name = fields.Char(
        string="Назва ТЦК та СП",
        required=True,
    )

    code = fields.Char(
        string="Код ТЦК та СП",
        required=True,
        index=True,
        help="Унікальний внутрішній код ТЦК та СП.",
    )

    phone = fields.Char(
        string="Телефон",
        help="Номер у форматі +380XXXXXXXXX або 0XXXXXXXXX.",
    )

    phone_invalid = fields.Boolean(
        compute="_compute_phone_invalid",
    )

    _code_unique = models.Constraint(
        "UNIQUE(code)",
        "Код ТЦК та СП повинен бути унікальним",
    )

    def copy(self, default=None):
        raise UserError(
            _("Дублювання записів ТЦК та СП заборонено.")
        )

    @api.depends("phone")
    def _compute_phone_invalid(self):
        for record in self:
            record.phone_invalid = not _is_valid_phone(record.phone)

    @api.constrains("phone")
    def _check_phone(self):
        for record in self:
            if not _is_valid_phone(record.phone):
                raise ValidationError(
                    _("Номер повинен мати формат "
                    "+380XXXXXXXXX або 0XXXXXXXXX.")
                )