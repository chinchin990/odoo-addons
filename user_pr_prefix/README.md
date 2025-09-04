# User PR Prefix & Auto Number Module

## Overview

This module enhances Odoo's Purchase Request system by adding user-defined prefixes and an automatic numbering feature.

## Features

✅ **User-Defined Prefixes**: Each user can have their own unique PR prefix.  
✅ **Automatic Numbering**: Automatically generates a PR number in the format `[Prefix][Year]-[Sequence]` upon creation.  
✅ **Annual Reset**: The sequence number resets to 0001 at the beginning of each year.  
✅ **User-Specific Sequences**: Numbering sequences are tracked independently for each user.  
✅ **Smart Parsing**: Automatically parses existing numbers to continue the sequence correctly.  

## Number Format

```
[User Prefix][Year]-[4-digit sequence number]
```

**Examples:**
- `K1-WH-PR-2025-0001`
- `K1-WH-PR-2025-0002`  
- `K2-SH-PR-2025-0001` (for a different user)

## Installation

### 1. Deploy the Module
Copy the `user_pr_prefix` folder to your Odoo addons directory:
```bash
cp -r user_pr_prefix /path/to/odoo/addons/
```

### 2. Verify Purchase Request Model
Ensure that the `purchase.request` model exists in your Odoo system (it may be provided by a third-party or custom module).

### 3. Update Module List
In Odoo:
- Go to the **Apps** menu.
- Click on **Update Apps List**.
- Search for "User PR Prefix".
- Click **Install**.

## Configuration & Usage

### 1. Set User PR Prefix

**Method 1: Via User Settings**
1. Go to **Settings → Users & Companies → Users**.
2. Select the user you want to configure.
3. In the user form, find the **PR Prefix** field below the email field.
4. Set the **PR Prefix** (e.g., `K1-WH-PR-`).

**Method 2: Via Dedicated Menu**
1. Go to **Settings → PR Prefix Setup**.
2. View and manage prefixes for all users in one place.

### 2. Create a Purchase Request

1. Go to **Purchase Requests → My Requests**.
2. Click **Create**.
3. The **PR number will be generated automatically**; no manual input is needed.
4. Fill in the other required information and save.

## Numbering Logic

### Generation Rules
1. **Get User Prefix**: Fetches the prefix from the current user's `pr_prefix` field.
2. **Get Current Year**: Uses the 4-digit year format.
3. **Find Max Sequence**: Searches for the highest existing number for that prefix and year.
4. **Increment Sequence**: Adds 1 to the highest found sequence.
5. **Format**: Pads the number with leading zeros to 4 digits.

### Example Scenarios
```python
# User A sets their prefix to "K1-WH-PR-"
# First PR created in 2025:
→ K1-WH-PR-2025-0001

# Subsequent PRs:
→ K1-WH-PR-2025-0002
→ K1-WH-PR-2025-0003

# User B sets their prefix to "K2-SH-PR-"
# Creates a PR in the same year:
→ K2-SH-PR-2025-0001  # Independent sequence
→ K2-SH-PR-2025-0002

# User A creates a PR in 2026:
→ K1-WH-PR-2026-0001  # Sequence resets for the new year
```

## Technical Details

### File Structure
```
user_pr_prefix/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── res_users.py          # Extends the user model
│   └── purchase_request.py   # Extends the PR model
└── views/
    └── res_users_views.xml   # Extends the user interface
```

### Core Methods
- `PurchaseRequest.create()` - Overridden to automatically generate the number.
- `_get_next_sequence_number()` - Gets the next number in the sequence.
- `preview_next_pr_number()` - Previews the next available number.

### Database Fields
- `res_users.pr_prefix` - Stores the user's PR prefix.

## Testing

### Test Steps
1. **Set User Prefix**
   - Set a prefix for a test user: `TEST-PR-`
   
2. **Create the First PR**
   - Expected number: `TEST-PR-2025-0001`
   
3. **Create a Second PR**
   - Expected number: `TEST-PR-2025-0002`
   
4. **Test with a Different User**
   - Set a different prefix for another user: `USER2-PR-`
   - Expected number: `USER2-PR-2025-0001`
   
5. **Annual Test** (if crossing a year)
   - First PR in the new year should be: `TEST-PR-2026-0001`

### Verification Points
- ✅ Correct number format.
- ✅ Sequential increment.
- ✅ Independent sequences per user.
- ✅ Annual sequence reset.
- ✅ UI displays correctly.

## Troubleshooting

### Common Issues

**Q: The number is not generating automatically.**
A: Check the following:
- Is the module installed correctly?
- Is the `custom_purchase_list` module installed?
- Has a PR prefix been set for the current user?

**Q: The number format is incorrect.**
A: Check the following:
- Does the PR prefix contain special characters?
- It is recommended to use a combination of letters, numbers, and hyphens.

**Q: The sequence is not continuous.**
A: Possible reasons:
- Deleted PRs do not free up their sequence numbers (this is normal).
- Gaps may appear during concurrent creation by multiple users.

### Debug Logging
Enable debug logs to see the number generation process:
```python
_logger.info(f"Generated PR number: {vals['name']} for user {user.name}")
```

## Compatibility

- **Odoo Version**: 17.0+
- **Dependencies**: `base` (requires `purchase.request` model to exist in the system)
- **Python Version**: 3.8+

## Author

Your Name  
Module Version: 17.0.1.0.0

## License

This module is licensed under Odoo's license terms.
