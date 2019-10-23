import time
import cv2



class BaseCamera(object):
   thread = None  # background thread that reads frames from camera
   frame = None  # current frame is stored here by background thread
   last_access = 0  # time of last client access to the camera
   # ...

   @staticmethod
   def frames():
      """Generator that returns frames from the camera."""
      raise RuntimeError('Must be implemented by subclasses.')

   @classmethod
   def _thread(cls):
      """Camera background thread."""
      print('Starting camera thread.')
      frames_iterator = cls.frames()
      for frame in frames_iterator:
            BaseCamera.frame = frame

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 10:
               frames_iterator.close()
               print('Stopping camera thread due to inactivity.')
               break
      BaseCamera.thread = None



class Camera(BaseCamera):
   @staticmethod
   def frames():
      camera = cv2.VideoCapture(0)
      if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

      while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
