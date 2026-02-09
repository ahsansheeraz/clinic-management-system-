from .models import ActivityLog

def log_action(user, action_type, table_name, record_id=None, old_value=None, new_value=None):
    ActivityLog.objects.create(
        user=user,
        action_type=action_type,
        table_name=table_name,
        record_id=record_id,
        old_value=old_value,
        new_value=new_value
    )
