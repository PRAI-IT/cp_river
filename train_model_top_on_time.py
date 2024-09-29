from typing import Dict, Text
import pyarrow.parquet as pq
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs

df_logs = pq.read_table("dataset/time/update_logs_df_2024-08-05.parquet", columns=['event_timestamp', 'video_id']).to_pandas()
df_logs['video_id'] = df_logs['video_id'].astype(str)
df_video = pq.read_table("dataset/video_stat.parquet", columns=['video_id']).to_pandas()
df_video['video_id'] = df_video['video_id'].astype(str)
ratings = tf.data.Dataset.from_tensor_slices(dict(df_logs)).map(lambda x: {
    "time": x["event_timestamp"],
    "video_id": x["video_id"]
})
video = tf.data.Dataset.from_tensor_slices(dict(df_video)).map(lambda x: x["video_id"])



class MovielensModel(tfrs.Model):

    def __init__(self, time_model, video_model):
        super().__init__()
        self.video_model: tf.keras.Model = video_model
        self.time_model: tf.keras.Model = time_model
        self.task: tf.keras.layers.Layer = task

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        time_embeddings = self.time_model(features["time"])
        positive_video_embeddings = self.video_model(features["video_id"])
        return self.task(time_embeddings, positive_video_embeddings)




tf.random.set_seed(42)
shuffled = ratings.shuffle(100_000, seed=42, reshuffle_each_iteration=False)

train = shuffled.take(80_000)
test = shuffled.skip(80_000).take(20_000)

video_id = video.batch(1_000_000)
time_ids = ratings.batch(1_000_000).map(lambda x: x["time"])

unique_video_ids = np.unique(np.concatenate(list(video_id)))
unique_time = np.unique(np.concatenate(list(time_ids)))


embedding_dimension = 64


time_model = tf.keras.Sequential([
    tf.keras.layers.StringLookup(
        vocabulary=unique_time, mask_token=None),
    tf.keras.layers.Embedding(len(unique_time) + 1, embedding_dimension)
])

video_model = tf.keras.Sequential([
    tf.keras.layers.StringLookup(
        vocabulary=unique_video_ids, mask_token=None),
    tf.keras.layers.Embedding(len(unique_video_ids) + 1, embedding_dimension)
])

metrics = tfrs.metrics.FactorizedTopK(
    candidates=video.batch(128).map(video_model)
)
task = tfrs.tasks.Retrieval(
    metrics=metrics
)

model = MovielensModel(time_model, video_model)
model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

cached_train = train.shuffle(100_000).batch(8192).cache()
cached_test = test.batch(4096).cache()
# Train.
model.fit(cached_train, epochs=10)


# model.evaluate(test.batch(4096), return_dict=True)

index = tfrs.layers.factorized_top_k.BruteForce(model.video_old_model)

index.index_from_dataset(
  tf.data.Dataset.zip((video.batch(15_000_000), video.batch(15_000_000).map(model.video_model)))
)


# _, titles = index(tf.constant([b"20"]))
# print(_, titles)

tf.saved_model.save(index, "models/time")
