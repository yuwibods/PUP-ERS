# controllers/notification_controller.py
from models.notification import NotificationModel

class NotificationController:
    def unread_for(self, user_id):
        return NotificationModel.unread_for(user_id)

    def mark_read(self, notif_id):
        NotificationModel.mark_read(notif_id)
