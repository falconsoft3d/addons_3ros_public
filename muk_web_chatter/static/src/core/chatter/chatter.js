/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { browser } from "@web/core/browser/browser";

import { Chatter } from "@mail/core/web/chatter";

/**
 * Patch for the Chatter component to add tracking toggle functionality.
 * Allows users to show/hide tracking information with persistent state.
 */
patch(Chatter.prototype, {
    /**
     * Setup the chatter component with tracking toggle functionality.
     * Initializes the tracking state from localStorage.
     */
    setup() {
        super.setup();
        this._initializeTrackingState();
    },

    /**
     * Initialize the tracking state from localStorage.
     * Defaults to true if no value is stored.
     * @private
     */
    _initializeTrackingState() {
        const storedTracking = browser.localStorage.getItem('muk_web_chatter.tracking');
        this.state.showTracking = storedTracking != null ? JSON.parse(storedTracking) : true;
    },

    /**
     * Toggle the tracking visibility and persist the state.
     * Updates both the component state and localStorage.
     */
    onClickTrackingToggle() {
        const showTracking = !this.state.showTracking;
        
        // Persist the preference
        browser.localStorage.setItem('muk_web_chatter.tracking', showTracking);
        
        // Update component state
        this.state.showTracking = showTracking;
    },
});
