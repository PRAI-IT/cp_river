from typing import Dict, Text
import pyarrow.parquet as pq
import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs

df_logs = pq.read_table("update_logs_df_2024-08-05_video_to_video.parquet").to_pandas()
df_logs[0] = df_logs[0].astype(str)
df_logs[1] = df_logs[1].astype(str)

df_video = pq.read_table("dataset/video_stat.parquet", columns=['video_id']).to_pandas()
df_video['video_id'] = df_video['video_id'].astype(str)
ratings = tf.data.Dataset.from_tensor_slices(dict(df_logs)).map(lambda x: {
    "video_old_id": x[0],
    "video_id": x[1]
})
video = tf.data.Dataset.from_tensor_slices(dict(df_video)).map(lambda x: x["video_id"])


class MovielensModel(tfrs.Model):

    def __init__(self, video_old_model, video_model, task):
        super().__init__()
        self.video_model: tf.keras.Model = video_model
        self.video_old_model: tf.keras.Model = video_old_model
        self.task: tf.keras.layers.Layer = task

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        video_old_embeddings = self.video_old_model(features["video_old_id"])
        positive_video_embeddings = self.video_model(features["video_id"])
        return self.task(video_old_embeddings, positive_video_embeddings)


# # Randomly shuffle data and split between train and test.
tf.random.set_seed(42)
shuffled = ratings.shuffle(1_000_000, seed=42, reshuffle_each_iteration=False)

train = shuffled.take(800_000)
test = shuffled.skip(800_000).take(200_000)

video_id = video.batch(100_000)
# video_old_ids = ratings.batch(100_000).map(lambda x: x["video_old_id"])

unique_video_ids = np.unique(np.concatenate(list(video_id)))
# unique_video_old = np.unique(np.concatenate(list(video_old_ids)))

embedding_dimension = 64

video_old_model = tf.keras.Sequential([
    tf.keras.layers.StringLookup(
        vocabulary=unique_video_ids, mask_token=None),
    tf.keras.layers.Embedding(len(unique_video_ids) + 1, embedding_dimension)
])

video_model = tf.keras.Sequential([
    tf.keras.layers.StringLookup(
        vocabulary=unique_video_ids, mask_token=None),
    tf.keras.layers.Embedding(len(unique_video_ids) + 1, embedding_dimension)
])


task = tfrs.tasks.Retrieval()
model = MovielensModel(video_old_model, video_model, task)
model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

cached_train = train.shuffle(100_000).batch(8192).cache()
cached_test = test.batch(4096).cache()
model.fit(cached_train, epochs=10)

task = tfrs.tasks.Retrieval()
test_accuracy = model.evaluate(test.batch(4096), return_dict=True)
print(test_accuracy)



index = tfrs.layers.factorized_top_k.BruteForce(model.video_old_model)

index.index_from_dataset(
  tf.data.Dataset.zip((video.batch(15_000_000), video.batch(15_000_000).map(model.video_model)))
)


# _, titles = index(tf.constant([b"0054d245-d7fd-4259-97b0-3f87a37e1b11",b"c35be620-b280-48b0-8556-043a57e36b1e"]))
# print(_, titles)




tf.saved_model.save(index, "models/video_to_video")
