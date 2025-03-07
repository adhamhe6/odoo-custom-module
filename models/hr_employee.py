from odoo import models, fields, api
from datetime import date


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    monthly_late_hours = fields.Float(
        string="Monthly Late Hours",
        compute="_compute_employee_hours",
        store=True
    )
    monthly_overtime = fields.Float(
        string="Monthly Overtime",
        compute="_compute_employee_hours",
        store=True
    )

    @api.depends('attendance_ids.check_in', 'attendance_ids.check_out')
    def _compute_employee_hours(self):
        """
        Computes the monthly late hours and overtime based on the current month's attendances.
        """
        for employee in self:
            # Get first day of the current month
            first_day_of_month = date.today().replace(day=1)

            # Fetch current month's attendances for this employee
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                ('check_in', '>=', first_day_of_month)
            ])

            # Sum up the calculated late hours and overtime
            employee.monthly_late_hours = sum(att.monthly_late_hours for att in attendances)
            employee.monthly_overtime = sum(att.monthly_overtime for att in attendances)


class PublicEmployee(models.Model):
    """
    Public Employee inherits from hr.employee.public to expose calculated attendance fields.
    """
    _inherit = 'hr.employee.public'

    monthly_late_hours = fields.Float(string="Monthly Late Hours", readonly=True)
    monthly_overtime = fields.Float(string="Monthly Overtime", readonly=True)

    def _compute_public_employee_hours(self):
        """
        Syncs the computed attendance data from hr.employee to hr.employee.public.
        """
        for public_employee in self:
            # Find the corresponding internal hr.employee record
            internal_employee = self.env['hr.employee'].search([('user_id', '=', public_employee.user_id.id)], limit=1)
            if internal_employee:
                public_employee.monthly_late_hours = internal_employee.monthly_late_hours
                public_employee.monthly_overtime = internal_employee.monthly_overtime

    @api.model
    def create(self, vals):
        record = super(PublicEmployee, self).create(vals)
        record._compute_public_employee_hours()
        return record

    def write(self, vals):
        result = super(PublicEmployee, self).write(vals)
        self._compute_public_employee_hours()
        return result
