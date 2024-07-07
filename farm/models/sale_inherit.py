from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    phone2 = fields.Char(string='Phone 2')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    phone2 = fields.Char(string='Phone 2')
    cost2 = fields.Char(string='cost2')

    def action_draft (self):
        print("Hello")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    note = fields.Char(string='Notes')

    @api.constrains('product_uom_qty')
    def check_quantity(self):
        for rec in self:
            if rec.product_uom_qty <= 0:
                raise ValidationError('The Quantity must be > 0 !!!!!')



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quantity = fields.Float(string='Quantity')

    # photo = fields.Binary(string='Photo ')




