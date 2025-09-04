# Purchase Request Hide Cost and Remark

## Module Introduction

This module provides cost hiding and remark functionalities for the Odoo 17 Purchase Request system, implementing permission-based field visibility control.

### Main Features

1.  **Smart Empty Line Handling**: Frontend JavaScript intelligently detects and handles empty product lines.
2.  **Interactive Dialog**: A user-friendly selection dialog instead of a system error.
3.  **Cost Information Hiding**: Regular users cannot view price-related information.
4.  **Remark Field**: Adds an internal remark function to purchase request lines.
5.  **Permission Control**: Manages field and button visibility based on user roles.
6.  **Button Hiding**: Hides sensitive action buttons from regular users.

## Installation

### Prerequisites
- Odoo 17.0
- `purchase_request` module installed

### Installation Steps

1.  **Copy the module to the addons directory**
    ```bash
    cp -r Purchase_request_Hide_Cost_and_Remark /path/to/odoo/addons/
    ```

2.  **Installation in a Docker environment**
    ```bash
    # Copy the module into the container
    docker cp Purchase_request_Hide_Cost_and_Remark odoo:/mnt/extra-addons/
   
    # Restart the container
    docker restart odoo
    ```

3.  **Activate Developer Mode**
    - Log in to Odoo.
    - Go to Settings → Activate the developer mode.

4.  **Install the Module**
    - Go to Apps → Update Apps List.
    - Search for "Purchase Request Hide Cost and Remark".
    - Click Install.

## Permissions Explained

### User Role Definitions

| Role                | Permission Group                               | Description                               |
|---------------------|------------------------------------------------|-------------------------------------------|
| **Regular User**    | `purchase_request.group_purchase_request_user` | Can create and view their own purchase requests. |
| **Purchase Manager**| `purchase_request.group_purchase_request_manager`| Can view all purchase requests and cost information. |

### How to Assign Permissions

1.  **Go to User Management**
    - Settings → Users & Companies → Users

2.  **Edit User Permissions**
    - Select the target user.
    - In the "Access Rights" tab, find the "Purchase Request" section.
    - Choose the appropriate permission level:
      - **Purchase Request User**: Regular user rights.
      - **Purchase Request Manager**: Manager rights (includes user rights).

## Feature Details

### 1. Smart Empty Line Handling

**Core Concept**: An elegant solution combining frontend and backend.
- **Backend Python**: Remains silent, does not raise a `ValidationError`.
- **Frontend JavaScript**: Acts as a "detective," monitoring user actions.

**Trigger Conditions**:
- When a user has not selected a product in a line.
- But has entered a quantity (`product_qty` > 0) or a remark (`x_remark` is not empty).
- The check is triggered when the user clicks elsewhere.

**Smart Dialog**:
```
Title: "Invalid Line"
Content: "You have not selected a product for this line. 
          Clicking 'OK' will remove this line. 
          'Cancel' will allow you to continue editing."
Buttons: [OK] [Cancel]
```

**User Choices**:
- ✅ **Cancel**: The dialog closes, and the user can go back to select a product.
- ✅ **OK**: The empty line is automatically deleted, cleaning up the interface.

**Technical Implementation**:
- A JavaScript patch intercepts the `onCellClicked` event.
- A custom Dialog component and QWeb template are used.
- The frontend intelligently deletes the line without backend involvement.

### 2. Cost Information Hiding

**Hidden Fields**:
- The "Estimated Cost" column in purchase request lines.
- The total amount at the bottom of the form.
- The label for the total amount.

**Visibility Rules**:
- ✅ **Purchase Manager**: Can see all cost information.
- ❌ **Regular User**: Cannot see any price-related information.

### 3. Remark Field

**Functionality**:
- Adds a "Remark" field to each purchase request line.
- Used for internal communication and recording special instructions.

**Field Location**:
- In the tree view of the purchase request form lines.
- In the separate purchase request line form view.
- In the purchase request line list view.

**Visibility Rules**:
- ✅ **Purchase Manager**: Can view and edit remarks.
- ❌ **Regular User**: The remark field is completely hidden.

### 4. Button Hiding Logic

**Hidden Button**:
- The "Show Details" button (`action_show_details`).

**Reason for Hiding**:
- To prevent regular users from accessing detailed cost and management information.
- To ensure consistency in permission control.

**Visibility Rules**:
- ✅ **Purchase Manager**: Can see all action buttons.
- ❌ **Regular User**: Sensitive action buttons are hidden.

