
class NotificationService:
    """
    Sends notifications to our users when important things happen.
    """

    def notify_users(self, message: str) -> None:
        # Imagine this method sends a notification to the user.
        print(f"Notification sent to all users: {message}")


notification_service = NotificationService()