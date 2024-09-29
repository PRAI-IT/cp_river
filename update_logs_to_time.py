import pyarrow.parquet as pq

df_logs = pq.read_table("dataset/logs_df_2024-08-05.parquet", columns=['event_timestamp', 'video_id'],
                        filters=[('watchtime', '>', 30), ('region', '=', 'f28a922a-68b9-46ce-8b52-c0be09413514')]).to_pandas()
df_logs['event_timestamp'] = df_logs['event_timestamp'].map(lambda x: x.strftime('%H'))
df_logs.to_parquet('update_logs_df_2024-08-05_time.parquet')



