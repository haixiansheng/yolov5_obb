import os 
import cv2
import shutil

data_root = r"E:\code\data\gen_barcode_data\train_obb"
save_root = r"E:\code\obb_detect\yolov5_obb\dataset\box"


images_dir = os.path.join(save_root,"images")
os.makedirs(images_dir,exist_ok=True)
label_dir = os.path.join(save_root,"labelTxt")
os.makedirs(label_dir,exist_ok=True)
jpg_formats = [".jpg","png","jpeg",".bmp"]
cls_list = ["box"]

def traverse_txt_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        
        for file in files:
            if file.endswith('.txt'):
                # with open(os.path.join(save_root,"imgnamefile.txt"),"a+") as ss:
                #     base_name = file.split(".")[0]
                #     ss.write(f"{base_name} \n")
                txt_file_path = os.path.join(root, file)
                for format in jpg_formats:
                    img_file_path = txt_file_path.replace("labels","images").replace(".txt",format)
                    if os.path.exists(img_file_path):
                        image = cv2.imread(img_file_path)
                        h, w, c = image.shape                        
                        break
                with open(txt_file_path,"r") as f:
                    lines = []
                    for line in f:
                        lines.append(line.strip())
                    cur_txt_path = os.path.basename(txt_file_path)
                    save_txt = os.path.join(label_dir,cur_txt_path)                    
                    print(f"[INFO] save txt:{save_txt}")
                    shutil.copy(img_file_path,images_dir)
                    print(f"[INFO] save image:{images_dir}")

                    with open(save_txt,"w") as fl:
                        for l in lines:
                            d = l.split(" ")
                            cls_id = int(d[0])
                            x1,y1,x2,y2,x3,y3,x4,y4 = float(d[1]),float(d[2]),float(d[3]),float(d[4]),float(d[5]),float(d[6]),float(d[7]),float(d[8])
                            x1,x2,x3,x4 = float(x1*w),float(x2*w),float(x3*w),float(x4*w)
                            y1,y2,y3,y4 = float(y1*h),float(y2*h),float(y3*h),float(y4*h)
                            fl.write(f"{x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} {cls_list[cls_id]} 0\n")


if __name__=="__main__":
    traverse_txt_files(data_root)