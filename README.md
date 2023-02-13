# Tool-label-Img-for-Yolo

labeling.py: vẽ boundingbox trên frame, lưu thông tin boundingbox vào file text  
decode.py: kiểm tra xem boundingbox có đúng?  
rectangle.py: vẽ lại boundingbox nếu như bị lệch  
crop_webcam.py: cắt lại webcam  
relabels.py: label lại ảnh


# Install env for python
pip install -r requirements.txt

# Init data
face: ('python src/init_data_face.py')  
result: ('python src/init_data_result.py')  

# Add data of employee into train_data
'python src/make_data_train.py name' 
## name is name of new employee after save face_image into raw  

# Train model Face identification
'python src/train.py'

# Run Face-recognition process with webcam
'python src/face_rec_cam.py'
## Result of process was saved in 'Dataset/FaceData/processed/result.json'

# Remove employee 
'python src/delete_member.py name' 
## name is name of employee
