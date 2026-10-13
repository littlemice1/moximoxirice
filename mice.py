import pygame
import sys
import time
import pickle
from queue import Queue

# 初始化 Pygame
pygame.init()

# 常量定义
CELL_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
BORDER_SIZE = 20
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE + BORDER_SIZE * 2
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE + BORDER_SIZE * 2 + 80
TIME_LIMIT = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
GOLD = (255, 191, 0)
ORANGE = (255, 140, 0)
PURPLE = (168, 85, 253)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("迷宫游戏：挑战版")

LEVELS = [
    {
        "maze": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
            [1,0,1,0,1,0,1,1,1,0,1,1,1,0,1],
            [1,0,1,0,1,0,0,0,1,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,0,1,1,1,1,1,0,1],
            [1,1,1,1,1,0,0,0,0,0,0,0,1,0,1],
            [1,0,0,0,1,0,1,1,1,1,1,0,1,0,1],
            [1,0,1,0,1,0,1,0,0,0,1,0,1,0,1],
            [1,0,1,0,0,0,1,0,1,0,1,0,1,0,1],
            [1,0,1,1,1,1,1,0,1,0,0,0,1,0,1],
            [1,0,0,0,0,0,0,0,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,1,1,1,1,1,1,1,0,1],
            [1,0,1,1,1,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ],
        "start": [7, 7],
        "goal": [13, 13],
        "collectibles": [[1, 1], [5, 12], [9, 2], [12, 5]],
    },
    {
        "maze": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
            [1,0,1,0,1,0,1,1,1,1,1,0,1,0,1],
            [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
            [1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
            [1,1,1,1,1,0,1,1,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
            [1,0,1,0,1,1,1,1,1,0,1,0,0,0,1],
            [1,0,1,0,0,0,0,0,1,0,1,1,1,1,1],
            [1,0,1,1,1,1,1,0,1,0,0,0,1,0,1],
            [1,0,0,0,0,0,1,0,1,1,1,0,1,0,1],
            [1,1,1,1,1,0,1,0,0,0,1,0,1,0,1],
            [1,0,0,0,0,0,1,1,1,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ],
        "start": [1, 1],
        "goal": [13, 13],
        "collectibles": [[1, 12], [5, 3], [11, 11], [9, 7]],
    },
    {
        "maze": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,1,1,0,1,1,1,0,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ],
        "start": [1, 1],
        "goal": [13, 13],
        "collectibles": [[1, 13], [5, 1], [9, 12], [12, 2]],
    },
]


class MazeGame:
    def __init__(self):
        self.levels = LEVELS
        self.level_index = 0
        self.score = 0
        self.game_started = False
        self.game_over = False
        self.success = False
        self.editing = False
        self.edit_start_time = 0
        self.start_time = time.time()
        self.pause_time = 0
        self.show_path = False
        self.shortest_path = []
        self.all_paths = []
        self.status_message = ""
        self.collectibles = []
        self.reset_game()

    def reset_game(self):
        self.level_index = 0
        self.score = 0
        self.load_level(0)

    def load_level(self, index, reset_timer=True):
        if index < 0:
            index = 0
        if index >= len(self.levels):
            index = len(self.levels) - 1
        level = self.levels[index]
        self.level_index = index
        self.maze = [row[:] for row in level["maze"]]
        self.mouse_pos = list(level["start"])
        self.goal_pos = list(level["goal"])
        self.collectibles = []
        for pos in level["collectibles"]:
            if self.maze[pos[0]][pos[1]] == 0:
                self.collectibles.append([pos[0], pos[1]])
        self.start_time = time.time() if reset_timer else self.start_time
        self.game_over = False
        self.success = False
        self.editing = False
        self.pause_time = 0
        self.show_path = False
        self.shortest_path = []
        self.all_paths = []
        self.status_message = f"第 {self.level_index + 1} 关" if self.game_started else ""
        self.find_shortest_path()

    def draw_cheese(self, x, y):
        pixel_size = CELL_SIZE // 8
        cheese_color = (255, 191, 0)
        highlight_color = (255, 223, 128)
        shadow_color = (255, 140, 0)
        cheese_pixels = [
            (2,1), (3,1), (4,1), (5,1),
            (1,2), (2,2), (3,2), (4,2), (5,2), (6,2),
            (1,3), (2,3), (3,3), (4,3), (5,3), (6,3),
            (1,4), (2,4), (3,4), (4,4), (5,4), (6,4),
            (2,5), (3,5), (4,5), (5,5)
        ]
        holes_pixels = [(2,2), (5,2), (3,4), (5,3), (4,5)]
        highlight_pixels = [(2,1), (3,1), (1,2), (2,3)]
        for px, py in cheese_pixels:
            pygame.draw.rect(screen, cheese_color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
        for px, py in holes_pixels:
            pygame.draw.rect(screen, shadow_color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
        for px, py in highlight_pixels:
            pygame.draw.rect(screen, highlight_color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))

    def draw_coin(self, x, y):
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        radius = CELL_SIZE // 4
        pygame.draw.circle(screen, GOLD, (center_x, center_y), radius)
        pygame.draw.circle(screen, (255, 223, 128), (center_x - 4, center_y - 4), radius // 3)
        pygame.draw.circle(screen, ORANGE, (center_x, center_y), radius, 2)

    def draw_mouse(self, offset=0):
        x = self.mouse_pos[1] * CELL_SIZE + offset
        y = self.mouse_pos[0] * CELL_SIZE + offset
        pixel_size = CELL_SIZE // 10
        mouse_pixels = [
            (4,2), (5,2), (6,2), (3,3), (4,3), (5,3), (6,3), (7,3),
            (2,4), (3,4), (4,4), (5,4), (6,4), (7,4),
            (2,5), (3,5), (4,5), (5,5), (6,5), (7,5),
            (3,6), (4,6), (5,6), (6,6), (7,6),
            (4,7), (5,7), (6,7), (7,7), (8,7)
        ]
        outline_pixels = [(3,2), (7,2), (2,3), (8,3), (1,4), (8,4), (1,5), (8,5), (2,6), (8,6), (3,7), (9,7)]
        pink_pixels = [(4,3), (6,3), (5,4)]
        white_pixels = [(4,4), (6,4)]
        black_pixels = [(4,4), (6,4)]
        for px, py in outline_pixels:
            pygame.draw.rect(screen, (120, 120, 120), (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
        for px, py in mouse_pixels:
            pygame.draw.rect(screen, (180, 180, 180), (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
        for px, py in pink_pixels:
            pygame.draw.rect(screen, (255, 192, 203), (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
        for px, py in white_pixels:
            pygame.draw.rect(screen, WHITE, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
        for px, py in black_pixels:
            pygame.draw.rect(screen, BLACK, (x + (px + 0.3) * pixel_size, y + py * pixel_size, pixel_size // 2, pixel_size // 2))

    def draw_paths(self):
        if not self.show_path:
            return
        for path in self.all_paths:
            for i in range(len(path) - 1):
                x1 = path[i][1] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                y1 = path[i][0] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                x2 = path[i + 1][1] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                y2 = path[i + 1][0] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), 2)
        if self.shortest_path:
            for i in range(len(self.shortest_path) - 1):
                x1 = self.shortest_path[i][1] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                y1 = self.shortest_path[i][0] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                x2 = self.shortest_path[i + 1][1] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                y2 = self.shortest_path[i + 1][0] * CELL_SIZE + BORDER_SIZE + CELL_SIZE // 2
                pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 3)

    def draw(self):
        screen.fill(BLACK)
        if not self.game_started:
            big_font = pygame.font.SysFont('SimHei', 72)
            title_text = big_font.render("迷宫游戏", True, GREEN)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 110))
            small_font = pygame.font.SysFont('SimHei', 36)
            start_text = small_font.render("按空格键开始游戏", True, WHITE)
            screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            help_font = pygame.font.SysFont('SimHei', 24)
            controls = [
                "方向键: 移动老鼠",
                "E键: 进入/退出编辑模式",
                "S键: 保存迷宫",
                "L键: 加载迷宫",
                "P键: 显示/隐藏路径",
                "A键: 重新开始",
                "Q键: 退出游戏"
            ]
            for i, text in enumerate(controls):
                help_text = help_font.render(text, True, WHITE)
                screen.blit(help_text, (BORDER_SIZE, SCREEN_HEIGHT // 2 + 60 + i * 30))
            return

        pygame.draw.rect(screen, WHITE, (BORDER_SIZE, BORDER_SIZE, MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE))
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if self.maze[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * CELL_SIZE + BORDER_SIZE, y * CELL_SIZE + BORDER_SIZE, CELL_SIZE, CELL_SIZE))

        self.draw_paths()

        for coin in self.collectibles:
            if coin == self.mouse_pos:
                continue
            coin_x = coin[1] * CELL_SIZE + BORDER_SIZE
            coin_y = coin[0] * CELL_SIZE + BORDER_SIZE
            self.draw_coin(coin_x, coin_y)

        cheese_x = self.goal_pos[1] * CELL_SIZE + BORDER_SIZE
        cheese_y = self.goal_pos[0] * CELL_SIZE + BORDER_SIZE
        self.draw_cheese(cheese_x, cheese_y)
        self.draw_mouse(BORDER_SIZE)
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), BORDER_SIZE)

        font = pygame.font.SysFont('SimHei', 22)
        status_line = font.render(f"关卡 {self.level_index + 1}/{len(self.levels)}  分数: {self.score}  奶酪: {len(self.collectibles)}", True, WHITE)
        screen.blit(status_line, (BORDER_SIZE, SCREEN_HEIGHT - 55))

        if not self.game_over:
            remaining = max(0, TIME_LIMIT - (time.time() - self.start_time - self.pause_time))
        else:
            remaining = 0
        time_text = font.render(f"时间: {int(remaining)}秒", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 55))

        if not self.game_over and not self.editing:
            help_text = font.render("方向键移动 | E:编辑 | S:保存 | L:加载 | P:路径", True, WHITE)
            screen.blit(help_text, (BORDER_SIZE, SCREEN_HEIGHT - 80))

        if self.editing:
            edit_text = font.render("编辑模式: 点击切换墙/路 (按E退出)", True, RED)
            screen.blit(edit_text, (SCREEN_WIDTH // 2 - 150, BORDER_SIZE // 2))

        if self.status_message:
            msg_font = pygame.font.SysFont('SimHei', 26)
            msg_text = msg_font.render(self.status_message, True, YELLOW)
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - 100, BORDER_SIZE + 5))

        if self.game_over:
            big_font = pygame.font.SysFont('SimHei', 72)
            small_font = pygame.font.SysFont('SimHei', 24)
            if self.success:
                result_text = big_font.render("VICTORY!", True, GREEN)
                shadow_text = big_font.render("VICTORY!", True, (255, 255, 100))
                screen.blit(shadow_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 120))
                screen.blit(result_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 115))
                restart_text = small_font.render("按 A 键再来一局 按 Q 键退出游戏", True, WHITE)
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 50))
            else:
                result_text = big_font.render("GAME OVER", True, RED)
                shadow_text = big_font.render("GAME OVER", True, (139, 0, 0))
                screen.blit(shadow_text, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT - 120))
                screen.blit(result_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 115))

    def move(self, dx, dy):
        if self.game_over or self.editing:
            return
        new_x = self.mouse_pos[0] + dx
        new_y = self.mouse_pos[1] + dy
        if 0 <= new_x < MAZE_HEIGHT and 0 <= new_y < MAZE_WIDTH and self.maze[new_x][new_y] == 0:
            self.mouse_pos = [new_x, new_y]

        for coin in self.collectibles[:]:
            if self.mouse_pos == coin:
                self.collectibles.remove(coin)
                self.score += 25
                self.pause_time -= 5
                self.status_message = "收集到宝藏 +25"
                break

        if self.mouse_pos == self.goal_pos:
            self.score += 100
            if self.level_index < len(self.levels) - 1:
                self.status_message = f"第 {self.level_index + 1} 关通过！"
                self.level_index += 1
                self.load_level(self.level_index, reset_timer=True)
            else:
                self.game_over = True
                self.success = True
                self.status_message = "全部关卡完成!"

    def edit_maze(self, pos):
        if not self.editing:
            return
        x = (pos[0] - BORDER_SIZE) // CELL_SIZE
        y = (pos[1] - BORDER_SIZE) // CELL_SIZE
        if 0 <= x < MAZE_WIDTH and 0 <= y < MAZE_HEIGHT and [y, x] != self.mouse_pos and [y, x] != self.goal_pos:
            self.maze[y][x] = 1 - self.maze[y][x]

    def find_all_paths(self):
        def dfs(x, y, path):
            if [x, y] == self.goal_pos:
                self.all_paths.append(path[:])
                return
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < MAZE_HEIGHT and 0 <= new_y < MAZE_WIDTH and self.maze[new_x][new_y] == 0 and (new_x, new_y) not in path:
                    path.append((new_x, new_y))
                    dfs(new_x, new_y, path)
                    path.pop()
        self.all_paths = []
        dfs(self.mouse_pos[0], self.mouse_pos[1], [(self.mouse_pos[0], self.mouse_pos[1])])
        return self.all_paths

    def find_shortest_path(self):
        queue = Queue()
        queue.put((self.mouse_pos[0], self.mouse_pos[1]))
        visited = {(self.mouse_pos[0], self.mouse_pos[1]): None}
        while not queue.empty():
            x, y = queue.get()
            if [x, y] == self.goal_pos:
                break
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < MAZE_HEIGHT and 0 <= new_y < MAZE_WIDTH and self.maze[new_x][new_y] == 0 and (new_x, new_y) not in visited:
                    queue.put((new_x, new_y))
                    visited[(new_x, new_y)] = (x, y)
        if (self.goal_pos[0], self.goal_pos[1]) not in visited:
            self.shortest_path = []
            return []
        path = []
        current = (self.goal_pos[0], self.goal_pos[1])
        while current is not None:
            path.append(current)
            current = visited[current]
        self.shortest_path = path[::-1]
        return self.shortest_path

    def save_maze(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump({
                    'maze': self.maze,
                    'mouse_pos': self.mouse_pos,
                    'goal_pos': self.goal_pos,
                    'level_index': self.level_index,
                    'score': self.score,
                    'collectibles': self.collectibles,
                }, f)
            print(f"迷宫已保存到 {filename}")
        except Exception as e:
            print(f"保存失败: {e}")

    def load_maze(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.maze = data.get('maze', self.maze)
                self.mouse_pos = data.get('mouse_pos', self.mouse_pos)
                self.goal_pos = data.get('goal_pos', self.goal_pos)
                self.level_index = data.get('level_index', self.level_index)
                self.score = data.get('score', self.score)
                self.collectibles = data.get('collectibles', self.collectibles)
                self.start_time = time.time()
                self.game_over = False
                self.success = False
                self.pause_time = 0
                self.show_path = False
            print(f"迷宫已从 {filename} 加载")
        except Exception as e:
            print(f"加载失败: {e}")

    def handle_event(self, event):
        """处理单个 Pygame 事件，返回 "quit" 表示请求退出游戏。"""
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:
            if not self.game_started:
                if event.key == pygame.K_SPACE:
                    self.game_started = True
                    self.start_time = time.time()
                return None

            if self.game_over:
                if event.key == pygame.K_a:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    return "quit"
                return None

            if not self.editing:
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self.move(1, 0)
                elif event.key == pygame.K_LEFT:
                    self.move(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                elif event.key == pygame.K_e:
                    self.editing = True
                    self.edit_start_time = time.time()
                elif event.key == pygame.K_s:
                    self.save_maze("maze.dat")
                elif event.key == pygame.K_l:
                    self.load_maze("maze.dat")
                elif event.key == pygame.K_p:
                    self.show_path = not self.show_path
                    if self.show_path:
                        self.find_all_paths()
                        self.find_shortest_path()
                elif event.key == pygame.K_a:
                    self.reset_game()
            elif event.key == pygame.K_e:
                self.editing = False
                edit_duration = time.time() - self.edit_start_time
                self.pause_time += edit_duration
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and self.editing and self.game_started:
            self.edit_maze(event.pos)
        return None

    def check_timeout(self):
        if self.game_started and not self.game_over and not self.editing:
            elapsed = time.time() - self.start_time - self.pause_time
            if elapsed > TIME_LIMIT:
                self.game_over = True
                self.success = False
                self.status_message = "时间到！"


def main():
    game = MazeGame()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if game.handle_event(event) == "quit":
                pygame.quit()
                sys.exit()

        game.check_timeout()
        game.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
