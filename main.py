from PIL import Image, ImageDraw
from flask import Flask, Response
from mss import mss
import face_recognition, cv2, io, numpy

SCREENSHOT_COORDS = (78,0,1200,800)

# map but converts to list
def map_to_list(func, iter_obj):
  return list(map(func, iter_obj))

def toBytes(image):
  imageByteArr = io.BytesIO()
  image.save(imageByteArr, format='JPEG')
  return imageByteArr.getvalue()

def create_image(image, pil_image, dimensions_match_multiplier):
  def match_dimensions(e):
    return (e[0] * dimensions_match_multiplier, e[1] * dimensions_match_multiplier)

  # find facial features in all the faces in the image
  face_landmarks_list = face_recognition.face_landmarks(image)

  for face_landmarks in face_landmarks_list:
    draw_obj = ImageDraw.Draw(pil_image, 'RGBA')

    # match dimensions for all landmarks
    face_landmarks['left_eyebrow'] = map_to_list(match_dimensions, face_landmarks['left_eyebrow'])
    face_landmarks['right_eyebrow'] = map_to_list(match_dimensions, face_landmarks['right_eyebrow'])
    face_landmarks['top_lip'] = map_to_list(match_dimensions, face_landmarks['top_lip'])
    face_landmarks['bottom_lip'] = map_to_list(match_dimensions, face_landmarks['bottom_lip'])
    face_landmarks['left_eye'] = map_to_list(match_dimensions, face_landmarks['left_eye'])
    face_landmarks['right_eye'] = map_to_list(match_dimensions, face_landmarks['right_eye'])

    # eyebrows
    draw_obj.polygon(face_landmarks['left_eyebrow'], fill=(255, 255, 0, 127))
    draw_obj.polygon(face_landmarks['right_eyebrow'], fill=(255, 255, 0, 127))

    # lipstick
    draw_obj.polygon(face_landmarks['top_lip'], fill=(0, 0, 255, 127))
    draw_obj.polygon(face_landmarks['bottom_lip'], fill=(0, 0, 255, 127))

    # eyeliner
    draw_obj.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill="#000", width=5)
    draw_obj.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill="#000", width=5)

    # initialize mustache landmarks
    def mustache_from_lip(arr):
      for i, e in enumerate(arr):
        arr[i] = ((e[0], e[1] - SCREENSHOT_COORDS[3] * 0.01383399209 ))
      return arr
    mustache_landmarks = mustache_from_lip(face_landmarks['top_lip'])

    # mustache
    draw_obj.polygon(mustache_landmarks, fill=(255, 0, 0, 127))


  return toBytes(pil_image)

def getResizeDimensions(initialWidth, initialHeight, targetPixelCount):
  divisor = (initialWidth * initialHeight / targetPixelCount) ** .5
  newWidth, newHeight = int(initialWidth // divisor), int(initialHeight // divisor)
  return newWidth, newHeight

def screenshot_and_filter(screenshot_obj):
  global SCREENSHOT_COORDS
  
  screenshot_obj.get_pixels({
    'top': SCREENSHOT_COORDS[0],
    'left': SCREENSHOT_COORDS[1],
    'width': SCREENSHOT_COORDS[2],
    'height': SCREENSHOT_COORDS[3]
  })
  img = Image.frombytes('RGB', (screenshot_obj.width, screenshot_obj.height), screenshot_obj.image)

  image_to_filter_dimensions = getResizeDimensions(img.size[0], img.size[1], 100000)
  dimensions_match_multiplier = img.size[0] / image_to_filter_dimensions[0]

  image_to_filter = img.resize(image_to_filter_dimensions, Image.ANTIALIAS)
  image_to_filter = cv2.cvtColor(numpy.array(image_to_filter), cv2.COLOR_RGB2BGR)

  rVal = create_image(image_to_filter, img, dimensions_match_multiplier)
  return rVal

app = Flask(__name__)

def gen():
  with mss() as screenshot_obj:
    while True:
      frame = screenshot_and_filter(screenshot_obj)
      if(frame):
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
  return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)