from odoo import models, fields, api
from datetime import datetime, timedelta


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    daily_late_hour = fields.Float(string="Daily Late Hours", compute="_compute_late_and_overtime", store=True)
    daily_overtime = fields.Float(string="Daily Overtime", compute="_compute_late_and_overtime", store=True)
    monthly_late_hours = fields.Float(string="Monthly Late Hours", compute="_compute_monthly_hours", store=True)
    monthly_overtime = fields.Float(string="Monthly Overtime", compute="_compute_monthly_hours", store=True)

    @api.depends('check_in', 'check_out')
    def _compute_late_and_overtime(self):
        for record in self:
            record.daily_late_hour = 0.0
            record.daily_overtime = 0.0

            if not record.check_in or not record.employee_id.resource_calendar_id:
                continue

            work_schedule = record.employee_id.resource_calendar_id
            check_in_time = record.check_in
            check_out_time = record.check_out if record.check_out else fields.Datetime.now()

            for attendance in work_schedule.attendance_ids:
                if int(attendance.dayofweek) == check_in_time.weekday():
                    # Convert float hours (e.g., 8.5) to time objects
                    work_start = datetime.combine(check_in_time.date(), (datetime.min + timedelta(hours=attendance.hour_from)).time())
                    work_end = datetime.combine(check_in_time.date(), (datetime.min + timedelta(hours=attendance.hour_to)).time())

                    # Late Hours Calculation
                    if check_in_time > work_start:
                        record.daily_late_hour = (check_in_time - work_start).total_seconds() / 3600

                    # Overtime Calculation
                    if check_out_time > work_end:
                        record.daily_overtime = (check_out_time - work_end).total_seconds() / 3600

    @api.depends('employee_id', 'daily_late_hour', 'daily_overtime')
    def _compute_monthly_hours(self):
        for record in self:
            first_day = datetime.today().replace(day=1)
            last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            attendances = self.search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', first_day),
                ('check_in', '<=', last_day)
            ])

            record.monthly_late_hours = sum(att.daily_late_hour for att in attendances)
            record.monthly_overtime = sum(att.daily_overtime for att in attendances)

    @api.model
    def reset_monthly_hours(self):
        """Reset monthly late and overtime hours on the first day of each month."""
        today = fields.Date.today()
        if today.day == 1:
            self.search([]).write({'monthly_late_hours': 0.0, 'monthly_overtime': 0.0})
