# Copyright 2017 Comunitea Servicios Tecnológicos S.L.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging
import time
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):

    _inherit = "hr.employee"
        # _sql_constraints = [(
        #     'rfid_card_code_uniq',
        #     'UNIQUE(rfid_card_code)',
        #     'The rfid code should be unique.'
        # )]

        # rfid_card_code = fields.Char("RFID Card Code")


        # @api.model
        # def register_attendance(self, card_code):
        #     """ Register the attendance of the employee.
        #     :returns: dictionary
        #         'rfid_card_code': char
        #         'employee_name': char
        #         'employee_id': int
        #         'error_message': char
        #         'logged': boolean
        #         'action': check_in/check_out
        #     """

        #     res = {
        #         'rfid_card_code': card_code,
        #         'employee_name': '',
        #         'employee_id': False,
        #         'error_message': '',
        #         'logged': False,
        #         'action': 'FALSE',
        #     }
        #     employee = self.search([('rfid_card_code', '=', card_code)], limit=1)
        #     if employee:
        #         res['employee_name'] = employee.name
        #         res['employee_id'] = employee.id
        #     else:
        #         msg = _("No employee found with card %s") % card_code
        #         _logger.warning(msg)
        #         res['error_message'] = msg
        #         return res
        #     try:
        #         attendance = employee.attendance_action_change()
        #         if attendance:
        #             msg = _('Attendance recorded for employee %s') % employee.name
        #             _logger.debug(msg)
        #             res['logged'] = True
        #             if attendance.check_out:
        #                 res['action'] = 'check_out'
        #             else:
        #                 res['action'] = 'check_in'
        #             return res
        #         else:
        #             msg = _('No attendance was recorded for '
        #                     'employee %s') % employee.name
        #             _logger.error(msg)
        #             res['error_message'] = msg
        #             return res
        #     except Exception as e:
        #         res['error_message'] = e
        #         _logger.error(e)
        #     return res

############ until here it was standard OCA

    @api.multi
    def attendance_action_with_external_timestamp(self, timestamp = None):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))

        if not timestamp:
            timestamp = fields.Datetime.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("in attendance_action_change_sync - got timestamp as an input from outside the method (call)", timestamp)

        print("in attendance_action_change_sync - timestamp ", timestamp)

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': timestamp,
            }
            print("in attendance_action_change_sync - when checked_out - self", self)
            print("in attendance_action_change_sync - when checked_out - self.attendance_state ", self.attendance_state)
            return self.env['hr.attendance'].create(vals)
        else:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
            if attendance:
                print("in attendance_action_change_sync - when checked_in - self", self)
                print("in attendance_action_change_sync - when checked_in - self.attendance_state ", self.attendance_state)
                attendance.check_out = timestamp
            else:
                raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                    'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.name, })
            return attendance

    @api.model
    def registerAttendanceWithExternalTimestamp(self, card_code, timestamp = None ):
        """ Register the attendance of the employee.
        :returns: dictionary
            'rfid_card_code': char
            'employee_name': char
            'employee_id': int
            'error_message': char
            'logged': boolean
            'action': check_in/check_out
        """
        #timestamp= None

        res = {
            'rfid_card_code': card_code,
            'employee_name': '',
            'employee_id': False,
            'error_message': '',
            'logged': False,
            'action': 'FALSE',
        }
        employee = self.search([('rfid_card_code', '=', card_code)], limit=1)
        if not timestamp:
            timestamp = fields.Datetime.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("in register_attendance - got timestamp as an input from outside the method (call)", timestamp)
        print("in register_attendance - timestamp: ", timestamp)
        print("in register_attendance - fields.Datetime.to_datetime(time.strftime())", fields.Datetime.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S")))
        if employee:
            res['employee_name'] = employee.name
            res['employee_id'] = employee.id
        else:
            msg = _("No employee found with card %s") % card_code
            _logger.warning(msg)
            res['error_message'] = msg
            return res
        try:
            attendance = employee.attendance_action_with_external_timestamp(timestamp)
            print("in register_attendance - attendance: ", attendance)
            if attendance:
                msg = _('Attendance recorded for employee %s') % employee.name
                _logger.debug(msg)
                res['logged'] = True
                if attendance.check_out:
                    res['action'] = 'check_out'
                else:
                    res['action'] = 'check_in'
                print("in register_attendance - res: ", res)
                return res
            else:
                msg = _('No attendance was recorded for '
                        'employee %s') % employee.name
                _logger.error(msg)
                res['error_message'] = msg
                return res
        except Exception as e:
            res['error_message'] = e
            _logger.error(e)
        return res

    @api.model
    def registerMultipleAsyncAttendances(self, attendancesToDispatch):
        """ Register the attendance of the employee.
        :returns: string
        "All OK"
        "Something went wrong"
        """
        response = "All OK"
        for attendance in attendancesToDispatch:
            res = self.registerAttendanceWithExternalTimestamp(attendance[0], attendance[1])
            if res['action']==attendance[2]:
                print("wonderful, there is concordance database and async checkinORcheckout")
            else:
                print("Oh! no concordance database and async checkinORcheckout")
                response = "Something went wrong"

        return response

