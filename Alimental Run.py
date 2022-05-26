"""
Alimental Run
@PracheeNanda, @Isabela Arriojas
@ICS3U1
@1/28/2019
"""

###Pygame base template borrowed from
#Simpson College Computer Science
#http://programarcadegames.com/

import pygame
import random
import sys
import time

#Initialize pygame
pygame.init()

#COLORS
black = (0, 0, 0)
white = (255, 255, 255)
green = (196, 232, 99)
red = (255, 0, 0)
blue = (44,205,232)

# Set screen dimensions and screen
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

class Player(pygame.sprite.Sprite):
    """This class represents the player"""
    def __init__(self):  
        super().__init__()
        
        #Loads and sets up player image
        ###Image created by us
        self.image = pygame.image.load("Mike.png").convert()
        self.image.set_colorkey (black)
        
        #Gets dimensions for image
        self.rect = self.image.get_rect()
        
        #Creates a "mask" which is later used for collision
        #This ignores the transparent parts of the image
        #and only looks at the opaque parts
        
        ###Borrowed from
        #http://renesd.blogspot.com/2017/03/pixel-perfect-collision-detection-in.html
        self.mask = pygame.mask.from_surface(self.image)
        
        #Set player lives and starting position
        self.lives = 3 
        self.rect.x = 490
        self.rect.y = 370
        
        #Set speed vector of player
        self.speed = 20
    
    def borderCheck(self):
        """Ensures player can't move past border"""
        
        if self.rect.x >= 930:       #If player is at the border and tries to move past it,
            self.rect.x = 930        #they can't move past it
        if self.rect.y >= 700:
            self.rect.y = 700
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y <= 0:
            self.rect.y = 0

class Food(pygame.sprite.Sprite):
    """This class represents the food items in the game"""
    def __init__(self):
        super().__init__()
        
        #Loads and sets up image for food
        ###Image borrowed from 
        #http://www.pixelberrystudios.com/
        self.image = pygame.image.load("berries.png").convert()
        self.image = pygame.transform.scale(self.image, [40, 40])
        self.image.set_colorkey (black)
        
        #Gets dimensions for image
        self.rect = self.image.get_rect()
        
        #Creates a "mask" which is later used for collision
        #This ignores the transparent parts of the image
        #and only looks at the opaque parts

        ###Borrowed from
        #http://renesd.blogspot.com/2017/03/pixel-perfect-collision-detection-in.html
        self.mask = pygame.mask.from_surface(self.image)
        
        #Sets a random direction where each number represents a direction
        self.way = random.randint (1,4)
        
    def reset_pos(self):
        """Resets the position and direction of object"""
        self.way = random.randint (1,4)             #These choose new positions and directions to go
        self.rect.y = random.randrange(0, 800)
        self.rect.x = random.randrange(0, 1000)
        
        if self.rect.y == player.rect.y:            #However, they will not spawn at the player's spawn coordinates
            self.rect.y = random.randrange(0, 800)
        if self.rect.x == player.rect.x:
            self.rect.x = random.randrange(0, 800)
     
    def update (self):
        """Updates the object's position"""
        if self.rect.x > 1000 or self.rect.x < 0:   #If it is past the border, then it
            self.reset_pos()                        #will reset it's positions and choose a new direction
        if self.rect.y > 800 or self.rect.y < 0:
            self.reset_pos()
        
        #This handles which direction they are travelling in
        if self.way == 1: #Food item moves upwards
            self.rect.y+=1
        if self.way == 2: #Food item moves downwards
            self.rect.y-=1
        if self.way == 3: #Food item moves left
            self.rect.x-=1
        if self.way == 4: #Food item moves right
            self.rect.x+=1

###Borrowed from
#https://stackoverflow.com/questions/25221036/pygame-music-pause-unpause-toggle
class Pause():
    """This class handles the play/stop function of the music"""
    def __init__(self):
        self.paused = pygame.mixer.music.get_busy() 
        #Checks to see if music is being played currently

    def toggle(self):
        """Switches between playing music and not playing music"""
        if self.paused:                     #If music is not being played,
            pygame.mixer.music.unpause()    #then start playing.
        if not self.paused:
            pygame.mixer.music.pause()      #Vice-versa, ff music is being played,
        self.paused = not self.paused       #then stop playing.

