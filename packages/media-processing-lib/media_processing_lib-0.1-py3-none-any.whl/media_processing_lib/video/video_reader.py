import numpy as np
from typing import Optional

from .mpl_video import MPLVideo
from ..utils import dprint

def tryReadVideo(path:str, vidLib:str="imageio", count:int=5, nFrames:Optional[int]=None) -> MPLVideo:
	extension = path.lower().split(".")[-1]
	assert extension in ("gif", "mp4", "mov", "mkv")
	assert vidLib in ("imageio", "pims", "opencv")

	if vidLib == "pims":
		from .libs.pims import readRaw as readFn
	elif vidLib == "imageio":
		from .libs.imageio import readRaw as readFn
	elif vidLib == "opencv":
		from .libs.opencv import readRaw as readFn

	i = 0
	while True:
		try:
			data, fps, shape, nFrames = readFn(path, nFrames)
			assert len(shape) == 4
			video = MPLVideo(data, fps, shape, nFrames)
			dprint("[mpl::video] Read video %s. Shape: %s. FPS: %2.3f" % (path, str(video.shape), video.fps))
			return video
		except Exception as e:
			dprint("Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception(e)
