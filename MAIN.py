# Author - Hinesh Nyati
# Application development and model - Hinesh Nyati
# Creative work and GUI - Ranveer Singh and Hinesh Nyati
# Robotics and Arduino - Aditya Toshniwal and Hinesh Nyati

# =============================================================================
# IMPORTS
# =============================================================================
from customtkinter import *                        # Provides custom themed Tkinter widgets
from customtkinter import CTkInputDialog           # Custom input dialog for getting user input
from tkinter import messagebox                     # Standard tkinter messagebox for alerts
from math import *                                 # Import all math functions (e.g., sin, cos, etc.)
from random import randint                         # For generating random integer values
from PIL import Image                              # Python Imaging Library for image operations
import gtts, time, pygame, os                      # gTTS for text-to-speech, time for delays, pygame for multimedia, os for filesystem operations
import threading, csv                              # threading for concurrency, csv for reading CSV files
import cv2 as cv                                   # OpenCV for computer vision, aliased as cv
import cvzone                                      # cvzone simplifies computer vision tasks using OpenCV
from cvzone.HandTrackingModule import HandDetector # Module to detect hands using computer vision
from cvzone.ClassificationModule import Classifier # Module for classification tasks using pre-trained models
import numpy as np                                 # For numerical operations on arrays
import random, playsound                # threading for concurrency, random for randomness, playsound for playing sound files
from pyfirmata import Arduino, SERVO               # For interfacing with Arduino boards and controlling servo motors
from time import sleep                             # sleep to pause program execution

# =============================================================================
# INITIAL SETUP & GLOBAL VARIABLES
# =============================================================================

# Initialize the pygame mixer for audio playback (used for background music and sound effects)
pygame.mixer.init()

# Global variables used across functions in this application
name = ""     # Will hold the user's name as input via a dialog
flag = False  # A flag that might be used for controlling program flow in error conditions or other logic

# Configure the appearance and theme of the GUI using CustomTkinter
set_appearance_mode("dark")       # Set the visual style to a dark theme
set_default_color_theme("blue")   # Set the primary color theme to blue

# Re-initialize pygame mixer and load background music file to be played in a loop
pygame.mixer.init()
pygame.mixer.music.load("__resources/bgm.mp3")
pygame.mixer.music.play(loops=100)  # Background music will continuously play in the background

# =============================================================================
# FUNCTION DEFINITIONS
# =============================================================================

def _say(x):
    """
    Uses text-to-speech to vocalize the provided text in a separate thread.
    
    This function creates a new thread so that generating and playing the audio does not
    block the main GUI thread.
    
    Args:
        x (str): The text to be spoken.
    """
    def _sayThread():
        a, b = randint(1, 9999), randint(1, 9999)
        text = gtts.gTTS(x, lang="en")
        text.save(f"__resources/{a}{b}.mp3")
        time.sleep(1)
        playsound.playsound(f"__resources/{a}{b}.mp3")
    thread_gtts = threading.Thread(target=_sayThread)
    thread_gtts.start()
def fade_in(widget, scale=0.1):
    """
    Creates a fade-in effect for a given widget by incrementally increasing its size.
    
    This recursive function adjusts the placement and font size of the widget until
    a specified maximum scale is reached.
    
    Args:
        widget (tkinter widget): The widget to apply the fade-in effect to.
        scale (float, optional): The current scaling factor; default is 0.1.
    """
    if scale < 5:
        widget.place(relx=0.5, rely=0.5, anchor=CENTER,
                     relwidth=scale + (scale * 1.1), relheight=scale + (scale * 1.1))
        widget.configure(font=("chelsea market", scale * 60, "bold"))
        scale += 0.01
        splash.after(50, fade_in, widget, scale)
def change_banner(n):
    """
    Updates the banner text displayed in the application.
    
    This function attempts to update the global banner label with new text.
    
    Args:
        n (str): The banner text to display.
    """
    global head_label, bc, abchd
    try:
        head_label.configure(text=bc)
    except:
        head_label.configure(text=n)
    head_label.update()
