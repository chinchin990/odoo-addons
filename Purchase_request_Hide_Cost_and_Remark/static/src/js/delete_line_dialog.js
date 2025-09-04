/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";

export class DeleteLineDialog extends Component {
    static template = "purchase_request_hide_cost_and_remark.DeleteLineDialog"; 
    static components = { Dialog }; // Register the Dialog component
    static props = {
        close: { type: Function },
        body: { type: String, optional: true },
        confirm: { type: Function, optional: true },
        cancel: { type: Function, optional: true },
    };

    get title() {
        return _t("Invalid Line");
    }

    _onConfirm() {
        if (this.props.confirm) {
            this.props.confirm();
        }
        this.props.close();
    }

    _onCancel() {
        if (this.props.cancel) {
            this.props.cancel();
        }
        this.props.close();
    }
}