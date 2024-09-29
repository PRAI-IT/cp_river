import pyarrow.parquet as pq
import tensorflow as tf
import tensorflow_recommenders as tfrs

model_vtv = tf.saved_model.load("models/video_to_video")
df_video = pq.read_table("dataset/video_stat.parquet", columns=['video_id']).to_pandas()
df_video['video_id'] = df_video['video_id'].astype(str)
index = tfrs.layers.factorized_top_k.BruteForce(model_vtv.video_old_model)
video = tf.data.Dataset.from_tensor_slices(dict(df_video)).map(lambda x: x["video_id"])
index.index_from_dataset(
  tf.data.Dataset.zip((video.batch(15_000_000), video.batch(15_000_000).map(model_vtv.video_model)))
)

# Get recommendations.
_, titles = index(tf.constant(["0054d245-d7fd-4259-97b0-3f87a37e1b11","c35be620-b280-48b0-8556-043a57e36b1e"]))
print(titles)



