from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class FarmCustomer(models.Model):
    _name = 'farm.customer'
    _rec_name = 'customer_name'

    customer_name = fields.Char(string='Customer Name', )
    id_person = fields.Char(string='ID',)
    user_ids = fields.Many2many('res.partner', string='Select Users')
    phone = fields.Char(string='Phone', )
    responsible = fields.Many2one('res.users', string='Responsible', )
    date_of_sale = fields.Datetime(string='Date Of Sale', )
    # default = lambda self: fields.Datetime.now()
    note = fields.Html(string='Notes')
    product_ids = fields.One2many('farm.products', 'customer_id', string='Products')
    product_count = fields.Integer(string='', compute='get_product_count' )

    def get_product_count(self):
        count = self.env['farm.products'].search_count([('customer_id', '=', self.id)])
        self.product_count = count


    state = fields.Selection([
        ('confirm', 'Confirmed'),
        ('send_to_customer', 'Sent To Customer'),
        ('send_to_responsible', 'Sent To Responsible'),
        ('cancel', 'Cancelled'),
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('approve', 'Approved'),
    ], default='draft', string='States', readonly=True,)


    def action_test(self):
        customer_search = self.env['farm.customer'].search([('id', '=', '23')])
        print(customer_search.customer_name)


    def send_to_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def send_to_customer(self):
        for rec in self:
            rec.state = 'send_to_customer'

    def send_to_responsible(self):
        for rec in self:
            rec.state = 'send_to_responsible'

    def send_to_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def send_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def send_to_done(self):
        for rec in self:
            rec.state = 'done'

    def manager_approve(self):
        for rec in self:
            rec.state = 'approve'

    def send_to_yc(self):
        for rec in self:
            body = _('Customer "%s"needs your Approval/Rejection.')% rec.customer_name
            subject = _('Scrap Approval.')
            yc_approval = self.env.ref('farm.yc_group').id
            partner_ids = []
            for user in self.env['res.users'].search([("groups_id", "=", yc_approval)]):
                partner_ids.append(user.partner_id.id)
            # print(partner_ids.id)
            if len(partner_ids) > 0:
                for pid in partner_ids:
                    message = self.env['mail.message'].create({
                        'subject': subject,
                        'body': body,
                        'email_from': 'OdooERP@accm.com.eg',
                        'notification': True,
                        'recipient_ids': pid,
                        'message_type': 'notification',
                    })
                    self.env['mail.notification'].create({
                        'res_partner_id': pid,
                        'mail.message_id': message.id,
                    })

    def send_to_yc(self):
        for rec in self:
            rec.state = 'done'

    @api.constrains('phone','customer_name')
    def _ckeck_phone(self):
        for rec in self:
            if rec.phone[0] !='0' and rec.phone[1] !='1':
                raise ValidationError('Phone Number Is Not Valid (Must Start with (01) !!!!!')
            if len(rec.phone) !=11 :
                raise ValidationError('Phone Number Is Not Valid (Not 11 Digit )!!!!!')
            for number in rec.phone:
                if number not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    raise ValidationError('Phone Number Is Not Valid (All Number must be digits only )!!!!!')

            phone_numbers = self.search([('id', '!=', rec.id), ('phone', '=', rec.phone)])
            if phone_numbers:
                raise ValidationError('Phone Number must be unique !!!!!')

            names = self.search([('id', '!=', rec.id), ('customer_name', '=', rec.customer_name)])
            if names:
                raise ValidationError('Customer Name must be unique !!!!!')
