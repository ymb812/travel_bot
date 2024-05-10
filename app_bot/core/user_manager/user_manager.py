import logging
from core.database.models import User, RequestLog
from tortoise.expressions import Q

logger = logging.getLogger(__name__)


async def add_manager_to_user(user_id: int, request_id: int = None, is_from_scheduler: bool = False) -> User | None:
    # check if the user already has a manager
    user = await User.get(user_id=user_id)
    if user.manager_id:
        logger.info(f'User {user_id} already has the manager {user.manager_id}')

    else:
        # get all logs with request_id != None, order by ID
        managers = await User.filter(status='manager').all().order_by('id')
        if not managers:
            logger.error('There are no managers in the bot!')
            return
        manager_to_send: User = managers[0]

        # get logs with and w/o request if we have to pin all users w/o manager
        if is_from_scheduler:
            logs = await RequestLog.all().order_by('id')
        else:
            logs = await RequestLog.filter(~Q(request_id=None)).all().order_by('id')

        if logs:
            last_manager: User = await logs[-1].manager
            try:
                manager_to_send = managers[managers.index(last_manager) + 1]
            except IndexError:
                logger.info(f'Going to the 1st manager_id={manager_to_send.user_id}')
            except ValueError:
                logger.error(f'There is no manager manager_id={manager_to_send.user_id}')

        # add manager to user
        user.manager_id = manager_to_send.user_id
        await user.save()

    # create log w/o request id - if we only pin user
    if not request_id:
        await RequestLog.create_log(manager_id=user.manager_id, user_id=user_id)
    return await user.manager
