FIRS e-Invoice Integration Module (v1.0.6)
==========================================

This module integrates Odoo 18 with Nigeria's FIRS e-Invoicing (TaxPro Max).

Features:
- Automatically posts customer invoices to FIRS API.
- Retrieves and embeds IRN + QR code on invoice PDF (top-right boxed stamp after IRN received).
- Retry cron job for failed submissions.
- Sandbox & Production environments supported.
- Test FIRS Connection button for credential verification.

Installation:
1. Upload `odoo_firs_einvoice_v1.0.6.zip` to your Odoo `addons` folder or Apps interface.
2. Update Apps List and install "FIRS e-Invoice Integration".
3. Navigate to Settings → FIRS e-Invoice Integration section.
4. Enter your API URL, Username, Password, and TIN.
5. Click "Test FIRS Connection" to verify access.
6. Validate an invoice to auto-send to FIRS and display QR (box appears only after IRN is set).

For support or customization, contact your Odoo administrator or technical consultant.
