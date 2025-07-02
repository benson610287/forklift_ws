import pyrealsense2 as rs

# 建立 pipeline 並啟動
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# 取得相機內參
profile = pipeline.get_active_profile()
video_stream = profile.get_stream(rs.stream.color).as_video_stream_profile()
intrinsics = video_stream.get_intrinsics()

print("fx:", intrinsics.fx)
print("fy:", intrinsics.fy)
print("cx:", intrinsics.ppx)
print("cy:", intrinsics.ppy)

pipeline.stop()
