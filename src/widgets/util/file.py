GIF_FILE_EXTENSION = (".gif",)
IMAGE_FILE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff")
VIDEO_FILE_EXTENSIONS = (
    ".mp4",
    ".avi",
    ".flv",
    ".mov",
    ".webm",
    ".wmv",
    ".mkv",
    ".mpeg",
)


class File:
    @staticmethod
    def is_video_or_gif_file(file_path: str) -> bool:
        return file_path.endswith(VIDEO_FILE_EXTENSIONS + GIF_FILE_EXTENSION)

    @staticmethod
    def get_file_dialog_filter() -> str:
        return "*" + " *".join(
            GIF_FILE_EXTENSION + IMAGE_FILE_EXTENSIONS + VIDEO_FILE_EXTENSIONS
        )
