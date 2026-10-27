"""2026학년도 6월 모의평가 21번 — '위험한 점을 찾아라' (대본: script.md)

판서(노트 필기)형 화면: 인쇄된 문제 위에 펜으로 표시하고, 풀이를 한 장에 쌓아 간다.
렌더: manim -qh scene.py Killer21   (손글씨 폰트 Nanum Pen Script 필요)
"""
from manim import *

PEN = "Nanum Pen"
PRINT = "Noto Serif CJK KR"
SANS = "Noto Sans CJK KR"
config.background_color = "#fdfcf8"

INK = "#222222"      # 인쇄된 문제
PEN_INK = "#2b2b2b"  # 필기
ACCENT = "#d6342c"   # 포인팅 전용 (동그라미, 밑줄, 위험한 점, 답)
FAINT = "#9a9a9a"    # 보조 설명


def f(x):
    return (x - 1) * (x - 2)


def row(*parts, buff=0.1):
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def P(text, size=22):
    """인쇄체(문제 본문)."""
    return Text(text, font=PRINT, font_size=size, color=INK)


def PM(*tex, size=30):
    return MathTex(*tex, font_size=size, color=INK)


def hw(text, size=36, color=PEN_INK):
    """손글씨."""
    return Text(text, font=PEN, font_size=size, color=color)


def hfrac(num, den, size=36, color=PEN_INK):
    n = hw(num, size, color)
    d = hw(den, size, color)
    bar = Line(LEFT, RIGHT, color=color, stroke_width=2.5).set_width(max(n.width, d.width) + 0.15)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.07)


def hlim(sub, size=36, color=PEN_INK):
    return VGroup(hw("lim", size, color), hw(sub, size * 0.6, color)).arrange(DOWN, buff=0.0)


def check_mark(color=PEN_INK, size=0.22):
    return VMobject(color=color, stroke_width=3).set_points_as_corners(
        [LEFT * size * 0.5 + UP * size * 0.1, DOWN * size * 0.4, RIGHT * size * 0.6 + UP * size * 0.6]
    )


