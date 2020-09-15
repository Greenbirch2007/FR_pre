import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np




if __name__ == "__main__":
    for num in  range(1000011,1063062):
        try:



            bk_img = cv2.imread("id={0}.jpg".format(num))
            #设置需要显示的字体
            fontpath = "font/simsun.ttc"
            font = ImageFont.truetype(fontpath, 20)
            img_pil = Image.fromarray(bk_img)
            draw = ImageDraw.Draw(img_pil)
            #绘制文字信息
            draw.text((5, 10),  "id={0}".format(num), font = font, fill = (255, 255, 255))

            bk_img = np.array(img_pil)

            # cv2.imshow("add_text",bk_img)
            cv2.waitKey()
            cv2.imwrite("id={0}.jpg".format(num),bk_img)
            print("id={0}.jpg 添加完毕".format(num))
        except:
            pass