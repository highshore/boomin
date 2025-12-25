import pygame

# 1. 초기화 (Initialize)
pygame.init()

# 2. 설정 변수 (Constants)
WIDTH, HEIGHT = 800, 800
BOARD_PADDING = 100

# 색상 정의 (Colors)
WOOD_COLOR = (222, 184, 135)   # 나무 색깔
BG_COLOR = (30, 30, 30)        # 배경 색깔 (진한 회색)
GRID_COLOR = (40, 40, 40)      # 격자 무늬 색깔
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 화면 설정 (Screen Setup)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("알까기 게임 (Simple Alkagi)") # 창 제목
clock = pygame.time.Clock()

# 바둑판 영역 정의 (Board Rect)
BOARD_RECT = pygame.Rect(
    BOARD_PADDING, 
    BOARD_PADDING, 
    WIDTH - 2 * BOARD_PADDING, 
    HEIGHT - 2 * BOARD_PADDING
)

# 3. 클래스 정의 (Class Stone)
class Stone:
    def __init__(self, x, y, color):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.color = color
        self.radius = 22

    def move(self):
        # 위치 업데이트
        self.pos += self.vel
        # 마찰력 적용 (점점 느려지게)
        self.vel *= 0.96 
        if self.vel.length() < 0.1: 
            self.vel *= 0

    def draw(self):
        # 돌 그리기 (좌표는 정수형이어야 함)
        draw_pos = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, self.color, draw_pos, self.radius)
        # 돌 테두리 그리기
        pygame.draw.circle(screen, BLACK, draw_pos, self.radius, 1)

# 4. 돌 생성 (Setup Stones)
stones = []
for i in range(5):
    spacing = BOARD_RECT.width / 6
    x = BOARD_RECT.left + spacing * (i + 1)
    # 위쪽 검은돌, 아래쪽 흰돌 배치
    stones.append(Stone(x, BOARD_RECT.top + 80, BLACK))
    stones.append(Stone(x, BOARD_RECT.bottom - 80, WHITE))

# 5. 게임 루프 (Game Loop)
running = True
while running:
    # A. 이벤트 처리 (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # B. 데이터 업데이트 (Update)
    for s in stones:
        s.move()

    # C. 화면 그리기 (Draw) - 순서가 중요합니다! (배경 -> 판 -> 돌)
    
    # 1. 배경 색상 채우기
    screen.fill(BG_COLOR)

    # 2. 나무판 그리기
    pygame.draw.rect(screen, WOOD_COLOR, BOARD_RECT)
    pygame.draw.rect(screen, (100, 70, 30), BOARD_RECT, 5) # 나무판 테두리

    # 3. 줄 긋기 (Grid)
    for i in range(1, 13):
        gap = BOARD_RECT.width / 13
        
        # 세로줄 |
        x_pos = BOARD_RECT.left + (gap * i)
        pygame.draw.line(screen, GRID_COLOR, (x_pos, BOARD_RECT.top), (x_pos, BOARD_RECT.bottom), 2)
        
        # 가로줄 ㅡ
        y_pos = BOARD_RECT.top + (gap * i)
        pygame.draw.line(screen, GRID_COLOR, (BOARD_RECT.left, y_pos), (BOARD_RECT.right, y_pos), 2)

    # 4. 돌 그리기 (Draw Stones) - 반드시 flip() 전에 그려야 합니다.
    for s in stones: 
        s.draw()

    # D. 화면 업데이트 (Display Flip)
    pygame.display.flip()
    
    # 프레임 속도 조절
    clock.tick(60)

pygame.quit()