class LifeBar():
    """This class represents the lifebar/the health of the player"""
    def __init__(self):
        ###All images are edited from original taken from
        #https://www.amazon.ca/Use-The-Triforce-Luke-Container/dp/B006W10F8S
        #Loads and sets up image for food
        self.three_hearts = pygame.image.load("3_hearts.png").convert()
        self.three_hearts = pygame.transform.scale (self.three_hearts, [100, 50])
        self.three_hearts.set_colorkey(black)
        
        self.two_hearts = pygame.image.load("2_hearts.png").convert()
        self.two_hearts = pygame.transform.scale (self.two_hearts, [100, 50])
        self.two_hearts.set_colorkey(black)
        
        self.one_heart = pygame.image.load("1_heart.png").convert()
        self.one_heart = pygame.transform.scale (self.one_heart, [30, 50])
        self.one_heart.set_colorkey(black)

    def draw (self):
        """Updates and draws lifebar to match with the player's health"""
        if player.lives == 3:   #If player still has three lives, then three hearts appear
            screen.blit (self.three_hearts, [10,10])
        
        if player.lives == 2:   #If player still has two lives, then two hearts appear
            screen.blit (self.two_hearts, [10,10])
        
        if player.lives == 1:   #If player has only one life, then one heart appears
            screen.blit (self.one_heart, [10,10])
            
def gameReset(): 
    ###Idea for global borrowed from
    #https://stackoverflow.com/questions/5060465/get-variables-from-the-outside-inside-a-function-in-php
    """This function resets all the variables in the game"""
    #global makes it so all variables can be accessed throughtout the game
    global all_sprites_list, healthy_food_list, unhealthy_food_list, player, berry, doughnut, done, game_over, game_pause, score, font, myfont, lifebar, game_liveone, extra
    
    all_sprites_list = pygame.sprite.Group()    #This list holds all sprites in the game; used to draw them on screen
    healthy_food_list = pygame.sprite.Group()   #This holds all the berries (the good foods)
    unhealthy_food_list = pygame.sprite.Group() #This holds all the doughnuts (the bad foods)
    
    player = Player() #This represents the player
    all_sprites_list.add(player) #Add player to list for drawing
    for i in range(15):
        """
        This loop creates the instances for the food items, adds them on to a list,
        and sets a random position for each of them.
        """
        
        berry = Food() 
        doughnut = Food()
        
        #Sets a different image for the doughnuts and removes white background
        #Edited image; original image taken from
        #https://www.canva.com/media/MACH8Xa1DaY
        doughnut.image = pygame.image.load("doughnuts.png").convert()
        doughnut.image.set_colorkey (white)
        
        #Sets a random location for them
        doughnut.rect.x  = random.randrange(screen_width)
        doughnut.rect.y = random.randrange(screen_height)
        
        berry.rect.x = random.randrange(screen_width)
        berry.rect.y = random.randrange(screen_height)
        
        #Adds them to the list which will be used for collision and drawing later on
        healthy_food_list.add(berry)
        unhealthy_food_list.add(doughnut)
        
        all_sprites_list.add(doughnut)
        all_sprites_list.add(berry)
    
    done = False            #Loop until the user clicks some other button.
    game_over = False       #Starts when user loses/wins game
    game_pause = False      #Starts when user pauses the game
    game_liveone = False    #Starts when user has only one life
    extra = False           #Used to trigger the game_liveone function only once

    score = 0               #Counts the score (for player)

    lifebar = LifeBar()     #This represents the lifebar that monitors the player's health
    
    #Create two fonts for texts
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    font = pygame.font.Font(None, 36)

def gameOverScreen(score):  #This function plays when game is over (player has lost/won)
    #Draw blue rectangle, will serve as a background
    pygame.draw.rect(screen, blue, [250,250,500,250])
    
    # Draws two boxes
    y_offset = 0
    while y_offset < 500:
        pygame.draw.rect (screen, green, [350 + y_offset, 375, 75, 75])
        y_offset += 250
    
    #Resets the score to 0, if it is negative
    if score < 0:
        score = 0
    
    #Loads the font with final score and is they won or lost
    result_text = font.render(result+str(score), True, white)
    text = font.render("Game Over", True, white)
    
    #Blits text onto screen
    screen.blit(text, [440, 300])
    screen.blit(result_text, [300, 340])
    
    """This code creates a "button" that restarts the game"""
    
    global restart_button #Global allows it to be used everywhere, creates the button that will be used to restart the game
    restart_button = pygame.Rect(600, 375,75,75)    #Stores the rectangular coordinates of the button
    ###Edited image, original image taken from
    #https://www.canva.com/media/MAAQottX2P0
    done_icon = pygame.image.load("done.png") #loads image  of the button and then changes it's size
    done_icon = pygame.transform.scale (done_icon, [75,75])
    screen.blit (done_icon, [600, 375])
    
    global quit_button #When pressing this button, the game will be over
    quit_button = pygame.Rect(362, 389,50,50)
    ###Edited image, original image taken from
    #https://www.canva.com/media/MAAQogy-l7Q    
    restart_icon = pygame.image.load("gameOver.png")
    restart_icon = pygame.transform.scale (restart_icon, [50,50])
    screen.blit (restart_icon, [362, 389])
    
    
