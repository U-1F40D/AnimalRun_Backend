import cv2
import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
import imutils
from transform import four_point_transform


HEIGHT_FULL = 460
HEIGHT_BOTTOM = 212
WIDHT_FULL = 260
HEIGHT_SCALE = HEIGHT_FULL/WIDHT_FULL


class Rectangle:
    def __init__(self, ul, ur, bl, br):
        self.poster_width = 280
        self.poster_height = 362
        
        self.upper_left = ul
        self.upper_right = ur
        self.bottom_left = bl
        self.bottom_right = br
        
    def euclidean_distance(self, v1, v2):
        delta_x2 = (v1[0] - v2[0])**2
        delta_y2 = (v1[1] - v2[1])**2
        dist = (delta_x2+delta_y2)**(0.5)
        return dist
    
    def get_width_bottom(self):
        return self.euclidean_distance(self.bottom_left, self.bottom_right)
    
    def get_height_left(self):
        return self.euclidean_distance(self.bottom_left, self.upper_left)
    
    def get_height_right(self):
        return self.euclidean_distance(self.bottom_right, self.upper_right)
    
    def get_line(self, v1, v2):
        points = [v1, v2]
        x_coords, y_coords = zip(*points)
        A = vstack([x_coords,ones(len(x_coords))]).T
        a, b = lstsq(A, y_coords)[0]
        return a, b 
    
    def extrapolate_vect(self, v1, v2, a, b, scale):
        get_y = lambda x: a*x + b
        if v1[1] > v2[1]:
            v1, v2 = v2, v1
        new_x = scale*abs(v1[0]-v2[0])
        if v1[0] > v2[0]:
            new_x = v2[0] + new_x
        else:
            new_x = v2[0] - new_x
        new_y = get_y(new_x)
        return np.array([int(new_x), int(new_y)])
            
def get_vertex_index(vertices, which='upper left'):
    m1, m2 = 'smallest', 'smallest'
    if 'right' in which:
        m1 = 'greatest'
    if 'bottom' in which:
        m2 = 'greatest'
    l1_args = get_index_of_two(vertices[:, 0], method=m1)
    l2_args = get_index_of_two(vertices[:, 1], method=m2)
    uppwe_left_arg = set(l1_args).intersection(l2_args)
    if len(uppwe_left_arg) == 0:
        return None
    return list(uppwe_left_arg)[0]

def get_index_of_two(l1, method='greatest'):
    twos = []
    if method == 'smallest':
        twos = sorted(l1)[:2]
    elif method == 'greatest':
        twos = sorted(l1)[2:]
    return [list(l1).index(x) for x in twos]

def create_rect_from_contour(screenCnt):
    ul_idx = get_vertex_index(screenCnt, 'upper left')
    ur_idx = get_vertex_index(screenCnt, 'upper right')
    bl_idx = get_vertex_index(screenCnt, 'bottom left')
    br_idx = get_vertex_index(screenCnt, 'bottom right')
    l = [ul_idx, ur_idx, bl_idx, br_idx]
    
    if None in list(l):
        return None
    
    ul = screenCnt[ul_idx]
    ur = screenCnt[ur_idx]
    bl = screenCnt[bl_idx]
    br = screenCnt[br_idx]
    
    return Rectangle(ul, ur, bl, br)

def get_area(v1, v2, v3):
    a = ((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)**(0.5)
    b = ((v3[0]-v2[0])**2 + (v3[1]-v2[1])**2)**(0.5)
    c = ((v3[0]-v1[0])**2 + (v3[1]-v1[1])**2)**(0.5)

    s = (a+b+c)/2
    area = (s*(s-a)*(s-b)*(s-c))**(0.5)
    return area

def detect_poster(img):
    ratio = img.shape[0] / 500.0
    image = imutils.resize(img, height = 500)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 100, 210)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    max_area = 0
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            area1 = get_area(approx[0][0], approx[1][0], approx[2][0])
            area2 = get_area(approx[2][0], approx[3][0], approx[0][0])
            if area1+area2 > max_area:
                max_area = area1+area2
                screenCnt = approx

    if type(screenCnt) == None:
        return
    
    screenCnt = np.array([cnt[0] for cnt in screenCnt])
    rect = create_rect_from_contour(screenCnt)
    if rect == None:
        return

    a, b = rect.get_line(rect.upper_left, rect.bottom_left)
    new_upper_left = rect.extrapolate_vect(rect.upper_left, rect.bottom_left, a, b, HEIGHT_SCALE)
    
    a, b = rect.get_line(rect.upper_right, rect.bottom_right)
    new_upper_right = rect.extrapolate_vect(rect.upper_right, rect.bottom_right, a, b, HEIGHT_SCALE)
    
    rect.upper_left = new_upper_left
    rect.upper_right = new_upper_right

    screenCnt = np.array([np.array([rect.upper_left]), np.array([rect.upper_right]), np.array([rect.bottom_right]), np.array([rect.bottom_left])])
    ratio = 1
    warped = four_point_transform(imutils.resize(img, height = 500), screenCnt.reshape(4, 2) * ratio)
    return warped