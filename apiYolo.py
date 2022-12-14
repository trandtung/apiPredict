from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
import os
import my_yolov6
import cv2

# Khởi tạo Flask Server Backend
app = Flask(__name__)
CORS(app)

# Apply Flask CORS
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "static"
app.config['PREVIEW'] = "static/preview"
app.config['FOlDER_IMG'] = "predictFolder"
yolov6_model = my_yolov6.my_yolov6(
    "weights/best-train.pt", "cpu", "data/mydataset.yaml", 640, False)


@app.route('/predict', methods=['POST'])
def predict_yolov6():
    image = request.files.getlist("file")
    path_pred = []
    if image:
        for f in image:

            path_to_save = os.path.join(
                app.config['UPLOAD_FOLDER'], f.filename)
            f.save(path_to_save)
            # print("Save = ", path_to_save)

            frame = cv2.imread(path_to_save)
            # # Nhận diên qua model Yolov6
            frame, no_object = yolov6_model.infer(frame)

            # return yolov6_model.infer(frame)

            pre = {
                "originImg": path_to_save,
                "number": no_object
            }

            if no_object > 0:
                cv2.imwrite(path_to_save, frame)
            del frame
            # Trả về đường dẫn tới file ảnh đã bounding box
            path_pred.append(pre)

        return {"data": path_pred}  # http://server.com/static/path_to_save

    return 'Upload file to detect'

@app.route('/predict/folder', methods=['POST'])
def predictFolder_yolov6():
    image = request.files.getlist("file")
    abnormal=0
    normal=0
    if image:
        for f in image:

            path_to_save = os.path.join(
                app.config['FOlDER_IMG'], f.filename)
            f.save(path_to_save)

            frame = cv2.imread(path_to_save)
            frame, no_object = yolov6_model.infer(frame)

            if no_object > 0:
                abnormal=abnormal+1
            else:
                normal=normal+1    
            del frame

        return {"abnormal":abnormal,"normal":normal}  # http://server.com/static/path_to_save

    return 'Upload file to detect'

@app.route('/preview', methods=['POST'])
def preview():
    image = request.files.getlist("file")
    path_pred = []
    if image:
        for f in image:

            path_to_save = os.path.join(
                app.config['PREVIEW'], f.filename)
            f.save(path_to_save)
            # print("Save = ", path_to_save)

            frame = cv2.imread(path_to_save)
            # # Nhận diên qua model Yolov6
            # frame, no_object = yolov6_model.infer(frame)

            pre = {
                "originImg": path_to_save,
                # "number": no_object
            }

            # if no_object > 0:
            # cv2.imwrite(path_to_save, frame)
            del frame
            # Trả về đường dẫn tới file ảnh đã bounding box
            path_pred.append(pre)

        return {"data": path_pred}  # http://server.com/static/path_to_save

    return 'Upload file to detect'


# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6868')
