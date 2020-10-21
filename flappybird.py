import pygame,sys,random,json

pygame.init()

filename='/'.join(i for i in sys.argv[0].split('\\')[:-1])+'/'

print(filename)
screen=pygame.display.set_mode((288,512))
clock=pygame.time.Clock()

"""game variable"""
gravity=0.25
bird_move=0

"""image sizing"""
bg_surface=pygame.image.load(f'{filename}sprites/background.png').convert()
# print(bg_surface.get_height())
# print(bg_surface.get_width())
# bg_surface=pygame.transform.scale2x(bg_surface)
floor_surface=pygame.image.load(f'{filename}sprites/base.png').convert()
floor_x_pos=0

"""bird"""
bird_surface=pygame.image.load(f'{filename}sprites/bird.png').convert_alpha()
bird_pos_x=50
bird_pos_y=200
bird_rect=bird_surface.get_rect(midtop=(50,200))

"""pipe"""
pipe_surface=pygame.image.load(f'{filename}sprites/pipe.png')
pipe_list=[]
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height=[400,300,200]

"""score"""
score=0
text=pygame.font.Font('freesansbold.ttf',20)

"""game_function"""
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,512-65))
    screen.blit(floor_surface,(floor_x_pos+288,512-65))
    
def create_pipe():
    random_pipe=random.choice(pipe_height)
    bottom=pipe_surface.get_rect(midtop=(288,random_pipe))
    top=pipe_surface.get_rect(midbottom=(288,random_pipe-400))
    return bottom,top
   
def move_pipes(pipes):
    global score,pipe_list
    for pipe in pipes:
        pipe.centerx-=5
            
        # if bird_rect.centerx<pipe.centerx+32 and bird_rect.x>pipe.x-32:
        #     score+=1
        if pipe.centerx<0 and pipe.centerx>-3:
            score+=1
            pipe_list.remove(pipe_list[pipe_list.index(pipe)])
            
    return pipes

def draw_pipes(pipes): 
    for pipe in pipes:
        if pipe.bottom>=512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global running
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound=pygame.mixer.Sound(f'{filename}die.wav')
            die_sound.play()
            running=False
    
    if bird_rect.top<-100 or bird_rect.bottom>=512-64:
        die_sound=pygame.mixer.Sound(f'{filename}die.wav')
        die_sound.play()
        running=False
            
        
def rotated_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_move*5,1)
    return new_bird

def show_score():
    scoreing=text.render(f'{int(score/2)}',True,(0,0,0))
    screen.blit(scoreing,(100,100))
    
def game_over():
    high_score()
    filename='ss.json'
    
    with open(filename) as fob:
        highest=json.load(fob)['h']
        
    game_over_text=text.render(f'Highest score {highest}',True,(0,0,255))
    screen.blit(game_over_text,(0,100))

def high_score():
    filename='ss.json'
    dict1={'h':0}
    try:
        with open(filename) as fob:
            high_score=json.load(fob)['h']
        if score>high_score:
            dict1['h']=int(score/2)
            with open(filename,'w') as fob:
                json.dump(dict1,fob)
    except:
        with open(filename,'w') as fob:
            json.dump(dict1,fob)

running=True
while True:
    pygame.display.update()
    screen.blit(bg_surface,(0,0))
    draw_floor()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
            
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                bird_move=0
                bird_move-=8
                wing=pygame.mixer.Sound(f'{filename}wing.wav')
                wing.play()
                
        if event.type==pygame.MOUSEBUTTONDOWN:
            if not running:
                pipe_list=[]
                running=True
                bird_rect.y=20
                bird_move=0
                
        if event.type==SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
    if running:
        """background"""
        floor_x_pos-=1
        
        
        """bird_movement"""
        bird_move+=gravity
        sd_bird=rotated_bird(bird_surface)
        bird_rect.y+=bird_move
        screen.blit(sd_bird,bird_rect)

        """pipe"""
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)

        """floor movement"""
        if floor_x_pos<-288:
            floor_x_pos=0
            
        """show score"""
        show_score()
        check_collision(pipe_list)
    
    if not running:
        game_over()
    
    clock.tick(60)
