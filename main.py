import constants
from pipeline import VideoPipeline
from pipeline import AudioPipeline

pipeline = VideoPipeline(constants.OUTPUT_DIR, frameRate=constants.FRAME_RATE, prefix = constants.IMAGE_PREFIX, folder = constants.FRAME_DIR, processed_folder = constants.PROCESSED_DIR,)
                         #smileCNN_path = constants.SMILECNN_PATH)
report = pipeline.execute(constants.VIDEO_PATH)

audio_pipeline = AudioPipeline()
audio_report = pipeline.execute()

print(report)
print(audio_report)