def pause_game(): #This function starts when the game is paused
    #Draw blue rectangle, will serve as a background
    pygame.draw.rect(screen, blue, [250,250,500,250])
    
    #This loop draws three boxes
    y_offset = 0
    while y_offset < 450:
        pygame.draw.rect (screen, green, [315 + y_offset, 375, 75, 75])
        y_offset += 150
    
    #Loads the title text screen ( i.e. Menu) and then blits it onto screen
    text = font.render ("Menu", True, white)
    screen.blit(text, [460, 300])
    
    """This creates a mute button that will pause or play the background music in game"""
    global mute_button
    ###Image taken from
    #https://www.iconfinder.com/icons/572259/audio_loud_mute_silent_sound_volume_volume_button_icon
    mute_button = pygame.Rect (315, 375, 75, 75)  #Sets dimensions for the button
    mute_icon = pygame.image.load("play.png") #Sets, loads and blits image onto screen
    mute_icon = pygame.transform.scale (mute_icon, [75,75])
    screen.blit (mute_icon, [315, 375])
    
    """This creates a done button that will let user exit the pause screen"""
    global done_button
    done_button = pygame.Rect (615, 375, 75,75) #Sets dimensions for the button
    ###Edited image, original image taken from
    #https://www.canva.com/media/MAAQottX2P0
    done_icon = pygame.image.load("done.png") #Sets, loads and blits image onto screen
    done_icon = pygame.transform.scale (done_icon, [75,75])
    screen.blit (done_icon, [615, 375])
    
    """This creates a restart button that will let user restart the game"""
    global restart_button
    restart_button = pygame.Rect (465, 375, 75, 75) #Sets dimensions for the button
    ###Image taken from 
    #https://visualpharm.com/free-icons/restart-595b40b75ba036ed117d841f
    restart_icon = pygame.image.load("restart.png") #Sets, loads and blits image onto screen
    restart_icon = pygame.transform.scale (restart_icon, [75,75])
    screen.blit (restart_icon, [465, 375])

#Load and play music in an infinite loop while game plays
#Music borrowed from
#2https://www.youtube.com/watch?v=Zz1bfhtKsHM
pygame.mixer.music.load("undertake.mp3")
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play(-1) 
    
#Creates an instance for the "pause" class and will be used to toggle the music effects
pause = Pause()

#Used to set variables for the game
gameReset()

#Sound effects for when player eats any food item

###Sound effect borrowed from
#https://freesound.org/people/OwlStorm/sounds/404793/
eat_berries = pygame.mixer.Sound('eat.wav')

###Sound effect borrowed from
#https://freesound.org/people/suntemple/sounds/253174/
eat_doughnut = pygame.mixer.Sound('eat_doughnut.wav')

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Sets dimensions for the pause button
pause_button = pygame.Rect(750, 10, 35, 35)