def move_label(label):
    """
    Animates a label widget to move horizontally across the window.
    
    This function creates a scrolling effect by periodically updating the label's
    x-coordinate. Once the label moves off-screen, it resets its position.
    
    Args:
        label (tkinter widget): The label widget to animate.
    """
    global window
    current_x = label.winfo_x()
    label_width = label.winfo_width()
    screen_width = window.winfo_screenwidth()

    if current_x + label_width < screen_width + 100:
        label.place(x=current_x + 5, y=2)
    else:
        label.place(x=-label_width, y=2)
    
    window.after(50, lambda: move_label(label=label))
def execution():
    """
    Schedules periodic updates for the banner text in the GUI.
    
    Uses the head_frame's after() method to change the banner text at specific intervals.
    """
    global head_frame, window
    head_frame.after(7000, lambda: change_banner("Experience the Crescence of Wizardry!"))
    head_frame.after(40000, lambda: change_banner("Which one did you love the most!?"))
    head_frame.after(80000, lambda: change_banner("Share your experience, lend us a feeback!"))
    head_frame.after(120000, lambda: change_banner("'What are you? A MUDBLOOD MUGGLE!"))
    head_frame.after(150000, lambda: change_banner("Nomore, you're an official wizard now..."))
    head_frame.after(200000, lambda: change_banner("ALOHOMORA, EXPELLIARMUS, AVADA KEDAVRA!   "))
def show_splash_screen():
    """
    Displays a splash screen during application startup.
    
    This function creates a temporary window with animated text that updates at fixed intervals.
    Once the splash screen sequence is complete, the window is destroyed to allow the main window to load.
    """
    global splash
    splash = CTkToplevel()
    splash.geometry("800x400")
    splash.title("Loading...")
    splash.overrideredirect(True)  # Remove window decorations

    splash_x = (1366 - 800) // 2
    splash_y = (768 - 400) // 2
    splash.geometry(f"800x400+{splash_x}+{splash_y}")

    splash.configure(bg="blue")
    label = CTkLabel(splash, text="CRESCENCE OF WIZARDRY!!\nMuggles FEEL Magic!",
                     font=("chelsea market", 100, "bold"))
    label.pack(expand=True)

    fade_in(label)

    def splash1():
        label.configure(text="Almost there....", font=("chelsea market", 84, "bold"))
        splash.title("Loading..")
        splash.update()

    def splash2():
        label.configure(text="You're All Set!", font=("chelsea market", 114, "bold"))
        splash.title("Loading!")
        splash.update()

    splash.after(3000, splash1)
    splash.after(6000, splash2)
    splash.after(7000, splash.destroy)

