LINE_ROUTES = {
  "image": "line_bot:image_handler",
  "video": "line_bot:video_handler",
  "file": "line_bot:file_handler",
  "audio": "line_bot:audio_handler",
}

AWS_ROUTES = {
  "image": "s3_handler:image_upload",
  "video": "s3_handler:video_upload",
  "file": "s3_handler:file_upload",
  "audio": "s3_handler:audio_upload",
}
