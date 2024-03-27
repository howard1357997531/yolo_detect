from .models import Alert, AlertPrivate

def alert(request):
    if request.user.is_authenticated:
        alert_all = AlertPrivate.objects.filter(user=request.user).order_by('-created_at')[:5]
        alert_check = AlertPrivate.objects.filter(user=request.user, is_checked=False).first()
    else:
        alert_all = Alert.objects.all().order_by('-created_at')[:5]
        alert_check = Alert.objects.filter(is_checked=False).first()
        
    alert_not_checked_qty = alert_check.total_quantity if alert_check else 0
    context = {'alert_all': alert_all, 'alert_not_checked_qty': alert_not_checked_qty}
    return context
