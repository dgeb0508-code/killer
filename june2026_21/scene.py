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


def f(x):
    return (x - 1) * (x - 2)


def T(text, size=34, color=WHITE):
    return Text(text, font=FONT, font_size=size, color=color)


def sgn_f(x):
    return 1 if f(x) > 0 else -1


class Killer21(Scene):
    def construct(self):
        self.cap = None
        self.tag = None
        self.hl = None
        self.strip = None
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

    def persistent(self):
        return [m for m in (self.cap, self.tag, self.hl, self.strip) if m is not None]

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

    def axes(self, x_range, y_range, width, height):
        return Axes(
            x_range=x_range, y_range=y_range,
            x_length=width, y_length=height,
            axis_config={"color": GREY_B, "include_ticks": True, "tick_size": 0.05},
            tips=False,
        )

    def lim1_tex(self, size):
        return MathTex(r"\lim_{x\to a}\frac{g(x)\,|f(x)|}{f(x)}", font_size=size)

    def lim2_tex(self, size):
        return MathTex(r"\lim_{x\to a}\frac{|g(x)-f(x)|}{g(x)}", font_size=size)

    # ---------- 오프닝 ----------
    def opening(self):
        title = T("위험한 점을 찾아라", 64, G_COL)
        sub = T("2026학년도 6월 모의평가 21번", 30, GREY_B).next_to(title, DOWN)
        self.play(Write(title), FadeIn(sub, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(sub))

        given = MathTex(r"f(x)=(x-1)(x-2)", font_size=40, color=F_COL)
        g_desc = T("g(x): 최고차항의 계수가 1인 사차함수", 28, G_COL)
        lims = VGroup(self.lim1_tex(44), self.lim2_tex(44)).arrange(RIGHT, buff=1.0)
        cond_a = T("모든 실수 a에 대하여 두 극한이 ", 28)
        cond_b = T("모두 존재", 28, G_COL)
        cond = VGroup(cond_a, cond_b).arrange(RIGHT, buff=0.05)
        ask = MathTex(r"g(-1)=\ ?", font_size=44, color=G_COL)
        prob = VGroup(given, g_desc, lims, cond, ask).arrange(DOWN, buff=0.35).shift(UP * 0.5)
        src = T("출처: 2026학년도 6월 모의평가 수학 21번 (한국교육과정평가원)", 18, GREY_C)
        src.to_corner(UR, buff=0.25)
        self.play(FadeIn(src), FadeIn(prob, shift=UP * 0.2), run_time=1.2)
        self.say("오늘 문제는 이것입니다.")
        self.say("절대값 두 개, 극한 두 개. 처음 보면 막막하죠.")
        self.say("그런데 하나만 물어봅시다.", 1.5)
        box = SurroundingRectangle(cond_b, color=HL_COL, buff=0.08)
        self.play(Create(box))
        self.say("극한이 '존재한다'는 말을, 왜 굳이 했을까?")
        self.say("웬만한 점에서는 극한이 당연히 존재합니다.")
        signal = T("→ 어딘가에 '위험한 점'이 있다!", 34, SW_COL).next_to(prob, DOWN, buff=0.4)
        self.play(FadeIn(signal, shift=UP * 0.2))
        self.say("그러니 이 조건은 '위험한 점'이 따로 있다는 신호입니다.")

        # 원문을 상단 스트립으로 접어 둔다.
        s1 = self.lim1_tex(30)
        s2 = self.lim2_tex(30)
        s3 = T("모든 a에서 존재", 22, GREY_A)
        s4 = MathTex(r"g(-1)=?", font_size=30, color=G_COL)
        strip = VGroup(s1, s2, s3, s4).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.2)
        line = Line(LEFT * 7, RIGHT * 7, color=GREY_D, stroke_width=1).next_to(strip, DOWN, buff=0.12)
        self.play(
            FadeOut(src), FadeOut(signal), FadeOut(box), FadeOut(given), FadeOut(g_desc),
            FadeOut(cond), FadeOut(ask),
            ReplacementTransform(lims[0], s1), ReplacementTransform(lims[1], s2),
            FadeIn(s3), FadeIn(s4), Create(line),
        )
        # 개별로 추가된 조각들을 하나의 그룹으로 묶어 clear_content에서 보존되게 한다.
        self.remove(s1, s2, s3, s4, line)
        self.strip = VGroup(s1, s2, s3, s4, line)
        self.add(self.strip)
        self.say("오늘은 그 위험한 점을 찾아갑니다.")

    # ---------- STEP 1 ----------
    def step1(self):
        s1 = self.strip[0]
        self.chapter("STEP 1 · 첫 번째 식의 정체")
        self.focus(s1)
        self.say("첫 번째 식부터 봅시다.", 1.5)

        e = MathTex(r"\frac{g\,|f|}{f}", "=", "g", r"\cdot", r"\frac{|f|}{f}", font_size=64)
        e[2].set_color(G_COL)
        self.play(Write(e))
        self.say("g는 그냥 다항함수라 얌전합니다.", 1.8)
        self.play(e[4].animate.set_color(SW_COL), Circumscribe(e[4], color=SW_COL))
        self.say("수상한 건 |f|/f.", 1.8)
        self.play(e.animate.scale(0.6).move_to(UP * 1.75 + RIGHT * 3.3))

        ax = self.axes([-0.5, 3.5, 1], [-1.5, 3, 1], 5.6, 4.2).move_to(LEFT * 3.2 + DOWN * 0.45)
        nums = VGroup(*[MathTex(str(n), font_size=26).next_to(ax.c2p(n, 0), DOWN, buff=0.12) for n in (1, 2, 3)])
        fg = ax.plot(f, x_range=[-0.25, 3.25], color=F_COL)
        flab = MathTex("y=f(x)", color=F_COL, font_size=30).next_to(ax.c2p(3.2, 2.7), LEFT)
        self.play(Create(ax), FadeIn(nums), Create(fg), FadeIn(flab))

        d3 = Dot(ax.c2p(3, 2), color=WHITE)
        n3 = MathTex(r"x=3:\quad \frac{|2|}{2}=", "1", font_size=44).move_to(RIGHT * 3.3 + UP * 0.4)
        n3[1].set_color(SW_COL)
        self.play(FadeIn(d3, scale=2), Write(n3))
        self.say("숫자를 넣어 봅시다. x=3이면 f=2, 그래서 |2|/2 = 1.")
        d15 = Dot(ax.c2p(1.5, -0.25), color=WHITE)
        n15 = MathTex(r"x=1.5:\quad \frac{|-\frac14|}{-\frac14}=", "-1", font_size=44).next_to(n3, DOWN, buff=0.5)
        n15[1].set_color(SW_COL)
        self.play(FadeIn(d15, scale=2), Write(n15))
        self.say("x=1.5이면 f = −1/4, 그래서 |f|/f = −1.")

        signs = VGroup(
            MathTex("+", color=SW_COL).move_to(ax.c2p(0.3, 0.6)),
            MathTex("-", color=SW_COL).move_to(ax.c2p(1.5, 0.6)),
            MathTex("+", color=SW_COL).move_to(ax.c2p(2.7, 0.6)),
        )
        self.play(FadeIn(signs))
        self.say("즉 |f|/f는 f가 양수면 1, 음수면 −1입니다.")

        pieces = VGroup(
            ax.plot(lambda x: 1, x_range=[-0.5, 0.97], color=SW_COL, stroke_width=6),
            ax.plot(lambda x: -1, x_range=[1.03, 1.97], color=SW_COL, stroke_width=6),
            ax.plot(lambda x: 1, x_range=[2.03, 3.5], color=SW_COL, stroke_width=6),
        )
        sw_lab = MathTex(r"y=\frac{|f|}{f}", color=SW_COL, font_size=34).next_to(ax.c2p(3.4, 1), UP, buff=0.15)
        self.play(
            fg.animate.set_stroke(opacity=0.25), flab.animate.set_opacity(0.25),
            FadeOut(signs), FadeOut(d3), FadeOut(d15),
            Create(pieces), FadeIn(sw_lab), run_time=1.5,
        )
        self.say("g에 1 또는 −1을 곱하는 스위치인 셈이죠.")

        danger = VGroup(*[Dot(ax.c2p(x, 0), color=SW_COL, radius=0.1) for x in (1, 2)])
        jumps = VGroup(*[DashedLine(ax.c2p(x, -1), ax.c2p(x, 1), color=SW_COL) for x in (1, 2)])
        self.play(FadeIn(danger, scale=2), Create(jumps))
        self.say("스위치가 뒤집히는 곳은 f의 부호가 바뀌는 x=1, x=2뿐.")
        warn = T("위험한 점!", 36, SW_COL).next_to(ax.c2p(1.5, -1), DOWN, buff=0.25)
        self.play(FadeIn(warn, scale=1.3), Flash(danger[0], color=SW_COL), Flash(danger[1], color=SW_COL))
        self.say("바로 여기가 위험한 점입니다.")
        self.clear_content()

    # ---------- STEP 2 ----------
    def step2(self):
        self.chapter("STEP 2 · 위험한 점에서 무슨 일이?")
        ax = self.axes([0, 2, 0.5], [-3, 3, 1], 6, 4.4).move_to(LEFT * 2.6 + DOWN * 0.4)
        x1 = DashedLine(ax.c2p(1, -3), ax.c2p(1, 3), color=GREY_C)
        x1_lab = MathTex("x=1", font_size=30, color=GREY_A).next_to(ax.c2p(1, -3), DOWN, buff=0.1)
        self.play(Create(ax), Create(x1), FadeIn(x1_lab))
        self.say("x=1 근처를 확대해 봅시다.", 1.8)

        lsign = MathTex(r"g\times(+1)", font_size=36, color=SW_COL).move_to(ax.c2p(0.45, 2.6))
        rsign = MathTex(r"g\times(-1)", font_size=36, color=SW_COL).move_to(ax.c2p(1.55, 2.6))
        self.play(FadeIn(lsign), FadeIn(rsign))
        self.say("왼쪽에서는 g에 +1을, 오른쪽에서는 −1을 곱합니다.")

        c = ValueTracker(2.0)

        def g_near(x):
            return c.get_value() + 1.2 * (x - 1)

        left = always_redraw(lambda: ax.plot(g_near, x_range=[0.05, 0.99], color=G_COL, stroke_width=6))
        right = always_redraw(lambda: ax.plot(lambda x: -g_near(x), x_range=[1.01, 1.95], color=G_COL, stroke_width=6))
        el = always_redraw(lambda: Circle(0.09, color=G_COL).move_to(ax.c2p(1, c.get_value())))
        er = always_redraw(lambda: Circle(0.09, color=G_COL).move_to(ax.c2p(1, -c.get_value())))
        cval = always_redraw(lambda: MathTex(
            rf"g(1)={c.get_value():.1f}", font_size=48, color=G_COL
        ).move_to(RIGHT * 3.6 + UP * 1.2))
        self.play(Create(left), Create(right), FadeIn(el), FadeIn(er), FadeIn(cval))
        lv = MathTex("2", font_size=36, color=G_COL).next_to(ax.c2p(1, 2), RIGHT, buff=0.15)
        rv = MathTex("-2", font_size=36, color=G_COL).next_to(ax.c2p(1, -2), LEFT, buff=0.15)
        self.play(FadeIn(lv), FadeIn(rv))
        self.say("만약 g(1)이 2라면? 왼쪽은 2, 오른쪽은 −2로 갑니다.")
        tear = T("값이 찢어짐 → 극한 없음", 32, SW_COL).move_to(RIGHT * 3.6 + DOWN * 0.1)
        self.play(FadeIn(tear), Indicate(VGroup(el, er), color=SW_COL))
        self.say("값이 둘로 찢어지니 극한이 존재하지 않습니다.")

        self.say("찢어지지 않으려면… g(1)이 0이 되는 수밖에 없습니다.", 0.5)
        self.play(FadeOut(lv), FadeOut(rv), FadeOut(tear))
        self.play(c.animate.set_value(0), run_time=3)
        ok = MathTex(r"g(1)=0", font_size=52, color=H_COL).move_to(RIGHT * 3.6 + DOWN * 0.1)
        self.play(Write(ok), Flash(ax.c2p(1, 0), color=H_COL))
        self.wait(1.5)
        ok2 = MathTex(r"g(2)=0", font_size=52, color=H_COL).next_to(ok, DOWN, buff=0.4)
        self.play(Write(ok2))
        self.say("x=2에서도 똑같이 g(2)=0.")
        self.clear_content()

        self.say("규칙으로 기억해 둡시다.", 1.5)
        rule = VGroup(
            T("부호가 뒤집히는 곳에서는", 40),
            T("곱해진 값이 0이어야 한다", 44, G_COL),
        ).arrange(DOWN, buff=0.35)
        frame = SurroundingRectangle(rule, color=SW_COL, buff=0.45, corner_radius=0.15)
        self.play(Write(rule), Create(frame))
        self.say("부호가 뒤집히는 곳에서는, 곱해진 값이 0이어야 한다.", 3)
        self.clear_content()

    # ---------- STEP 3 ----------
    def step3(self):
        self.chapter("STEP 3 · g의 절반이 정해진다")
        a = MathTex(r"g(1)=0,\quad g(2)=0", font_size=52, color=H_COL).move_to(UP * 1.4)
        b = MathTex(r"g", "=", r"(x-1)(x-2)", r"\cdot", "h", font_size=56).next_to(a, DOWN, buff=0.6)
        b[0].set_color(G_COL)
        b[4].set_color(H_COL)
        self.play(Write(a))
        self.play(Write(b))
        self.say("g(1)=0, g(2)=0이면 g는 (x−1)(x−2)를 인수로 가집니다.")
        brace = Brace(b[2], DOWN, color=F_COL)
        bf = MathTex("f", font_size=48, color=F_COL).next_to(brace, DOWN)
        self.play(GrowFromCenter(brace), FadeIn(bf), b[2].animate.set_color(F_COL))
        self.say("그런데 (x−1)(x−2)는 바로 f.", 1.8)

        c = MathTex(r"g", "=", "f", r"\cdot", "h", font_size=80)
        c[0].set_color(G_COL)
        c[2].set_color(F_COL)
        c[4].set_color(H_COL)
        c.move_to(DOWN * 0.1)
        self.play(FadeOut(a), FadeOut(brace), FadeOut(bf), ReplacementTransform(b, c))
        hn = T("h: 최고차항 계수가 1인 이차함수", 28, H_COL).next_to(c, DOWN, buff=0.5)
        self.play(FadeIn(hn))
        self.say("그래서 g = f·h. h는 최고차항 계수가 1인 이차함수.")

        done = T("확정", 28, F_COL).next_to(c[2], UP, buff=0.35)
        q = T("?", 44, H_COL).next_to(c[4], UP, buff=0.25)
        self.play(FadeIn(done, shift=DOWN * 0.2), FadeIn(q, shift=DOWN * 0.2))
        self.say("첫 번째 식이 g의 절반을 정해 준 겁니다.")
        self.focus(self.strip[1])
        self.say("나머지 절반 h는? 두 번째 식이 정할 차례입니다.")
        self.clear_content()

    # ---------- STEP 4 ----------
    def step4(self):
        self.chapter("STEP 4 · 두 번째 식에 숨은 같은 스위치")
        e0 = MathTex(r"\frac{|g-f|}{g}", font_size=64).move_to(UP * 1.2)
        e1 = MathTex(r"\frac{|fh-f|}{fh}", font_size=64).move_to(UP * 1.2)
        self.play(Write(e0))
        self.play(TransformMatchingShapes(e0, e1), run_time=1.3)
        self.say("두 번째 식에 g = f·h를 넣어 봅시다.")

        num = VGroup(T("분자 ", 30, GREY_A), MathTex(r"|fh-f|=|f(h-1)|=|f|\,|h-1|", font_size=40))
        num.arrange(RIGHT, buff=0.2).next_to(e1, DOWN, buff=0.6)
        self.play(Write(num))
        self.say("분자는 fh − f = f(h−1). 그래서 |f|·|h−1|.")
        den = VGroup(T("분모 ", 30, GREY_A), MathTex(r"f\,h", font_size=40)).arrange(RIGHT, buff=0.2)
        den.next_to(num, DOWN, buff=0.35).align_to(num, LEFT)
        self.play(Write(den))
        self.say("분모는 f·h.", 1.8)

        e2 = MathTex(r"\frac{|f|\,|h-1|}{f\,h}", font_size=64).move_to(UP * 1.0)
        self.play(FadeOut(num), FadeOut(den), ReplacementTransform(e1, e2))
        self.say("둘을 정리하면…", 1.2)
        e3 = MathTex(r"\frac{|f|}{f}", r"\quad\cdot\quad", r"\frac{|h-1|}{h}", font_size=72).move_to(UP * 1.0)
        self.play(TransformMatchingShapes(e2, e3), run_time=1.3)
        self.play(e3[0].animate.set_color(SW_COL))
        b1 = Brace(e3[0], DOWN, color=SW_COL)
        t1 = T("아까 그 스위치!", 30, SW_COL).next_to(b1, DOWN)
        self.play(GrowFromCenter(b1), FadeIn(t1), Circumscribe(e3[0], color=SW_COL))
        self.say("아까 그 스위치, |f|/f가 또 나왔습니다!")

        self.play(e3[2].animate.set_color(G_COL))
        b2 = Brace(e3[2], DOWN, color=G_COL)
        t2 = T("곱해진 값", 30, G_COL).next_to(b2, DOWN)
        self.play(GrowFromCenter(b2), FadeIn(t2))
        r1 = MathTex(r"x=1,2:\ \frac{|h-1|}{h}=0", r"\ \Rightarrow\ ", r"h(1)=h(2)=1", font_size=40)
        r1[2].set_color(H_COL)
        r1.next_to(VGroup(t1, t2), DOWN, buff=0.45)
        self.play(Write(r1))
        self.say("그러면 규칙도 같습니다. x=1, 2에서 |h−1|/h가 0이어야 하니 h(1)=h(2)=1.")

        den_h = e3[2][-1]
        self.play(Circumscribe(den_h, color=SW_COL, shape=Circle))
        self.say("그리고 하나 더. 분모 h가 0이 되는 곳에서는 식이 터져 버립니다.")
        r2 = MathTex(r"h(x)\neq 0", font_size=44, color=H_COL).next_to(r1, DOWN, buff=0.3)
        self.play(Write(r2))
        self.say("그러니 h는 어디서도 0이 되면 안 됩니다.")
        self.clear_content()

    # ---------- STEP 5 ----------
    def step5(self):
        self.chapter("STEP 5 · h 찾기")
        self.focus(None)
        ax = self.axes([-0.5, 3.5, 1], [-1, 3.5, 1], 6, 4.4).move_to(LEFT * 2.8 + DOWN * 0.45)
        nums = VGroup(*[MathTex(str(n), font_size=26).next_to(ax.c2p(n, 0), DOWN, buff=0.12) for n in (1, 2, 3)])
        self.play(Create(ax), FadeIn(nums))
        pts = VGroup(*[Dot(ax.c2p(x, 1), color=H_COL, radius=0.09) for x in (1, 2)])
        ptl = MathTex(r"h(1)=h(2)=1", font_size=40, color=H_COL).move_to(RIGHT * 3.4 + UP * 1.5)
        self.play(FadeIn(pts, scale=2), Write(ptl))
        self.say("h(1)=1, h(2)=1. 두 점을 찍어 봅시다.")

        fg = ax.plot(f, x_range=[-0.1, 3.1], color=F_COL)
        flab = MathTex("f", color=F_COL, font_size=36).next_to(ax.c2p(3.1, f(3.1)), RIGHT)
        zeros = VGroup(*[Dot(ax.c2p(x, 0), color=F_COL, radius=0.07) for x in (1, 2)])
        self.play(Create(fg), FadeIn(flab), FadeIn(zeros))
        self.say("f는 x=1, 2에서 0이었죠. h는 같은 자리에서 1.")

        hg = fg.copy()
        target = ax.plot(lambda x: f(x) + 1, x_range=[-0.1, 3.1], color=H_COL)
        arrows = VGroup(*[Arrow(ax.c2p(x, 0), ax.c2p(x, 1), buff=0.05, color=H_COL) for x in (1, 1.5, 2)])
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), GrowArrow(arrows[2]))
        self.play(Transform(hg, target), run_time=2)
        hlab = MathTex("h", color=H_COL, font_size=36).next_to(ax.c2p(3.1, f(3.1) + 1), RIGHT)
        self.play(FadeIn(hlab), FadeOut(arrows))
        self.say("f를 위로 1만큼 올리면 딱 맞습니다.")
        eq = MathTex("h", "=", "f+1", font_size=64).next_to(ptl, DOWN, buff=0.6)
        eq[0].set_color(H_COL)
        self.play(Write(eq))
        self.say("최고차항 계수도 같으니 h는 이것뿐. h = f + 1.")

        bot_f = DashedLine(ax.c2p(-0.5, -0.25), ax.c2p(3.5, -0.25), color=F_COL, stroke_width=2)
        lf = MathTex(r"-\tfrac14", color=F_COL, font_size=30).next_to(bot_f, LEFT, buff=0.1)
        self.play(Create(bot_f), FadeIn(lf))
        self.say("이제 h가 0이 되는지 확인. f의 바닥은 −1/4.")
        bot_h = DashedLine(ax.c2p(-0.5, 0.75), ax.c2p(3.5, 0.75), color=H_COL, stroke_width=2)
        lh = MathTex(r"\tfrac34", color=H_COL, font_size=30).next_to(bot_h, LEFT, buff=0.1)
        self.play(Create(bot_h), FadeIn(lh))
        ok = MathTex(r"h\ge\tfrac34>0", font_size=48, color=H_COL).next_to(eq, DOWN, buff=0.5)
        self.play(Write(ok))
        self.say("1을 올리면 바닥은 3/4. 0보다 위에 있으니 h는 절대 0이 되지 않습니다.")
        self.clear_content()

    # ---------- STEP 6 ----------
    def step6(self):
        self.chapter("STEP 6 · 답")
        self.focus(self.strip[3])
        big = MathTex("g", "=", "f", "(", "f", "+1", ")", font_size=88).move_to(UP * 1.2)
        big[0].set_color(G_COL)
        big[2].set_color(F_COL)
        big[4].set_color(F_COL)
        self.play(Write(big))
        self.say("정리하면 g = f(f+1).")
        a1 = MathTex(r"f(-1)=(-2)(-3)=6", font_size=52, color=F_COL).next_to(big, DOWN, buff=0.5)
        self.play(Write(a1))
        self.say("f(−1) = (−2)(−3) = 6.")
        a2 = MathTex(r"g(-1)=6\times 7=", "42", font_size=64).next_to(a1, DOWN, buff=0.5)
        a2[1].set_color(G_COL).scale(1.4)
        self.play(Write(a2))
        self.play(Flash(a2[1], color=G_COL, line_length=0.4, num_lines=16))
        self.say("그러니 g(−1) = 6 × 7 = 42.", 2.5)
        self.clear_content()

    # ---------- 보너스 ----------
    def bonus(self):
        self.chapter("보너스 · 출제자는 왜 하필 1을 썼을까")
        self.focus(self.strip[1])
        q = MathTex(r"\frac{|g-", "k", r"f|}{g}", font_size=56).move_to(RIGHT * 3.4 + UP * 1.5)
        q[1].set_color(SW_COL)
        self.play(Write(q))
        self.say("마지막으로, 문제의 1이 다른 수 k였다면?")

        ax = self.axes([-0.5, 3.5, 1], [-1, 3.5, 1], 6, 4.4).move_to(LEFT * 2.8 + DOWN * 0.45)
        k = ValueTracker(1.0)

        def col():
            return H_COL if k.get_value() > 0.25 + 1e-3 else SW_COL

        hg = always_redraw(lambda: ax.plot(
            lambda x: f(x) + k.get_value(), x_range=[-0.1, 3.1], color=col()
        ))
        vertex = always_redraw(lambda: Dot(ax.c2p(1.5, k.get_value() - 0.25), color=col()))
        hk = MathTex("h", "=", "f+", "k", font_size=48).next_to(q, DOWN, buff=0.5)
        hk[3].set_color(SW_COL)
        kv = always_redraw(lambda: MathTex(
            rf"k={k.get_value():.2f}", font_size=44, color=col()
        ).next_to(hk, DOWN, buff=0.4))
        self.play(Create(ax), Create(hg), FadeIn(vertex), Write(hk), FadeIn(kv))
        self.say("같은 논리로 h = f + k. 포물선을 k만큼 올리는 겁니다.")
        self.say("k를 줄여 보면…", 0.5)
        self.play(k.animate.set_value(0.25), run_time=3.5, rate_func=linear)
        boom = T("h = 0인 곳 발생 → 극한 붕괴", 28, SW_COL).next_to(kv, DOWN, buff=0.35)
        self.play(Flash(vertex, color=SW_COL), FadeIn(boom))
        self.say("1/4에서 바닥이 x축에 닿습니다. h=0인 곳이 생기고 극한이 깨집니다.")
        self.play(k.animate.set_value(1.0), FadeOut(boom), run_time=2)

        nl = NumberLine(x_range=[-0.5, 2, 0.25], length=5.5, include_numbers=False).next_to(kv, DOWN, buff=0.8)
        safe = Line(nl.n2p(0.25), nl.n2p(2), color=H_COL, stroke_width=10)
        hole = Circle(0.08, color=SW_COL).move_to(nl.n2p(0.25))
        q_lab = MathTex(r"\tfrac14", font_size=32, color=SW_COL).next_to(nl.n2p(0.25), DOWN)
        one = Dot(nl.n2p(1), color=G_COL, radius=0.1)
        one_lab = MathTex("1", font_size=36, color=G_COL).next_to(one, UP)
        self.play(Create(nl), Create(safe), FadeIn(hole), FadeIn(q_lab), FadeIn(one, scale=2), FadeIn(one_lab))
        self.say("이 문제는 k > 1/4일 때만 답이 있습니다. 1은 안전한 선택이었던 거죠.", 3)
        self.focus(None)
        self.clear_content()

    # ---------- 정리 ----------
    def summary(self):
        self.play(FadeOut(self.tag), FadeOut(self.strip))
        self.tag = None
        self.strip = None
        head = T("오늘 쓴 도구는 딱 하나", 44, G_COL)
        l1 = T("①  |f|/f 는 부호 스위치", 32)
        l2 = T("②  스위치가 뒤집히는 곳에서는  곱해진 값 = 0", 32)
        l3 = T("③  분모는 어디서도 0이 되면 안 된다", 32)
        fin = MathTex(r"g=f(f+1),\qquad g(-1)=42", font_size=52, color=G_COL)
        VGroup(head, l1, l2, l3, fin).arrange(DOWN, buff=0.45).shift(UP * 0.4)
        for line in (l2, l3):
            line.align_to(l1, LEFT)
        VGroup(l1, l2, l3).set_x(0)
        self.play(Write(head))
        self.say("오늘 쓴 도구는 딱 하나.", 1.5)
        for line, cap in ((l1, "① |f|/f는 부호 스위치."),
                          (l2, "② 스위치가 뒤집히는 곳에서는 곱해진 값이 0."),
                          (l3, "③ 분모는 어디서도 0이 되면 안 된다.")):
            self.play(FadeIn(line, shift=RIGHT * 0.3))
            self.say(cap)
        self.play(Write(fin))
        self.say("g = f(f+1), 답은 42.", 3)
        self.play(*[FadeOut(m) for m in self.mobjects])
