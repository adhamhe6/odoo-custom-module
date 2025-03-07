from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    global_discount_percentage = fields.Float(string="Global Discount (%)")

    @api.depends('order_line.price_total', 'global_discount_percentage')
    def _compute_amount_all(self):
        """
        Override the method to apply a global discount on the total amount.
        """
        super(PurchaseOrder, self)._compute_amount_all()
        for order in self:
            if order.global_discount_percentage:
                discount_amount = (order.amount_untaxed + order.amount_tax) * (order.global_discount_percentage / 100)
                order.amount_total -= discount_amount