# Loop as long as done == False
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
                        
        if game_over == True:   #If user wins/loses the game
            if event.type == pygame.MOUSEBUTTONDOWN:    #If user presses his mouse
                if event.button == 1:   #If it is a left-click
                    if restart_button.collidepoint(event.pos):  #If they pressed the restart button
                        gameReset()     #Reset the game
                        game_over = False   #Exit game over screen
        
                    if quit_button.collidepoint(event.pos): #If they pressed the quit button
                        done = True #Exit game

        if game_pause == True: #If user pauses the game
            if event.type == pygame.MOUSEBUTTONDOWN: #If user presses his mouse
                if event.button == 1: #If it is a left-click
                    if mute_button.collidepoint(event.pos): #If user presses the "mute/play" button
                        pause.toggle()  #Then play/mute background music
                    
                    if restart_button.collidepoint(event.pos):   #If user presses the restart button
                        gameReset()    #Restart the game
                        game_pause = False #Exit the game paused screen
                        
                    if done_button.collidepoint(event.pos): #If they pressed the done button
                        game_pause = False #Exit the game paused screen

        if event.type == pygame.MOUSEBUTTONDOWN: #If user presses his mouse
            if event.button == 1: #If it is a left-click
                if pause_button.collidepoint(event.pos):  #If they pressed the pause button
                    game_pause = True #Pause the game
                
        if event.type == pygame.KEYDOWN: #If user presses a key
            if event.key == pygame.K_LEFT: #If it was the left button
                player.rect.x -= player.speed #Player moves left
                
            if event.key == pygame.K_RIGHT: #If it was the right button
                player.rect.x += player.speed #Player moves right
                
            if event.key == pygame.K_UP: #If it was the up button
                player.rect.y -= player.speed #Player moves up
                
            if event.key == pygame.K_DOWN:  #If it was the down button
                player.rect.y += player.speed #Player moves down
    
    """The if statements ensures that the player and other sprites can't move when game is paused or over"""
    if not game_over: #if the game isn't over
        if not game_pause: #if the game isn't paused
            
            #Creates a list of berries eaten by player, removes them from screen
            player_eat_berries = pygame.sprite.spritecollide(player, healthy_food_list, True, pygame.sprite.collide_mask)
            
            for i in player_eat_berries:
                """This loop plays the sound effects, adds score"""
                eat_berries.play() #Play sound effect
                score += 2 #add 2 to player score
                
            #Creates a list of doughnuts eaten by player, removes them from screen
            player_eat_doughnuts = pygame.sprite.spritecollide(player, unhealthy_food_list, True, pygame.sprite.collide_mask)
            
            for i in player_eat_doughnuts:
                """This loop plays the sound effects, decreases score"""
                eat_doughnut.play() #Play sound effect
                score -= 5  #deduct 5 from player score
        
            """The loop below handles user's lives"""
            if score < 0: #If user has a score of 0
                if player.lives == 0: #Check if player has no lives
                    if score > 0: #If score is less than 0
                        score = 0 #Make score 0
                    result = "You have lost. Here is your score:" #User has lost so the text to be displayed
                    game_over = True #Show game over screen
                
                elif player.lives == 1 and extra == False: #If player has 1 life left
                    player.lives -= 1 #Deduct a life
                    """This gives a warning to the player when they have no lives left"""
                    score = 0
                    game_liveone = True #Give a warning
                    extra = True
                    
                else:
                    player.lives -= 1 #Deduct a life
                    score = 0 #Reset score
            
            """This handles when there is nothing left to eat"""
            if len (healthy_food_list) == 0: #Checks to see if al berries are eaten
                game_over = True                #Show game over screen
                result = "You have won. Here is your score:" #User has won so the text to be displayed
            
            """The following loop prevents a negative score from being shown on screen"""
            if score < 0: #If the score is less than 0
                showscore = 0 #Then change score to 0
            else: #or let it be what score's current value
                showscore = score
            textsurface = myfont.render("Score {0}".format(showscore), False, (0, 0, 0)) #Load score text
    
            # Clear the screen and set the screen background
            screen.fill(green) 
            
            #Draw the lifebar
            lifebar.draw()
            
            #Draws the pause button
            pygame.draw.rect (screen, white, [750, 10, 35, 35])
            pygame.draw.rect (screen, black, [755, 12, 10, 30])
            pygame.draw.rect (screen, black, [768, 12, 10, 30])
            
            #Draws all the sprites onto screen and updates their movement
            all_sprites_list.draw(screen)
            all_sprites_list.update()
            
            #Checks to see if player is trying to go offscreen
            player.borderCheck()
            
            #Blits score onto screen
            screen.blit(textsurface,(810,20))

    if game_over == True: #If game is over
        game_liveone = False #Stop showing the warning
        gameOverScreen(score) #Show game over screen (uses score to show score for player)
    
    if game_pause == True: #If user pauses game
        pause_game() #Pause game
    
    if game_liveone == True: #If user has one life left
        pygame.draw.rect(screen, red, [0,750,1000, 30])
        #Draw a red rectangle (serves as background for warning message)
        full_font = pygame.font.SysFont('Calibri', 25) #Loads font
        #Loads messaage
        text = full_font.render ("A cat has nine lives but you have NONE. BE CAREFUL.", True, white)
        screen.blit (text, [300, 755]) #Displays message
        
    pygame.display.flip() #update screen
    
    # This limits the while loop to a max of 70 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(70)


# Quit pygame and close window
pygame.quit()
sys.exit()
