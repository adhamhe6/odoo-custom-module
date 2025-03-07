from odoo import models, fields

class CustomMoveLine(models.Model):
    _name = 'custom.move.line'
    _description = 'Custom Move Line'

    name = fields.Char(string="Description", required=True)
    amount = fields.Float(string="Amount")
    date = fields.Date(string="Date", default=fields.Date.today)
