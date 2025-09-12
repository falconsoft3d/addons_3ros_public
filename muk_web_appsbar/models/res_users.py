from odoo import models, fields, api


class ResUsers(models.Model):
    """Extends res.users to add sidebar preferences for the apps bar."""
    
    _inherit = 'res.users'
    
    # ----------------------------------------------------------
    # Constants
    # ----------------------------------------------------------
    
    SIDEBAR_TYPE_OPTIONS = [
        ('invisible', 'Invisible'),
        ('small', 'Small'),
        ('large', 'Large')
    ]
    
    # ----------------------------------------------------------
    # Properties
    # ----------------------------------------------------------
    
    @property
    def SELF_READABLE_FIELDS(self):
        """Add sidebar_type to readable fields for user self-service."""
        return super().SELF_READABLE_FIELDS + [
            'sidebar_type',
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        """Add sidebar_type to writable fields for user self-service."""
        return super().SELF_WRITEABLE_FIELDS + [
            'sidebar_type',
        ]

    # ----------------------------------------------------------
    # Fields
    # ----------------------------------------------------------
    
    sidebar_type = fields.Selection(
        selection=SIDEBAR_TYPE_OPTIONS,
        string="Sidebar Type",
        default='large',
        required=True,
        help="Controls the display type of the applications sidebar."
    )
