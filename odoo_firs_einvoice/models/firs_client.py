import requests, logging
from odoo import models

_logger = logging.getLogger(__name__)

class FirsClient(models.AbstractModel):
    _name = 'firs.client'
    _description = 'FIRS e-Invoice API Client'

    def _get_conf(self):
        ICP = self.env['ir.config_parameter'].sudo()
        return {
            'url': ICP.get_param('firs.api_url'),
            'username': ICP.get_param('firs.api_username'),
            'password': ICP.get_param('firs.api_password'),
            'tin': ICP.get_param('firs.tin'),
        }

    def send_invoice(self, payload):
        conf = self._get_conf()
        try:
            headers = {'Content-Type': 'application/json'}
            resp = requests.post(
                conf['url'], json=payload, headers=headers,
                auth=(conf['username'], conf['password']), timeout=30
            )
            resp.raise_for_status()
            return {'success': True, 'data': resp.json()}
        except Exception as e:
            _logger.exception("FIRS API error: %s", e)
            return {'success': False, 'error': str(e)}
