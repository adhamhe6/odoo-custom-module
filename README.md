# Odoo Sales & Attendance Enhancements

A custom Odoo module that extends the Sales and HR Attendance functionalities with new features like multi-sales orders, advanced attendance management, absence tracking, and global discounts.

## Features

1. **Multi Sales Orders**
   - Adds a "Multi Sale Order" menu under the Sales app.
   - Opens a wizard to create multiple sales orders simultaneously.
   - Auto-generates sales orders for selected partners with current date.

2. **Attendance Management**
   - Computes late hours and overtime in the `hr.attendance` model.
   - Monthly late/overtime calculations reset on the first day of the month.
   - Syncs with `resource_calendar_id` to track employee attendance.

3. **Absence Tracking**
   - Adds an "Absence" menu under the Attendance section.
   - Automatically logs absences if an employee has no attendance or leave records.
   - Daily cron job checks and records absent employees.

4. **Account Move Line Custom Field**
   - Custom field implementation within `account.move.line` (in progress due to enterprise limitations).

5. **Global Discount**
   - Adds a `global_discount_percentage` field to Sales and Purchase Orders.
   - Applies a global discount to the total amount.

## Usage

- Navigate to the **Sales** app to access the **Multi Sale Order** wizard.
- Check the **Attendance** section for enhanced tracking and the **Absence** menu.
- Apply global discounts directly from **Sales** or **Purchase Orders**.

## Known Issues

- Customizing `account.move.line` may require Odoo Enterprise access.
- Ensure the cron job for absence tracking is activated.
