import re
import base64

from odoo import models, fields, api
from odoo.tools import misc

from odoo.addons.base.models.assetsbundle import EXTENSIONS


class ScssEditor(models.AbstractModel):
    """Enhanced web editor assets for color customization functionality."""
    
    _inherit = 'web_editor.assets'

    # ----------------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------------

    @api.model
    def _get_colors_attachment(self, custom_url):
        """
        Get color attachment by URL.
        
        Args:
            custom_url (str): The custom URL to search for.
            
        Returns:
            ir.attachment: The attachment record or empty recordset.
        """
        return self.env['ir.attachment'].search([
            ('url', '=', custom_url)
        ])

    @api.model
    def _get_colors_asset(self, custom_url):
        """
        Get color asset by URL pattern.
        
        Args:
            custom_url (str): The custom URL to search for.
            
        Returns:
            ir.asset: The asset record or empty recordset.
        """
        return self.env['ir.asset'].search([
            ('path', 'like', custom_url)
        ])

    @api.model
    def _get_colors_from_url(self, url, bundle):
        """
        Get color content from URL, either from customized attachment or original file.
        
        Args:
            url (str): The URL of the asset.
            bundle (str): The bundle name.
            
        Returns:
            bytes: The content of the asset file.
        """
        custom_url = self._make_custom_asset_url(url, bundle)
        url_info = self._get_data_from_url(custom_url)
        
        if url_info['customized']:
            attachment = self._get_colors_attachment(custom_url)
            if attachment:
                return base64.b64decode(attachment.datas)
                
        # Fallback to original file
        with misc.file_open(url.strip('/'), 'rb', filter_ext=EXTENSIONS) as f:
            return f.read()

    def _get_color_variable(self, content, variable):
        """
        Extract a specific color variable value from SCSS content.
        
        Args:
            content (str): The SCSS content.
            variable (str): The variable name to search for.
            
        Returns:
            str: The variable value or None if not found.
        """
        value = re.search(fr'\$mk_{variable}\:?\s(.*?);', content)
        return value.group(1) if value else None

    def _get_color_variables(self, content, variables):
        """
        Extract multiple color variables from SCSS content.
        
        Args:
            content (str): The SCSS content.
            variables (list): List of variable names to extract.
            
        Returns:
            dict: Dictionary mapping variable names to their values.
        """
        return {
            var: self._get_color_variable(content, var) 
            for var in variables
        }

    def _replace_color_variables(self, content, variables):
        """
        Replace color variables in SCSS content.
        
        Args:
            content (str): The original SCSS content.
            variables (list): List of variable dictionaries with 'name' and 'value' keys.
            
        Returns:
            str: The modified SCSS content.
        """
        for variable in variables:
            content = re.sub(
                fr'{variable["name"]}\:?\s(.*?);', 
                f'{variable["name"]}: {variable["value"]};', 
                content
            )
        return content

    @api.model
    def _save_color_asset(self, url, bundle, content):
        """
        Save color asset content to database.
        
        Args:
            url (str): The asset URL.
            bundle (str): The bundle name.
            content (str): The SCSS content to save.
        """
        custom_url = self._make_custom_asset_url(url, bundle)
        asset_url = url[1:] if url.startswith(('/', '\\')) else url
        datas = base64.b64encode((content or "\n").encode("utf-8"))
        
        custom_attachment = self._get_colors_attachment(custom_url)
        
        if custom_attachment:
            # Update existing attachment
            custom_attachment.write({"datas": datas})
            self.env.registry.clear_cache('assets')
        else:
            # Create new attachment and asset
            self._create_new_color_asset(url, custom_url, asset_url, bundle, datas)

    def _create_new_color_asset(self, url, custom_url, asset_url, bundle, datas):
        """
        Create new color asset attachment and asset record.
        
        Args:
            url (str): Original URL.
            custom_url (str): Custom URL.
            asset_url (str): Asset URL.
            bundle (str): Bundle name.
            datas (bytes): Encoded content data.
        """
        attachment_values = {
            'name': url.split("/")[-1],
            'type': "binary",
            'mimetype': 'text/scss',
            'datas': datas,
            'url': custom_url,
        }
        
        asset_values = {
            'path': custom_url,
            'target': url,
            'directive': 'replace',
        }
        
        # Get target asset information
        target_asset = self._get_colors_asset(asset_url)
        if target_asset:
            asset_values.update({
                'name': '%s override' % target_asset.name,
                'bundle': target_asset.bundle,
                'sequence': target_asset.sequence,
            })
        else:
            asset_values.update({
                'name': '%s: replace %s' % (bundle, custom_url.split('/')[-1]),
                'bundle': self.env['ir.asset']._get_related_bundle(url, bundle),
            })
            
        # Create records
        self.env['ir.attachment'].create(attachment_values)
        self.env['ir.asset'].create(asset_values)

    # ----------------------------------------------------------
    # Public Methods
    # ----------------------------------------------------------

    def get_color_variables_values(self, url, bundle, variables):
        """
        Get color variable values from asset.
        
        Args:
            url (str): Asset URL.
            bundle (str): Bundle name.
            variables (list): List of variable names.
            
        Returns:
            dict: Variable name to value mapping.
        """
        content = self._get_colors_from_url(url, bundle)
        return self._get_color_variables(content.decode('utf-8'), variables)
    
    def replace_color_variables_values(self, url, bundle, variables):
        """
        Replace color variable values in asset.
        
        Args:
            url (str): Asset URL.
            bundle (str): Bundle name.
            variables (list): List of variable dictionaries with 'name' and 'value'.
        """
        original = self._get_colors_from_url(url, bundle).decode('utf-8')
        content = self._replace_color_variables(original, variables)
        self._save_color_asset(url, bundle, content)

    def reset_color_asset(self, url, bundle):
        """
        Reset color asset to original state by removing customizations.
        
        Args:
            url (str): Asset URL.
            bundle (str): Bundle name.
        """
        custom_url = self._make_custom_asset_url(url, bundle)
        
        # Remove attachment and asset records
        attachment = self._get_colors_attachment(custom_url)
        if attachment:
            attachment.unlink()
            
        asset = self._get_colors_asset(custom_url)
        if asset:
            asset.unlink()
