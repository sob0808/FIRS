from odoo import models, fields, api

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