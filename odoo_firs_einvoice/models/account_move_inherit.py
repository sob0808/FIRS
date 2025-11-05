from odoo import models, fields, api
import base64, qrcode, json
from io import BytesIO

class AccountMove(models.Model):
    _inherit = 'account.move'

    firs_irn = fields.Char("FIRS IRN", copy=False)
    firs_status = fields.Selection([('none','Not Submitted'),('pending','Pending'),('validated','Validated'),('error','Error')], default='none', copy=False)
    firs_response = fields.Text("FIRS Response", copy=False)
    firs_qr = fields.Binary("FIRS QR Code", copy=False)

    def _firs_build_payload(self):
        self.ensure_one()
        lines = [{
            "description": l.name,
            "quantity": float(l.quantity),
            "unitPrice": float(l.price_unit),
            "taxRate": sum(tax.amount for tax in l.tax_ids),
            "total": float(l.price_subtotal),
        } for l in self.invoice_line_ids]
        return {
            "invoiceNumber": self.name,
            "sellerTIN": self.company_id.vat or self.env['ir.config_parameter'].sudo().get_param('firs.tin'),
            "buyerName": self.partner_id.name,
            "buyerTIN": self.partner_id.vat or "",
            "invoiceDate": str(self.invoice_date),
            "invoiceTotal": float(self.amount_total),
            "lines": lines,
        }

    def send_to_firs(self):
        self.ensure_one()
        client = self.env['firs.client']
        payload = self._firs_build_payload()
        result = client.send_invoice(payload)
        if result.get('success'):
            data = result['data']
            self.firs_irn = data.get('irn') or data.get('invoiceReference')
            qr_text = data.get('qr') or self.firs_irn
            if qr_text:
                img = qrcode.make(qr_text)
                buf = BytesIO()
                img.save(buf, format='PNG')
                self.firs_qr = base64.b64encode(buf.getvalue())
            self.firs_status = 'validated'
            try:
                self.firs_response = json.dumps(data)
            except:
                self.firs_response = str(data)
        else:
            self.firs_status = 'error'
            self.firs_response = result.get('error')

    def action_post(self):
        res = super().action_post()
        for inv in self.filtered(lambda i: i.move_type == 'out_invoice'):
            inv.firs_status = 'pending'
            inv.send_to_firs()
        return res
