"""2026학년도 6월 모의평가 21번 — '절대값의 가면' (대본: script.md)

렌더: manim -qh scene.py Killer21
"""
from manim import *

FONT = "Noto Sans CJK KR"
config.background_color = "#0f1117"

F_COL = BLUE_C
G_COL = YELLOW_C
H_COL = GREEN_C
SW_COL = "#ff6b6b"  # 부호 스위치


def f(x):
    return (x - 1) * (x - 2)


def T(text, size=34, color=WHITE):
    return Text(text, font=FONT, font_size=size, color=color)


class Killer21(Scene):
    def construct(self):
        self.cap = None
        self.opening()
        self.switch_principle()
        self.condition1()
        self.condition2()
        self.find_h()
        self.reveal()
        self.answer()
        self.generalize()
        self.summary()

    # ---------- helpers ----------
    def say(self, text, wait=None):
        new = T(text, 30)
        if new.width > 13:
            new.scale_to_fit_width(13)
        new.to_edge(DOWN, buff=0.35)
        bg = BackgroundRectangle(new, color=BLACK, fill_opacity=0.6, buff=0.15)
        new = VGroup(bg, new)
        anims = [FadeIn(new, run_time=0.3)]
        if self.cap is not None:
            anims.append(FadeOut(self.cap, run_time=0.3))
        self.play(*anims)
        self.cap = new
        self.wait(wait if wait is not None else max(1.6, len(text) * 0.09))

    def clear_stage(self):
        keep = [self.cap] if self.cap is not None else []
        rest = [m for m in self.mobjects if m not in keep]
        if rest:
            self.play(*[FadeOut(m) for m in rest], run_time=0.6)

    def axes(self, x_range, y_range, width, height):
        return Axes(
            x_range=x_range, y_range=y_range,
            x_length=width, y_length=height,
            axis_config={"color": GREY_B, "include_ticks": True, "tick_size": 0.05},
            tips=False,
        )

    # ---------- S0 ----------
    def opening(self):
        title = T("절대값의 가면", 64, G_COL)
        sub = T("2026학년도 6월 모의평가 21번", 30, GREY_B).next_to(title, DOWN)
        self.play(Write(title), FadeIn(sub, shift=UP * 0.2))
        self.say("절대값 두 개, 극한 두 개.")
        self.say("복잡해 보이지만, 이 문제의 정체는 단 한 줄입니다.")
        self.play(FadeOut(title), FadeOut(sub))

        given = MathTex(r"f(x)=(x-1)(x-2)", font_size=40, color=F_COL)
        g_desc = T("g(x): 최고차항의 계수가 1인 사차함수", 28, G_COL)
        lim1 = MathTex(r"\lim_{x\to a}\frac{g(x)\,|f(x)|}{f(x)}", font_size=44)
        lim2 = MathTex(r"\lim_{x\to a}\frac{|g(x)-f(x)|}{g(x)}", font_size=44)
        lims = VGroup(lim1, lim2).arrange(RIGHT, buff=1.2)
        cond = T("모든 실수 a에 대하여 두 극한이 모두 존재", 28)
        ask = MathTex(r"g(-1)=\ ?", font_size=48, color=G_COL)
        src = T("출처: 2026학년도 6월 모의평가 수학 21번 (한국교육과정평가원)", 18, GREY_C)
        prob = VGroup(given, g_desc, lims, cond, ask).arrange(DOWN, buff=0.35).shift(UP * 0.6)
        src.to_corner(UR, buff=0.25)
        self.play(FadeIn(src), Write(given), FadeIn(g_desc))
        self.play(Write(lims), FadeIn(cond))
        self.say("오늘은 그 한 줄을 '부호 스위치' 하나로 찾아냅니다.")
        self.say("조건은 모든 실수 a에서 두 극한이 존재한다는 것.")
        self.play(Write(ask))
        self.say("구하는 것은 g(−1)입니다.")
        self.problem_src = src
        self.clear_stage()

    # ---------- S1 ----------
    def switch_principle(self):
        ax = self.axes([-3, 3, 1], [-2.5, 2.5, 1], 7, 4.2).shift(UP * 0.5)
        lab = MathTex(r"y=\frac{|x|}{x}", color=SW_COL, font_size=40).next_to(ax, UP, buff=0.1)
        right = ax.plot(lambda x: 1, x_range=[0.02, 3], color=SW_COL)
        left = ax.plot(lambda x: -1, x_range=[-3, -0.02], color=SW_COL)
        holes = VGroup(
            Circle(0.07, color=SW_COL).move_to(ax.c2p(0, 1)),
            Circle(0.07, color=SW_COL).move_to(ax.c2p(0, -1)),
        )
        self.play(Create(ax), Write(lab))
        self.say("먼저 |x|/x를 봅시다.", 1.2)
        self.play(Create(left), Create(right), FadeIn(holes))
        self.say("양수면 1, 음수면 −1. 0에서 딸깍 바뀌는 스위치입니다.")

        c = ValueTracker(1.0)

        def k(x):
            return 0.4 * x + c.get_value()

        kl = always_redraw(lambda: ax.plot(lambda x: -k(x), x_range=[-3, -0.02], color=G_COL))
        kr = always_redraw(lambda: ax.plot(lambda x: k(x), x_range=[0.02, 3], color=G_COL))
        gap = always_redraw(lambda: DashedLine(
            ax.c2p(0, -c.get_value()), ax.c2p(0, c.get_value()), color=WHITE
        ) if c.get_value() > 0.05 else VMobject())
        lab2 = MathTex(r"y=k(x)\cdot\frac{|x|}{x}", color=G_COL, font_size=40).move_to(lab)
        kval = always_redraw(lambda: MathTex(
            rf"k(0)={c.get_value():.2f}", font_size=36, color=G_COL
        ).next_to(ax, RIGHT, buff=0.2).shift(UP))
        self.say("이 스위치에 연속함수 k(x)를 곱하면?", 1.2)
        self.play(
            FadeOut(left), FadeOut(right), FadeOut(holes),
            ReplacementTransform(lab, lab2), Create(kl), Create(kr), FadeIn(gap), FadeIn(kval),
        )
        self.say("k(0)이 0이 아니면, 그래프가 0에서 찢어집니다.")
        self.say("그런데 k(0)을 0으로 보내면…", 0.3)
        self.play(c.animate.set_value(0), run_time=3)
        self.say("…틈이 닫힙니다.", 1.2)
        self.say("이것이 오늘의 유일한 무기입니다.", 1.2)
        self.clear_stage()

        box_txt = VGroup(
            T("부호 스위치  ×  연속함수", 40, WHITE),
            T("극한이 존재하려면", 30, GREY_B),
            T("스위치가 바뀌는 곳에서  곱해진 함수 = 0", 36, G_COL),
        ).arrange(DOWN, buff=0.35)
        box = SurroundingRectangle(box_txt, color=SW_COL, buff=0.4, corner_radius=0.15)
        self.play(Write(box_txt), Create(box))
        self.say("스위치가 바뀌는 곳에서, 곱해진 함수는 0이어야 한다.", 2.5)
        self.principle = VGroup(box, box_txt)
        self.play(self.principle.animate.scale(0.45).to_corner(UL, buff=0.25))

    # ---------- S2 ----------
    def condition1(self):
        ax = self.axes([-0.5, 3.5, 1], [-1, 3, 1], 5.5, 4).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        fg = ax.plot(f, x_range=[-0.2, 3.2], color=F_COL)
        flab = MathTex("y=f(x)", color=F_COL, font_size=32).next_to(ax.c2p(3.1, 2.4), LEFT)
        dots = VGroup(*[Dot(ax.c2p(x, 0), color=SW_COL, radius=0.08) for x in (1, 2)])
        signs = VGroup(
            MathTex("+", color=SW_COL).move_to(ax.c2p(0.2, 0.5)),
            MathTex("-", color=SW_COL).move_to(ax.c2p(1.5, 0.5)),
            MathTex("+", color=SW_COL).move_to(ax.c2p(2.8, 0.5)),
        )
        self.play(Create(ax), Create(fg), Write(flab))
        self.play(FadeIn(dots, scale=2), FadeIn(signs))
        self.say("f는 x=1, x=2에서 부호가 바뀝니다.")
        self.say("그러니 |f|/f는 1과 2에서 딸깍거리는 스위치.")

        e1 = MathTex(r"\frac{g\,|f|}{f}", "=", r"\frac{|f|}{f}", r"\cdot", "g", font_size=48)
        e1[2].set_color(SW_COL)
        e1[4].set_color(G_COL)
        e1.next_to(ax, RIGHT, buff=0.8).shift(UP * 1.2)
        self.play(Write(e1))
        self.say("첫 번째 식은 정확히 '스위치 × g' 꼴입니다.")
        e2 = MathTex(r"g(1)=0,\quad g(2)=0", font_size=44, color=G_COL).next_to(e1, DOWN, buff=0.6)
        self.play(Write(e2), Indicate(dots, color=G_COL))
        self.say("원리에 따라 g(1)=0, g(2)=0.")
        e3 = MathTex(r"g", "=", "f", r"\cdot", "h", font_size=56).next_to(e2, DOWN, buff=0.6)
        e3[0].set_color(G_COL)
        e3[2].set_color(F_COL)
        e3[4].set_color(H_COL)
        hn = MathTex(r"h=x^2+px+q", font_size=34, color=H_COL).next_to(e3, DOWN, buff=0.3)
        self.play(Write(e3), FadeIn(hn))
        self.say("그래서 g = f·h. h는 최고차항 계수가 1인 이차함수.")
        self.clear_stage_keep(self.principle)

    def clear_stage_keep(self, *keep):
        keep = list(keep) + ([self.cap] if self.cap is not None else [])
        rest = [m for m in self.mobjects if m not in keep]
        if rest:
            self.play(*[FadeOut(m) for m in rest], run_time=0.6)

    # ---------- S3 ----------
    def condition2(self):
        self.say("이제 두 번째 식. 여기가 핵심입니다.", 1.2)
        steps = [
            MathTex(r"\frac{|g-f|}{g}", font_size=60),
            MathTex(r"\frac{|fh-f|}{fh}", font_size=60),
            MathTex(r"\frac{|f|\,|h-1|}{f\,h}", font_size=60),
            MathTex(r"\frac{|f|}{f}", r"\cdot", r"\frac{|h-1|}{h}", font_size=60),
        ]
        steps[3][0].set_color(SW_COL)
        steps[3][2].set_color(H_COL)
        for s in steps:
            s.move_to(UP * 1.2)
        self.play(Write(steps[0]))
        self.say("g 자리에 f·h를 넣고, 분자에서 f를 묶으면,", 0.5)
        for a, b in zip(steps, steps[1:]):
            self.play(TransformMatchingShapes(a, b), run_time=1.3)
            self.wait(0.4)
        cur = steps[3]
        b1 = Brace(cur[0], DOWN, color=SW_COL)
        b2 = Brace(cur[2], DOWN, color=H_COL)
        t1 = T("스위치", 28, SW_COL).next_to(b1, DOWN)
        t2 = T("연속 부분", 28, H_COL).next_to(b2, DOWN)
        self.play(GrowFromCenter(b1), GrowFromCenter(b2), FadeIn(t1), FadeIn(t2))
        self.play(Indicate(self.principle, color=SW_COL))
        self.say("또다시 '스위치 × 무언가' 꼴이 나타납니다.")
        self.say("같은 스위치, 같은 원리. 요구는 두 가지.", 1.2)

        r1 = VGroup(
            T("① 스위치 지점 x=1, 2에서 0", 30),
            MathTex(r"\Rightarrow\ h(1)=h(2)=1", font_size=40, color=H_COL),
        ).arrange(RIGHT, buff=0.3)
        r2 = VGroup(
            T("② 어디서도 폭발 금지", 30),
            MathTex(r"\Rightarrow\ h(x)\neq 0", font_size=40, color=H_COL),
        ).arrange(RIGHT, buff=0.3)
        reqs = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(t1, DOWN, buff=0.5)
        reqs.set_x(0)
        self.play(FadeIn(r1, shift=RIGHT * 0.3))
        self.say("첫째, 스위치 지점 1, 2에서 0이어야 한다 → h(1)=h(2)=1.")
        self.play(FadeIn(r2, shift=RIGHT * 0.3))
        self.say("둘째, 어디서도 폭발하면 안 된다 → h는 0이 되면 안 된다.")
        self.reqs = reqs
        self.clear_stage_keep(self.principle)

    # ---------- S4 ----------
    def find_h(self):
        ax = self.axes([-0.5, 3.5, 1], [-1, 4, 1], 6, 4.6).shift(LEFT * 2.6 + DOWN * 0.2)
        fg = ax.plot(f, x_range=[-0.25, 3.25], color=F_COL)
        flab = MathTex("f", color=F_COL, font_size=36).next_to(ax.c2p(3.25, f(3.25)), RIGHT)
        pts = VGroup(*[Dot(ax.c2p(x, 1), color=H_COL, radius=0.08) for x in (1, 2)])
        ptl = MathTex(r"h(1)=h(2)=1", font_size=34, color=H_COL).next_to(ax.c2p(1.5, 1), UP, buff=0.9)
        self.play(Create(ax), Create(fg), FadeIn(flab))
        self.play(FadeIn(pts, scale=2), Write(ptl))

        eq = MathTex(r"h-1", "=", r"(x-1)(x-2)", font_size=44).to_edge(RIGHT, buff=0.6).shift(UP * 1.8)
        eq[0].set_color(H_COL)
        self.play(Write(eq))
        self.say("h−1은 1과 2를 근으로 갖고, 최고차항 계수는 1.")
        eq2 = MathTex(r"h-1", "=", "f", font_size=52).move_to(eq)
        eq2[0].set_color(H_COL)
        eq2[2].set_color(F_COL)
        self.play(TransformMatchingTex(eq, eq2))
        self.say("그렇다면 h−1은 바로 f입니다.", 1.2)

        hg = fg.copy()
        target = ax.plot(lambda x: f(x) + 1, x_range=[-0.25, 3.25], color=H_COL)
        arrow = Arrow(ax.c2p(1.5, -0.25), ax.c2p(1.5, 0.75), buff=0, color=H_COL)
        eq3 = MathTex(r"h", "=", r"f+1", font_size=56).next_to(eq2, DOWN, buff=0.5)
        eq3[0].set_color(H_COL)
        self.play(Transform(hg, target), GrowArrow(arrow), run_time=2)
        hlab = MathTex("h", color=H_COL, font_size=36).next_to(ax.c2p(3.25, f(3.25) + 1), RIGHT)
        self.play(FadeIn(hlab), Write(eq3))
        self.say("즉 h는 f를 위로 1만큼 들어 올린 포물선.")

        bot_f = DashedLine(ax.c2p(-0.5, -0.25), ax.c2p(3.5, -0.25), color=F_COL, stroke_width=2)
        bot_h = DashedLine(ax.c2p(-0.5, 0.75), ax.c2p(3.5, 0.75), color=H_COL, stroke_width=2)
        lf = MathTex(r"-\tfrac14", color=F_COL, font_size=30).next_to(bot_f, LEFT, buff=0.1)
        lh = MathTex(r"\tfrac34", color=H_COL, font_size=30).next_to(bot_h, LEFT, buff=0.1)
        self.play(Create(bot_f), FadeIn(lf), Create(bot_h), FadeIn(lh))
        self.say("f의 바닥은 −1/4. 1을 올리면 바닥은 3/4.")
        ok = MathTex(r"h(x)\ge \tfrac34 > 0", font_size=44, color=H_COL).next_to(eq3, DOWN, buff=0.5)
        check = T("② 자동 해결", 30, H_COL).next_to(ok, DOWN, buff=0.25)
        self.play(Write(ok), FadeIn(check))
        self.say("절대 0에 닿지 않습니다. 둘째 요구는 저절로 해결.")
        self.say("판별식 계산은 필요 없습니다. 그림이 이미 증명했으니까요.")
        self.clear_stage_keep(self.principle)

    # ---------- S5 ----------
    def reveal(self):
        big = MathTex("g", "=", "f", "(", "f", "+1", ")", font_size=96)
        big[0].set_color(G_COL)
        big[2].set_color(F_COL)
        big[4].set_color(F_COL)
        self.play(Write(big), run_time=1.5)
        self.play(Circumscribe(big, color=G_COL))
        self.say("그래서 g의 정체는 g = f(f+1).", 1.5)
        self.play(big.animate.scale(0.55).to_edge(UP, buff=0.5))
        self.say("이제 가면을 벗겨 봅시다.", 1.2)

        m1 = MathTex(r"\frac{g\,|f|}{f}", font_size=52)
        m1b = MathTex(r"|f|\,(f+1)", font_size=52, color=G_COL)
        m2 = MathTex(r"\frac{|g-f|}{g}", font_size=52)
        m2a = MathTex(r"g-f=f^2+f-f=f^2", font_size=40, color=GREY_A)
        m2b = MathTex(r"\frac{f^2}{f(f+1)}=\frac{f}{f+1}", font_size=52, color=G_COL)
        row1 = VGroup(m1, MathTex(r"\longrightarrow"), m1b).arrange(RIGHT, buff=0.4)
        row2 = VGroup(m2, MathTex(r"\longrightarrow"), m2b).arrange(RIGHT, buff=0.4)
        rows = VGroup(row1, row2).arrange(DOWN, buff=0.9, aligned_edge=LEFT).shift(DOWN * 0.2)
        m2a.next_to(row2, UP, buff=0.15).align_to(row2[2], LEFT)

        self.play(FadeIn(m1))
        self.play(Write(row1[1]), Write(m1b))
        self.say("첫 번째 식은 |f|(f+1). 그냥 연속함수입니다.")
        self.play(FadeIn(m2))
        self.play(Write(m2a))
        self.say("두 번째 식: g − f = f². 완전제곱이라 절대값이 필요 없습니다.")
        self.play(Write(row2[1]), Write(m2b))
        self.say("그래서 f/(f+1). 역시 그냥 연속함수.")
        masks = VGroup(*[
            Cross(m, stroke_color=SW_COL, stroke_width=4) for m in (m1, m2)
        ])
        self.play(Create(masks))
        self.say("절대값은 처음부터 가면이었습니다.", 2)
        self.clear_stage_keep(self.principle)

    # ---------- S6 ----------
    def answer(self):
        a1 = MathTex(r"f(-1)=(-2)(-3)=6", font_size=56, color=F_COL)
        a2 = MathTex(r"g(-1)=f(-1)\,\{f(-1)+1\}=6\times 7", font_size=56)
        a3 = MathTex("42", font_size=160, color=G_COL)
        VGroup(a1, a2).arrange(DOWN, buff=0.5).shift(UP * 1.2)
        a3.next_to(a2, DOWN, buff=0.5)
        self.play(Write(a1))
        self.say("f(−1) = (−2)(−3) = 6.", 1.2)
        self.play(Write(a2))
        self.play(FadeIn(a3, scale=0.5))
        self.play(Flash(a3, color=G_COL, line_length=0.5, num_lines=16))
        self.say("그러니 g(−1) = 6 × 7 = 42.", 2)
        self.clear_stage_keep(self.principle)

    # ---------- S7 ----------
    def generalize(self):
        q = MathTex(r"\frac{|g-", "k", r"f|}{g}", font_size=56).to_edge(UP, buff=0.5).shift(RIGHT * 2.5)
        q[1].set_color(SW_COL)
        self.play(Write(q))
        self.say("하나만 더. 문제의 1이 다른 수 k였다면?")

        ax = self.axes([-0.5, 3.5, 1], [-1, 3.5, 1], 6, 4.4).shift(LEFT * 2.6 + DOWN * 0.4)
        k = ValueTracker(1.0)

        def col():
            return H_COL if k.get_value() > 0.25 + 1e-3 else SW_COL

        hg = always_redraw(lambda: ax.plot(
            lambda x: f(x) + k.get_value(), x_range=[-0.1, 3.1], color=col()
        ))
        vertex = always_redraw(lambda: Dot(ax.c2p(1.5, k.get_value() - 0.25), color=col()))
        hk = MathTex("h", "=", "f+", "k", font_size=48).next_to(q, DOWN, buff=0.6)
        hk[3].set_color(SW_COL)
        kv = always_redraw(lambda: MathTex(
            rf"k={k.get_value():.2f}", font_size=44, color=col()
        ).next_to(hk, DOWN, buff=0.5))
        self.play(Create(ax), Create(hg), FadeIn(vertex), Write(hk), FadeIn(kv))
        self.say("같은 논리로 h = f + k. 포물선을 k만큼 올리는 것.")
        self.say("k를 줄여 봅시다.", 0.5)
        self.play(k.animate.set_value(0.25), run_time=3.5, rate_func=linear)
        boom = T("x = 3/2 에서 h = 0  →  극한 붕괴", 28, SW_COL).next_to(kv, DOWN, buff=0.4)
        self.play(Flash(vertex, color=SW_COL), FadeIn(boom))
        self.say("k가 1/4에 닿는 순간, 포물선이 x축에 닿고 극한이 깨집니다.")
        self.play(k.animate.set_value(-0.3), run_time=1.5)
        self.play(k.animate.set_value(1.0), FadeOut(boom), run_time=2.5)

        nl = NumberLine(x_range=[-0.5, 2, 0.25], length=6, include_numbers=False).next_to(kv, DOWN, buff=0.8)
        safe = Line(nl.n2p(0.25), nl.n2p(2), color=H_COL, stroke_width=10)
        hole = Circle(0.08, color=SW_COL).move_to(nl.n2p(0.25))
        q_lab = MathTex(r"\tfrac14", font_size=32, color=SW_COL).next_to(nl.n2p(0.25), DOWN)
        one = Dot(nl.n2p(1), color=G_COL, radius=0.1)
        one_lab = MathTex("1", font_size=36, color=G_COL).next_to(one, UP)
        safe_lab = MathTex(r"k>\tfrac14", font_size=40, color=H_COL).next_to(nl, DOWN, buff=0.6)
        self.play(Create(nl), Create(safe), FadeIn(hole), FadeIn(q_lab), Write(safe_lab))
        self.say("이 문제는 k > 1/4일 때만 성립합니다.")
        self.play(FadeIn(one, scale=2), FadeIn(one_lab))
        self.say("출제자가 고른 1은 이 안전지대 안에 있었던 겁니다.", 2.5)
        self.clear_stage()

    # ---------- S8 ----------
    def summary(self):
        head = T("외울 것은 공식이 아니라 원리 하나", 44, G_COL)
        l1 = T("①  절대값 분수는  '부호 스위치 × 연속 부분' 으로 쪼갠다", 30)
        l2 = T("②  스위치가 바뀌는 곳에서  연속 부분 = 0", 30)
        l3 = T("③  연속 부분은 어디서도 폭발하면 안 된다", 30)
        fin = MathTex(r"g=f(f+1),\qquad g(-1)=42", font_size=52, color=G_COL)
        grp = VGroup(head, l1, l2, l3, fin).arrange(DOWN, buff=0.45).shift(UP * 0.4)
        for line in (l2, l3):
            line.align_to(l1, LEFT)
        self.play(Write(head))
        self.say("외울 것은 공식이 아니라 원리 하나.", 1)
        for line, cap in ((l1, "① 절대값 분수는 '부호 스위치 × 연속 부분'으로 쪼갠다."),
                          (l2, "② 스위치가 바뀌는 곳에서 연속 부분은 0."),
                          (l3, "③ 연속 부분은 어디서도 폭발하면 안 된다.")):
            self.play(FadeIn(line, shift=RIGHT * 0.3))
            self.say(cap)
        self.play(Write(fin))
        self.say("g = f(f+1), 답은 42.", 3)
        self.play(*[FadeOut(m) for m in self.mobjects])
