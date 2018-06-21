
#!/usr/bin/env python
"""
Knots
"""
 
 
#Import Modules
import os, pygame, random
from pygame.locals import *
from pygame.compat import geterror
 
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
 
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
 
# Define the size of the game (7, 11 and 15 work)
gameWidth = 5
gameHeight = 5
crossingValues = 0
DoNotStop = True
randomCrossingMode = False
demoMode = True
verboseLevel = 0
def verboseprint(level, *args):
    if level <= verboseLevel: 
        print args
    else:
        pass
 
 
#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
 
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound
 
 
 
#classes for our game objects
class Pointer(pygame.sprite.Sprite):
    """moves a the Pointer on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        #self.image, self.rect = load_image('fist.bmp', -1)
        self.image, self.rect = load_image('pointer.png')
        self.punching = 0
 
    def update(self):
        "move the pointer based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        #if self.punching:
        #    self.rect.move_ip(50, 10)
     
 
    def mouseDown(self, imageSelected):
        "returns true if the pointer collides with the target"
        if not self.punching:
            #hitbox = self.rect.inflate(-5, -5)
            #hitbox = self.rect
            #print "hitbox = ", hitbox
            self.image, self.rect = load_image(imageSelected + '.png', -1)
            #print "target.rect = ", target.rect
            #if hitbox.colliderect(target.rect):
            self.punching = 1
            #    return True
            #else:
            #    return False
 
    def mouseUp(self):
        "called to pull the pointer back"
        self.punching = 0
        self.image, self.rect = load_image('pointer.png')
 
class Peg(pygame.sprite.Sprite):
    """ Displays a Vertical overpass"""
     
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.imageName = name
        self.image, self.rect = load_image(self.imageName + '.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 50*x, 50*y
        #print "rect = ", self.rect
        self.x = x
        self.y = y
 
    def getType(self):
        return self.imageName
 
    def setType(self, imageName):            
        self.imageName = imageName
        self.image, self.rect = load_image(self.imageName + '.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 50*self.x, 50*self.y
        #print "knot piece rect = ", self.rect
 
    def mouseDownSelect(self):
        return self.imageName
 
    def mouseUpSelect(self, imageName):            
        self.imageName = imageName
        self.image, self.rect = load_image(self.imageName + '.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 50*self.x, 50*self.y
        print "knot piece rect = ", self.rect
 
    def update(self):
        "walk or spin, depending on the monkeys state"
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos
 
 
 
class Game():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
         
    def setInitialCellValues(self):
        self.cells.append(knotPiece(4,0, "nopeg"))
        self.cells.append(knotPiece(3,1, "peg"))
        self.cells.append(knotPiece(5,1, "peg"))
        self.cells.append(knotPiece(2,2, "peg"))
        self.cells.append(knotPiece(4,2, "peg"))
        self.cells.append(knotPiece(6,2, "peg"))
        self.cells.append(knotPiece(1,3, "peg"))
        self.cells.append(knotPiece(3,3, "peg"))
        self.cells.append(knotPiece(5,3, "peg"))
        self.cells.append(knotPiece(7,3, "peg"))
        self.cells.append(knotPiece(0,4, "peg"))
        self.cells.append(knotPiece(2,4, "peg"))
        self.cells.append(knotPiece(4,4, "peg"))
        self.cells.append(knotPiece(6,4, "peg"))
        self.cells.append(knotPiece(8,4, "peg"))
  
 
    def resetCellValues(self ):
  
    def getSprites(self):
        return self.cells
 
    def getCellType(self, x, y):
        for i in range(15)
            cell_x = self.cells[i].getX()
            cell_y = self.cells[i].getY()
            if cell_y = y:
                if cell_x == x or cell_x+1 == x
                        return self.cells[i].getType()
        return None
 
    def setCellType(self, x, y, cellType):
        for i in range(15)
            cell_x = self.cells[i].getX()
            cell_y = self.cells[i].getY()
            if cell_y = y:
                if cell_x == x or cell_x+1 == x
                    self.cells[i].setType(cellType)
                    =
 
         
 
def main():
    """ this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((100*gameWidth, 100*gameHeight))
    pygame.display.set_caption('PEG GAMES')
    pygame.mouse.set_visible(0)
 
#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
 
#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Jump PEGS", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)
 
#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
 
#Prepare Game Objects
    game = Game(gameWidth,gameHeight, crossingValues, randomCrossingMode)
    game.setInitialCellValues()
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    pointer = Pointer()
    spriteNames = [pointer]
    cells = game.getSprites()
    for row in cells:
        for cell in row:
                spriteNames.append(cell)    
    allsprites = pygame.sprite.RenderPlain(spriteNames)
 
 
#Main Loop
    going = True
    mouse_status = "up"
    start_x = 0
    start_y = 0
    imageSelected = ""
    while going:
        clock.tick(20)
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                start_x, start_y = pygame.mouse.get_pos()
                start_x /= 50
                start_y /= 50
                print "start_x= ",start_x , "start_y=", start_y
                cellType = game.getCellType(start_x,start_y)
                if cellType == "hole":
                    whiff_sound.play() #miss
                else:
                    punch_sound.play() #punch
                    pointer.mouseDown("pegPointer")
                    mouse_status = "down"
 
            elif event.type == MOUSEBUTTONUP:
                if mouseStatus == "down":
                    x, y = pygame.mouse.get_pos()
                    x = x/50 # Pick the closest square
                    y = y/50
                    mouse_status = "up"
                    result = game.movePeg(start_x, start_y, x, y)
                    pointer.mouseUp()
                    #print "start_x =", start_x, "start_y =", start_y
                    if result == True:
                        punch_sound.play()
                    elif:
                        whiff_sound.play()                
 
        allsprites.update()
 
        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
 
    pygame.quit()
 
#Game Over
 
 
#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
