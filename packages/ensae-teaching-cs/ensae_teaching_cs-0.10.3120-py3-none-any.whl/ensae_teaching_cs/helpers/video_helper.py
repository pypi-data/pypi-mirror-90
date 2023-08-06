"""
@file
@brief video helpers
"""
import os


def make_video(images, outvid=None, fps=5, size=None,
               is_color=True, format="XVID"):
    """
    Creates a video from a list of images.

    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frames per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see `fourcc <http://www.fourcc.org/codecs.php>`_
    @return                 `VideoWriter <http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/
                            py_gui/py_video_display/py_video_display.html>`_

    The function relies on `opencv <http://opencv-python-tutroals.readthedocs.org/en/latest/>`_.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
    The function does not use :epkg:`moviepy` but it is a
    a recommended module to do that.
    """
    if len(images) == 0:
        raise ValueError("no image to convert into a video")
    from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize  # pylint: disable=E0401
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    vid.release()
    return vid
