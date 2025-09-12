/** @odoo-module **/

import { url } from '@web/core/utils/urls';
import { useService } from '@web/core/utils/hooks';

import { Component, onWillUnmount } from '@odoo/owl';

/**
 * AppsBar component that displays a sidebar with application navigation.
 * Shows a list of all installed apps similar to the home menu.
 */
export class AppsBar extends Component {
    static template = 'muk_web_appsbar.AppsBar';
    static props = {};

    /**
     * Component setup and initialization.
     * Sets up services, sidebar image URL, and event listeners.
     */
    setup() {
        this.companyService = useService('company');
        this.appMenuService = useService('app_menu');
        
        // Initialize sidebar image URL if available
        this._initializeSidebarImage();
        
        // Set up menu change listener
        this._setupMenuChangeListener();
    }

    /**
     * Initialize the sidebar image URL for the current company.
     * @private
     */
    _initializeSidebarImage() {
        const currentCompany = this.companyService.currentCompany;
        if (currentCompany && currentCompany.has_appsbar_image) {
            this.sidebarImageUrl = url('/web/image', {
                model: 'res.company',
                field: 'appbar_image',
                id: currentCompany.id,
            });
        }
    }

    /**
     * Set up event listener for menu changes and cleanup on unmount.
     * @private
     */
    _setupMenuChangeListener() {
        const renderAfterMenuChange = () => {
            this.render();
        };
        
        this.env.bus.addEventListener('MENUS:APP-CHANGED', renderAfterMenuChange);
        
        onWillUnmount(() => {
            this.env.bus.removeEventListener('MENUS:APP-CHANGED', renderAfterMenuChange);
        });
    }
}
