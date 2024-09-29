import pyarrow.parquet as pq
import pandas as pd

df_logs = pq.read_table("dataset/logs_df_2024-08-05.parquet", columns=['user_id', 'video_id'],
                        filters=[('watchtime', '>', 30)]).to_pandas()
df_logs = df_logs[df_logs['video_id'].notnull()]
df_logs = df_logs.groupby('user_id', as_index=False).agg({'video_id': '|'.join})
df_logs = df_logs[df_logs['video_id'].str.len() > 36]
df_logs['video_id'] = df_logs['video_id'].map(lambda x: x[:73])
df_logs.pop('user_id')
df_logs = df_logs['video_id'].str.split('|', expand=True)
for idx in df_logs.columns.tolist():
    if idx != 0 and idx != 1:
        df_logs.pop(idx)
df_logs = df_logs[df_logs[0] != df_logs[1]]
df_logs.to_parquet('update_logs_df_2024-08-05_video_to_video.parquet')

