import tkinter as tk
from tkinter import messagebox
import threading
import time

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
BG_DARK       = "#0D1117"   # nền chính
BG_PANEL      = "#161B22"   # panel bên
BG_BOARD      = "#0D1117"   # nền bàn cờ
CELL_NORMAL   = "#1C2333"   # ô bình thường
CELL_HOVER    = "#243044"   # ô khi hover
GRID_LINE     = "#2D3748"   # đường lưới
X_COLOR       = "#38BDF8"   # xanh nước (X)
X_GLOW        = "#0EA5E9"
O_COLOR       = "#F87171"   # đỏ nhạt (O)
O_GLOW        = "#EF4444"
WIN_HIGHLIGHT = "#FFD700"   # vàng cho ô thắng
TEXT_PRIMARY  = "#E2E8F0"
TEXT_MUTED    = "#64748B"
TEXT_X        = X_COLOR
TEXT_O        = O_COLOR
ACCENT        = "#7C3AED"
BTN_BG        = "#1E293B"
BTN_HOVER     = "#334155"
BTN_BORDER    = "#334155"

CELL_SIZE  = 54
PADDING    = 20
FONT_TITLE = ("Courier New", 20, "bold")
FONT_CELL  = ("Courier New", 22, "bold")
FONT_INFO  = ("Courier New", 11)
FONT_BTN   = ("Courier New", 10, "bold")
FONT_LABEL = ("Courier New", 10)
FONT_SCORE = ("Courier New", 24, "bold")


