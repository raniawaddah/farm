from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class FarmProducts(models.Model):
    _name = 'farm.products'
    _rec_name = 'product_name'

    customer_id = fields.Many2one('farm.customer', string='Customer', required=True, )

    product_name = fields.Char(string='Product Name')
    expiration = fields.Date(string='Expiration')

    product_type = fields.Selection([
        ('insect', 'Insect'),
        ('fangi', 'Fangi'),
        ('fertilizer', 'Fertilizer')
    ], default='insect', required=True, string='Product Type')

    quantity = fields.Float(string='Quantity')

    unit_price = fields.Float(string='Unit Price')

    total = fields.Float(string='Total', compute='get_total_amount', readonly=True)


    @api.depends('quantity', 'unit_price')
    def get_total_amount(self):
        for rec in self:
            rec.total = rec.quantity * rec.unit_price


    @api.constrains('quantity')
    def ckeck_quantity(self):
        for rec in self:
            # if rec.quantity <= 0:
            #     raise ValidationError('Quantity must be > 0   !!!!!')
            if rec.quantity < 0:
                rec.quantity = abs(rec.quantity)