# controllers/reservation_controller.py
from models.reservation import ReservationModel
from models.notification import NotificationModel

class ReservationController:
    # Student actions
    def create(self, user_id, inventory_id, start_dt, end_dt):
        ReservationModel.create(user_id, inventory_id, start_dt, end_dt)
        # Notify professor(s) — in a real app, map to course/professor
        NotificationModel.create(user_id, "Reservation submitted. Awaiting professor review.")

    def student_history(self, user_id):
        return ReservationModel.by_student(user_id)

    def cancel_pending(self, res_id, user_id):
        ReservationModel.update_status(res_id, "cancelled")
        NotificationModel.create(user_id, "Your reservation was cancelled.")

    def request_return(self, res_id, user_id):
        ReservationModel.update_status(res_id, "return_requested")
        NotificationModel.create(user_id, "Return request submitted to admin.")

    def modify_pending(self, res_id, user_id, start_dt=None, end_dt=None, notes=""):
        if start_dt and end_dt:
            ReservationModel.modify_times(res_id, start_dt, end_dt)
        ReservationModel.update_status(res_id, "modified")
        NotificationModel.create(user_id, "Reservation updated (pending).")

    # Professor actions
    def pending_for_professor(self):
        return ReservationModel.by_status("pending_prof")

    def professor_approve(self, res_id, professor_id=None):
        ReservationModel.update_status(res_id, "pending_admin")
        res = ReservationModel.get(res_id)
        NotificationModel.create(res["user_id"], "Professor approved your reservation.")

    def professor_reject(self, res_id, professor_id=None):
        ReservationModel.update_status(res_id, "cancelled")
        res = ReservationModel.get(res_id)
        NotificationModel.create(res["user_id"], "Professor rejected your reservation.")

    # Admin actions
    def pending_for_admin(self):
        return ReservationModel.by_status("pending_admin")

    def admin_approve(self, res_id, admin_id=None):
        ReservationModel.update_status(res_id, "approved")
        res = ReservationModel.get(res_id)
        NotificationModel.create(res["user_id"], "Admin approved your reservation.")

    def admin_reject(self, res_id, admin_id=None):
        ReservationModel.update_status(res_id, "cancelled")
        res = ReservationModel.get(res_id)
        NotificationModel.create(res["user_id"], "Admin rejected your reservation.")

    def admin_confirm_return(self, res_id, admin_id=None):
        ReservationModel.update_status(res_id, "returned")
        res = ReservationModel.get(res_id)
        NotificationModel.create(res["user_id"], "Return confirmed. Thank you.")