class CaroGUI:
    def __init__(self, game_factory, ai_agent, board_size=9):
        """
        game_factory: callable() → Game_Caro instance
        ai_agent    : agent instance (has .get_best_move(game))
        board_size  : kích thước bàn cờ
        """
        self.game_factory = game_factory
        self.ai           = ai_agent
        self.size         = board_size
        self.game         = game_factory()
        self.human_player = 'X'
        self.ai_player    = 'O'
        self.ai_thinking  = False
        self.game_over    = False
        self.scores       = {'X': 0, 'O': 0, 'Draw': 0}
        self.last_move    = None
        self.win_cells    = []
        self._hover_cell  = None

        self.root = tk.Tk()
        self.root.title("CARO — Dark Edition")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self._build_ui()
        self._draw_board()
        self.root.mainloop()

    # ──────────────────────────────────────────────────────── BUILD UI ──────
    def _build_ui(self):
        # ── Header
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill='x', padx=24, pady=(18, 0))

        tk.Label(header, text="⬡  CARO", font=FONT_TITLE,
                 bg=BG_DARK, fg=TEXT_PRIMARY).pack(side='left')
        tk.Label(header, text="DARK EDITION", font=("Courier New", 8, "bold"),
                 bg=BG_DARK, fg=TEXT_MUTED).pack(side='left', padx=(8, 0), pady=(8, 0))

        # ── Main layout
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(padx=20, pady=12)

        # Left panel
        self.left = tk.Frame(body, bg=BG_PANEL, width=160,
                             highlightbackground=GRID_LINE, highlightthickness=1)
        self.left.pack(side='left', fill='y', padx=(0, 14))
        self.left.pack_propagate(False)
        self._build_left_panel()

        # Canvas
        canvas_size = self.size * CELL_SIZE + PADDING * 2
        self.canvas = tk.Canvas(body, width=canvas_size, height=canvas_size,
                                bg=BG_BOARD, highlightthickness=0)
        self.canvas.pack(side='left')
        self.canvas.bind("<Motion>",          self._on_hover)
        self.canvas.bind("<Button-1>",        self._on_click)
        self.canvas.bind("<Leave>",           self._on_leave)

        # Right panel
        self.right = tk.Frame(body, bg=BG_PANEL, width=160,
                              highlightbackground=GRID_LINE, highlightthickness=1)
        self.right.pack(side='left', fill='y', padx=(14, 0))
        self.right.pack_propagate(False)
        self._build_right_panel()

        # ── Status bar
        self.status_var = tk.StringVar(value="Your turn  ›  X")
        status_bar = tk.Frame(self.root, bg=BG_PANEL,
                              highlightbackground=GRID_LINE, highlightthickness=1)
        status_bar.pack(fill='x', padx=20, pady=(0, 16))
        tk.Label(status_bar, textvariable=self.status_var,
                 font=FONT_INFO, bg=BG_PANEL, fg=TEXT_PRIMARY,
                 anchor='w', padx=14, pady=8).pack(side='left')
        self.thinking_var = tk.StringVar(value="")
        tk.Label(status_bar, textvariable=self.thinking_var,
                 font=FONT_INFO, bg=BG_PANEL, fg=TEXT_MUTED,
                 anchor='e', padx=14).pack(side='right')

    def _build_left_panel(self):
        pad = dict(bg=BG_PANEL)
        tk.Label(self.left, text="SCORE", font=("Courier New", 8, "bold"),
                 fg=TEXT_MUTED, **pad).pack(pady=(18, 4))

        # X score
        xf = tk.Frame(self.left, **pad)
        xf.pack(fill='x', padx=14, pady=4)
        tk.Label(xf, text="X", font=("Courier New", 13, "bold"),
                 fg=X_COLOR, **pad).pack(side='left')
        tk.Label(xf, text="YOU", font=("Courier New", 7),
                 fg=TEXT_MUTED, **pad).pack(side='left', padx=4, pady=2)
        self.score_x = tk.Label(xf, text="0", font=FONT_SCORE,
                                fg=X_COLOR, **pad)
        self.score_x.pack(side='right')

        tk.Frame(self.left, bg=GRID_LINE, height=1).pack(fill='x', padx=14, pady=2)

        # O score
        of = tk.Frame(self.left, **pad)
        of.pack(fill='x', padx=14, pady=4)
        tk.Label(of, text="O", font=("Courier New", 13, "bold"),
                 fg=O_COLOR, **pad).pack(side='left')
        tk.Label(of, text="AI", font=("Courier New", 7),
                 fg=TEXT_MUTED, **pad).pack(side='left', padx=4, pady=2)
        self.score_o = tk.Label(of, text="0", font=FONT_SCORE,
                                fg=O_COLOR, **pad)
        self.score_o.pack(side='right')

        tk.Frame(self.left, bg=GRID_LINE, height=1).pack(fill='x', padx=14, pady=2)

        # Draw score
        df = tk.Frame(self.left, **pad)
        df.pack(fill='x', padx=14, pady=4)
        tk.Label(df, text="—", font=("Courier New", 11),
                 fg=TEXT_MUTED, **pad).pack(side='left')
        tk.Label(df, text="DRAW", font=("Courier New", 7),
                 fg=TEXT_MUTED, **pad).pack(side='left', padx=4)
        self.score_d = tk.Label(df, text="0", font=("Courier New", 18, "bold"),
                                fg=TEXT_MUTED, **pad)
        self.score_d.pack(side='right')

        # ── Side picker
        tk.Frame(self.left, bg=GRID_LINE, height=1).pack(fill='x', padx=14, pady=(16, 4))
        tk.Label(self.left, text="PLAY AS", font=("Courier New", 8, "bold"),
                 fg=TEXT_MUTED, **pad).pack(pady=(4, 6))
        sf = tk.Frame(self.left, **pad)
        sf.pack()
        self._side_btns = {}
        for sym, col in [('X', X_COLOR), ('O', O_COLOR)]:
            b = tk.Button(sf, text=sym, font=("Courier New", 11, "bold"),
                          bg=CELL_NORMAL, fg=col, width=3, relief='flat',
                          activebackground=CELL_HOVER, activeforeground=col,
                          cursor='hand2',
                          command=lambda s=sym: self._pick_side(s))
            b.pack(side='left', padx=4)
            self._side_btns[sym] = b
        self._highlight_side_btn('X')

    def _build_right_panel(self):
        pad = dict(bg=BG_PANEL)
        tk.Label(self.right, text="INFO", font=("Courier New", 8, "bold"),
                 fg=TEXT_MUTED, **pad).pack(pady=(18, 8))

        tk.Label(self.right, text="NODES", font=FONT_LABEL,
                 fg=TEXT_MUTED, **pad).pack(anchor='w', padx=14)
        self.nodes_var = tk.StringVar(value="—")
        tk.Label(self.right, textvariable=self.nodes_var,
                 font=("Courier New", 12, "bold"), fg=TEXT_PRIMARY, **pad).pack(anchor='w', padx=14)

        tk.Frame(self.right, bg=GRID_LINE, height=1).pack(fill='x', padx=14, pady=8)

        tk.Label(self.right, text="TIME (s)", font=FONT_LABEL,
                 fg=TEXT_MUTED, **pad).pack(anchor='w', padx=14)
        self.time_var = tk.StringVar(value="—")
        tk.Label(self.right, textvariable=self.time_var,
                 font=("Courier New", 12, "bold"), fg=TEXT_PRIMARY, **pad).pack(anchor='w', padx=14)

        tk.Frame(self.right, bg=GRID_LINE, height=1).pack(fill='x', padx=14, pady=8)

        tk.Label(self.right, text="DEPTH", font=FONT_LABEL,
                 fg=TEXT_MUTED, **pad).pack(anchor='w', padx=14)
        tk.Label(self.right, text=str(self.ai.depth),
                 font=("Courier New", 12, "bold"), fg=ACCENT, **pad).pack(anchor='w', padx=14)

        tk.Frame(self.right, bg=GRID_LINE, height=1).pack(fill='x', padx=14, pady=(8, 16))

        # Buttons
        for txt, cmd in [("NEW GAME", self._new_game), ("UNDO", self._undo)]:
            b = tk.Button(self.right, text=txt, font=FONT_BTN,
                          bg=BTN_BG, fg=TEXT_PRIMARY, relief='flat',
                          activebackground=BTN_HOVER, activeforeground=TEXT_PRIMARY,
                          cursor='hand2', width=13, pady=7,
                          highlightbackground=BTN_BORDER, highlightthickness=1,
                          command=cmd)
            b.pack(padx=14, pady=4)

    # ──────────────────────────────────────────────────────── DRAW ───────────
    def _draw_board(self):
        self.canvas.delete("all")
        sz = self.size
        cs = CELL_SIZE
        p  = PADDING

        # Background cells
        for r in range(sz):
            for c in range(sz):
                x0 = p + c * cs + 2
                y0 = p + r * cs + 2
                x1 = x0 + cs - 4
                y1 = y0 + cs - 4
                color = CELL_NORMAL
                if (r, c) == self._hover_cell and not self.game_over and not self.ai_thinking:
                    if self.game.board[r][c] == '.':
                        color = CELL_HOVER
                self.canvas.create_rectangle(x0, y0, x1, y1,
                                             fill=color, outline="", tags=f"cell_{r}_{c}")

        # Grid lines
        for i in range(sz + 1):
            x = p + i * cs
            self.canvas.create_line(x, p, x, p + sz * cs, fill=GRID_LINE, width=1)
            self.canvas.create_line(p, x, p + sz * cs, x, fill=GRID_LINE, width=1)

        # Pieces
        for r in range(sz):
            for c in range(sz):
                v = self.game.board[r][c]
                if v != '.':
                    self._draw_piece(r, c, v)

        # Last move highlight
        if self.last_move:
            lr, lc = self.last_move
            cx = p + lc * cs + cs // 2
            cy = p + lr * cs + cs // 2
            self.canvas.create_rectangle(
                p + lc * cs + 2, p + lr * cs + 2,
                p + lc * cs + cs - 2, p + lr * cs + cs - 2,
                outline=WIN_HIGHLIGHT if self.win_cells else (X_COLOR if self.game.board[lr][lc] == 'X' else O_COLOR),
                width=2, fill=""
            )

        # Win highlight
        for (wr, wc) in self.win_cells:
            x0 = p + wc * cs + 3
            y0 = p + wr * cs + 3
            self.canvas.create_rectangle(x0, y0, x0 + cs - 6, y0 + cs - 6,
                                         fill=WIN_HIGHLIGHT + "33", outline=WIN_HIGHLIGHT, width=2)

        # Hover ghost piece
        if self._hover_cell and not self.game_over and not self.ai_thinking:
            hr, hc = self._hover_cell
            if self.game.board[hr][hc] == '.':
                self._draw_piece(hr, hc, self.human_player, ghost=True)

    def _draw_piece(self, r, c, player, ghost=False):
        p  = PADDING
        cs = CELL_SIZE
        cx = p + c * cs + cs // 2
        cy = p + r * cs + cs // 2

        if player == 'X':
            color = X_COLOR if not ghost else X_COLOR + "55"
            margin = 10
            self.canvas.create_line(cx - margin + cs//2 - cs//2, cy - margin,
                                    cx + margin, cy + margin,
                                    fill=color, width=4, capstyle='round')
            self.canvas.create_line(cx + margin, cy - margin,
                                    cx - margin, cy + margin,
                                    fill=color, width=4, capstyle='round')
        else:
            color = O_COLOR if not ghost else O_COLOR + "55"
            r_ = cs // 2 - 10
            self.canvas.create_oval(cx - r_, cy - r_, cx + r_, cy + r_,
                                    outline=color, width=4)

    # ──────────────────────────────────────────────────────── EVENTS ─────────
    def _cell_from_event(self, event):
        c = (event.x - PADDING) // CELL_SIZE
        r = (event.y - PADDING) // CELL_SIZE
        if 0 <= r < self.size and 0 <= c < self.size:
            return r, c
        return None

    def _on_hover(self, event):
        cell = self._cell_from_event(event)
        if cell != self._hover_cell:
            self._hover_cell = cell
            self._draw_board()

    def _on_leave(self, event):
        self._hover_cell = None
        self._draw_board()

    def _on_click(self, event):
        if self.game_over or self.ai_thinking:
            return
        if self.game.current_player != self.human_player:
            return
        cell = self._cell_from_event(event)
        if cell is None:
            return
        r, c = cell
        if self.game.board[r][c] != '.':
            return
        self._place_move(r, c)

    def _place_move(self, r, c):
        self.last_move = (r, c)
        finished = self.game.make_move(r, c)
        self._draw_board()
        if finished:
            self._handle_game_over(r, c)
            return
        if not self.game_over:
            self._set_status(f"AI thinking…  O", TEXT_MUTED)
            self.thinking_var.set("▌")
            self.root.after(80, self._ai_turn)

    def _ai_turn(self):
        self.ai_thinking = True
        self._animate_thinking()
        def run():
            (x, y), nodes, elapsed = self.ai.get_best_move(self.game)
            self.root.after(0, lambda: self._finish_ai(x, y, nodes, elapsed))
        threading.Thread(target=run, daemon=True).start()

    def _finish_ai(self, x, y, nodes, elapsed):
        self.ai_thinking = False
        self.thinking_var.set("")
        self.nodes_var.set(f"{nodes:,}")
        self.time_var.set(f"{elapsed:.3f}")
        self.last_move = (x, y)
        finished = self.game.make_move(x, y)
        self._draw_board()
        if finished:
            self._handle_game_over(x, y)
        else:
            self._set_status(f"Your turn  ›  X", TEXT_PRIMARY)

    def _animate_thinking(self):
        if not self.ai_thinking:
            return
        frames = ["▌", "▐", "▌▐", "·"]
        cur = self.thinking_var.get()
        nxt = frames[(frames.index(cur) + 1) % len(frames)] if cur in frames else "▌"
        self.thinking_var.set(nxt)
        self.root.after(300, self._animate_thinking)

    def _handle_game_over(self, x, y):
        self.game_over = True
        winner = self.game.board[x][y] if hasattr(self.game, 'board') else None
        # Try to find winner from last placed piece
        if self.game.check_win(x, y):
            winner = self.game.board[x][y]
            self.scores[winner] += 1
            self._update_scores()
            color = X_COLOR if winner == 'X' else O_COLOR
            label = "YOU WIN! 🎉" if winner == self.human_player else "AI WINS"
            self._set_status(f"{'★  ' if winner==self.human_player else ''}  {label}  {'  ★' if winner==self.human_player else ''}", color)
            self._highlight_win(x, y, winner)
        else:
            self.scores['Draw'] += 1
            self._update_scores()
            self._set_status("DRAW  —  Well played", TEXT_MUTED)

    def _highlight_win(self, lx, ly, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        board = self.game.board
        for dx, dy in directions:
            cells = [(lx, ly)]
            for d in [1, -1]:
                nx, ny = lx + d * dx, ly + d * dy
                while 0 <= nx < self.size and 0 <= ny < self.size and board[nx][ny] == player:
                    cells.append((nx, ny))
                    nx += d * dx
                    ny += d * dy
            if len(cells) >= 5:
                self.win_cells = cells
                self._draw_board()
                return

    def _set_status(self, text, color=TEXT_PRIMARY):
        self.status_var.set(text)

    def _update_scores(self):
        self.score_x.config(text=str(self.scores['X']))
        self.score_o.config(text=str(self.scores['O']))
        self.score_d.config(text=str(self.scores['Draw']))

    # ──────────────────────────────────────────────────────── CONTROLS ───────
    def _new_game(self):
        self.game      = self.game_factory()
        self.game_over = False
        self.last_move = None
        self.win_cells = []
        self._hover_cell = None
        self.nodes_var.set("—")
        self.time_var.set("—")
        self.thinking_var.set("")

        # If human chose O, AI goes first
        if self.human_player == 'O':
            self._set_status("AI thinking…  X", TEXT_MUTED)
            self.root.after(80, self._ai_turn)
        else:
            self._set_status("Your turn  ›  X", TEXT_PRIMARY)

        self._draw_board()

    def _undo(self):
        if self.ai_thinking or not hasattr(self.game, 'undo_move'):
            return
        # Undo AI + human moves (2 plies)
        for _ in range(2):
            if self.last_move:
                r, c = self.last_move
                self.game.undo_move(r, c)
        self.game_over  = False
        self.win_cells  = []
        self.last_move  = None
        self._set_status("Your turn  ›  X", TEXT_PRIMARY)
        self._draw_board()

    def _pick_side(self, sym):
        self.human_player = sym
        self.ai_player    = 'O' if sym == 'X' else 'X'
        self._highlight_side_btn(sym)
        self._new_game()

    def _highlight_side_btn(self, sym):
        for s, b in self._side_btns.items():
            if s == sym:
                b.config(bg=CELL_HOVER,
                         fg=X_COLOR if s == 'X' else O_COLOR)
            else:
                b.config(bg=CELL_NORMAL, fg=TEXT_MUTED)