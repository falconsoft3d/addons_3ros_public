# -*- coding: utf-8 -*-
"""
Common utilities for MuK Web Theme modules.
This module provides shared functionality to reduce code duplication.
"""

from odoo import models, fields


class MukWebThemeConstants:
    """Constants used across MuK web theme modules."""
    
    # Color fields used in theme customization
    COLOR_FIELDS = [
        'color_brand',
        'color_primary', 
        'color_success',
        'color_info',
        'color_warning',
        'color_danger',
    ]
    
    # Asset URLs for light and dark themes
    COLOR_ASSET_LIGHT_URL = '/muk_web_colors/static/src/scss/colors_light.scss'
    COLOR_BUNDLE_LIGHT_NAME = 'web._assets_primary_variables'
    COLOR_ASSET_DARK_URL = '/muk_web_colors/static/src/scss/colors_dark.scss'
    COLOR_BUNDLE_DARK_NAME = 'web.assets_web_dark'
    
    # User preference options
    SIDEBAR_TYPE_OPTIONS = [
        ('invisible', 'Invisible'),
        ('small', 'Small'),
        ('large', 'Large')
    ]
    
    DIALOG_SIZE_OPTIONS = [
        ('minimize', 'Minimize'),
        ('maximize', 'Maximize'),
    ]


class MukWebThemeMixin(models.AbstractModel):
    """
    Mixin class providing common functionality for MuK web theme modules.
    """
    
    _name = 'muk.web.theme.mixin'
    _description = 'MuK Web Theme Mixin'
    
    def _get_theme_constants(self):
        """
        Get theme constants for use in models.
        
        Returns:
            MukWebThemeConstants: Constants class instance.
        """
        return MukWebThemeConstants()
    
    def _validate_color_value(self, color_value):
        """
        Validate color value format (hex, rgb, etc.).
        
        Args:
            color_value (str): Color value to validate.
            
        Returns:
            bool: True if valid color format, False otherwise.
        """
        if not color_value:
            return True
            
        # Basic validation for common color formats
        import re
        
        # Hex color validation (#RGB or #RRGGBB)
        if re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color_value):
            return True
            
        # RGB/RGBA validation
        if re.match(r'^rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(\s*,\s*[01]?\.?\d*)?\s*\)$', color_value):
            return True
            
        # Named colors (basic check)
        named_colors = [
            'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink',
            'black', 'white', 'gray', 'grey', 'brown', 'cyan', 'magenta'
        ]
        if color_value.lower() in named_colors:
            return True
            
        return False