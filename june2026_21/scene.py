"""2026학년도 6월 모의평가 21번 — '위험한 점을 찾아라' (대본: script.md)

렌더: manim -qh scene.py Killer21
"""
from manim import *

FONT = "Noto Sans CJK KR"
config.background_color = "#0f1117"

F_COL = BLUE_C
G_COL = YELLOW_C
H_COL = GREEN_C
SW_COL = "#ff6b6b"  # 부호 스위치 / 위험
HL_COL = YELLOW

CX = -1.8  # 본문 중심 x (오른쪽은 메모 칸)


def f(x):
    return (x - 1) * (x - 2)


def T(text, size=34, color=WHITE):
    return Text(text, font=FONT, font_size=size, color=color)


def M(tex, size=40, color=WHITE):
    return MathTex(tex, font_size=size, color=color)


def row(*parts, buff=0.15):
    return VGroup(*parts).arrange(RIGHT, buff=buff)


class Killer21(Scene):
    def construct(self):
        self.cap = None
        self.tag = None
        self.hl = None
        self.strip = None
        self.memo_box = None
        self.memo_items = []
        self.opening()
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()
        self.bonus()
        self.summary()

    # ---------- helpers ----------
    def say(self, text, wait=None):
        new = T(text, 32)
        if new.width > 13:
            new.scale_to_fit_width(13)
        new.to_edge(DOWN, buff=0.35)
        bg = BackgroundRectangle(new, color=BLACK, fill_opacity=0.7, buff=0.15)
        new = VGroup(bg, new)
        anims = [FadeIn(new, run_time=0.35)]
        if self.cap is not None:
            anims.append(FadeOut(self.cap, run_time=0.35))
        self.play(*anims)
        self.cap = new
        self.wait(wait if wait is not None else max(2.2, len(text) * 0.12))

    def show(self, *mobs, write=False):
        """요소를 한꺼번에 띄우지 않고 하나씩 순서대로 등장시킨다."""
        for m in mobs:
            if write:
                self.play(Write(m), run_time=0.9)
            else:
                self.play(FadeIn(m, shift=UP * 0.15), run_time=0.6)
            self.wait(0.25)

    def persistent(self):
        fixed = [self.cap, self.tag, self.hl, self.strip, self.memo_box]
        return [m for m in fixed if m is not None] + self.memo_items

    def clear_content(self):
        keep = self.persistent()
        rest = [m for m in self.mobjects if m not in keep]
        if rest:
            self.play(*[FadeOut(m) for m in rest], run_time=0.6)

    def chapter(self, text):
        new = T(text, 26, GREY_A).to_corner(UL, buff=0.3).shift(DOWN * 1.0)
        anims = [FadeIn(new, shift=RIGHT * 0.2)]
        if self.tag is not None:
            anims.append(FadeOut(self.tag))
        self.play(*anims)
        self.tag = new

    def focus(self, part):
        """원문 스트립에서 지금 보고 있는 부분을 하이라이트한다."""
        if part is None:
            if self.hl is not None:
                self.play(FadeOut(self.hl))
                self.hl = None
            return
        new = SurroundingRectangle(part, color=HL_COL, buff=0.08, corner_radius=0.08)
        if self.hl is None:
            self.play(Create(new))
        else:
            self.play(ReplacementTransform(self.hl, new))
        self.hl = new

    def open_memo(self):
        panel = RoundedRectangle(width=3.5, height=5.3, corner_radius=0.15,
                                 stroke_color=GREY_D, fill_color="#161a23", fill_opacity=1)
        panel.move_to(RIGHT * 5.05 + DOWN * 0.3)
        title = T("메모", 26, GREY_A).next_to(panel.get_corner(UL), DR, buff=0.2)
        self.memo_anchor = title
        self.play(FadeIn(panel), FadeIn(title))
        # 하나의 그룹으로 다시 추가해야 clear_content에서 보존된다.
        self.remove(panel, title)
        self.memo_box = VGroup(panel, title)
        self.add(self.memo_box)

    def memo(self, mob):
        """알아낸 사실을 메모 칸에 남긴다. 이후 화면이 바뀌어도 계속 보인다."""
        if mob.width > 3.1:
            mob.scale_to_fit_width(3.1)
        last = self.memo_items[-1] if self.memo_items else self.memo_anchor
        mob.next_to(last, DOWN, buff=0.2).align_to(self.memo_anchor, LEFT)
        self.play(FadeIn(mob, shift=RIGHT * 0.3))
        self.play(Indicate(mob, color=HL_COL, scale_factor=1.08))
        self.memo_items.append(mob)

    def axes(self, x_range, y_range, width, height):
        return Axes(
            x_range=x_range, y_range=y_range,
            x_length=width, y_length=height,
            axis_config={"color": GREY_B, "include_ticks": True, "tick_size": 0.05},
            tips=False,
        )

    def ticks(self, ax, xs):
        return VGroup(*[M(str(n), 24).next_to(ax.c2p(n, 0), DOWN, buff=0.12) for n in xs])

    # ---------- 오프닝 ----------
    def opening(self):
        title = T("위험한 점을 찾아라", 64, G_COL)
        sub = T("2026학년도 6월 모의평가 21번", 30, GREY_B).next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(sub))

        given = M(r"f(x)=(x-1)(x-2)", 40, F_COL)
        g_desc = T("g(x): 최고차항의 계수가 1인 사차함수", 28, G_COL)
        lim1 = M(r"\lim_{x\to a}\frac{g(x)\,|f(x)|}{f(x)}", 44)
        lim2 = M(r"\lim_{x\to a}\frac{|g(x)-f(x)|}{g(x)}", 44)
        lims = VGroup(lim1, lim2).arrange(RIGHT, buff=1.0)
        cond_a = T("모든 실수 a에 대하여 두 극한이 ", 28)
        cond_b = T("모두 존재", 28, G_COL)
        cond = VGroup(cond_a, cond_b).arrange(RIGHT, buff=0.05)
        ask = M(r"g(-1)=\ ?", 44, G_COL)
        VGroup(given, g_desc, lims, cond, ask).arrange(DOWN, buff=0.35).shift(UP * 0.5)
        src = T("출처: 2026학년도 6월 모의평가 수학 21번 (한국교육과정평가원)", 18, GREY_C)
        src.to_corner(UR, buff=0.25)
        self.play(FadeIn(src))
        self.show(given, g_desc, lim1, lim2, cond, ask)
        self.say("오늘 문제는 이것입니다.")
        self.say("절대값 두 개, 극한 두 개. 처음 보면 막막하죠.")
        self.say("그런데 하나만 물어봅시다.", 1.5)
        box = SurroundingRectangle(cond_b, color=HL_COL, buff=0.08)
        self.play(Create(box))
        self.say("극한이 '존재한다'는 말을, 왜 굳이 했을까?")
        self.say("웬만한 점에서는 극한이 당연히 존재합니다.")
        signal = T("→ 어딘가에 '위험한 점'이 있다!", 34, SW_COL).next_to(ask, DOWN, buff=0.4)
        self.play(FadeIn(signal, shift=UP * 0.2))
        self.say("그러니 이 조건은 '위험한 점'이 따로 있다는 신호입니다.")

        # 원문을 상단 스트립으로 접어 둔다.
        s1 = M(r"\lim_{x\to a}\frac{g(x)\,|f(x)|}{f(x)}", 30)
        s2 = M(r"\lim_{x\to a}\frac{|g(x)-f(x)|}{g(x)}", 30)
        s3 = T("모든 a에서 존재", 22, GREY_A)
        s4 = M(r"g(-1)=?", 30, G_COL)
        VGroup(s1, s2, s3, s4).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.2)
        line = Line(LEFT * 7, RIGHT * 7, color=GREY_D, stroke_width=1).next_to(s1, DOWN, buff=0.12)
        self.play(
            FadeOut(src), FadeOut(signal), FadeOut(box), FadeOut(given), FadeOut(g_desc),
            FadeOut(cond), FadeOut(ask),
            ReplacementTransform(lim1, s1), ReplacementTransform(lim2, s2),
            FadeIn(s3), FadeIn(s4), Create(line),
        )
        # 개별로 추가된 조각들을 하나의 그룹으로 묶어 clear_content에서 보존되게 한다.
        self.remove(s1, s2, s3, s4, line)
        self.strip = VGroup(s1, s2, s3, s4, line)
        self.add(self.strip)
        self.say("오늘은 그 위험한 점을 찾아갑니다.")

    # ---------- STEP 1 ----------
    def step1(self):
        self.chapter("STEP 1 · 평범한 점과 위험한 점")
        self.open_memo()
        self.focus(self.strip[0])
        self.say("첫 번째 식부터 봅시다.", 1.5)

        e = MathTex(r"\frac{g(x)\,|f(x)|}{f(x)}", "=", "g(x)", r"\times", r"\frac{|f(x)|}{f(x)}",
                    font_size=56).move_to(RIGHT * CX + UP * 0.6)
        e[2].set_color(G_COL)
        self.show(e[0])
        self.show(e[1], e[2], e[3], e[4], write=True)
        self.say("g(x)는 다항함수라 얌전합니다.", 1.8)
        self.play(e[4].animate.set_color(SW_COL))
        self.play(Circumscribe(e[4], color=SW_COL))
        self.say("신경 쓰이는 건 |f(x)|/f(x).", 1.8)
        self.play(e.animate.scale(0.6).move_to(RIGHT * CX + UP * 1.9))

        ax = self.axes([-0.5, 3.5, 1], [-1.5, 3, 1], 4.4, 3.6).move_to(LEFT * 4.6 + DOWN * 0.7)
        fg = ax.plot(f, x_range=[-0.25, 3.25], color=F_COL)
        flab = M("y=f(x)", 28, F_COL).next_to(ax.c2p(3.2, 2.7), LEFT)
        self.show(ax, self.ticks(ax, (1, 2, 3)))
        self.play(Create(fg), run_time=1.2)
        self.show(flab)

        tx = 0.55  # 오른쪽 설명 열의 중심 x
        band3 = Rectangle(width=ax.x_axis.unit_size * 0.6, height=3.6, stroke_width=0,
                          fill_color=WHITE, fill_opacity=0.08).move_to(ax.c2p(3, 0.75))
        self.play(FadeIn(band3))
        h3 = T("x = 3 근처 (평범한 점)", 26, GREY_A)
        a1 = M(r"f(x)>0\ \Rightarrow\ \frac{|f(x)|}{f(x)}=1", 34)
        a2 = M(r"\frac{g(x)\,|f(x)|}{f(x)}=g(x)", 34)
        a3 = M(r"\lim_{x\to3}\ =\ g(3)", 34, H_COL)
        blk3 = VGroup(h3, a1, a2, a3).arrange(DOWN, buff=0.3).move_to(RIGHT * tx + DOWN * 0.5)
        self.show(h3)
        self.say("먼저 평범한 점, x=3 근처를 봅시다.", 1.5)
        self.show(a1, a2)
        self.say("여기서는 f(x)가 양수라 |f(x)|/f(x)=1. 식은 그냥 g(x)입니다.")
        self.show(a3)
        self.say("그러니 극한은 g(3). 아무 일도 일어나지 않습니다.")
        self.play(FadeOut(blk3), FadeOut(band3))

        band15 = band3.copy().move_to(ax.c2p(1.5, 0.75))
        self.play(FadeIn(band15))
        h15 = T("x = 1.5 근처", 26, GREY_A)
        b1 = M(r"f(x)<0\ \Rightarrow\ \frac{|f(x)|}{f(x)}=-1", 34)
        blk15 = VGroup(h15, b1).arrange(DOWN, buff=0.3).move_to(RIGHT * tx + DOWN * 0.2)
        self.show(h15, b1)
        self.say("이번엔 x=1.5 근처. f(x)가 음수라 |f(x)|/f(x)=−1.")
        self.play(FadeOut(band15))

        signs = VGroup(
            M("+", 36, SW_COL).move_to(ax.c2p(0.3, 0.7)),
            M("-", 36, SW_COL).move_to(ax.c2p(1.5, 0.7)),
            M("+", 36, SW_COL).move_to(ax.c2p(2.7, 0.7)),
        )
        self.show(*signs)
        self.say("즉 |f(x)|/f(x)는 f(x)의 부호에 따라 1 또는 −1.")

        pieces = [
            ax.plot(lambda x: 1, x_range=[-0.5, 0.97], color=SW_COL, stroke_width=6),
            ax.plot(lambda x: -1, x_range=[1.03, 1.97], color=SW_COL, stroke_width=6),
            ax.plot(lambda x: 1, x_range=[2.03, 3.5], color=SW_COL, stroke_width=6),
        ]
        self.play(fg.animate.set_stroke(opacity=0.25), flab.animate.set_opacity(0.25),
                  FadeOut(signs), FadeOut(blk15))
        for p in pieces:
            self.play(Create(p), run_time=0.6)
        sw_lab = M(r"y=\frac{|f(x)|}{f(x)}", 30, SW_COL).move_to(RIGHT * tx + UP * 0.2)
        self.show(sw_lab)
        self.say("g(x)에 1이나 −1을 곱하는 스위치인 셈이죠.")

        for x in (1, 2):
            self.play(Create(DashedLine(ax.c2p(x, -1), ax.c2p(x, 1), color=SW_COL)),
                      FadeIn(Dot(ax.c2p(x, 0), color=SW_COL, radius=0.1), scale=2), run_time=0.7)
        self.say("이 스위치가 뒤집히는 곳은 f(x)의 부호가 바뀌는 x=1, x=2뿐.")
        warn = T("위험한 점!", 34, SW_COL).next_to(ax.c2p(1.5, -1.5), DOWN, buff=0.1)
        self.show(warn)
        self.say("바로 여기가 위험한 점입니다. 메모해 둡시다.", 1.0)
        self.memo(row(T("위험한 점", 24, SW_COL), M(r"x=1,\ 2", 32, SW_COL), buff=0.2))
        self.wait(1)
        self.clear_content()

    # ---------- STEP 2 ----------
    def step2(self):
        self.chapter("STEP 2 · x=1에서 무슨 일이?")
        ax = self.axes([0, 2, 0.5], [-3, 3, 1], 4.6, 4.0).move_to(LEFT * 4.3 + DOWN * 0.5)
        x1 = DashedLine(ax.c2p(1, -3), ax.c2p(1, 3), color=GREY_C)
        x1_lab = M("x=1", 26, GREY_A).next_to(ax.c2p(1, -3), DOWN, buff=0.1)
        self.show(ax, x1, x1_lab)
        self.say("x=1 근처를 확대해 봅시다.", 1.5)

        lsign = VGroup(M(r"f(x)>0", 26, F_COL), M(r"g(x)\times(+1)", 30, SW_COL)).arrange(DOWN, buff=0.1)
        lsign.move_to(ax.c2p(0.5, 2.4))
        rsign = VGroup(M(r"f(x)<0", 26, F_COL), M(r"g(x)\times(-1)", 30, SW_COL)).arrange(DOWN, buff=0.1)
        rsign.move_to(ax.c2p(1.5, 2.4))
        self.show(lsign)
        self.say("x=1의 왼쪽에서는 f(x)>0, 그래서 g(x)×(+1).")
        self.show(rsign)
        self.say("오른쪽에서는 f(x)<0, 그래서 g(x)×(−1).")

        tx = 0.7
        l_lim = M(r"\lim_{x\to1-}=\ g(1)", 36).move_to(RIGHT * tx + UP * 1.2)
        r_lim = M(r"\lim_{x\to1+}=\ -g(1)", 36).next_to(l_lim, DOWN, buff=0.35)
        self.show(l_lim, r_lim)
        self.say("그러면 좌극한은 g(1), 우극한은 −g(1).")

        c = ValueTracker(2.0)

        def g_near(x):
            return c.get_value() + 1.2 * (x - 1)

        left = always_redraw(lambda: ax.plot(g_near, x_range=[0.05, 0.99], color=G_COL, stroke_width=6))
        right = always_redraw(lambda: ax.plot(lambda x: -g_near(x), x_range=[1.01, 1.95], color=G_COL, stroke_width=6))
        el = always_redraw(lambda: Circle(0.09, color=G_COL).move_to(ax.c2p(1, c.get_value())))
        er = always_redraw(lambda: Circle(0.09, color=G_COL).move_to(ax.c2p(1, -c.get_value())))
        cval = always_redraw(lambda: M(rf"g(1)={c.get_value():.1f}", 36, G_COL).next_to(r_lim, DOWN, buff=0.5))
        self.show(cval)
        self.play(Create(left))
        self.play(FadeIn(el))
        self.play(Create(right))
        self.play(FadeIn(er))
        tear = T("찢어짐 → 극한 없음", 28, SW_COL).next_to(cval, DOWN, buff=0.35)
        self.show(tear)
        self.say("만약 g(1)=2라면? 2와 −2로 찢어져 극한이 없습니다.")

        self.play(FadeOut(tear))
        eq = M(r"g(1)=-g(1)", 40, G_COL).next_to(cval, DOWN, buff=0.35)
        self.show(eq, write=True)
        self.play(c.animate.set_value(0), run_time=3)
        eq0 = M(r"g(1)=0", 44, H_COL).move_to(eq)
        self.play(ReplacementTransform(eq, eq0))
        self.say("둘이 같으려면 g(1) = −g(1), 즉 g(1)=0.")
        self.say("x=2에서도 같은 이유로 g(2)=0. 메모.", 1.0)
        self.memo(M(r"g(1)=0,\ \ g(2)=0", 32, H_COL))
        self.wait(0.5)
        self.clear_content()

        rule_a = T("부호가 뒤집히는 곳에서는", 38)
        rule_b = T("곱해진 값 = 0", 44, G_COL)
        rule = VGroup(rule_a, rule_b).arrange(DOWN, buff=0.35).move_to(RIGHT * CX)
        frame = SurroundingRectangle(rule, color=SW_COL, buff=0.4, corner_radius=0.15)
        self.play(Create(frame))
        self.show(rule_a, rule_b)
        self.say("이걸 규칙으로 남겨 둡시다. 부호가 뒤집히는 곳에서는, 곱해진 값이 0이어야 한다.", 1.0)
        rule_memo = VGroup(
            T("규칙", 22, SW_COL),
            T("부호가 뒤집히는 곳에서", 22),
            T("곱해진 값 = 0", 22, G_COL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        self.memo(rule_memo)
        self.rule_memo = rule_memo
        self.wait(0.5)
        self.clear_content()

    # ---------- STEP 3 ----------
    def step3(self):
        self.chapter("STEP 3 · g(x)의 절반이 정해진다")
        a = M(r"g(1)=0,\quad g(2)=0", 46, H_COL).move_to(RIGHT * CX + UP * 1.4)
        self.show(a)
        b = MathTex("g(x)", "=", r"(x-1)(x-2)", r"\,", "h(x)", font_size=52)
        b.next_to(a, DOWN, buff=0.6).set_x(CX)
        b[0].set_color(G_COL)
        b[4].set_color(H_COL)
        self.show(b[0], b[1], b[2], b[4], write=True)
        self.say("g(1)=0, g(2)=0이니 g(x)는 (x−1)(x−2)를 인수로 가집니다.")
        brace = Brace(b[2], DOWN, color=F_COL)
        bf = M("f(x)", 44, F_COL).next_to(brace, DOWN)
        self.play(GrowFromCenter(brace))
        self.play(b[2].animate.set_color(F_COL), FadeIn(bf))
        self.say("그런데 (x−1)(x−2)는 바로 f(x).", 1.8)

        c = MathTex("g(x)", "=", "f(x)", r"\,", "h(x)", font_size=72)
        c[0].set_color(G_COL)
        c[2].set_color(F_COL)
        c[4].set_color(H_COL)
        c.move_to(RIGHT * CX)
        self.play(FadeOut(a), FadeOut(brace), FadeOut(bf), ReplacementTransform(b, c))
        hn = T("h(x): 최고차항 계수가 1인 이차함수", 26, H_COL).next_to(c, DOWN, buff=0.5)
        self.show(hn)
        self.say("그래서 g(x)=f(x)h(x). h(x)는 최고차항 계수가 1인 이차함수.", 1.0)
        self.memo(VGroup(
            M(r"g(x)=f(x)\,h(x)", 32, G_COL),
            T("h(x): 최고차항 계수 1인 이차", 18, H_COL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08))

        done = T("확정", 26, F_COL).next_to(c[2], UP, buff=0.35)
        q = T("?", 44, H_COL).next_to(c[4], UP, buff=0.25)
        self.show(done, q)
        self.say("첫 번째 식으로 g(x)의 절반이 정해졌습니다.")
        self.focus(self.strip[1])
        self.say("나머지 h(x)는 두 번째 식이 정할 차례입니다.")
        self.clear_content()

    # ---------- STEP 4 ----------
    def step4(self):
        self.chapter("STEP 4 · 두 번째 식에 숨은 같은 스위치")
        e0 = M(r"\frac{|g(x)-f(x)|}{g(x)}", 56).move_to(RIGHT * CX + UP * 1.4)
        self.show(e0, write=True)
        e1 = M(r"\frac{|f(x)h(x)-f(x)|}{f(x)h(x)}", 56).move_to(e0)
        self.play(TransformMatchingShapes(e0, e1), run_time=1.3)
        self.say("두 번째 식에 g(x)=f(x)h(x)를 넣어 봅시다.")

        n1 = row(T("분자", 26, GREY_A), M(r"f(x)h(x)-f(x)=f(x)\{h(x)-1\}", 36), buff=0.25)
        n2 = M(r"\Rightarrow\ |f(x)|\,|h(x)-1|", 36)
        d1 = row(T("분모", 26, GREY_A), M(r"f(x)\,h(x)", 36), buff=0.25)
        VGroup(n1, n2, d1).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(e1, DOWN, buff=0.5).set_x(CX)
        self.show(n1)
        self.say("분자는 f(x)h(x) − f(x) = f(x){h(x)−1}.")
        self.show(n2)
        self.say("절대값을 나누면 |f(x)|·|h(x)−1|.")
        self.show(d1)
        self.say("분모는 f(x)h(x).", 1.8)

        e3 = MathTex(r"\frac{|f(x)|}{f(x)}", r"\quad\times\quad", r"\frac{|h(x)-1|}{h(x)}", font_size=60)
        e3.move_to(RIGHT * CX + UP * 1.1)
        self.play(FadeOut(n1), FadeOut(n2), FadeOut(d1), FadeOut(e1))
        self.show(e3[0], e3[1], e3[2], write=True)
        self.say("정리하면 |f(x)|/f(x) × |h(x)−1|/h(x).")

        self.play(e3[0].animate.set_color(SW_COL))
        b1 = Brace(e3[0], DOWN, color=SW_COL)
        t1 = T("아까 그 스위치!", 26, SW_COL).next_to(b1, DOWN)
        self.play(GrowFromCenter(b1))
        self.show(t1)
        self.play(Circumscribe(e3[0], color=SW_COL))
        self.say("아까 그 스위치, |f(x)|/f(x)가 또 나왔습니다!")

        self.play(e3[2].animate.set_color(G_COL))
        b2 = Brace(e3[2], DOWN, color=G_COL)
        t2 = T("곱해진 값", 26, G_COL).next_to(b2, DOWN)
        self.play(GrowFromCenter(b2))
        self.show(t2)
        self.play(Indicate(self.rule_memo, color=HL_COL, scale_factor=1.08))
        self.say("그러면 메모해 둔 규칙 그대로. x=1, 2에서 |h(x)−1|/h(x)가 0이어야 합니다.")
        r1 = M(r"h(1)=1,\quad h(2)=1", 44, H_COL).next_to(VGroup(t1, t2), DOWN, buff=0.5).set_x(CX)
        self.show(r1, write=True)
        self.say("그래서 h(1)=1, h(2)=1.", 1.0)
        self.memo(M(r"h(1)=1,\ \ h(2)=1", 32, H_COL))

        den = e3[2][-4:]  # 분모 h(x)
        self.play(Circumscribe(den, color=SW_COL))
        self.say("그리고 분모 h(x)가 0이 되는 곳이 있으면 식이 터집니다.")
        r2 = M(r"h(x)\neq 0", 44, H_COL).next_to(r1, DOWN, buff=0.3)
        self.show(r2, write=True)
        self.say("그러니 h(x)는 어디서도 0이 되면 안 됩니다.", 1.0)
        self.memo(M(r"h(x)\neq 0", 32, H_COL))
        self.wait(0.5)
        self.clear_content()

    # ---------- STEP 5 ----------
    def step5(self):
        self.chapter("STEP 5 · h(x) 구하기")
        self.focus(None)
        l1 = M(r"h(1)-1=0,\quad h(2)-1=0", 40)
        l2 = M(r"h(x)-1=(x-1)(x-2)", 40)
        l3 = M(r"h(x)=(x-1)(x-2)+1", 40, H_COL)
        l4 = M(r"=x^2-3x+3", 40, H_COL)
        VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.35).move_to(RIGHT * CX + UP * 0.6)
        l4.align_to(l3[0][4], LEFT)
        self.show(l1)
        self.say("h(1)=1, h(2)=1이니 h(x)−1은 x=1, 2에서 0.")
        self.show(l2)
        self.say("최고차항 계수가 1이니 h(x)−1=(x−1)(x−2).")
        self.show(l3)
        self.say("즉 h(x)=(x−1)(x−2)+1.", 1.8)
        self.show(l4)
        self.say("전개하면 x²−3x+3.", 1.8)

        self.play(FadeOut(l1), FadeOut(l2), VGroup(l3, l4).animate.shift(UP * 1.3))
        dd = M(r"D=(-3)^2-4\cdot3=9-12=-3<0", 40).next_to(l4, DOWN, buff=0.5).set_x(CX)
        self.show(dd, write=True)
        self.say("이제 h(x)≠0인지 확인. 판별식 D = 9 − 12 = −3 < 0.")
        ok = T("실근 없음 → h(x)는 0이 되지 않는다", 28, H_COL).next_to(dd, DOWN, buff=0.4).set_x(CX)
        self.show(ok)
        self.say("실근이 없으니 h(x)는 0이 되지 않습니다. 통과!", 1.0)
        self.memo(M(r"h(x)=f(x)+1\ \checkmark", 32, H_COL))
        self.wait(0.5)
        self.clear_content()

        ax = self.axes([-0.5, 3.5, 1], [-1, 3.5, 1], 5.2, 4.2).move_to(RIGHT * CX + DOWN * 0.5)
        fg = ax.plot(f, x_range=[-0.1, 3.1], color=F_COL)
        flab = M("f(x)", 30, F_COL).next_to(ax.c2p(3.1, f(3.1)), RIGHT)
        self.show(ax, self.ticks(ax, (1, 2, 3)))
        self.play(Create(fg))
        self.show(flab)
        hg = fg.copy()
        target = ax.plot(lambda x: f(x) + 1, x_range=[-0.1, 3.1], color=H_COL)
        arrows = [Arrow(ax.c2p(x, f(x)), ax.c2p(x, f(x) + 1), buff=0.05, color=H_COL) for x in (1, 1.5, 2)]
        for a in arrows:
            self.play(GrowArrow(a), run_time=0.5)
        self.play(Transform(hg, target), run_time=2)
        hlab = M("h(x)", 30, H_COL).next_to(ax.c2p(3.1, f(3.1) + 1), RIGHT)
        self.play(FadeIn(hlab), *[FadeOut(a) for a in arrows])
        self.say("그림으로 보면, h(x)는 f(x)를 위로 1만큼 올린 것.")

        bot_f = DashedLine(ax.c2p(-0.5, -0.25), ax.c2p(3.5, -0.25), color=F_COL, stroke_width=2)
        lf = M(r"-\tfrac14", 28, F_COL).next_to(bot_f, LEFT, buff=0.1)
        bot_h = DashedLine(ax.c2p(-0.5, 0.75), ax.c2p(3.5, 0.75), color=H_COL, stroke_width=2)
        lh = M(r"\tfrac34", 28, H_COL).next_to(bot_h, LEFT, buff=0.1)
        self.play(Create(bot_f), FadeIn(lf))
        self.play(Create(bot_h), FadeIn(lh))
        self.say("f(x)의 바닥 −1/4이 3/4으로 올라가 x축에 닿지 않죠.")
        self.clear_content()

    # ---------- STEP 6 ----------
    def step6(self):
        self.chapter("STEP 6 · 답")
        self.focus(self.strip[3])
        big = M(r"g(x)=f(x)\{f(x)+1\}", 60, G_COL).move_to(RIGHT * CX + UP * 1.2)
        self.show(big, write=True)
        self.say("정리하면 g(x)=f(x){f(x)+1}.")
        a1 = M(r"f(-1)=(-2)(-3)=6", 48, F_COL).next_to(big, DOWN, buff=0.5).set_x(CX)
        self.show(a1, write=True)
        self.say("f(−1) = (−2)(−3) = 6.")
        a2 = MathTex(r"g(-1)=6\times 7=", "42", font_size=60).next_to(a1, DOWN, buff=0.5).set_x(CX)
        a2[1].set_color(G_COL).scale(1.4)
        self.show(a2[0], write=True)
        self.play(FadeIn(a2[1], scale=0.5))
        self.play(Flash(a2[1], color=G_COL, line_length=0.4, num_lines=16))
        self.say("그러니 g(−1) = 6 × 7 = 42.", 2.5)
        self.clear_content()

    # ---------- 보너스 ----------
    def bonus(self):
        self.chapter("보너스 · 출제자는 왜 하필 1을 썼을까")
        self.focus(self.strip[1])
        tx = 0.9
        q = MathTex(r"\frac{|g(x)-", "k", r"f(x)|}{g(x)}", font_size=48).move_to(RIGHT * tx + UP * 1.6)
        q[1].set_color(SW_COL)
        self.show(q, write=True)
        self.say("마지막으로, 문제의 1이 다른 수 k였다면?")

        ax = self.axes([-0.5, 3.5, 1], [-1, 3.5, 1], 4.6, 4.2).move_to(LEFT * 4.3 + DOWN * 0.5)
        k = ValueTracker(1.0)

        def col():
            return H_COL if k.get_value() > 0.25 + 1e-3 else SW_COL

        hg = always_redraw(lambda: ax.plot(
            lambda x: f(x) + k.get_value(), x_range=[-0.1, 3.1], color=col()
        ))
        vertex = always_redraw(lambda: Dot(ax.c2p(1.5, k.get_value() - 0.25), color=col()))
        hk = MathTex("h(x)", "=", "f(x)+", "k", font_size=44).next_to(q, DOWN, buff=0.4)
        hk[3].set_color(SW_COL)
        kv = always_redraw(lambda: M(rf"k={k.get_value():.2f}", 40, col()).next_to(hk, DOWN, buff=0.3))
        self.show(ax)
        self.show(hk, write=True)
        self.play(Create(hg), FadeIn(vertex))
        self.show(kv)
        self.say("같은 논리로 h(x) = f(x) + k. 포물선을 k만큼 올리는 겁니다.")
        self.say("k를 줄여 보면…", 0.5)
        self.play(k.animate.set_value(0.25), run_time=3.5, rate_func=linear)
        boom = T("h(x)=0인 곳 발생 → 극한 붕괴", 24, SW_COL).next_to(kv, DOWN, buff=0.3)
        self.play(Flash(vertex, color=SW_COL))
        self.show(boom)
        self.say("1/4에서 바닥이 x축에 닿습니다. h(x)=0인 곳이 생기고 극한이 깨집니다.")
        self.play(k.animate.set_value(1.0), FadeOut(boom), run_time=2)

        nl = NumberLine(x_range=[-0.5, 2, 0.25], length=4.2, include_numbers=False).next_to(kv, DOWN, buff=0.7)
        safe = Line(nl.n2p(0.25), nl.n2p(2), color=H_COL, stroke_width=10)
        hole = Circle(0.08, color=SW_COL).move_to(nl.n2p(0.25))
        q_lab = M(r"\tfrac14", 30, SW_COL).next_to(nl.n2p(0.25), DOWN)
        one = Dot(nl.n2p(1), color=G_COL, radius=0.1)
        one_lab = M("1", 34, G_COL).next_to(one, UP)
        self.show(nl)
        self.play(Create(safe), FadeIn(hole), FadeIn(q_lab))
        self.play(FadeIn(one, scale=2), FadeIn(one_lab))
        self.say("이 문제는 k > 1/4일 때만 답이 있습니다. 1은 안전한 선택이었던 거죠.", 3)
        self.focus(None)
        self.clear_content()

    # ---------- 정리 ----------
    def summary(self):
        self.play(*[FadeOut(m) for m in [self.tag, self.strip, self.memo_box] + self.memo_items])
        self.tag = self.strip = self.memo_box = None
        self.memo_items = []
        head = T("오늘 쓴 도구는 딱 하나", 44, G_COL)
        l1 = T("①  |f(x)|/f(x) 는 부호 스위치", 32)
        l2 = T("②  스위치가 뒤집히는 곳에서는  곱해진 값 = 0", 32)
        l3 = T("③  분모는 어디서도 0이 되면 안 된다", 32)
        fin = M(r"g(x)=f(x)\{f(x)+1\},\qquad g(-1)=42", 48, G_COL)
        VGroup(head, l1, l2, l3, fin).arrange(DOWN, buff=0.45).shift(UP * 0.4)
        for line in (l2, l3):
            line.align_to(l1, LEFT)
        VGroup(l1, l2, l3).set_x(0)
        self.show(head, write=True)
        self.say("오늘 쓴 도구는 딱 하나.", 1.5)
        for line, cap in ((l1, "① |f(x)|/f(x)는 부호 스위치."),
                          (l2, "② 스위치가 뒤집히는 곳에서는 곱해진 값이 0."),
                          (l3, "③ 분모는 어디서도 0이 되면 안 된다.")):
            self.show(line)
            self.say(cap)
        self.show(fin, write=True)
        self.say("g(x) = f(x){f(x)+1}, 답은 42.", 3)
        self.play(*[FadeOut(m) for m in self.mobjects])
