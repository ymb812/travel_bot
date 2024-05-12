import io
import pandas as pd


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
