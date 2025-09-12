from odoo import models, fields, api


class ResUsers(models.Model):
    """Extends res.users to add dialog size preferences."""
    
    _inherit = 'res.users'
    
    # ----------------------------------------------------------
    # Constants
    # ----------------------------------------------------------
    
    DIALOG_SIZE_OPTIONS = [
        ('minimize', 'Minimize'),
        ('maximize', 'Maximize'),
    ]
    
    # ----------------------------------------------------------
    # Properties
    # ----------------------------------------------------------
    
    @property
    def SELF_READABLE_FIELDS(self):
        """Add dialog_size to readable fields for user self-service."""
        return super().SELF_READABLE_FIELDS + [
            'dialog_size',
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        """Add dialog_size to writable fields for user self-service."""
        return super().SELF_WRITEABLE_FIELDS + [
            'dialog_size',
        ]

    # ----------------------------------------------------------
    # Fields
    # ----------------------------------------------------------
    
    dialog_size = fields.Selection(
        selection=DIALOG_SIZE_OPTIONS,
        string="Dialog Size",
        default='minimize',
        required=True,
        help="Default size preference for dialog windows."
    )
