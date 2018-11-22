import cv2
import numpy as np

# Envs: Global Variables
image_path = "char_02-06-0287.jpg"
text_path = "char_02-06-0287.txt"

class BoxDrawer(object):
    def __init__(self):
        print("Box Drawer starts -- ")
        self.img = None
        self.img_rsz = None
        self.img_prc = None
        self.txt = None
        # variable 'p' stores two vertices
        # [ leftmost-upmost && rightmost-downmost ]
        self.p = list()
        # variable 'p2' 
        # position of box-object after resizing image
        self.p2 = list()
        # variable 'p3'
        # position of box-object after adding zero padding
        self.p3 = list()
        self.half_diff = 0
        self.expand_up_down = True
        self.same_width_height = False
        self.w_ratio = 1
        self.h_ratio = 1

        self.init_and_do_everything()
        # self.test_anything()            # only for test
    
    def init_and_do_everything(self):
        '''
        Here in this func, everything is done inside here
        '''
        self.load_image()
        self.read_text()
        self.get_box_position()

        # self.resize_image_new_sz(self.img, 960, 540)
        self.resize_image_with_ratio(self.img, (0,0), 0.5, 0.5)
        self.reposition_box(self.img, self.img_rsz)

        self.add_zero_padding(self.img_rsz)
        self.move_box_position_appropriately()

        self.draw_box_on_image()
        self.draw_rectangle_on_processed_image()
        self.display_image()

    def test_anything(self):
        '''
        this is only for test
        '''
        img1 = np.full((540,960,3), [0,0,0], dtype=np.uint8)
        img2 = np.full((540,960,3), [255,0,0], dtype=np.uint8)
        img3 = np.full((540,960,3), [0,255,0], dtype=np.uint8)
        # img4 = np.full((540,960,3), [0,0,255], dtype=np.uint8)

        img7 = np.full((540,240,3), [0,0,0], dtype=np.uint8)

        img5 = np.full((210,960,3), [0,0,0], dtype=np.uint8)

        img6_0 = np.concatenate((img5, img3), axis=0)
        img6 = np.concatenate((img6_0, img5), axis=0)

        img8_0 = np.concatenate((img7, img2), axis=1)
        img8 = np.concatenate((img8_0, img7), axis=1)

        # cv2.imshow("Image 1", img1)
        cv2.imshow("Image 2", img2)
        # cv2.imshow("Image 3", img3)
        # cv2.imshow("Image 4", img4)

        cv2.imshow("Image 5", img5)
        cv2.imshow("Image 6", img6)
        cv2.imshow("Image 8", img8)

        # cv2.imshow("Image ", img)

        while True:
            k = cv2.waitKey()
            print("Displayed Image... waitKey()...")

            if k == ord('q') or k == 27:
                print("Now Exit with Keyboard Input")
                cv2.destroyAllWindows()
                break

    def load_image(self):
        '''
        func "load_image()" loads image from the image_path
        and store the np.array in var 'img_dp'
        '''
        self.img = cv2.imread(image_path)
        # configure the size of the image
        # [ height, weight, channel ]
        print(self.img.shape)
        print("type of Image.shape attribute: {} {} {}".format(
            type(self.img.shape[1]), type(self.img.shape[0]), type(self.img.shape[2])
        ))

    def read_text(self):
        '''
        func "read_text()" opens and reads data from text_path 
        and store it in a list [ self.txt ]
        '''
        self.txt = []
        with open(text_path) as t:
            self.txt = t.read().split()
        print("{}___from func read_text()".format(self.txt))

    def get_box_position(self):
        '''
        func "get_box_position()" 
        store the returned value in 'self.p'
        '''
        x_factor = self.txt[1]
        y_factor = self.txt[2]
        w_factor = self.txt[3]
        h_factor = self.txt[4]
        x1 = (float(x_factor) - float(w_factor) / 2) * self.img.shape[1]
        y1 = (float(y_factor) - float(h_factor) / 2) * self.img.shape[0]
        x2 = (float(x_factor) + float(w_factor) / 2) * self.img.shape[1]
        y2 = (float(y_factor) + float(h_factor) / 2) * self.img.shape[0]
        self.p.append([x1, y1])
        self.p.append([x2, y2])
        print("{}___from get_box_position()".format(self.p))

    def resize_image_new_sz(self, img, width, height):
        '''
        func "resize_image(np.array, int, int)" resizes 
        with two values 'width', 'height'
        '''
        self.img_rsz = cv2.resize(img, (width, height))
        print("Resizing Image with width, height Complete!")
        print("AFTER RESIZE : {}".format(self.img_rsz.shape))

    def resize_image_with_ratio(self, img, point_O=(0,0), x_ratio=1, y_ratio=1):
        '''
        func "resize_image(np.array, tuple, float, float)" resizes 
        with two values 'x_ratio', 'y_ratio'
        '''
        # self.img_rsz = cv2.resize(img, point_O, fx = x_ratio, fy = y_ratio)
        self.img_rsz = cv2.resize(img, point_O, fx=x_ratio, fy=y_ratio)
        print("Resizing Image with ratio Complete!")
        print("AFTER RESIZE : {}".format(self.img_rsz.shape))

    def reposition_box(self, img_old, img_new):
        '''
        func "reposition_box(np.array, np.array)"
        reposition box object before drawing on image
        '''
        self.w_ratio = float(img_new.shape[1]) / float(img_old.shape[1])
        self.h_ratio = float(img_new.shape[0]) / float(img_old.shape[0])
        self.p2.append([self.p[0][0] * self.w_ratio, self.p[0][1] * self.h_ratio])
        self.p2.append([self.p[1][0] * self.w_ratio, self.p[1][1] * self.h_ratio])
        print("Repositioning Box Object Complete!!")
        print("{}___from reposition_box".format(self.p2))

    def draw_box_on_image(self):
        '''
        func "draw_box_on_image()"
        converts float values of 'p' into int values
        '''
        self.p[0][0], self.p[0][1] = int(self.p[0][0]), int(self.p[0][1])
        self.p[1][0], self.p[1][1] = int(self.p[1][0]), int(self.p[1][1])
        print(self.p)
        cv2.rectangle(self.img, tuple(self.p[0]), tuple(self.p[1]), (0,0,255), 3)
        self.p2[0][0], self.p2[0][1] = int(self.p2[0][0]), int(self.p2[0][1])
        self.p2[1][0], self.p2[1][1] = int(self.p2[1][0]), int(self.p2[1][1])
        print(self.p2)
        cv2.rectangle(self.img_rsz, tuple(self.p2[0]), tuple(self.p2[1]), (0,0,255), 3)
        print("Drew Rectangle ___from draw_box_on_image()")

    def add_zero_padding(self, mImg):
        '''
        func "add_zero_padding()"
        when width is longer, then add zero padding above-and-below
        when height is longer, then add zero padding left-and-right size
        '''
        print("{}___from add_zero_padding_and_move_box_position_appropriately".format(mImg.shape))
        w, h, = mImg.shape[1], mImg.shape[0]
        black_square = None
        if w > h:
            self.half_diff = (w - h) // 2
            print("half_diff : {}".format(self.half_diff))
            black_square = np.full((self.half_diff, w, 3), [0,0,0], dtype=np.uint8)
            self.img_prc = np.concatenate(
                (black_square, np.concatenate((self.img_rsz, black_square), axis=0)), axis=0
            )
            self.expand_up_down = True
            self.same_width_height = False
        elif w < h:
            self.half_diff = (h - w) // 2
            print("half_diff : {}".format(self.half_diff))
            black_square = np.full((h, self.half_diff, 3), [0,0,0], dtype=np.uint8)
            self.img_prc = np.concatenate(
                (black_square, np.concatenate( (self.img_rsz, black_square), axis=1 )), axis=1
            )
            self.expand_up_down = False
            self.same_width_height = False
        else:
            self.same_width_height = True
            self.img_prc = self.img_rsz
            print("No padding is needed - same width, height")
            return
        print("Adding zero-padding and moving box-object Complete!!!")

    def move_box_position_appropriately(self):
        '''
        func "move_box_position_appropriately()"
        reposition the box object
        '''
        if self.same_width_height == False:
            if self.expand_up_down == True:
                self.p3.append([self.p2[0][0], self.p2[0][1] + self.half_diff])
                self.p3.append([self.p2[1][0], self.p2[1][1] + self.half_diff])
            else:
                self.p3.append([self.p2[0][0] + self.half_diff, self.p2[0][1]])
                self.p3.append([self.p2[1][0] + self.half_diff, self.p2[1][1]])
        else:
            self.p3 = self.p2

    def draw_rectangle_on_processed_image(self):
        '''
        func "draw_rectangle_on_processed_image()" 
        draw rectangle on processed image 
        '''
        self.p3[0][0], self.p3[0][1] = int(self.p3[0][0]), int(self.p3[0][1])
        self.p3[1][0], self.p3[1][1] = int(self.p3[1][0]), int(self.p3[1][1])
        cv2.rectangle(self.img_prc, tuple(self.p3[0]), tuple(self.p3[1]), (0,255,0), 3)
        print("Drew Box Object ___from draw_rectangle_on_processed_image()")

    def display_image(self):
        cv2.imshow("Original Image", self.img)
        cv2.imshow("Resized Image", self.img_rsz)
        cv2.imshow("Processed Image", self.img_prc)

        while True:
            k = cv2.waitKey()
            print("Displayed Image... waitKey()...")

            if k == ord('q') or k == 27:
                print("Now Exit with Keyboard Input")
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    print("main starts here!")
    bd = BoxDrawer()



