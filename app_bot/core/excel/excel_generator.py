import io
import pandas as pd
from datetime import datetime, timedelta
from tortoise.expressions import Q
from core.database.models import UserLog, User, RequestLog
from settings import settings


async def create_excel(model):
    file_in_memory = io.BytesIO()
    try:
        data = await model.all().values_list('id', 'type', 'calculator_data', 'support_data', 'created_at',
                                             'user__username', 'user__fio', 'manager__username', 'manager_answer')

        df = pd.DataFrame(list(data), columns=['id', 'type', 'calculator_data', 'support_data', 'created_at',
                                               'user__username', 'user__fio', 'manager__username', 'manager_answer'])
    except:
        data = await model.all().values_list('id', 'user__username', 'state', 'created_at')

        df = pd.DataFrame(list(data), columns=['id', 'user__username', 'state', 'created_at'])

    df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None) if x is not None else None)
    df.to_excel(file_in_memory, index=False)

    file_in_memory.seek(0)
    return file_in_memory


async def manager_daily_excel(manager: User):
    file_in_memory = io.BytesIO()
    data = []

    today = datetime.now().replace(hour=settings.notification_hours, minute=settings.notification_minutes, second=0)
    yesterday = today - timedelta(days=1)

    # get user w/o log with request in RequestLog
    users = await User.filter(~Q(status='manager') & ~Q(status='admin') & Q(manager=manager))
    logs_with_request = await RequestLog.filter(~Q(request_id=None) & Q(created_at__range=(yesterday, today)))
    users_with_request = list(set([await log.user for log in logs_with_request]))
    for user in users:
        if user in users_with_request:  # we are interested in user w/o any requests
            continue
        user_logs = await UserLog.filter(
            user_id=user.user_id, created_at__range=(yesterday, today),
        ).order_by('created_at').values_list('state', flat=True)
        seconds_in_bot = (user.last_activity - user.created_at).total_seconds()

        # add data
        user_data = [
            user.user_id,
            user.username,
            user.status,
            ', '.join(user_logs),
            f'{seconds_in_bot // 3600}ч {(seconds_in_bot % 3600) // 60} мин',
        ]
        data.append(user_data)

    df = pd.DataFrame(data, columns=['Telegram user_id', 'username', 'Статус', 'Места', 'Время в боте'])
    df.to_excel(file_in_memory, index=False)

    file_in_memory.seek(0)
    return file_in_memory