def playGame():
    """
    Runs the snake game within the application.
    
    This function initializes the game environment using pygame,
    sets up the game window, loads the required images for the snake,
    enemy, and game over screen, and handles the main game loop that
    processes events, moves the snake, detects collisions, and updates
    the score. The game ends when the snake collides with a boundary or an enemy.
    
    Returns:
        bool: True if the player's score is at or above a threshold (>=150),
              False otherwise.
              
    Notes:
        - The snake's speed increases gradually as the player scores points.
        - New enemy objects (referred to as "death eaters") spawn randomly.
        - The game loop runs until a collision is detected, triggering a game over.
    """
    global score
    pygame.init()  # Initialize pygame modules

    # Define dimensions for the game window
    window_width = 1212
    window_height = 600
    game_window = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()  # Create a clock object to control frame rate

    GameOver = False  # Boolean flag to indicate when the game is over
    z = 10            # Initial movement step increment for the snake

    # Set the title of the game window
    pygame.display.set_caption('Snake Game')

    # =============================================================================
    # LOAD IMAGES
    # =============================================================================
    snake_head_image = pygame.image.load('__resources/snake_head.png')
    snake_head_image = pygame.transform.scale(snake_head_image, (60, 60))
    game_over_img = pygame.image.load('__resources/GAME_OVER.png')
    game_over_img = pygame.transform.scale(game_over_img, (window_width, window_height))
    enemy_image = pygame.image.load('__resources/enemy.png')
    enemy_image = pygame.transform.scale(enemy_image, (45, 45))
    death_eater_image = pygame.image.load("__resources/death_eater.png")
    death_eater_image = pygame.transform.scale(death_eater_image, (60, 60))

    # =============================================================================
    # INITIAL GAME STATE
    # =============================================================================
    score = 0  # Initialize player score
    snake_position = [(window_width // 2), (window_height // 2)]  # Start at center
    enemy_position = [
        random.randrange(1, (window_width // 10)) * 10,
        random.randrange(1, (window_height // 10)) * 10
    ]

    snake_speed = 15  # Base speed for the snake
    death_eaters = []       # List to store enemy objects that move downwards
    death_eater_speed = 10  # Speed at which the death eaters move
    A = 1  # Parameter controlling the frequency of spawning additional enemies

    # Set up font for displaying score on screen
    font = pygame.font.Font(None, 36)
    snake_direction = "down"  # Default initial movement direction

    # =============================================================================
    # MAIN GAME LOOP
    # =============================================================================
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle user input to change snake direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            snake_direction = 'left'
        elif keys[pygame.K_RIGHT]:
            snake_direction = 'right'
        elif keys[pygame.K_UP]:
            snake_direction = 'up'
        elif keys[pygame.K_DOWN]:
            snake_direction = 'down'

        # Update snake position based on direction
        if snake_direction:
            if snake_direction == 'left':
                snake_position[0] -= z
            elif snake_direction == 'right':
                snake_position[0] += z
            elif snake_direction == 'up':
                snake_position[1] -= z
            else:
                snake_position[1] += z

        # Collision detection: boundaries and enemy proximity
        if snake_position[0] < 0 or snake_position[0] >= window_width - 10 or \
           snake_position[1] < 0 or snake_position[1] >= window_height - 10:
            GameOver = True

        elif ((snake_position[0] - enemy_position[0]) <= 30 and (snake_position[0] - enemy_position[0]) >= -30) and \
             ((snake_position[1] - enemy_position[1]) <= 30 and (snake_position[1] - enemy_position[1]) >= -30):
            print('enemy Eaten!')
            score += 10  # Increase score when enemy is "eaten"
            enemy_position = [
                random.randrange(1, (window_width // 10)) * 10,
                random.randrange(1, (window_height // 10)) * 10
            ]
            z = z * 1.05  # Increase snake speed gradually
            A = A + 0.25  # Increase spawn rate of additional enemies

        # =============================================================================
        # RENDERING
        # =============================================================================
        game_window.fill("WHITE")
        game_window.blit(snake_head_image, (snake_position[0], snake_position[1]))
        game_window.blit(enemy_image, (enemy_position[0], enemy_position[1]))

        for death_eater in death_eaters:
            death_eater[1] += death_eater_speed  # Move enemy downward
            game_window.blit(death_eater_image, (death_eater[0], death_eater[1]))
            if (snake_position[0] < death_eater[0] + 30 and
                snake_position[0] + 30 > death_eater[0] and
                snake_position[1] < death_eater[1] + 30 and
                snake_position[1] + 30 > death_eater[1]):
                GameOver = True

        # Display the current score
        score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
        game_window.blit(score_text, (10, 10))

        if random.randint(0, 100) < int(A):
            death_eaters.append([
                random.randrange(1, (window_width // 10)) * 10,
                0
            ])

        death_eaters = [death_eater for death_eater in death_eaters if death_eater[1] < window_height]

        pygame.display.update()
        clock.tick(snake_speed)

        if GameOver == True:
            sleep(1)
            if score >= 150:
                ans = True
                pygame.quit()
            else:
                ans = False
                pygame.quit()
            return ans
def open_and_close_box():
    """
    Controls an Arduino-connected servo to simulate opening and closing a box.
    
    This function connects to an Arduino board on COM4 and controls a servo motor on pin 9.
    It gradually rotates the servo to an "open" position, holds it open for 5 seconds, then rotates
    it back to the "closed" position.
    
    If an error occurs (e.g., the Arduino board is not connected), the function pauses the background
    music, uses text-to-speech to notify the user, and then terminates the program gracefully.
    """
    try:
        board = Arduino("COM4") #Change as per requirement
        board.digital[9].mode = SERVO

        def rotateservo(pin, angle):
            board.digital[pin].write(angle)
            sleep(0.015)

        for i in range(0, 180):
            sleep(0.01)
            rotateservo(9, 110)
        sleep(5)
        for i in range(0, 180):
            sleep(0.01)
            rotateservo(9, 0)
    except:
        pygame.mixer.music.pause()
        engine = gtts.gTTS("Ah! Seems like the robotics system hasn't been connected. But don't you worry cuz you have won the game! Congratulations!")
        engine.save(f"newfile{randint(1, 100000)}.mp3")
        playsound.playsound(f"newfile{randint(1, 100000)}.mp3")
        pygame.mixer.music.play()
        sleep(2)
        cv.destroyAllWindows()
        sys.exit()
def wizardry_m():
    """
    Launches the interactive "wizardry" drawing game.
    
    This function starts a new thread to run a real-time video capture application.
    It initializes the webcam, loads a pre-trained gesture recognition model, and allows the user to draw on a digital canvas by moving a blue-colored object or their hand. Depending on the recognized gesture (spell), specific actions such as playing sounds or opening a box are triggered.
    
    Note on threading:
        - A new thread is created so that the drawing game can process video frames concurrently,
          without freezing the main GUI.
        - This is achieved by instantiating a Thread object with the target function and calling .start().
    """
    global classifier

    def threaded_game_1():
        """
        Handles real-time video capture, gesture detection, and drawing.
        
        This inner function runs in a separate thread. It captures frames from the webcam,
        processes the image to detect blue-colored objects, and draws on a canvas accordingly.
        When certain gestures are recognized by the classifier, corresponding actions are executed.
        """
        pygame.mixer.init()
        global classifier
        pygame.mixer.music.load("__resources/bgm.mp3")
        pygame.mixer.music.play(loops=5)

        cap = cv.VideoCapture(0)
        classifier = Classifier("keras_model.h5", "labels.txt")
        imgCanvas = np.zeros((480, 640, 3), np.uint8)
        xp, yp = 0, 0
        color = (255, 0, 255)
        labels = ["Alohomora", "Avada Kedavra", "Expecto Patronum", "Expelliarmus", "Silencio", "Sonorus"]

        while True:
            success, img = cap.read()
            xyz = img.copy()
            xyz = cv.flip(xyz, 1)

            blueLower = np.array([100, 200, 220])
            blueUpper = np.array([120, 255, 255])
            hsv = cv.cvtColor(xyz, cv.COLOR_BGR2HSV)
            blueMask = cv.inRange(hsv, blueLower, blueUpper)

            _, cnts = cv.findContours(blueMask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours, _ = cv.findContours(blueMask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            if contours:
                cnt = max(contours, key=cv.contourArea)
                epsilon = 0.02 * cv.arcLength(cnt, True)
                approx = cv.approxPolyDP(cnt, epsilon, True)
                (x, y), _ = cv.minEnclosingCircle(approx)

                cv.circle(xyz, (int(x), int(y)), 13, color, cv.FILLED)
                cv.line(xyz, (int(xp), int(yp)), (int(x), int(y)), color, 15)
                cv.line(imgCanvas, (int(xp), int(yp)), (int(x), int(y)), color, 15)
                xp, yp = int(x), int(y)

            imgGray = cv.cvtColor(imgCanvas, cv.COLOR_BGR2GRAY)
            _, imgInv = cv.threshold(imgGray, 50, 255, cv.THRESH_BINARY_INV)
            imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
            xyz = cv.bitwise_and(xyz, imgInv)
            xyz = cv.bitwise_or(xyz, imgCanvas)
            xyz = cv.addWeighted(xyz, 1, imgCanvas, 1, 0)

            cv.imshow("Crescence of Wizardry - Be a wizard!", xyz)

            if cv.waitKey(10) & 0xFF == ord('.'):
                imgCanvas = np.zeros((480, 640, 3), np.uint8)

            if cv.waitKey(10) & 0xFF == ord('d'):
                index, confidence = classifier.getPrediction(imgCanvas)
                print(str(labels[confidence]))
                print(str(labels[confidence]))
                if str(labels[confidence]) == "Alohomora":
                    pygame.mixer.music.pause()
                    playsound.playsound("__resources/alohomora.mp3")
                    pygame.mixer.music.play()
                    open_and_close_box()
                if str(labels[confidence]) == "Avada Kedavra":
                    pygame.mixer.music.pause()
                    playsound.playsound("__resources/avada-kedavra.mp3")
                    engine = gtts.gTTS("We're sorry for you, but, you chose death! Bye Sorcerer!")
                    a = random.randint(1, 100000)
                    engine.save(f"newfile{a}.mp3")
                    playsound.playsound(f"newfile{a}.mp3")
                    sleep(5)
                    cv.destroyAllWindows()
                    sys.exit()
                if str(labels[confidence]) == "Expelliarmus":
                    pygame.mixer.music.pause()
                    playsound.playsound("__resources/expelliarmus.mp3")
                    engine = gtts.gTTS("You lost control of your wand! It won't work for the next 10 seconds!")
                    a = random.randint(1, 100000)
                    engine.save(f"newfile{a}.mp3")
                    playsound.playsound(f"newfile{a}.mp3")
                    sleep(10)
                    pygame.mixer.music.play()
                if str(labels[confidence]) == "Expecto Patronum":
                    pygame.mixer.music.pause()
                    playsound.playsound("__resources/expecto-patronum.mp3")
                    a = playGame()
                    pygame.mixer.init()
                    pygame.mixer.music.load("__resources/bgm.mp3")
                    pygame.mixer.music.play()
                    if a == True:
                        pygame.mixer.music.pause()
                        engine = gtts.gTTS("Congrats! You almost kissed the cheeks of death!")
                        engine.save(f"newfile{a}.mp3")
                        playsound.playsound(f"newfile{a}.mp3")
                        pygame.mixer.music.play()
                    else:
                        engine = gtts.gTTS("You failed it!")
                        a = random.randint(1, 100000)
                        engine.save(f"newfile{a}.mp3")
                        playsound.playsound(f"newfile{a}.mp3")
                        cv.destroyAllWindows()
                        sys.exit()
                if str(labels[confidence]) == "Silencio":
                    playsound.playsound("__resources/SilencioSonorous.mp3")
                    pygame.mixer.music.pause()
                if str(labels[confidence]) == "Sonorus":
                    # pygame.mixer.init()qqqqqqqqqq
                    # pygame.mixer.music.load("__resources/bgm.mp3")
                    playsound.playsound("__resources/SilencioSonorous.mp3")
                    pygame.mixer.music.play()

            if cv.waitKey(10) & 0xFF == ord('q'):
                cv.destroyAllWindows()
                sys.exit()

    # Start the pattern based wizardry program in a new thread to avoid blocking the main GUI.
    # This demonstrates the use of threading to run concurrent tasks.
    abc = threading.Thread(target=threaded_game_1)
    abc.start()
    pygame.mixer.init()
    pygame.mixer.music.load("__resources/bgm.mp3")
    pygame.mixer.music.play(loops=100)

def invisibility_cloak():
    """
    Activates an invisibility cloak effect using real-time computer vision.
    
    Captures the background from the webcam and then continuously replaces pixels of a specified
    red color (representing the cloak) with the corresponding background pixels. The effect is run
    in a separate thread.
    """
    def threaded_game_2():
        cap = cv.VideoCapture(0)
        time.sleep(3)
        background = 0
        for i in range(30):
            ret, background = cap.read()
        background = np.flip(background, axis=1)

        while cap.isOpened():
            ret, img = cap.read()
            img = np.flip(img, axis=1)
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            value = (35, 35)
            lower_red = np.array([0, 40, 30])
            upper_red = np.array([10, 255, 255])
            mask1 = cv.inRange(hsv, lower_red, upper_red)
            lower_red = np.array([160, 80, 50])
            upper_red = np.array([180, 255, 255])
            mask2 = cv.inRange(hsv, lower_red, upper_red)
            mask = mask1 + mask2
            mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5, 5), np.uint8))
            img[np.where(mask == 255)] = background[np.where(mask == 255)]
            cv.imshow('Enjoy your invisibility cloak!', img)
            k = cv.waitKey(10)
            if k == 27:
                break
            if cv.waitKey(10) & 0xFF == ord('q'):
                break
        cv.destroyAllWindows()

    # Start the invisibility cloak effect in a separate thread.
    abc_2 = threading.Thread(target=threaded_game_2)
    abc_2.start()

def sorting_hat():
    """
    Implements the "Sorting Hat!" quiz game using computer vision.
    
    This function utilizes the webcam to capture user hand movements for a multiple-choice quiz.
    Quiz data is read from a CSV file, and a hand detection module allows users to select answers
    by moving their hand over the choices. Final score is computed and displayed once all questions are answered.
    """
    pathCSV = "C:\\Users\\Gadhedi\\Music\\Crescence of Wizardry\\__resources\\QuizR\\HarryQuiz1.csv"

    cap = cv.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    class mcq():
        """
        Class representing a multiple-choice question.
        
        Attributes:
            question (str): The quiz question.
            choice1 (str): Text for the first answer choice.
            choice2 (str): Text for the second answer choice.
            choice3 (str): Text for the third answer choice.
            choice4 (str): Text for the fourth answer choice.
            answer (int): The correct answer (1-indexed).
            userAns (int): The answer selected by the user.
        """
        def __init__(self, data):
            self.question = data[0]
            self.choice1 = data[1]
            self.choice2 = data[2]
            self.choice3 = data[3]
            self.choice4 = data[4]
            self.answer = int(data[5])
            self.userAns = None
            
        def update(self, cursor, bboxs):
            """
            Checks if the hand cursor is within any answer bounding boxes.
            
            Args:
                cursor (tuple): The (x, y) coordinates of the hand pointer.
                bboxs (list): A list of bounding box coordinates for each answer.
            """
            for x, bbox in enumerate(bboxs):
                x1, y1, x2, y2 = bbox
                if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                    self.userAns = x + 1
                    for mcq_item in mcqlist:
                        if mcq_item.answer == mcq_item.userAns:
                            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv.FILLED)

    with open(pathCSV, newline="\n") as f:
        reader = csv.reader(f)
        dataAll = list(reader)[1:]

    mcqlist = []
    for q in dataAll:
        mcqlist.append(mcq(q))

    qNo = 0
    qTotal = len(dataAll)

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img, draw=True,flipType=True)
        img=cv.flip(img,flipCode=1)
        if qNo < qTotal:
            mcq_item = mcqlist[qNo]
            img, bbox = cvzone.putTextRect(img, mcq_item.question, [100, 100], 2, 2, offset=30, border=3)
            img, bbox1 = cvzone.putTextRect(img, mcq_item.choice1, [100, 255], 2, 2, offset=30, border=3)
            img, bbox2 = cvzone.putTextRect(img, mcq_item.choice2, [600, 255], 2, 2, offset=30, border=3)
            img, bbox3 = cvzone.putTextRect(img, mcq_item.choice3, [100, 375], 2, 2, offset=30, border=3)
            img, bbox4 = cvzone.putTextRect(img, mcq_item.choice4, [600, 375], 2, 2, offset=30, border=3)
        
            if hands:
                lmList = hands[0]['lmList']
                cursor = lmList[8]
                length, info, x = detector.findDistance(cursor, lmList[12])
                if length < 50:
                    mcq_item.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                    if mcq_item.userAns is not None:
                        time.sleep(0.5)
                        qNo += 1
        else:
            score = 0
            for mcq_item in mcqlist:
                if mcq_item.answer == mcq_item.userAns:
                    score += 1
            score = round((score / qTotal) * 100, 2)
            img, _ = cvzone.putTextRect(img, 'Quiz Completed!', [250, 300], 2, 2, offset=16)
            img, _ = cvzone.putTextRect(img, f'Your score is {score}%', [200, 350], 2, 2, offset=16)

        barValue = 150 + (950 // qTotal) * qNo
        cv.rectangle(img, (150, 600 - 100), (barValue, 650 - 100), (0, 255, 0), cv.FILLED)
        cv.rectangle(img, (150, 600 - 100), (1100, 650 - 100), (0, 255, 0), 5)
        img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635 - 100], 2, 2, offset=16)
        
        
        cv.imshow("Sorting Hat!", img)

        if cv.waitKey(20) == ord('q'):
            cv.destroyAllWindows()
            break

# =============================================================================
# MAIN APPLICATION WINDOW SETUP
# =============================================================================

window = CTk()
window.title("Crescence of Wizardry! - Muggles feel Magic!")
winhh_x = (1366 - 1100) // 2
winhh_y = (768 - 658) // 2
window.geometry(f"808x458+{winhh_x}+{winhh_y}")

a = CTkInputDialog(title="What's your Muggle Name!?", text="What's your name?", font=("chelsea market", 15, "bold"))
name = str(a.get_input())

try:
    while True:
        if len(name) > 20:
            messagebox.showinfo("Ouch! Error!", "The length of your name mustn't be more than 20...\nTry keeping it concise in the next prompt...")
            a = CTkInputDialog(title="Your Sweet Name", text="What's your name?", font=("", 25, "bold"))
            name = str(a.get_input())
        else:
            break
    if name == "None" or name == "":
        name = "Boss"
except:
    name = "Boss"

_say(f"experience the Crescence of Wizardry!")

a = os.path.dirname(os.path.realpath(__file__))
b = CTkImage(Image.open(a + "/__resources/yes.png"), size=(60, 60))
head_frame = CTkFrame(window, height=75, width=800)
head_label = CTkLabel(head_frame, text=f"Be a Wizard, Sorcerer {name}! ", image=b, justify=CENTER, font=("chelsea market", 50, "bold"), compound="right")
head_frame.grid(row=0, columnspan=2)

g = CTkImage(Image.open(a + "/__resources/review.png"), size=(45, 45))
l = CTkImage(Image.open(a + "/__resources/invisible-man.png"), size=(45, 45))
d = CTkImage(Image.open(a + "/__resources/magic-wand.png"), size=(45, 45))
d = CTkImage(Image.open(a + "/__resources/magic.png"), size=(45, 45))
k = CTkImage(Image.open(a + "/__resources/download.png"), size=(310, 310))

draw_button = CTkButton(window, text="Wizardry", command=lambda: wizardry_m(), anchor=CENTER,
                        font=("chelsea market", 30, "bold"), width=300, image=d, compound="right", corner_radius=700, border_width=7)
draw_button.grid(row=1, column=0, pady=4, padx=4)

invisibility_button = CTkButton(window, text="Invisibility Cloak", command=lambda: invisibility_cloak(), anchor=CENTER,
                                font=("chelsea market", 30, "bold"), width=300, image=l, compound="right", corner_radius=700, border_width=7)
invisibility_button.grid(row=2, column=0, pady=4, padx=4)

normie_button = CTkButton(window, text="sorting_hat!", command=lambda: sorting_hat(), anchor=CENTER,
                          font=("chelsea market", 30, "bold"), width=300, image=g, compound="right", corner_radius=700, border_width=7)
normie_button.grid(row=3, column=0, pady=4, padx=4)

sort_button = CTkButton(window, text="Sorting Hat!", command=lambda: sorting_hat(), anchor=CENTER,
                        font=("chelsea market", 30, "bold"), width=300, image=g, compound="right", corner_radius=700, border_width=7)
sort_button.grid(row=3, column=0, pady=4, padx=4)

k_button = CTkLabel(window, text="", anchor=CENTER, font=("chelsea market", 30, "bold"), width=300, image=k, compound="right", corner_radius=700)
k_button.grid(row=1, rowspan=3, column=1, pady=4, padx=4)

show_splash_screen()
window.wait_window(splash)
execution()
move_label(head_label)

window.mainloop()
