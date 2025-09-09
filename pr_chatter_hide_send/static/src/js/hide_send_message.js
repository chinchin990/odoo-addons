/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Chatter } from "@mail/chatter/chatter";

patch(Chatter.prototype, "pr_chatter_hide_send_message", {
    setup() {
        this._super();
        // 禁用 Send Message 按钮
        this.canPostMessage = false;
    },
});