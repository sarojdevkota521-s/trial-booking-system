
def notification_count(request):
    if request.user.is_authenticated:
        return {
            'notification_count': request.user.notifications.filter(is_read=False).count()
        }
    return {}

