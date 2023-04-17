import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_mainwindow import Ui_Form
from display import MainWindow2

#importing constants from other file
import mod_constant

image_path = "images/"
filler = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus vel nisl justo. Nunc vitae sem sed."
class MainWindow(QMainWindow):
    # class constructor
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('CogInsight')
        self.setFixedWidth(1350)
        self.setFixedHeight(900)
        
        self.timer_mod1 = QTimer(self)
        self.timer_mod1.timeout.connect(self.act1_UI_mc1)

        self.timer_mod2_1 = QTimer(self)
        self.timer_mod2_2 = QTimer(self)
        self.timer_mod2_3 = QTimer(self)
        

        self.setStyleSheet("background-color: white")
        self.init_ui()  
        
    def init_ui(self):
        starter_page = self.homePage()
        #navBar = self.create_navBar()
        #assessUI = self.act1_UI_intro()
        #activity1_UI = self.act1_UI_p1()
        #activity2_UI = self.act2_UI_intro()
        #start = self.act2_UI_p3_first()
    
    #Nav Bar Definition
    def create_navBar(self):
        navBar = QWidget()
        navBarLayout = QHBoxLayout()
        
        aboutMenu = QPushButton("About")
        assessMenu = QPushButton("Assessment")
        resourceMenu = QPushButton("Resources")
        contactMenu = QPushButton("Contact Us")
        loginMenu = QPushButton("Login/Sign Up")
        
        assessMenu.clicked.connect(self.act1_UI_intro)
        aboutMenu.clicked.connect(self.homePage)
        
        navBarLayout.addWidget(aboutMenu)
        navBarLayout.addWidget(assessMenu)
        navBarLayout.addWidget(resourceMenu)
        navBarLayout.addWidget(contactMenu)
        navBarLayout.addWidget(loginMenu)
        navBarLayout.insertSpacing(0,400)
        
        navBar.setLayout(navBarLayout)
        
        return navBar
        

    def display(self,i):
        self.Stack.setCurrentIndex(i)

    def homePage(self):
        navBar = self.create_navBar()
        desc = mod_constant.HOMEPAGE_DESC1
    
        homePageTitle = QLabel("CogInsight")
        homePageTitleFont = homePageTitle.font()
        homePageTitleFont.setPointSize(40)
        homePageTitle.setAlignment(Qt.AlignCenter)
        homePageTitle.setFont(homePageTitleFont)
        
        homePageDescription = QLabel(desc)
        homePageDescriptionFont = homePageDescription.font()
        homePageDescriptionFont.setPointSize(16)
        homePageDescription.setFont(homePageDescriptionFont)
        homePageDescription.setAlignment(Qt.AlignLeft)
        
        homePageDescription.setWordWrap(True)
        
        descLayout = QHBoxLayout()
        emptyLabel = QLabel(" ")
        descLayout.addWidget(emptyLabel)
        descLayout.addWidget(homePageDescription)
        descLayout.addWidget(emptyLabel)
        
        descLayout.setStretch(0,1)
        descLayout.setStretch(1,4)
        descLayout.setStretch(2,1)
        
        descWidget = QWidget()
        descWidget.setLayout(descLayout)
        
        homePageLayout = QVBoxLayout()
        homePageLayout.addWidget(navBar)
        homePageLayout.addWidget(homePageTitle)
        homePageLayout.addWidget(descWidget)
        
        homePageLayout.setStretch(0,1)
        homePageLayout.setStretch(1,3)
        homePageLayout.setStretch(2,6)
        
        homePageWidget = QWidget()
        homePageWidget.setLayout(homePageLayout)
        
        self.setCentralWidget(homePageWidget) 

    #Activity 1 Definition
    def act1_UI_intro(self):
        #Creating all the widgets necessary in the page
        #Title of the module
        moduleTitleWidget = QLabel("Module 1")
        moduleTitleWidget.setFont(QFont('Times font',20))
        moduleTitleWidget.setAlignment(Qt.AlignVCenter)
        moduleTitleWidget.setAlignment(Qt.AlignHCenter)
        
        #Description of the module
        moduleDescWidget = QLabel()
        moduleDescWidget.setText("{}".format(mod_constant.MOD1_PRE_AMBLE))
        moduleDescWidget.setFont(QFont('Times font',12))
        moduleDescWidget.setWordWrap(True)
        moduleDescWidget.setAlignment(Qt.AlignHCenter)
        moduleDescWidget.setAlignment(Qt.AlignTop)
        
        moduleDescLayout = QHBoxLayout()
        emptyLabel = QLabel(" ")
        moduleDescLayout.addWidget(emptyLabel)
        moduleDescLayout.addWidget(moduleDescWidget)
        moduleDescLayout.addWidget(emptyLabel)
        
        moduleDescLayout.setStretch(0,1)
        moduleDescLayout.setStretch(1,4)
        moduleDescLayout.setStretch(2,1)
        
        descWidget = QWidget()
        descWidget.setLayout(moduleDescLayout)
        
        #Assessment start button of the module
        moduleStartButton = QPushButton("Start Module 1")
        moduleStartButton.resize(20,10)
        
        navBar = self.create_navBar()
        
        #Adding to the layout
        layout = QVBoxLayout()
        layout.addWidget(navBar)
        layout.addWidget(moduleTitleWidget)
        #layout.addWidget(moduleDescWidget)
        layout.addWidget(descWidget)
        layout.addWidget(moduleStartButton)
        layout.insertStretch(3,1)
        
        layout.setStretch(0,1)
        layout.setStretch(1,3)
        layout.setStretch(2,4)
        layout.setStretch(4,1)
        
        #Changing sizing of the rows and columns
        #layout.setRowStretch(0,5)
        #layout.setRowStretch(1,15)
        #layout.setRowStretch(2,25)
        
        #Adding widgets to the final page
        pageWidget = QWidget()
        pageWidget.setLayout(layout)
        
        self.setCentralWidget(pageWidget)
        
        #What do buttons do
        moduleStartButton.clicked.connect(self.act1_UI_p1)
        
    def act1_create_quads(self, headline, description, picture):
        QuadPic = QLabel()
        QuadHeadline = QLabel(headline)
        QuadDescription = QLabel(description)
        
        #Setting Font Style
        headlineFont = QuadHeadline.font()
        headlineFont.setPointSize(14)
        headlineFont.setBold(True)
        
        descriptFont = QuadDescription.font()
        descriptFont.setPointSize(11)
        
        QuadHeadline.setFont(headlineFont)
        QuadDescription.setFont(descriptFont)
        
        #Alignment and Positioning
        QuadHeadline.setAlignment(Qt.AlignCenter)
        QuadDescription.setWordWrap(True)
        QuadHeadline.setWordWrap(True)
        QuadDescription.setAlignment(Qt.AlignLeft)
        
        #pixmap = QPixmap(image_path + picture).scaledToWidth(250)
        pixmap = QPixmap(picture).scaledToWidth(370)
        QuadPic.setPixmap(pixmap)
        QuadPic.setAlignment(Qt.AlignCenter)
        
        QuadLayout = QVBoxLayout()
        QuadLayout.addWidget(QuadPic)
        QuadLayout.addWidget(QuadHeadline)
        QuadLayout.addWidget(QuadDescription)
        
        Quad = QWidget()
        Quad.setLayout(QuadLayout)
        
        return Quad
        
    def act1_UI_p1(self):
        #Top Left Quad
        tl_head = mod_constant.ARTICLE1_HEADLINE
        tl_desc = mod_constant.ARTICLE1_TEXT
        tl_pic = mod_constant.ARTICLE1_IMAGE
        
        TLQuad = self.act1_create_quads(tl_head,tl_desc,tl_pic)
        
        #Top Right Quad
        tr_head = mod_constant.ARTICLE2_HEADLINE
        tr_desc = mod_constant.ARTICLE2_TEXT
        tr_pic = mod_constant.ARTICLE2_IMAGE
        
        TRQuad = self.act1_create_quads(tr_head,tr_desc,tr_pic)
        
        #Bottom Left Quad
        bl_head = mod_constant.ARTICLE3_HEADLINE
        bl_desc = mod_constant.ARTICLE3_TEXT
        bl_pic = mod_constant.ARTICLE3_IMAGE
        
        BLQuad = self.act1_create_quads(bl_head,bl_desc,bl_pic)
        
        #Bottom Right Quad
        br_head = mod_constant.ARTICLE4_HEADLINE
        br_desc = mod_constant.ARTICLE4_TEXT
        br_pic = mod_constant.ARTICLE4_IMAGE
        
        BRQuad = self.act1_create_quads(br_head,br_desc,br_pic)
        
        #Set up layout of all objects
        gridLayout = QGridLayout()
        mainLayout = QVBoxLayout()
        paginationWidget = QWidget()
        
        #Set up layout for pages
        p1 = QPushButton("1")
        p1.setStyleSheet("QPushButton""{""background-color: lightblue;""}")
        p2 = QPushButton("2")
        p3 = QPushButton("3")
        
        pageLayout = QHBoxLayout()
        
        pageLayout.addWidget(p1)
        pageLayout.addWidget(p2)
        pageLayout.addWidget(p3)
        pageLayout.insertStretch(0)
        pageLayout.insertStretch(4)
        
        pageLayout.setStretch(0,1)
        pageLayout.setStretch(1,3)
        pageLayout.setStretch(2,3)
        pageLayout.setStretch(3,3)
        pageLayout.setStretch(4,1)
        
        #Adding all widgets together
        pageWidget = QWidget()
        gridWidget = QWidget()
        mainWidget = QWidget()
        navBar = self.create_navBar()
        
        #Adding each quadrant widget to the main widget
        gridLayout.addWidget(TLQuad,0,0)
        gridLayout.addWidget(TRQuad,0,1)
        gridLayout.addWidget(BLQuad,1,0)
        gridLayout.addWidget(BRQuad,1,1)
        gridLayout.setSpacing(50)
        
        #Integrating all into one widget
        gridWidget.setLayout(gridLayout)
        pageWidget.setLayout(pageLayout)
        
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(gridWidget)
        mainLayout.addWidget(pageWidget)
        
        mainWidget.setLayout(mainLayout)
        
        self.setCentralWidget(mainWidget)
        if not self.timer_mod1.isActive():
            self.timer_mod1.start(mod_constant.TIME1)
     
        p1.clicked.connect(self.act1_UI_p1)
        p2.clicked.connect(self.act1_UI_p2)
        p3.clicked.connect(self.act1_UI_p3)
        
    def act1_UI_p2(self):
        #Top Left Quad
        tl_head = mod_constant.ARTICLE5_HEADLINE
        tl_desc = mod_constant.ARTICLE5_TEXT
        tl_pic = mod_constant.ARTICLE5_IMAGE
        
        TLQuad = self.act1_create_quads(tl_head,tl_desc,tl_pic)
        
        #Top Right Quad
        tr_head = mod_constant.ARTICLE6_HEADLINE
        tr_desc = mod_constant.ARTICLE6_TEXT
        tr_pic = mod_constant.ARTICLE6_IMAGE
        
        TRQuad = self.act1_create_quads(tr_head,tr_desc,tr_pic)
        
        #Bottom Left Quad
        bl_head = mod_constant.ARTICLE7_HEADLINE
        bl_desc = mod_constant.ARTICLE7_TEXT
        bl_pic = mod_constant.ARTICLE7_IMAGE
        
        BLQuad = self.act1_create_quads(bl_head,bl_desc,bl_pic)
        
        #Bottom Right Quad
        br_head = mod_constant.ARTICLE8_HEADLINE
        br_desc = mod_constant.ARTICLE8_TEXT
        br_pic = mod_constant.ARTICLE8_IMAGE
        
        BRQuad = self.act1_create_quads(br_head,br_desc,br_pic)
        
        #Set up layout of all objects
        gridLayout = QGridLayout()
        mainLayout = QVBoxLayout()
        paginationWidget = QWidget()
        
        #Set up layout for pages
        p1 = QPushButton("1")
        p2 = QPushButton("2")
        p2.setStyleSheet("QPushButton""{""background-color: lightblue;""}")
        p3 = QPushButton("3")
        
        pageLayout = QHBoxLayout()
        
        pageLayout.addWidget(p1)
        pageLayout.addWidget(p2)
        pageLayout.addWidget(p3)
        pageLayout.insertStretch(0)
        pageLayout.insertStretch(4)
        
        pageLayout.setStretch(0,1)
        pageLayout.setStretch(1,3)
        pageLayout.setStretch(2,3)
        pageLayout.setStretch(3,3)
        pageLayout.setStretch(4,1)
        
        #Adding all widgets together
        pageWidget = QWidget()
        gridWidget = QWidget()
        mainWidget = QWidget()
        navBar = self.create_navBar()
        
        #Adding each quadrant widget to the main widget
        gridLayout.addWidget(TLQuad,0,0)
        gridLayout.addWidget(TRQuad,0,1)
        gridLayout.addWidget(BLQuad,1,0)
        gridLayout.addWidget(BRQuad,1,1)
        gridLayout.setSpacing(50)
        
        #Integrating all into one widget
        gridWidget.setLayout(gridLayout)
        pageWidget.setLayout(pageLayout)
        
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(gridWidget)
        mainLayout.addWidget(pageWidget)
        
        mainWidget.setLayout(mainLayout)
        
        self.setCentralWidget(mainWidget)
        #self.timer_mod1.start(10000)
     
        p1.clicked.connect(self.act1_UI_p1)
        p2.clicked.connect(self.act1_UI_p2)
        p3.clicked.connect(self.act1_UI_p3)
        
    def act1_UI_p3(self):
        #Top Left Quad
        tl_head = mod_constant.ARTICLE9_HEADLINE
        tl_desc = mod_constant.ARTICLE9_TEXT
        tl_pic = mod_constant.ARTICLE9_IMAGE
        
        TLQuad = self.act1_create_quads(tl_head,tl_desc,tl_pic)
        
        #Top Right Quad
        tr_head = mod_constant.ARTICLE10_HEADLINE
        tr_desc = mod_constant.ARTICLE10_TEXT
        tr_pic = mod_constant.ARTICLE10_IMAGE
        
        TRQuad = self.act1_create_quads(tr_head,tr_desc,tr_pic)
        
        #Bottom Left Quad
        bl_head = mod_constant.ARTICLE11_HEADLINE
        bl_desc = mod_constant.ARTICLE11_TEXT
        bl_pic = mod_constant.ARTICLE11_IMAGE
        
        BLQuad = self.act1_create_quads(bl_head,bl_desc,bl_pic)
        
        #Bottom Right Quad
        br_head = mod_constant.ARTICLE12_HEADLINE
        br_desc = mod_constant.ARTICLE12_TEXT
        br_pic = mod_constant.ARTICLE12_IMAGE
        
        BRQuad = self.act1_create_quads(br_head,br_desc,br_pic)
        
        #Set up layout of all objects
        gridLayout = QGridLayout()
        mainLayout = QVBoxLayout()
        paginationWidget = QWidget()
        
        #Set up layout for pages
        p1 = QPushButton("1")
        p2 = QPushButton("2")
        p3 = QPushButton("3")
        p3.setStyleSheet("QPushButton""{""background-color: lightblue;""}")
        
        pageLayout = QHBoxLayout()
        
        pageLayout.addWidget(p1)
        pageLayout.addWidget(p2)
        pageLayout.addWidget(p3)
        pageLayout.insertStretch(0)
        pageLayout.insertStretch(4)
        
        pageLayout.setStretch(0,1)
        pageLayout.setStretch(1,3)
        pageLayout.setStretch(2,3)
        pageLayout.setStretch(3,3)
        pageLayout.setStretch(4,1)
        
        #Adding all widgets together
        pageWidget = QWidget()
        gridWidget = QWidget()
        mainWidget = QWidget()
        navBar = self.create_navBar()
        
        #Adding each quadrant widget to the main widget
        gridLayout.addWidget(TLQuad,0,0)
        gridLayout.addWidget(TRQuad,0,1)
        gridLayout.addWidget(BLQuad,1,0)
        gridLayout.addWidget(BRQuad,1,1)
        gridLayout.setSpacing(50)
        
        #Integrating all into one widget
        gridWidget.setLayout(gridLayout)
        pageWidget.setLayout(pageLayout)
        
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(gridWidget)
        mainLayout.addWidget(pageWidget)
        
        mainWidget.setLayout(mainLayout)
        
        self.setCentralWidget(mainWidget)
        #self.timer_mod1.start(10000)
     
        p1.clicked.connect(self.act1_UI_p1)
        p2.clicked.connect(self.act1_UI_p2)
        p3.clicked.connect(self.act1_UI_p3)
        
    def act1_UI_mc1(self):
    # The spacing of the 
        self.timer_mod1.stop()
        self.timer_mod1.deleteLater()

        navBar = self.create_navBar()
        question_title = QLabel("Question 1")
        question_title.setFont(QFont('Times font',20))
        question_title.setAlignment(Qt.AlignCenter)
        
        question_content = QLabel(mod_constant.Q1_CONTENT)
        question_content.setFont(QFont('Times font',14))
        question_content.setAlignment(Qt.AlignCenter)
        
        choice1 = QRadioButton(mod_constant.Q1_CHOICE1,self)
        choice2 = QRadioButton(mod_constant.Q1_CHOICE2,self)
        choice3 = QRadioButton(mod_constant.Q1_CHOICE3,self)
        choice4 = QRadioButton(mod_constant.Q1_CHOICE4,self)

        choice1.setStyleSheet("QRadioButton { font-size: 24px; text-align: center; }")
        choice2.setStyleSheet("QRadioButton { font-size: 24px; text-align: center; }")
        choice3.setStyleSheet("QRadioButton { font-size: 24px; text-align: center; }")
        choice4.setStyleSheet("QRadioButton { font-size: 24px; text-align: center; }")
        
        submitButton = QPushButton("Submit")
        submitButton.setEnabled(False)
        submitButton.clicked.connect(self.act2_UI_intro)

        choice1.clicked.connect(lambda: submitButton.setEnabled(True))
        choice2.clicked.connect(lambda: submitButton.setEnabled(True))
        choice3.clicked.connect(lambda: submitButton.setEnabled(True))
        choice4.clicked.connect(lambda: submitButton.setEnabled(True))

        choiceLayout = QVBoxLayout()
        choiceLayout.addWidget(choice1)
        choiceLayout.addWidget(choice2)
        choiceLayout.addWidget(choice3)
        choiceLayout.addWidget(choice4)
        choiceLayout.setAlignment(Qt.AlignCenter)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(question_title)
        mainLayout.addWidget(question_content)
        mainLayout.addLayout(choiceLayout)
        mainLayout.addWidget(submitButton)
        
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,1)
        mainLayout.setStretch(2,1)
        mainLayout.setStretch(3,8)
        mainLayout.setStretch(4,8)
        mainLayout.setStretch(5,8)
        mainLayout.setStretch(6,8)
        mainLayout.setStretch(7,1)
        
        
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        
        self.setCentralWidget(mainWidget)
        
        
        
    def act1_UI_mc2(self):
        filler = 0
        
    def act1_UI_mc3(self):
        filler = 0
    
    #Activity 2 Definition
    def create_mod2_rows(self, left_image, right_image):
        face1 = QPixmap(left_image).scaledToWidth(400)
        face2 = QPixmap(right_image).scaledToWidth(400)
        #SHAPE = QPixmap(shape).scaledToWidth(150)
        CROSS = QPixmap(mod_constant.CROSS_IMAGE).scaledToWidth(100)
                
        left_face = QLabel()
        left_face.setPixmap(face1)
        left_face.setAlignment(Qt.AlignCenter)
        
        right_face = QLabel()
        right_face.setPixmap(face2)
        right_face.setAlignment(Qt.AlignCenter)
        
        cross = QLabel()
        cross.setPixmap(CROSS)
        cross.setAlignment(Qt.AlignCenter)
        
        #Widgets
        faceRowLayout = QHBoxLayout()
        buttonRowLayout = QHBoxLayout()
        
        faceRowLayout.addWidget(left_face)
        faceRowLayout.addWidget(cross)
        faceRowLayout.addWidget(right_face)
        faceRowLayout.setStretch(0,5)
        faceRowLayout.setStretch(1,1)
        faceRowLayout.setStretch(2,5)
        
        faceRowWidget = QWidget()
        faceRowWidget.setLayout(faceRowLayout)
        
        buttonRowWidget = QWidget()
        buttonRowWidget.setLayout(buttonRowLayout)
   
        return faceRowWidget
    
    def act2_UI_intro(self):
        #Creating all the widgets necessary in the page
        #Title of the module
        moduleTitleWidget = QLabel("Module 2")
        moduleTitleWidget.setFont(QFont('Times font',20))
        moduleTitleWidget.setAlignment(Qt.AlignVCenter)
        moduleTitleWidget.setAlignment(Qt.AlignHCenter)
        
        #Description of the module
        moduleDescWidget = QLabel()
        moduleDescWidget.setText("{}".format(mod_constant.MOD2_PRE_AMBLE))
        moduleDescWidget.setFont(QFont('Times font', 12))
        moduleDescWidget.setWordWrap(True)
        moduleDescWidget.setAlignment(Qt.AlignHCenter)
        moduleDescWidget.setAlignment(Qt.AlignTop)
        
        moduleDescLayout = QHBoxLayout()
        emptyLabel = QLabel(" ")
        moduleDescLayout.addWidget(emptyLabel)
        moduleDescLayout.addWidget(moduleDescWidget)
        moduleDescLayout.addWidget(emptyLabel)
        
        moduleDescLayout.setStretch(0,1)
        moduleDescLayout.setStretch(1,4)
        moduleDescLayout.setStretch(2,1)
        
        descWidget = QWidget()
        descWidget.setLayout(moduleDescLayout)
        
        #Assessment start button of the module
        moduleStartButton = QPushButton("Start Module 2")
        moduleStartButton.resize(20,10)
        
        navBar = self.create_navBar()
        
        #Adding to the layout
        layout = QVBoxLayout()
        layout.addWidget(navBar)
        layout.addWidget(moduleTitleWidget)
        #layout.addWidget(moduleDescWidget)
        layout.addWidget(descWidget)
        layout.addWidget(moduleStartButton)
        layout.insertStretch(3,1)
        
        layout.setStretch(0,1)
        layout.setStretch(1,3)
        layout.setStretch(2,4)
        layout.setStretch(4,1)
        
        #Changing sizing of the rows and columns
        #layout.setRowStretch(0,5)
        #layout.setRowStretch(1,15)
        #layout.setRowStretch(2,25)
        
        #Adding widgets to the final page
        pageWidget = QWidget()
        pageWidget.setLayout(layout)
        
        self.setCentralWidget(pageWidget)
        
        #What do buttons do
        moduleStartButton.clicked.connect(self.act2_UI_p1_first)
    
    def act2_UI_p1_first(self):
        self.timer_mod2_1.timeout.connect(self.act2_UI_p1_second)
        self.timer_mod2_1.start(1500)
        navbar = self.create_navBar()
        
        CROSS_IMAGE = QPixmap(mod_constant.CROSS_IMAGE).scaledToWidth(100)
        cross = QLabel()
        cross.setPixmap(CROSS_IMAGE)
        cross.setAlignment(Qt.AlignCenter)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navbar)
        mainLayout.addWidget(cross)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
        
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
    def act2_UI_p1_second(self):
        self.timer_mod2_1.start(1500)
        self.timer_mod2_1.timeout.connect(self.act2_UI_p1_third)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT1_IMAGE, mod_constant.RIGHT1_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
        
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
    def act2_UI_p1_third(self):
        self.timer_mod2_1.start(100)
        self.timer_mod2_1.timeout.connect(self.act2_UI_p1_fourth)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT1_SHAPE, mod_constant.RIGHT1_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)        
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget) 
        
    def act2_UI_p1_fourth(self):
        self.timer_mod2_1.start(1000)
        self.timer_mod2_1.timeout.connect(self.act2_UI_p1_end)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT1_IMAGE, mod_constant.RIGHT1_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)   
        
    def act2_UI_p1_end(self):
        self.timer_mod2_1.deleteLater()
        navbar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT1_IMAGE, mod_constant.RIGHT1_IMAGE)
        
        #Create the buttons
        circle_button = QPushButton("Circle")
        triangle_button = QPushButton("Triangle")
        square_button = QPushButton("Square")
        emptyLabel = QLabel()
        
        buttonRowLayout = QHBoxLayout()
        
        buttonRowLayout.addWidget(emptyLabel)
        buttonRowLayout.addWidget(circle_button)
        buttonRowLayout.addWidget(square_button)
        buttonRowLayout.addWidget(triangle_button)
        buttonRowLayout.addWidget(emptyLabel)
        buttonRowLayout.setStretch(0,1)
        buttonRowLayout.setStretch(1,2)
        buttonRowLayout.setStretch(2,2)
        buttonRowLayout.setStretch(3,2)
        buttonRowLayout.setStretch(4,1)
        
        buttonRow = QWidget()
        buttonRow.setLayout(buttonRowLayout)
               
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navbar)
        mainLayout.addWidget(faceRow)
        mainLayout.addWidget(buttonRow)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
      
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
        circle_button.clicked.connect(self.act2_UI_p2_first)
        square_button.clicked.connect(self.act2_UI_p2_first)
        triangle_button.clicked.connect(self.act2_UI_p2_first)
             
    def act2_UI_p2_first(self):
        self.timer_mod2_2.start(1500)
        self.timer_mod2_2.timeout.connect(self.act2_UI_p2_second)
        navbar = self.create_navBar()
        
        CROSS_IMAGE = QPixmap(mod_constant.CROSS_IMAGE).scaledToWidth(100)
        cross = QLabel()
        cross.setPixmap(CROSS_IMAGE)
        cross.setAlignment(Qt.AlignCenter)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navbar)
        mainLayout.addWidget(cross)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
        
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
    def act2_UI_p2_second(self):
        self.timer_mod2_2.start(1500)
        self.timer_mod2_2.timeout.connect(self.act2_UI_p2_third)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT2_IMAGE, mod_constant.RIGHT2_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)        
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
    def act2_UI_p2_third(self):
        self.timer_mod2_2.start(200)
        self.timer_mod2_2.timeout.connect(self.act2_UI_p2_fourth)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT2_SHAPE, mod_constant.RIGHT2_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget) 
        
    def act2_UI_p2_fourth(self):
        self.timer_mod2_2.start(1500)
        self.timer_mod2_2.timeout.connect(self.act2_UI_p2_end)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT2_IMAGE, mod_constant.RIGHT2_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)   
        
    def act2_UI_p2_end(self):
        self.timer_mod2_2.deleteLater()
        navbar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT2_IMAGE, mod_constant.RIGHT2_IMAGE)
               
        #Create the buttons
        circle_button = QPushButton("Circle")
        triangle_button = QPushButton("Triangle")
        square_button = QPushButton("Square")
        emptyLabel = QLabel()
        
        buttonRowLayout = QHBoxLayout()
        
        buttonRowLayout.addWidget(emptyLabel)
        buttonRowLayout.addWidget(circle_button)
        buttonRowLayout.addWidget(square_button)
        buttonRowLayout.addWidget(triangle_button)
        buttonRowLayout.addWidget(emptyLabel)
        buttonRowLayout.setStretch(0,1)
        buttonRowLayout.setStretch(1,2)
        buttonRowLayout.setStretch(2,2)
        buttonRowLayout.setStretch(3,2)
        buttonRowLayout.setStretch(4,1)
        
        buttonRow = QWidget()
        buttonRow.setLayout(buttonRowLayout)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navbar)
        mainLayout.addWidget(faceRow)
        mainLayout.addWidget(buttonRow)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
      
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
        circle_button.clicked.connect(self.act2_UI_p3_first)
        square_button.clicked.connect(self.act2_UI_p3_first)
        triangle_button.clicked.connect(self.act2_UI_p3_first)     
           
    def act2_UI_p3_first(self):
        self.timer_mod2_3.start(1100)
        self.timer_mod2_3.timeout.connect(self.act2_UI_p3_second)
        navbar = self.create_navBar()
        
        CROSS_IMAGE = QPixmap(mod_constant.CROSS_IMAGE).scaledToWidth(100)
        cross = QLabel()
        cross.setPixmap(CROSS_IMAGE)
        cross.setAlignment(Qt.AlignCenter)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navbar)
        mainLayout.addWidget(cross)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
        
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
    def act2_UI_p3_second(self):
        self.timer_mod2_3.start(1100)
        self.timer_mod2_3.timeout.connect(self.act2_UI_p3_third)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT3_IMAGE, mod_constant.RIGHT3_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
    def act2_UI_p3_third(self):
        self.timer_mod2_3.start(100)
        self.timer_mod2_3.timeout.connect(self.act2_UI_p3_fourth)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT3_IMAGE, mod_constant.RIGHT3_SHAPE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget) 
        
    def act2_UI_p3_fourth(self):
        self.timer_mod2_3.start(800)
        self.timer_mod2_3.timeout.connect(self.act2_UI_p3_end)
        navBar = self.create_navBar()
        faceRow = self.create_mod2_rows(mod_constant.LEFT3_IMAGE, mod_constant.RIGHT3_IMAGE)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navBar)
        mainLayout.addWidget(faceRow)
        mainLayout.insertStretch(2)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
    
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)   
        
    def act2_UI_p3_end(self):
        navbar = self.create_navBar()
        self.timer_mod2_3.deleteLater()
        faceRow = self.create_mod2_rows(mod_constant.LEFT3_IMAGE, mod_constant.RIGHT3_IMAGE)
                
        #Create the buttons
        circle_button = QPushButton("Circle")
        triangle_button = QPushButton("Triangle")
        square_button = QPushButton("Square")
        emptyLabel = QLabel()
        
        buttonRowLayout = QHBoxLayout()
        
        buttonRowLayout.addWidget(emptyLabel)
        buttonRowLayout.addWidget(circle_button)
        buttonRowLayout.addWidget(square_button)
        buttonRowLayout.addWidget(triangle_button)
        buttonRowLayout.addWidget(emptyLabel)
        buttonRowLayout.setStretch(0,1)
        buttonRowLayout.setStretch(1,2)
        buttonRowLayout.setStretch(2,2)
        buttonRowLayout.setStretch(3,2)
        buttonRowLayout.setStretch(4,1)
        
        buttonRow = QWidget()
        buttonRow.setLayout(buttonRowLayout)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(navbar)
        mainLayout.addWidget(faceRow)
        mainLayout.addWidget(buttonRow)
        mainLayout.insertStretch(2)
        mainLayout.insertStretch(2)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,7)
        mainLayout.setStretch(2,1)
      
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
        circle_button.clicked.connect(self.act3_UI_intro)
        square_button.clicked.connect(self.act3_UI_intro)
        triangle_button.clicked.connect(self.act3_UI_intro)       

    def act3_UI_intro(self):
        #Creating all the widgets necessary in the page
        #Title of the module
        moduleTitleWidget = QLabel("Module 3")
        moduleTitleWidget.setFont(QFont('Times font',20))
        moduleTitleWidget.setAlignment(Qt.AlignVCenter)
        moduleTitleWidget.setAlignment(Qt.AlignHCenter)
        
        #Description of the module
        moduleDescWidget = QLabel()
        moduleDescWidget.setText("{}".format(mod_constant.MOD3_PRE_AMBLE))
        moduleDescWidget.setFont(QFont('Times font', 12))
        moduleDescWidget.setWordWrap(True)
        moduleDescWidget.setAlignment(Qt.AlignHCenter)
        moduleDescWidget.setAlignment(Qt.AlignTop)
        
        moduleDescLayout = QHBoxLayout()
        emptyLabel = QLabel(" ")
        moduleDescLayout.addWidget(emptyLabel)
        moduleDescLayout.addWidget(moduleDescWidget)
        moduleDescLayout.addWidget(emptyLabel)
        
        moduleDescLayout.setStretch(0,1)
        moduleDescLayout.setStretch(1,4)
        moduleDescLayout.setStretch(2,1)
        
        descWidget = QWidget()
        descWidget.setLayout(moduleDescLayout)
        
        #Assessment start button of the module
        moduleStartButton = QPushButton("Start Module 3")
        moduleStartButton.resize(20,10)
        
        navBar = self.create_navBar()
        
        #Adding to the layout
        layout = QVBoxLayout()
        layout.addWidget(navBar)
        layout.addWidget(moduleTitleWidget)
        #layout.addWidget(moduleDescWidget)
        layout.addWidget(descWidget)
        layout.addWidget(moduleStartButton)
        layout.insertStretch(3,1)
        
        layout.setStretch(0,1)
        layout.setStretch(1,3)
        layout.setStretch(2,4)
        layout.setStretch(4,1)
        
        #Changing sizing of the rows and columns
        #layout.setRowStretch(0,5)
        #layout.setRowStretch(1,15)
        #layout.setRowStretch(2,25)
        
        #Adding widgets to the final page
        pageWidget = QWidget()
        pageWidget.setLayout(layout)
        
        self.setCentralWidget(pageWidget)
        
        #What do buttons do
        #Change this to the name of the function that defines Assessment 3
        moduleStartButton.clicked.connect(self.act3_UI_p1_first)
        
    def act3_UI_p1_first(self):
        # navbar = self.create_navBar()
        # filler = QLabel("This is where you put Assessment 3")
        # moduleDescLayout = QVBoxLayout()
        # emptyLabel = QLabel(" ")
        
        # moduleDescLayout.addWidget(navbar)
        # moduleDescLayout.addWidget(emptyLabel)
        # moduleDescLayout.addWidget(filler)
        # moduleDescLayout.addWidget(emptyLabel)
        
        # mainWidget = QWidget()
        # mainWidget.setLayout(moduleDescLayout)
        # self.setCentralWidget(mainWidget)
        self.window2 = MainWindow2()
        #self.window2.show()
        self.window2.animate(self.geometry().getRect(), self.window2.geometry().getRect())
        self.close()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #act1_intro_Window = 

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())