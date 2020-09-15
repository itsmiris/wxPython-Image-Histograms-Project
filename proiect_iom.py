import wx
import cv2
import os.path
import numpy as np
from matplotlib import pyplot as plt
import math

class WindowClass(wx.Frame):

    def __init__(self,parent,title):
        super(WindowClass,self).__init__(parent, title='Image Processing GUI',size=(600,400),style=wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        # self.basicGUI()
        panel = wx.Panel(self, size=(600, 600))
        openfiledialog = wx.FileDialog(None, 'open', '', '', '(*.png)|*.png', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openfiledialog.ShowModal() == wx.ID_OK:
            path = openfiledialog.GetPath()
            print(path)
        w = os.path.split(path)[1]
        print(w)
        global img
        img = cv2.imread(path)
        # cv2.imshow('123',img)

    # Box1 image processing
        # Title
        titlebox1 = wx.StaticText(panel, -1, '1.Image Processing', (20, 20))
        titlebox1.SetForegroundColour('Black')

        # Buttons
        self.button11 = wx.Button(panel, -1, "1.1 Load Image", pos=(20, 40))
        self.Bind(wx.EVT_BUTTON, self.OnClick11, self.button11)
        self.button11.SetDefault()
        self.button12 = wx.Button(panel, -1, "1.2 Color Conversion", pos=(20, 70))
        self.Bind(wx.EVT_BUTTON, self.OnClick12, self.button12)
        self.button12.SetDefault()
        self.button13 = wx.Button(panel, -1, "1.3 Image Flipping", pos=(20, 100))
        self.Bind(wx.EVT_BUTTON, self.OnClick13, self.button13)
        self.button13.SetDefault()
        self.button14 = wx.Button(panel, -1, "1.4 Blending", pos=(20, 130))
        self.Bind(wx.EVT_BUTTON, self.OnClick14, self.button14)
        self.button14.SetDefault()


    # Box3 Image histograms
        # Title
        titlebox2 = wx.StaticText(panel, -1, '2.Image Histograms', (220, 20))
        titlebox2.SetForegroundColour('Black')
        # Buttons
        self.button21 = wx.Button(panel, -1, "2.1 R-Histogram", pos=(220, 40))
        self.button22 = wx.Button(panel, -1, "2.2 G-Histogram", pos=(220, 70))
        self.button23 = wx.Button(panel, -1, "2.3 B-Histogram", pos=(220, 100))
        
        self.Bind(wx.EVT_BUTTON, self.OnClick21, self.button21)
        self.Bind(wx.EVT_BUTTON, self.OnClick22, self.button22)
        self.Bind(wx.EVT_BUTTON, self.OnClick23, self.button23)
        self.button21.SetDefault()
        
        self.Show(True)
        self.Center()

    def OnClick11(self, event):
        print(type(img))
        cv2.imshow('Loaded Image', img)
        w = img.shape
        k = str(w[0])
        p = str(w[1])
        wx.StaticText(self, -1, 'Image Width', (20, 300)),wx.StaticText(self, -1, k, (120, 300))
        wx.StaticText(self, -1, 'Image Height', (20, 320)),wx.StaticText(self, -1, p, (120, 320))
        # cv2.imshow('123', img)
        # staticBmp=wx.StaticBitmap(self,-1,img2,pos=(440,300),size=(100,100))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def OnClick12(self,event):
        [B, G, R] = cv2.split(img)
        chooseOneBox = wx.SingleChoiceDialog(None, 'Change color from BGR to...','Make Your Choice！', ['RGB', 'RBG', 'BRG','BGR','GRB','GBR','Gray'])
        if chooseOneBox.ShowModal() == wx.ID_OK:
            choice = chooseOneBox.GetStringSelection()
            if choice == 'RGB':
                display = cv2.merge([R,G,B])
            if choice == 'RBG':
                display = cv2.merge([R, B, G])
            if choice == 'BRG':
                display = cv2.merge([B, R, G])
            if choice == 'BGR':
                display = cv2.merge([B, G, R])
            if choice == 'GRB':
                display = cv2.merge([G, R, B])
            if choice == 'GBR':
                display = cv2.merge([G, B, R])
            if choice == 'Gray':
                display = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imshow('Merged Image',display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def OnClick13(self,event):
        chooseOneBox = wx.SingleChoiceDialog(None, 'Which axis to flip?', 'Make Your Choice！', ['X axis', 'Y axis', 'XY axis'])
        if chooseOneBox.ShowModal() == wx.ID_OK:
            global display
            choice = chooseOneBox.GetStringSelection()
            if choice == 'X axis':
                display = cv2.flip(img,int(0))
            if choice == 'Y axis':
                display = cv2.flip(img,  int(1))
            if choice == 'XY axis':
                display = cv2.flip(img, int(-1))
        global img13
        img13 = cv2.imshow('Flipped Image', display)
        img13
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def OnClick14(self,event):
        def nothing(x):
            pass
        a = 0
        cv2.namedWindow('Blended Image')
        cv2.createTrackbar('Blending','Blended Image',0,100,nothing)
        switch = 'close '
        cv2.createTrackbar(switch, 'Blended Image', 0, 1, nothing)
        while(1):
            k = cv2.addWeighted( display, 0.01*a,img, 0.01*(100 - a), 0)
            cv2.imshow('Blended Image', k)
            cv2.waitKey(1)
            a = cv2.getTrackbarPos('Blending', 'Blended Image')
            s = cv2.getTrackbarPos(switch, 'Blended Image')
            if s == 1:
                break
            else:
                pass
        cv2.destroyAllWindows()
    def OnClick21(self, event):
        
        h = np.zeros((300,256,3))
        b,g,r = cv2.split(img)
        bins = np.arange(256).reshape(256,1)


        
        hist_item = cv2.calcHist(r,[0],None,[256],[0,255])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,(0,0,255))

        h=np.flipud(h)

        cv2.imshow('colorhist',h)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def OnClick22(self, event):
        h = np.zeros((300,256,3))
        b,g,r = cv2.split(img)
        bins = np.arange(256).reshape(256,1)
        hist_item = cv2.calcHist(g,[0],None,[256],[0,255])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,(0,255,0))

        h=np.flipud(h)

        cv2.imshow('colorhist',h)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def OnClick23(self, event):
        h = np.zeros((300,256,3))
        b,g,r = cv2.split(img)
        bins = np.arange(256).reshape(256,1)
        hist_item = cv2.calcHist(b,[0],None,[256],[0,255])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,(255,0,0))

        h=np.flipud(h)

        cv2.imshow('colorhist',h)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def OnClick(self,  event):
        self.button11.SetLabel("Clicked")
        pass

def main():
    app = wx.App()
    WindowClass(None, 'title')
    app.MainLoop()

main()