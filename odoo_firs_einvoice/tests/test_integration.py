from odoo.tests import TransactionCase

class TestFirsIntegration(TransactionCase):
    def test_invoice_payload(self):
        inv = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.env.ref('base.res_partner_1').id,
            'invoice_line_ids': [(0, 0, {'name': 'Test Item', 'quantity': 1, 'price_unit': 100})]
        })
        payload = inv._firs_build_payload()
        self.assertIn('invoiceNumber', payload)