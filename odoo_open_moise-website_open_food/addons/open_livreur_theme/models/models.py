from odoo import models, fields, api, tools, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import logging
from datetime import datetime, date

_logger = logging.getLogger(__name__)


class PickingOrderInherit(models.Model):
    _inherit = "picking.order"

    state = fields.Selection([
        ('assigned', 'Assigné'),
        ('accepted', 'Accepté'),
        ('collected', 'Récupéré'),
        ('delivered', 'Livré'),
        ('canceled', 'Annulé'),
        ('rejected', 'Rejeté'),
    ], string='Status', default='assigned')


class DeliveryTimetable(models.Model):
    _name = "delivery.daily_check"

    delivery_man = fields.Many2one(
        comodel_name='res.partner', string='Livreur', domain="[('is_driver', '=', True)]")
    date = fields.Date(string='Date du check')
    checked_time = fields.Many2many(
        comodel_name='delivery.available_time', string='Heure sélectionnée')


class DeliveryHours(models.Model):
    _name = "delivery.available_time"
    # _sql_constraints = [
    #                     ("hour_rank_unique",
    #                     "unique(hour_rank)",
    #                     "Horaire déjà crée!"),
    #                     ("start_time_unique",
    #                     'unique(start_time)',
    #                     "L'heure de debut doit être unique!"),
    # ]

    start_time = fields.Float(string='Heure de debut')
    end_time = fields.Float(string='Heure de fin')
    hour_rank = fields.Integer(string="Position de l'heure!")

    # @api.constrains('start_time')
    # @api.one
    # def _check_start_time(self):
    #     if (self.start_time and self.start_time > 23) or (self.end_time and self.end_time > 23):
    #         raise ValidationError(_("L'heure ne peut pas dépasser 23"))
    #     elif (self.start_time and self.start_time < 0) or (self.end_time and self.end_time < 0):
    #         raise ValidationError(_("L'heure ne pas avoir une valeur négative!"))

    # @api.one
    # @api.depends('start_time')
    # def _default_endtime(self):
    #     if self.start_time and self.start_time != 23:
    #         self.end_time = self.start_time + 1

    # @api.model
    # def create(self, vals):
    #     if (vals['start_time'] and vals['start_time'] > 23) or (vals['end_time'] and vals['end_time'] > 23):
    #         return
    #     elif (vals['start_time'] and vals['start_time'] < 0) or (vals['end_time'] and vals['end_time'] < 0):
    #         return
    #     else:
    #         return super(DeliveryHours, self).create(vals)

    # @api.multi
    # def write(self, vals):
    #     if (vals['start_time'] and vals['start_time'] > 23) or (vals['end_time'] and vals['end_time'] > 23):
    #         return
    #     elif (vals['start_time'] and vals['start_time'] < 0) or (vals['end_time'] and vals['end_time'] < 0):
    #         return
    #     else:
    #         return super(DeliveryHours, self).write(vals)
