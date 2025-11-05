from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class FirsConfig(models.TransientModel):
    _inherit = "res.config.settings"

    firs_api_url = fields.Char("FIRS API URL", default="https://api.taxpromax.com/einvoice/v1")
    firs_api_username = fields.Char("FIRS API Username")
    firs_api_password = fields.Char("FIRS API Password")
    firs_tin = fields.Char("Company TIN")
    firs_environment = fields.Selection([('sandbox','Sandbox'),('prod','Production')], default='prod')

    def get_values(self):
        res = super().get_values()
        ICP = self.env['ir.config_parameter'].sudo()
        res.update({
            'firs_api_url': ICP.get_param('firs.api_url'),
            'firs_api_username': ICP.get_param('firs.api_username'),
            'firs_api_password': ICP.get_param('firs.api_password'),
            'firs_tin': ICP.get_param('firs.tin'),
            'firs_environment': ICP.get_param('firs.environment') or 'prod',
        })
        return res

    def set_values(self):
        super().set_values()
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('firs.api_url', self.firs_api_url or '')
        ICP.set_param('firs.api_username', self.firs_api_username or '')
        ICP.set_param('firs.api_password', self.firs_api_password or '')
        ICP.set_param('firs.tin', self.firs_tin or '')
        ICP.set_param('firs.environment', self.firs_environment or 'prod')

    def action_test_connection(self):
        """Simple connectivity test to the configured FIRS endpoint.
        Returns an Odoo notification action with success/failure info.
        Does not send invoice data; only pings the endpoint (GET).
        """
        ICP = self.env['ir.config_parameter'].sudo()
        url = ICP.get_param('firs.api_url')
        username = ICP.get_param('firs.api_username')
        password = ICP.get_param('firs.api_password')
        if not url:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'FIRS Connection',
                    'message': 'FIRS API URL not configured.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        try:
            # Use HEAD if supported, else GET. We try GET for broad compatibility.
            resp = requests.get(url, auth=(username, password) if username and password else None, timeout=10)
            status = resp.status_code
            text = resp.text[:1000] if resp.text else ''
            if 200 <= status < 300:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'FIRS Connection',
                        'message': '✅ Connection successful (HTTP %s).' % status,
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                _logger.warning('FIRS ping returned non-2xx: %s %s', status, text)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'FIRS Connection',
                        'message': '❌ Connection failed (HTTP %s). See logs for details.' % status,
                        'type': 'danger',
                        'sticky': True,
                    }
                }
        except Exception as e:
            _logger.exception('FIRS connection test error: %s', e)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'FIRS Connection',
                    'message': '❌ Connection error: %s' % e,
                    'type': 'danger',
                    'sticky': True,
                }
            }