## Technical Implementation

### Module Structure
```
Purchase_request_Hide_Cost_and_Remark/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── purchase_request_line.py
├── views/
│   └── purchase_request_views.xml
├── static/src/
│   ├── js/
│   │   ├── delete_line_dialog.js
│   │   └── list_renderer.js
│   └── xml/
│       └── delete_line_dialog.xml
└── README.md
```

### Frontend Architecture

**JavaScript Patch Example**:
```javascript
// Intercept the cell click event
async onCellClicked(record, column, ev) {
    if (record.resModel === "purchase.request.line") {
        const product = record.data.product_id;
        const qty = record.data.product_qty || 0;
        const remark = record.data.x_remark || "";
        
        if (!product && (qty > 0 || remark.trim())) {
            // Show the custom dialog
            this.dialogService.add(DeleteLineDialog, {
                body: "You have not selected a product...",
                confirm: () => record.delete(),
                cancel: () => console.log("User cancelled")
            });
            return false;
        }
    }
    return super.onCellClicked(...arguments);
}
```

**QWeb Template Example**:
```xml
<t t-name="purchase_request_hide_cost_and_remark.DeleteLineDialog" owl="1">
    <Dialog title="title" size="'md'">
        <div class="modal-body">
            <p><t t-esc="props.body"/></p>
        </div>
        <t t-set-slot="footer">
            <button class="btn btn-primary" t-on-click="_onConfirm">OK</button>
            <button class="btn btn-secondary" t-on-click="_onCancel">Cancel</button>
        </t>
    </Dialog>
</t>
```

### Permission Group Reference
```xml
<!-- Correct permission group reference -->
<attribute name="groups">purchase_request.group_purchase_request_manager</attribute>
```

### Asset Loading Configuration
```python
'assets': {
    'web.assets_backend': [
        'Purchase_request_Hide_Cost_and_Remark/static/src/js/delete_line_dialog.js',
        'Purchase_request_Hide_Cost_and_Remark/static/src/js/list_renderer.js',
        'Purchase_request_Hide_Cost_and_Remark/static/src/xml/delete_line_dialog.xml',
    ],
},
```

## Customization

### Modifying Visibility

To adjust the visibility of fields or buttons, edit the `views/purchase_request_views.xml` file:

1.  **Change the permission group**:
    - Replace `purchase_request.group_purchase_request_manager` with another group.
    - Or remove the `groups` attribute entirely to make it visible to all users.

2.  **Add a new hidden field**:
    ```xml
    <xpath expr="//field[@name='your_field_name']" position="attributes">
        <attribute name="groups">purchase_request.group_purchase_request_manager</attribute>
    </xpath>
    ```

3.  **Hide other buttons**:
    ```xml
    <xpath expr="//button[@name='button_name']" position="attributes">
        <attribute name="groups">purchase_request.group_purchase_request_manager</attribute>
    </xpath>
    ```

### Modifying Remark Field Properties

Edit `models/purchase_request_line.py`:

```python
x_remark = fields.Char(
    string="Internal Remark",           # Change the field label
    help="Internal remark for managers", # Change the help text
    size=100,                          # Limit the character length
    required=False,                    # Set as a required field
)
```

## Troubleshooting

### Common Issues

1.  **Permissions not taking effect**
    - Check if the user is assigned to the correct permission group.
    - Clear the browser cache and log in again.
    - Ensure the module has been correctly installed and updated.

2.  **View not updating**
    - Update the module in developer mode.
    - Clear view cache: Settings → Technical → User Interface → Views.

3.  **Button still visible**
    - Verify that the button's `name` attribute is correct.
    - Check if the xpath expression is matching accurately.

### Debugging Methods

1.  **Check permission groups**:
    ```python
    # Execute in a Python shell
    user = self.env.user
    print("User groups:", user.groups_id.mapped('name'))
    ```

2.  **Check field permissions**:
    - Right-click on the field → View Metadata.
    - Check the `groups` attribute setting.

## Version Info

- **Module Version**: 17.0.1.0.0
- **Odoo Version**: 17.0
- **Dependencies**: purchase_request
- **Author**: System Administrator
- **License**: LGPL-3

## Support

For issues or custom development, please contact the system administrator or technical support team.

---

**Note**: After modifying permission configurations, it is recommended to verify the functionality in a test environment before deploying to production.
