/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { DeleteLineDialog } from "./delete_line_dialog"; // Import our custom dialog
import { _t } from "@web/core/l10n/translation";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);
        this.dialogService = useService("dialog");
    },

    // Intercept the field change event, triggered after the user finishes editing a field
    async onFieldChanged(record, fieldName, value) {
        // If it's in the purchase.request.line model
        if (record.resModel === "purchase.request.line") {
            // First, execute the original field change logic
            await super.onFieldChanged(...arguments);
            
            // Then, check our specific conditions
            const product = record.data.product_id;
            const qty = record.data.product_qty || 0;
            const remark = record.data.x_remark || "";

            // If no product is selected but there is a quantity or remark, and the user was not just editing the product field
            if (!product && (qty > 0 || remark.trim()) && fieldName !== 'product_id') {
                // Display our custom dialog
                this.dialogService.add(DeleteLineDialog, {
                    body: _t("You have not selected a product for this line. Clicking 'OK' will remove this line. 'Cancel' will allow you to continue editing."),
                    confirm: () => {
                        // This is the logic executed after clicking OK: delete this line
                        try {
                            if (record.isNew) {
                                // If it's a new record, remove it directly from the list
                                const list = record.model;
                                if (list && list.records) {
                                    const index = list.records.indexOf(record);
                                    if (index > -1) {
                                        list.records.splice(index, 1);
                                        list._updateCount();
                                    }
                                }
                            } else {
                                // If it's a saved record, mark it for deletion
                                if (record.resId && record.resId !== false) {
                                    record.delete();
                                } else {
                                    // Fallback method: remove directly from the list
                                    const list = record.model;
                                    if (list && list.records) {
                                        const index = list.records.indexOf(record);
                                        if (index > -1) {
                                            list.records.splice(index, 1);
                                            list._updateCount();
                                        }
                                    }
                                }
                            }
                        } catch (error) {
                            console.warn("Error while deleting record:", error);
                            // Final fallback: reset the field values
                            record.update({
                                product_qty: 0,
                                x_remark: ""
                            });
                        }
                    },
                    cancel: () => {
                        // On Cancel, do nothing
                        console.log("User chose to cancel");
                    },
                });
            }
        } else {
            // If it's not the purchase.request.line model, execute the original logic
            return super.onFieldChanged(...arguments);
        }
    },
});