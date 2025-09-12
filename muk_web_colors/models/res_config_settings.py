from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re


class ResConfigSettings(models.TransientModel):
    """Configuration settings for web color customization."""

    _inherit = 'res.config.settings'

    # ----------------------------------------------------------
    # Constants
    # ----------------------------------------------------------

    COLOR_FIELDS = [
        'color_brand',
        'color_primary', 
        'color_success',
        'color_info',
        'color_warning',
        'color_danger',
    ]

    COLOR_ASSET_LIGHT_URL = '/muk_web_colors/static/src/scss/colors_light.scss'
    COLOR_BUNDLE_LIGHT_NAME = 'web._assets_primary_variables'
    COLOR_ASSET_DARK_URL = '/muk_web_colors/static/src/scss/colors_dark.scss'
    COLOR_BUNDLE_DARK_NAME = 'web.assets_web_dark'

    # ----------------------------------------------------------
    # Fields Light Mode
    # ----------------------------------------------------------
    
    color_brand_light = fields.Char(
        string='Brand Light Color',
        help='Brand color for light theme'
    )
    
    color_primary_light = fields.Char(
        string='Primary Light Color',
        help='Primary color for light theme'
    )
    
    color_success_light = fields.Char(
        string='Success Light Color',
        help='Success color for light theme'
    )
    
    color_info_light = fields.Char(
        string='Info Light Color',
        help='Info color for light theme'
    )
    
    color_warning_light = fields.Char(
        string='Warning Light Color',
        help='Warning color for light theme'
    )
    
    color_danger_light = fields.Char(
        string='Danger Light Color',
        help='Danger color for light theme'
    )

    # ----------------------------------------------------------
    # Fields Dark Mode
    # ----------------------------------------------------------
    
    color_brand_dark = fields.Char(
        string='Brand Dark Color',
        help='Brand color for dark theme'
    )
    
    color_primary_dark = fields.Char(
        string='Primary Dark Color',
        help='Primary color for dark theme'
    )
    
    color_success_dark = fields.Char(
        string='Success Dark Color',
        help='Success color for dark theme'
    )
    
    color_info_dark = fields.Char(
        string='Info Dark Color',
        help='Info color for dark theme'
    )
    
    color_warning_dark = fields.Char(
        string='Warning Dark Color',
        help='Warning color for dark theme'
    )
    
    color_danger_dark = fields.Char(
        string='Danger Dark Color',
        help='Danger color for dark theme'
    )
    
    # ----------------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------------
    
    def _get_light_color_values(self):
        """
        Get current light color values from web editor assets.
        
        Returns:
            dict: Current light color variable values.
        """
        return self.env['web_editor.assets'].get_color_variables_values(
            self.COLOR_ASSET_LIGHT_URL, 
            self.COLOR_BUNDLE_LIGHT_NAME,
            self.COLOR_FIELDS
        )
        
    def _get_dark_color_values(self):
        """
        Get current dark color values from web editor assets.
        
        Returns:
            dict: Current dark color variable values.
        """
        return self.env['web_editor.assets'].get_color_variables_values(
            self.COLOR_ASSET_DARK_URL, 
            self.COLOR_BUNDLE_DARK_NAME,
            self.COLOR_FIELDS
        )
        
    def _set_light_color_values(self, values):
        """
        Set light color values in the provided values dictionary.
        
        Args:
            values (dict): Dictionary to update with light color values.
            
        Returns:
            dict: Updated values dictionary.
        """
        colors = self._get_light_color_values()
        for var, value in colors.items():
            values[f'{var}_light'] = value
        return values
        
    def _set_dark_color_values(self, values):
        """
        Set dark color values in the provided values dictionary.
        
        Args:
            values (dict): Dictionary to update with dark color values.
            
        Returns:
            dict: Updated values dictionary.
        """
        colors = self._get_dark_color_values()
        for var, value in colors.items():
            values[f'{var}_dark'] = value
        return values
    
    def _detect_light_color_change(self):
        """
        Detect if any light color values have changed.
        
        Returns:
            bool: True if any light color has changed, False otherwise.
        """
        colors = self._get_light_color_values()
        return any(
            self[f'{var}_light'] != val
            for var, val in colors.items()
        )
        
    def _detect_dark_color_change(self):
        """
        Detect if any dark color values have changed.
        
        Returns:
            bool: True if any dark color has changed, False otherwise.
        """
        colors = self._get_dark_color_values()
        return any(
            self[f'{var}_dark'] != val
            for var, val in colors.items()
        )
    def _validate_color_format(self, color_value):
        """
        Validate color value format.
        
        Args:
            color_value (str): Color value to validate.
            
        Returns:
            bool: True if valid color format.
            
        Raises:
            ValidationError: If color format is invalid.
        """
        if not color_value:
            return True
            
        # Hex color validation (#RGB or #RRGGBB)
        if re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color_value):
            return True
            
        # RGB/RGBA validation
        if re.match(r'^rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(\s*,\s*[01]?\.?\d*)?\s*\)$', color_value):
            return True
            
        # CSS color names (basic validation)
        css_colors = [
            'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink',
            'black', 'white', 'gray', 'grey', 'brown', 'cyan', 'magenta',
            'transparent', 'inherit', 'initial', 'unset'
        ]
        if color_value.lower() in css_colors:
            return True
            
        raise ValidationError(f"Invalid color format: {color_value}")

    @api.constrains('color_brand_light', 'color_primary_light', 'color_success_light', 
                    'color_info_light', 'color_warning_light', 'color_danger_light')
    def _check_light_colors(self):
        """Validate light color values."""
        for record in self:
            for field in self.COLOR_FIELDS:
                field_name = f'{field}_light'
                if hasattr(record, field_name):
                    record._validate_color_format(getattr(record, field_name))

    @api.constrains('color_brand_dark', 'color_primary_dark', 'color_success_dark',
                    'color_info_dark', 'color_warning_dark', 'color_danger_dark')
    def _check_dark_colors(self):
        """Validate dark color values."""
        for record in self:
            for field in self.COLOR_FIELDS:
                field_name = f'{field}_dark'
                if hasattr(record, field_name):
                    record._validate_color_format(getattr(record, field_name))
        
    def _replace_light_color_values(self):
        """
        Replace light color values in the web editor assets.
        
        Returns:
            bool: True if replacement was successful.
        """
        variables = [
            {
                'name': field, 
                'value': self[f'{field}_light']
            }
            for field in self.COLOR_FIELDS
        ]
        return self.env['web_editor.assets'].replace_color_variables_values(
            self.COLOR_ASSET_LIGHT_URL, 
            self.COLOR_BUNDLE_LIGHT_NAME,
            variables
        )
        
    def _replace_dark_color_values(self):
        """
        Replace dark color values in the web editor assets.
        
        Returns:
            bool: True if replacement was successful.
        """
        variables = [
            {
                'name': field, 
                'value': self[f'{field}_dark']
            }
            for field in self.COLOR_FIELDS
        ]
        return self.env['web_editor.assets'].replace_color_variables_values(
            self.COLOR_ASSET_DARK_URL, 
            self.COLOR_BUNDLE_DARK_NAME,
            variables
        )
    
    def _reset_light_color_assets(self):
        """Reset light color assets to default values."""
        self.env['web_editor.assets'].reset_color_asset(
            self.COLOR_ASSET_LIGHT_URL, 
            self.COLOR_BUNDLE_LIGHT_NAME,
        )
        
    def _reset_dark_color_assets(self):
        """Reset dark color assets to default values."""
        self.env['web_editor.assets'].reset_asset(
            self.COLOR_ASSET_DARK_URL, 
            self.COLOR_BUNDLE_DARK_NAME,
        )
        
    # ----------------------------------------------------------
    # Action Methods
    # ----------------------------------------------------------
    
    def action_reset_light_color_assets(self):
        """
        Action to reset light color assets and reload the client.
        
        Returns:
            dict: Client action to reload the page.
        """
        self._reset_light_color_assets()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def action_reset_dark_color_assets(self):
        """
        Action to reset dark color assets and reload the client.
        
        Returns:
            dict: Client action to reload the page.
        """
        self._reset_dark_color_assets()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    # ----------------------------------------------------------
    # Override Methods
    # ----------------------------------------------------------

    def get_values(self):
        """
        Get configuration values including color settings.
        
        Returns:
            dict: Configuration values with color settings.
        """
        res = super().get_values()
        res = self._set_light_color_values(res)
        res = self._set_dark_color_values(res)
        return res

    def set_values(self):
        """
        Set configuration values and update color assets if changed.
        
        Returns:
            bool: Result of the parent set_values call.
        """
        res = super().set_values()
        
        # Update assets if colors have changed
        if self._detect_light_color_change():
            self._replace_light_color_values()
        if self._detect_dark_color_change():
            self._replace_dark_color_values()
            
        return res
