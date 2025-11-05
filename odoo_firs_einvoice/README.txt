FIRS e-Invoice Integration Module (v1.0.7)
==========================================

This module integrates Odoo 18 with Nigeria's FIRS e-Invoicing (TaxPro Max).

Features:
- Automatically posts customer invoices to FIRS API.
- Retrieves and embeds IRN + QR code on invoice PDF (top-right boxed stamp after IRN received).
- Retry cron job for failed submissions.
- Sandbox & Production environments supported.
- Test FIRS Connection button for credential verification.
- SaaS-safe views and report templates for Odoo Cloud / Enterprise 18+.

Installation:
1. Upload `odoo_firs_einvoice_v1.0.7.zip` to your Odoo `addons` folder or Apps interface on odoo.com.
2. Update Apps List and install "FIRS e-Invoice Integration".
3. Navigate to Settings → FIRS e-Invoice Integration section.
4. Enter your API URL, Username, Password, and TIN.
5. Click "Test FIRS Connection" to verify access.
6. Validate an invoice to auto-send to FIRS and display QR (box appears only after IRN is set).

Notes:
- The module adds a small hidden comment inside the invoice report to indicate the module version used to generate the invoice PDF.
- If FIRS requires client-certificate or OAuth authentication, the client code must be extended accordingly.

For support or customization, contact your Odoo administrator or technical consultant.
