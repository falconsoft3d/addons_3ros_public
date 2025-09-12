from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    """Extends ir.http to include company appsbar image information in session."""

    _inherit = "ir.http"

    # ----------------------------------------------------------
    # Public Methods
    # ----------------------------------------------------------
    
    def session_info(self):
        """
        Extend session info to include appsbar image availability.
        
        Returns:
            dict: Enhanced session information including company appsbar image status.
        """
        result = super(IrHttp, self).session_info()
        
        if request.env.user._is_internal():
            # Add appsbar image information for each company
            user_companies = request.env.user.company_ids.with_context(bin_size=True)
            for company in user_companies:
                company_info = result['user_companies']['allowed_companies'].get(company.id)
                if company_info:
                    company_info.update({
                        'has_appsbar_image': bool(company.appbar_image),
                    })
                    
        return result
