from odoo import models, fields, api

class MultiSaleOrderWizard(models.TransientModel):
    _name = 'multi.sale.order.wizard'
    _description = 'Multi Sale Order Wizard'

    partner_ids = fields.Many2many('res.partner', string="Customers", required=True)
    order_line = fields.One2many('multi.sale.order.line', 'wizard_id', string="Order Lines")

    def create_orders(self):
        SaleOrder = self.env['sale.order']
        for partner in self.partner_ids:
            order = SaleOrder.create({
                'partner_id': partner.id,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit
                }) for line in self.order_line]
            })
            order.action_confirm()  # Confirm the sale order
        return {'type': 'ir.actions.act_window_close'}

class MultiSaleOrderLine(models.TransientModel):
    _name = 'multi.sale.order.line'
    _description = 'Multi Sale Order Line'

    wizard_id = fields.Many2one('multi.sale.order.wizard', string="Wizard Reference", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_uom_qty = fields.Float(string="Quantity", required=True, default=1.0)
    price_unit = fields.Float(string="Unit Price", required=True, default=0.0)
