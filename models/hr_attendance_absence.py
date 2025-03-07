from odoo import models, fields, api
from datetime import date, timedelta


class AttendanceAbsence(models.Model):
    _name = 'attendance.absence'
    _description = 'Employee Absence Record'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True)
    date = fields.Date(string="Absence Date", required=True, readonly=True)

    @api.model
    def check_absences(self):
        """
        Cron method: Check daily for absent employees and log their absence.
        """
        today = date.today()

        # Get all employees with a working schedule for today
        employees = self.env['hr.employee'].search([]).filtered(
            lambda emp: emp.resource_calendar_id and any(
                int(att.dayofweek) == today.weekday() for att in emp.resource_calendar_id.attendance_ids
            )
        )

        for employee in employees:
            # Check if the employee is present (attendance or leave record for today)
            attendance_today = self.env['hr.attendance'].search_count([
                ('employee_id', '=', employee.id),
                ('check_in', '>=', today.strftime('%Y-%m-%d 00:00:00')),
                ('check_in', '<=', today.strftime('%Y-%m-%d 23:59:59'))
            ])

            leave_today = self.env['hr.leave'].search_count([
                ('employee_id', '=', employee.id),
                ('date_from', '<=', today),
                ('date_to', '>=', today),
                ('state', '=', 'validate')
            ])

            # If no attendance or leave records exist, mark as absent
            if not attendance_today and not leave_today:
                self.create({
                    'employee_id': employee.id,
                    'date': today,
                })