class Killer21(Scene):
    def construct(self):
        self.cap = None
        self.pen = Dot(radius=0.06, color=PEN_INK).set_opacity(0)
        self.add(self.pen)
        self.page1()
        self.turn_page()
        self.page2()

    # ---------- helpers ----------
    def say(self, text, wait=None):
        new = Text(text, font=SANS, font_size=28, color=WHITE)
        if new.width > 13:
            new.scale_to_fit_width(13)
        new.to_edge(DOWN, buff=0.22)
        bg = BackgroundRectangle(new, color=BLACK, fill_opacity=0.72, buff=0.12)
        new = VGroup(bg, new)
        anims = [FadeIn(new, run_time=0.3)]
        if self.cap is not None:
            anims.append(FadeOut(self.cap, run_time=0.3))
        self.play(*anims)
        self.cap = new
        self.wait(wait if wait is not None else max(2.0, len(text) * 0.11))

    def write(self, *mobs, color=None):
        """펜 끝이 따라가며 한 요소씩 필기한다."""
        for m in mobs:
            c = color or m.get_color()
            self.pen.set_color(c)
            start = m.get_left()
            if self.pen.get_fill_opacity() == 0:
                self.pen.move_to(start)
                self.play(self.pen.animate.set_opacity(1), run_time=0.2)
            else:
                self.play(self.pen.animate.move_to(start), run_time=0.35)
            rt = min(2.4, max(0.5, m.width * 0.32))
            self.play(Write(m), self.pen.animate.move_to(m.get_right()), run_time=rt)
            self.wait(0.15)

    def mark(self, anim, run_time=0.7):
        self.play(anim, run_time=run_time)

    def ellipse_around(self, mob, color, pad=(0.25, 0.2)):
        return Ellipse(width=mob.width + pad[0], height=mob.height + pad[1],
                       color=color, stroke_width=3).move_to(mob)

    def underline(self, mob, color, buff=0.06):
        return Line(mob.get_corner(DL) + DOWN * buff, mob.get_corner(DR) + DOWN * buff,
                    color=color, stroke_width=3)

    # ---------- 1장 ----------
    def build_problem(self):
        no = P("21.", 24)
        m_f = PM(r"f(x)=(x-1)(x-2)")
        t_and = P("와")
        t_lead = P("최고차항의 계수가 1인")
        r1 = row(no, P("함수"), m_f, t_and, t_lead)
        t_quart = P("사차함수")
        m_g = PM("g(x)")
        r2 = row(t_quart, m_g, P("가 다음 조건을 만족시킨다."))
        b1a = P("모든 실수")
        b1 = row(b1a, PM("a"), P("에 대하여"))
        lim1 = PM(r"\lim_{x\to a}", r"\frac{g(x)\times|f(x)|}{f(x)}")
        lim2 = PM(r"\lim_{x\to a}", r"\frac{|g(x)-f(x)|}{g(x)}")
        b2 = row(lim1, P("의 값과"), lim2, P("의 값이"), buff=0.12)
        b3b = P("존재")
        b3 = row(P("모두"), b3b, P("한다."), buff=0.06)
        inner = VGroup(b1, b2, b3).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        box = SurroundingRectangle(inner, color=INK, stroke_width=1.5, buff=0.18, corner_radius=0)
        m_gm1 = PM("g(-1)")
        r3 = row(m_gm1, P("의 값을 구하시오. [4점]"))
        prob = VGroup(r1, r2, VGroup(box, inner), r3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for part in (r2, prob[2], r3):
            part.shift(RIGHT * 0.38)
        if prob.width > 7.4:
            prob.scale_to_fit_width(7.4)
        prob.to_corner(UL, buff=0.3)
        self.prob = prob
        self.p_lead = VGroup(t_lead, t_quart, m_g)
        self.p_all = b1a
        self.p_exist = b3b
        self.p_lim1 = lim1[1]
        self.p_lim2 = lim2[1]
        self.p_gm1 = m_gm1
        self.p_r3 = r3
        return prob

    def page1(self):
        prob = self.build_problem()
        src = Text("출처: 2026학년도 6월 모의평가 수학 21번 (한국교육과정평가원)",
                   font=SANS, font_size=14, color=FAINT).to_corner(UR, buff=0.12)
        self.play(FadeIn(src))
        for part in prob:
            self.play(FadeIn(part, shift=UP * 0.1), run_time=0.6)
        self.say("오늘 문제는 2026학년도 6월 모의평가 21번입니다.")
        self.say("먼저 문제부터 꼼꼼히 읽어 봅시다.", 1.5)

        # 문제 위에 직접 표시
        ul1 = VGroup(self.underline(self.prob[0][-1], PEN_INK),
                     self.underline(VGroup(self.p_lead[1], self.p_lead[2]), PEN_INK))
        self.mark(Create(ul1))
        self.say("g(x)는 최고차항의 계수가 1인 사차함수.")
        e_all = self.ellipse_around(self.p_all, ACCENT)
        e_exist = self.ellipse_around(self.p_exist, ACCENT)
        self.mark(Create(e_all))
        self.mark(Create(e_exist))
        self.say("조건을 보면, 모든 실수 a에서 두 극한이 존재한다고 합니다.")
        self.say("웬만한 점에서는 극한이 당연히 존재하죠.")
        self.say("그런데도 굳이 말한 건, 위험한 점이 있다는 신호입니다.")

        # ---- 첫 번째 조건 ----
        e_lim1 = self.ellipse_around(self.p_lim1, ACCENT, pad=(0.3, 0.15))
        self.mark(Create(e_lim1))
        self.say("첫 번째 식부터 봅시다. 신경 쓰이는 건 |f(x)|/f(x).")

        top = prob.get_bottom()[1] - 0.25
        ax = Axes(x_range=[-0.5, 3.5, 1], y_range=[-0.8, 2.6, 1], x_length=2.7, y_length=1.95,
                  tips=False, axis_config={"color": INK, "stroke_width": 1.5, "include_ticks": False})
        ax.move_to([-5.35, top - 1.05, 0])
        fg = ax.plot(f, x_range=[-0.15, 3.15], color=PEN_INK, stroke_width=3)
        flab = hw("y=f(x)", 28).next_to(ax.c2p(0.05, 2.3), RIGHT, buff=0.15)
        n1 = hw("1", 24).next_to(ax.c2p(1, 0), DL, buff=0.05)
        n2 = hw("2", 24).next_to(ax.c2p(2, 0), DR, buff=0.05)
        self.play(Create(ax), run_time=0.6)
        self.pen.set_color(PEN_INK)
        self.play(Create(fg), MoveAlongPath(self.pen.set_opacity(1), fg), run_time=1.4)
        self.write(flab, n1, n2)
        self.say("f(x)의 그래프를 그려 보면, 1과 2에서 x축을 지납니다.")
        sp = hw("+", 34).move_to(ax.c2p(0.05, 0.9))
        sm = hw("-", 40).move_to(ax.c2p(1.5, -0.55))
        sp2 = hw("+", 34).move_to(ax.c2p(2.95, 0.9))
        self.write(sp, sm, sp2)
        self.mark(Create(self.ellipse_around(sm, PEN_INK, pad=(0.2, 0.2))))
        self.say("부호는 +, −, +.")

        bx = -3.75
        d3 = Dot(ax.c2p(3, 2), color=FAINT, radius=0.05)
        l3 = hw("x=3 근처:  |f(x)|/f(x) = 1  →  그냥 g(x)", 28, FAINT)
        l3.move_to([bx, top - 0.25, 0], aligned_edge=LEFT)
        self.play(FadeIn(d3))
        self.write(l3)
        self.say("x=3 근처처럼 부호가 안 바뀌는 곳은 |f(x)|/f(x)=1. 식은 그냥 g(x)라 아무 일도 없습니다.")

        dangers = VGroup(*[Dot(ax.c2p(x, 0), color=ACCENT, radius=0.07) for x in (1, 2)])
        warn = hw("위험!", 30, ACCENT).next_to(ax.c2p(2.2, -0.45), RIGHT, buff=0.1)
        self.play(FadeIn(dangers, scale=2))
        self.write(warn)
        self.say("문제는 부호가 바뀌는 x=1, x=2. 여기가 위험한 점입니다.")
        self.warn = warn

        lim_p = row(hlim("x→1+", 32), hw("-g(x) = -g(1)", 34), buff=0.12)
        lim_m = row(hlim("x→1-", 32), hw(" g(x) =  g(1)", 34), buff=0.12)
        lim_p.move_to([bx, top - 0.95, 0], aligned_edge=LEFT)
        lim_m.move_to([bx, top - 1.75, 0], aligned_edge=LEFT)
        self.write(lim_p)
        self.say("x=1의 오른쪽은 f(x)<0이라 −g(x)로 나와, −g(1)로 갑니다.")
        self.write(lim_m)
        self.say("왼쪽은 f(x)>0이라 g(x) 그대로, g(1)로 갑니다.")

        arrow = hw("⇒", 34).next_to(VGroup(lim_p, lim_m), RIGHT, buff=0.15)
        concl = VGroup(hw("g(1) = 0", 36), hw("g(2) = 0", 36)).arrange(DOWN, buff=0.22)
        concl.next_to(arrow, RIGHT, buff=0.15)
        self.write(arrow, concl[0])
        self.wait(0.5)
        self.write(concl[1])
        self.mark(Create(self.ellipse_around(concl, ACCENT, pad=(0.35, 0.3))))
        self.say("두 값이 같아야 하니 g(1)=0. 같은 이유로 g(2)=0.")
        self.concl = concl

        gy = -2.45
        g1 = hw("g(x) = (x-1)(x-2) · h(x)", 40).move_to([-6.75, gy, 0], aligned_edge=LEFT)
        self.write(g1)
        self.say("그러면 g(x)는 (x−1)(x−2)를 인수로 가집니다.")
        hnote = hw("h(x): 이차, 최고차항 계수 1", 28).next_to(g1, DOWN, buff=0.12).align_to(g1, LEFT)
        self.write(hnote)
        self.say("남은 부분을 h(x)라 하면, h(x)는 최고차항 계수가 1인 이차함수.")
        fx_part = g1[5:15]
        self.mark(Create(self.underline(fx_part, PEN_INK)))
        g2 = hw("= f(x) h(x)", 40).next_to(g1, RIGHT, buff=0.25)
        self.write(g2)
        self.say("그리고 (x−1)(x−2)는 바로 f(x)죠.")
        self.g2 = g2

        # ---- 두 번째 조건 (빨간 펜) ----
        checks = VGroup(*[check_mark(ACCENT).move_to(self.p_lim2.get_top() + UP * 0.15 + RIGHT * dx)
                          for dx in (-0.35, 0.25)])
        self.mark(Create(checks))
        ex = 1.35
        e0 = row(hw("②", 34, PEN_INK), hfrac("|g(x) - f(x)|", "g(x)", 34, PEN_INK), buff=0.2)
        e0.move_to([ex, 3.12, 0], aligned_edge=LEFT)
        sub = hw("g(x) = f(x)h(x) 대입", 28, PEN_INK).next_to(e0, RIGHT, buff=0.35)
        self.write(e0, sub)
        e1 = row(hw("=", 34, PEN_INK), hfrac("|f(x)h(x) - f(x)|", "f(x)h(x)", 34, PEN_INK), buff=0.2)
        e1.next_to(e0, DOWN, buff=0.22).align_to(e0, LEFT)
        self.write(e1)
        self.say("이제 두 번째 식. g(x) 자리에 f(x)h(x)를 넣습니다.")
        e2 = row(hw("=", 34, PEN_INK), hfrac("|f(x)| · |h(x) - 1|", "f(x) · h(x)", 34, PEN_INK), buff=0.2)
        e2.next_to(e1, DOWN, buff=0.22).align_to(e0, LEFT)
        self.write(e2)
        self.say("분자에서 f(x)를 묶으면 |f(x)|·|h(x)−1|.")
        sw = hfrac("|f(x)|", "f(x)", 34, PEN_INK)
        rest = hfrac("|h(x) - 1|", "h(x)", 34, PEN_INK)
        e3 = row(hw("=", 34, PEN_INK), sw, hw("×", 34, PEN_INK), rest, buff=0.2)
        e3.next_to(e2, DOWN, buff=0.22).align_to(e0, LEFT)
        self.write(e3)
        self.say("정리하면 |f(x)|/f(x) × |h(x)−1|/h(x).")
        e_sw = self.ellipse_around(sw, ACCENT, pad=(0.35, 0.2))
        sw_lab = hw("스위치!", 28, ACCENT).next_to(e_sw, DOWN, buff=0.05)
        self.mark(Create(e_sw))
        self.write(sw_lab)
        self.play(Indicate(e_lim1, color=ACCENT), Indicate(VGroup(sp, sm, sp2), color=ACCENT))
        self.say("아까 그 스위치가 또 나왔습니다.")

        c1 = hw("x = 1, 2 에서  |h(x) - 1| = 0", 32, PEN_INK)
        c1.next_to(sw_lab, DOWN, buff=0.15).align_to(e0, LEFT)
        self.write(c1)
        self.say("그러면 같은 논리로, x=1, 2에서 |h(x)−1|이 0이어야 합니다.")
        c3 = hw("→  h(1) = 1,  h(2) = 1", 34, PEN_INK).next_to(c1, DOWN, buff=0.18).align_to(e0, LEFT)
        self.write(c3)
        box_c3 = SurroundingRectangle(c3[1:], color=ACCENT, buff=0.08, stroke_width=2.5)
        self.mark(Create(box_c3))
        self.say("즉 h(1)=1, h(2)=1.")
        self.c3 = c3
        c4 = hw("분모 h(x) ≠ 0", 32, PEN_INK).next_to(c3, RIGHT, buff=0.3)
        self.mark(Create(self.ellipse_around(rest[2], ACCENT, pad=(0.25, 0.15))))
        self.write(c4)
        self.say("그리고 분모 h(x)는 어디서도 0이면 안 됩니다.")
        self.c4 = c4

        k2 = hw("h(x) = (x-1)(x-2) + 1 = x² - 3x + 3", 34, PEN_INK)
        k2.next_to(c3, DOWN, buff=0.25).align_to(e0, LEFT)
        self.write(k2[:17])
        self.say("h(x)−1은 x=1, 2를 근으로 갖고 최고차항 계수가 1이니 (x−1)(x−2).")
        self.write(k2[17:])
        self.say("따라서 h(x)=(x−1)(x−2)+1 = x²−3x+3.")
        self.k2 = k2
        k3 = hw("D = 9 - 12 < 0   →  h(x) ≠ 0  OK", 34, PEN_INK)
        k3.next_to(k2, DOWN, buff=0.2).align_to(e0, LEFT)
        self.write(k3)
        self.mark(Create(self.underline(k3, ACCENT)))
        self.say("판별식 D = 9 − 12 < 0. 실근이 없으니 h(x)≠0도 만족.")

        # ---- 답 (주황 펜) ----
        a1 = hw("g(x) = f(x){f(x) + 1},   f(-1) = 6", 32, PEN_INK).move_to([-3.15, -3.0, 0], aligned_edge=LEFT)
        self.write(a1)
        self.say("정리하면 g(x)=f(x){f(x)+1}. 그리고 f(−1)=(−2)(−3)=6.")
        self.mark(Create(self.ellipse_around(self.p_gm1, ACCENT, pad=(0.25, 0.15))))
        a2 = hw("= 6 × 7 =", 32, PEN_INK).next_to(self.p_r3, RIGHT, buff=0.3)
        ans = hw("42", 46, ACCENT).next_to(a2, RIGHT, buff=0.15)
        self.write(a2, ans)
        ans_box = SurroundingRectangle(ans, color=ACCENT, buff=0.1, stroke_width=3)
        self.mark(Create(ans_box))
        self.play(Flash(ans, color=ACCENT, line_length=0.25, num_lines=12))
        self.say("그러니 g(−1)=6×7=42.")
        self.ans = VGroup(ans, ans_box)
        self.play(self.pen.animate.set_opacity(0), run_time=0.3)
        self.wait(1.5)
        self.say("여기까지가 풀이 전체입니다. 핵심만 모아서 다음 장으로 넘어갑시다.", 2.5)

    # ---------- 장 넘김: 핵심 수집 ----------
    def turn_page(self):
        page1 = [m for m in self.mobjects if m not in (self.cap, self.pen)]
        panel = RoundedRectangle(width=13.6, height=1.75, corner_radius=0.12,
                                 stroke_color="#cfcfcf", fill_color="#f3f2ee", fill_opacity=0.97)
        panel.to_edge(UP, buff=0.25)
        title = hw("지난 장에서 얻은 것", 32, INK).next_to(panel.get_corner(UL), DR, buff=0.15)
        items = [
            (self.warn, hw("위험한 점: x = 1, 2", 30, PEN_INK)),
            (self.concl, hw("g(1) = g(2) = 0", 30, PEN_INK)),
            (self.g2, hw("g(x) = f(x) h(x)", 30, PEN_INK)),
            (self.c3, hw("h(1) = h(2) = 1", 30, PEN_INK)),
            (self.c4, hw("h(x) ≠ 0", 30, PEN_INK)),
            (self.k2, hw("h(x) = f(x) + 1", 30, PEN_INK)),
        ]
        grid = VGroup(*[t for _, t in items]).arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.15),
                                                              col_alignments="lll")
        grid.next_to(title, RIGHT, buff=0.5).align_to(title, UP).shift(DOWN * 0.1)
        ans_t = row(hw("g(-1) =", 36, PEN_INK), hw("42", 46, ACCENT), buff=0.15)
        ans_t.move_to(panel.get_right() + LEFT * 1.0)

        self.play(*[m.animate.set_opacity(0.25) for m in page1 if m is not self.prob], run_time=0.8)
        self.play(FadeIn(panel), FadeIn(title))
        for src, tgt in items:
            self.play(Indicate(src, color=ACCENT, scale_factor=1.15), run_time=0.5)
            self.play(TransformFromCopy(src, tgt), run_time=0.8)
        self.play(TransformFromCopy(self.ans, ans_t), run_time=0.8)
        self.say("지난 장에서 얻은 것들입니다.", 1.5)
        self.play(*[FadeOut(m, shift=LEFT * 2) for m in page1], run_time=1.0)
        self.collected = VGroup(panel, title, grid, ans_t)

    # ---------- 2장 ----------
    def page2(self):
        ax = Axes(x_range=[-0.5, 3.5, 1], y_range=[-1, 3.2, 1], x_length=4.8, y_length=3.9,
                  tips=False, axis_config={"color": INK, "stroke_width": 1.5, "include_ticks": False})
        ax.move_to([-4.2, -1.15, 0])
        n1 = hw("1", 26).next_to(ax.c2p(1, 0), DOWN, buff=0.08)
        n2 = hw("2", 26).next_to(ax.c2p(2, 0), DOWN, buff=0.08)
        fg = ax.plot(f, x_range=[-0.2, 3.2], color=FAINT, stroke_width=3)
        flab = hw("f(x)", 30, FAINT).next_to(ax.c2p(3.2, f(3.2)), RIGHT, buff=0.05)
        self.play(Create(ax), FadeIn(n1), FadeIn(n2))
        self.pen.set_color(PEN_INK)
        self.play(Create(fg), MoveAlongPath(self.pen.set_opacity(1), fg), run_time=1.4)
        self.write(flab)

        k = ValueTracker(1.0)

        def hcol():
            return PEN_INK if k.get_value() > 0.25 + 1e-3 else ACCENT

        hg = always_redraw(lambda: ax.plot(lambda x: f(x) + k.get_value(), x_range=[-0.1, 3.1],
                                           color=hcol(), stroke_width=3))
        arrows = VGroup(*[Arrow(ax.c2p(x, f(x)), ax.c2p(x, f(x) + 1), buff=0.04, color=PEN_INK,
                                stroke_width=3, max_tip_length_to_length_ratio=0.3) for x in (1, 1.5, 2)])
        for a in arrows:
            self.play(GrowArrow(a), run_time=0.4)
        self.play(Create(hg), run_time=1.2)
        hlab = hw("h(x)", 30, PEN_INK).next_to(ax.c2p(3.1, f(3.1) + 1), RIGHT, buff=0.05)
        self.play(FadeIn(hlab), FadeOut(arrows))
        self.say("h(x)=f(x)+1을 그림으로 보면, f(x)를 위로 1만큼 올린 포물선.")

        bot_f = DashedLine(ax.c2p(-0.5, -0.25), ax.c2p(3.5, -0.25), color=FAINT, stroke_width=2)
        lf = hw("-1/4", 26, FAINT).next_to(bot_f, RIGHT, buff=0.08)
        bot_h = always_redraw(lambda: DashedLine(ax.c2p(-0.5, k.get_value() - 0.25),
                                                 ax.c2p(3.5, k.get_value() - 0.25),
                                                 color=hcol(), stroke_width=2))
        lh = always_redraw(lambda: hw(f"{k.get_value() - 0.25:.2f}", 26, hcol())
                           .next_to(ax.c2p(3.5, k.get_value() - 0.25), RIGHT, buff=0.08))
        self.play(Create(bot_f), FadeIn(lf))
        self.play(Create(bot_h), FadeIn(lh))
        self.say("f(x)의 바닥 −1/4이 3/4으로 올라가 x축에 닿지 않습니다.")

        nx = -0.9
        q = row(hw("만약 1 → k 라면?", 36, PEN_INK), hfrac("|g(x) - k·f(x)|", "g(x)", 34, PEN_INK), buff=0.35)
        q.move_to([nx, 1.4, 0], aligned_edge=LEFT)
        self.write(q)
        self.say("그런데 문제의 1이 다른 수 k였다면?")
        r1 = hw("→  h(x) = f(x) + k,   바닥 = k - 1/4", 34, PEN_INK).next_to(q, DOWN, buff=0.22).align_to(q, LEFT)
        self.write(r1)
        kval = always_redraw(lambda: hw(f"k = {k.get_value():.2f}", 34, hcol())
                             .next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
        self.play(FadeIn(kval))
        self.say("같은 논리로 h(x)=f(x)+k. 바닥은 k−1/4.")
        self.play(self.pen.animate.set_opacity(0), run_time=0.2)
        self.play(k.animate.set_value(0.25), run_time=3.5, rate_func=linear)
        boom = hw("x축에 닿음 → h(x)=0 → 극한 붕괴", 30, ACCENT).next_to(r1, DOWN, buff=0.2).align_to(q, LEFT)
        self.play(Flash(ax.c2p(1.5, 0), color=ACCENT))
        self.write(boom)
        self.say("k를 줄여 보면… 1/4에서 바닥이 x축에 닿고, 극한이 깨집니다.")
        self.play(k.animate.set_value(1.0), run_time=2)
        r2 = hw("∴  k > 1/4  일 때만 성립,  1은 안전!", 36, PEN_INK).next_to(boom, DOWN, buff=0.22).align_to(q, LEFT)
        self.write(r2)
        self.mark(Create(SurroundingRectangle(r2, color=ACCENT, buff=0.12, stroke_width=2.5)))
        self.say("그래서 이 문제는 k > 1/4일 때만 성립합니다. 1은 안전한 선택이었죠.")

        sum_title = hw("오늘의 도구", 28, PEN_INK)
        s1 = hw("① |f(x)|/f(x) 는 부호 스위치", 26, PEN_INK)
        s2 = hw("② 스위치가 뒤집히는 곳에서 곱해진 값 = 0", 26, PEN_INK)
        s3 = hw("③ 분모는 어디서도 0이 되면 안 된다", 26, PEN_INK)
        sg = VGroup(sum_title, s1, s2, s3).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        sg.next_to(r2, DOWN, buff=0.3).align_to(q, LEFT)
        frame = SurroundingRectangle(sg, color=PEN_INK, buff=0.12, corner_radius=0.1, stroke_width=2)
        self.play(Create(frame), run_time=0.6)
        self.write(sum_title)
        self.say("오늘 쓴 도구를 정리하면,", 1.2)
        for line, cap in ((s1, "① |f(x)|/f(x)는 부호 스위치."),
                          (s2, "② 스위치가 뒤집히는 곳에서는 곱해진 값이 0."),
                          (s3, "③ 분모는 어디서도 0이 되면 안 된다.")):
            self.write(line)
            self.say(cap)
        self.play(self.pen.animate.set_opacity(0), Indicate(self.collected[3], color=ACCENT))
        self.say("답은 42.", 3)
        self.play(*[FadeOut(m) for m in self.mobjects])
