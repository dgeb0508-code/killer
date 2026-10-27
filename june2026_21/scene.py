"""2026학년도 6월 모의평가 21번 — '스위치 하나로 끝나는 문제' (대본: script.md, 나레이션: narration.py)

화면 구성: 왼쪽은 애니메이션 무대, 오른쪽은 장면마다 결론이 한 줄씩 적히는 노트.
나레이션 음성 길이에 맞춰 장면이 진행된다 (먼저 make_voice.py로 voice/ 생성).
렌더: manim -qh scene.py Killer21   (손글씨 폰트 Nanum Pen Script 필요)
"""
import json
from pathlib import Path

from manim import *

HERE = Path(__file__).parent
VOICE_DIR = HERE / "voice"
DUR = json.loads((VOICE_DIR / "durations.json").read_text())

PEN = "Nanum Pen"
SANS = "Noto Sans CJK KR"
config.background_color = "#101218"

# 무대: 흰 선 + 강조색 하나
W = "#e8e8e8"
DIM = "#6f7480"
ACC = "#ff6b6b"
# 노트 카드: 종이 + 잉크 + 같은 강조색 계열
PAPER = "#f7f5ee"
NOTE_INK = "#2b2b2b"
NOTE_ACC = "#d6342c"

SX = -2.2  # 무대 중심 x (오른쪽 3.0부터는 노트)


def f(x):
    return (x - 1) * (x - 2)


def M(tex, size=48, color=W):
    return MathTex(tex, font_size=size, color=color)


def T(text, size=30, color=W):
    return Text(text, font=SANS, font_size=size, color=color)


def hw(text, size=28, color=NOTE_INK):
    return Text(text, font=PEN, font_size=size, color=color)


class Killer21(Scene):
    def construct(self):
        self.deadline = 0
        self.notes = []
        self.strip = None
        self.card = None
        self.hook()
        self.scene1()
        self.scene2()
        self.scene3()
        self.scene4()
        self.scene5()
        self.scene6()
        self.outro()

    # ---------- 나레이션 동기화 ----------
    def vo(self, key):
        """음성을 틀고, 이 문장이 끝나는 시각을 기억한다."""
        self.sync()
        self.add_sound(str(VOICE_DIR / f"{key}.mp3"))
        self.deadline = self.renderer.time + DUR[key]

    def sync(self, pad=0.25):
        """현재 문장이 끝날 때까지 기다린다."""
        rem = self.deadline - self.renderer.time
        if rem > 0:
            self.wait(rem + pad)

    # ---------- 공통 ----------
    def keep(self):
        fixed = [self.strip, self.card, getattr(self, "src", None)]
        return [m for m in fixed if m is not None] + self.notes

    def clear_stage(self):
        kept = set()
        for m in self.keep():
            kept.update(m.get_family())
        rest = [m for m in self.mobjects
                if m not in kept and not (m.submobjects and all(s in kept for s in m.get_family()[1:]))]
        if rest:
            self.play(*[FadeOut(m) for m in rest], run_time=0.5)

    def stage_axes(self, x_range, y_range, width, height, center):
        return Axes(x_range=x_range, y_range=y_range, x_length=width, y_length=height, tips=False,
                    axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}).move_to(center)

    def ticks(self, ax, xs, size=28):
        return VGroup(*[M(str(n), size, DIM).next_to(ax.c2p(n, 0), DOWN, buff=0.12) for n in xs])

    # ---------- 노트 카드 ----------
    def open_card(self):
        card = RoundedRectangle(width=4.0, height=7.6, corner_radius=0.15, stroke_width=0,
                                fill_color=PAPER, fill_opacity=1).move_to([5.0, 0, 0])
        title = hw("21번 노트", 38).next_to(card.get_corner(UL), DR, buff=0.25)
        rule = Line(LEFT, RIGHT, color="#d9d5c8", stroke_width=2).set_width(3.5)
        rule.next_to(title, DOWN, buff=0.12).set_x(card.get_x())
        src = Text("출처: 2026학년도 6월 모의평가 수학 21번 (한국교육과정평가원)",
                   font=SANS, font_size=13, color=DIM)
        src.to_corner(DL, buff=0.15)
        self.play(FadeIn(card, shift=LEFT * 0.6), run_time=0.7)
        self.play(Write(title), Create(rule), FadeIn(src), run_time=0.8)
        self.remove(card, title, rule)
        self.card = VGroup(card, title, rule)
        self.add(self.card)
        self.src = src
        self.note_anchor = rule

    def note(self, *lines, accent=None, run_time=None):
        """노트에 한 항목(여러 줄)을 손글씨로 적는다. accent: 강조할 줄 번호."""
        group = VGroup(*[hw(t, 27, NOTE_ACC if i == accent else NOTE_INK) for i, t in enumerate(lines)])
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        for g in group[1:]:
            g.shift(RIGHT * 0.3)
        if group.width > 3.55:
            group.scale_to_fit_width(3.55)
        last = self.notes[-1] if self.notes else self.note_anchor
        group.next_to(last, DOWN, buff=0.22).align_to(self.note_anchor, LEFT).shift(RIGHT * 0.05)
        self.play(Write(group), run_time=run_time or min(2.5, 0.9 * len(lines)))
        self.notes.append(group)
        return group

    # ---------- 오프닝: 훅 ----------
    def hook(self):
        given = M(r"f(x)=(x-1)(x-2)", 44)
        g_desc = T("g(x): 최고차항의 계수가 1인 사차함수", 26, DIM)
        lim1 = MathTex(r"\lim_{x\to a}", r"g(x)", r"\frac{|f(x)|}{f(x)}", font_size=50, color=W)
        lim2 = MathTex(r"\lim_{x\to a}", r"\frac{|g(x)-f(x)|}{g(x)}", font_size=50, color=W)
        lims = VGroup(lim1, lim2).arrange(RIGHT, buff=1.4)
        cond = T("모든 실수 a에서 두 극한이 모두 존재", 26, DIM)
        ask = M(r"g(-1)=\ ?", 46)
        prob = VGroup(given, g_desc, lims, cond, ask).arrange(DOWN, buff=0.35)

        self.vo("hook1")
        for m in (given, g_desc):
            self.play(FadeIn(m, shift=UP * 0.15), run_time=0.5)
        self.play(Write(lim1), Write(lim2), run_time=1.6)
        self.play(FadeIn(cond), FadeIn(ask), run_time=0.6)

        self.vo("hook2")
        self.play(lim1[2].animate.set_color(ACC), run_time=0.5)
        sw = T("스위치", 26, ACC).next_to(lim1[2], DOWN, buff=0.15)
        q = T("…여기도?", 26, ACC).next_to(lim2, DOWN, buff=0.15)
        self.play(FadeIn(sw, shift=UP * 0.1), Circumscribe(lim1[2], color=ACC), run_time=1.0)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)

        # 문제를 무대 위쪽 한 줄로 접고, 노트를 연다.
        self.vo("hook3")
        s1 = MathTex(r"\lim_{x\to a}", r"g(x)", r"\frac{|f(x)|}{f(x)}", font_size=30, color=DIM)
        s2 = MathTex(r"\lim_{x\to a}", r"\frac{|g(x)-f(x)|}{g(x)}", font_size=30, color=DIM)
        s3 = MathTex(r"g(-1)=", r"?", font_size=30, color=DIM)
        strip = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.7).move_to([SX, 3.45, 0])
        self.play(FadeOut(sw), FadeOut(q), FadeOut(given), FadeOut(g_desc), FadeOut(cond),
                  ReplacementTransform(lim1, s1), ReplacementTransform(lim2, s2),
                  ReplacementTransform(ask, s3), run_time=1.2)
        self.remove(s1, s2, s3)
        self.strip = strip
        self.add(strip)
        self.open_card()

    # ---------- 1: 스위치 발견 ----------
    def scene1(self):
        self.vo("s1a")
        e = MathTex(r"g(x)", r"\times", r"\frac{|f(x)|}{f(x)}", font_size=64, color=W).move_to([SX, 1.9, 0])
        self.play(TransformFromCopy(self.strip[0], e), run_time=1.2)
        self.play(e[2].animate.set_color(ACC), run_time=0.5)
        self.play(Circumscribe(e[2], color=ACC), run_time=1.0)

        self.vo("s1b")
        ax = self.stage_axes([-0.5, 3.5, 1], [-1.6, 2.6, 1], 6.2, 3.6, [SX, -1.25, 0])
        fg = ax.plot(f, x_range=[-0.25, 3.25], color=W, stroke_width=4)
        self.play(Create(ax), FadeIn(self.ticks(ax, (1, 2, 3))), run_time=0.8)
        self.play(Create(fg), run_time=1.2)
        plus1 = M("+1", 36, ACC).move_to(ax.c2p(0.25, 1.6))
        minus = M("-1", 36, ACC).move_to(ax.c2p(1.5, 1.0))
        plus2 = M("+1", 36, ACC).move_to(ax.c2p(2.75, 1.6))
        for m in (plus1, minus, plus2):
            self.play(FadeIn(m, scale=1.4), run_time=0.45)

        self.vo("s1c")
        steps = VGroup(
            ax.plot(lambda x: 1, x_range=[-0.5, 0.97], color=ACC, stroke_width=6),
            ax.plot(lambda x: -1, x_range=[1.03, 1.97], color=ACC, stroke_width=6),
            ax.plot(lambda x: 1, x_range=[2.03, 3.5], color=ACC, stroke_width=6),
        )
        ghost = fg.copy()
        self.play(fg.animate.set_stroke(color=DIM, opacity=0.4), run_time=0.4)
        self.play(ReplacementTransform(ghost, steps), FadeOut(VGroup(plus1, minus, plus2)), run_time=2.0)

        self.vo("s1d")
        jumps = VGroup(*[DashedLine(ax.c2p(x, -1), ax.c2p(x, 1), color=ACC) for x in (1, 2)])
        dots = VGroup(*[Dot(ax.c2p(x, 0), color=ACC, radius=0.1) for x in (1, 2)])
        self.play(Create(jumps), run_time=0.8)
        self.play(FadeIn(dots, scale=2), Flash(dots[0], color=ACC), Flash(dots[1], color=ACC), run_time=1.0)
        lab = T("위험한 점", 28, ACC).next_to(ax.c2p(1.5, -1.5), DOWN, buff=0.1)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.sync()
        self.note("① |f(x)|/f(x) = 부호 스위치", "x = 1, 2 에서 뒤집힘")
        self.switch_mini = VGroup(ax, steps).copy()
        self.clear_stage()

    # ---------- 2: 찢어지는 그래프 + 퀴즈 ----------
    def scene2(self):
        self.vo("s2a")
        ax = self.stage_axes([0, 2, 0.5], [-3, 3, 1], 5.0, 4.6, [SX - 1.2, -0.75, 0])
        x1 = DashedLine(ax.c2p(1, -3), ax.c2p(1, 3), color=DIM)
        x1_lab = M("x=1", 28, DIM).next_to(ax.c2p(1, -3), DOWN, buff=0.1)
        self.play(Create(ax), Create(x1), FadeIn(x1_lab), run_time=0.8)
        lsign = M(r"g(x)\times(+1)", 34).move_to(ax.c2p(0.45, 2.6))
        rsign = M(r"g(x)\times(-1)", 34).move_to(ax.c2p(1.55, 2.6))
        self.play(FadeIn(lsign, shift=DOWN * 0.1), run_time=0.6)
        self.wait(1.2)
        self.play(FadeIn(rsign, shift=DOWN * 0.1), run_time=0.6)

        self.vo("s2b")
        c = ValueTracker(2.0)

        def g_near(x):
            return c.get_value() + 1.2 * (x - 1)

        left = always_redraw(lambda: ax.plot(g_near, x_range=[0.05, 0.99], color=W, stroke_width=6))
        right = always_redraw(lambda: ax.plot(lambda x: -g_near(x), x_range=[1.01, 1.95], color=W, stroke_width=6))
        el = always_redraw(lambda: Circle(0.1, color=W, stroke_width=3).move_to(ax.c2p(1, c.get_value())))
        er = always_redraw(lambda: Circle(0.1, color=W, stroke_width=3).move_to(ax.c2p(1, -c.get_value())))
        gap = always_redraw(lambda: Line(ax.c2p(1, -c.get_value()), ax.c2p(1, c.get_value()),
                                         color=ACC, stroke_width=6) if c.get_value() > 0.05 else VMobject())
        self.play(Create(left), FadeIn(el), run_time=1.0)
        self.play(Create(right), FadeIn(er), run_time=1.0)
        self.play(FadeIn(gap), run_time=0.4)
        tear = T("찢어짐!", 32, ACC).next_to(ax.c2p(1, 0), RIGHT, buff=0.3)
        self.play(FadeIn(tear, scale=1.3), Wiggle(gap), run_time=1.0)
        cval = M(r"g(1)=2", 44).move_to([1.4, 1.6, 0])
        self.play(FadeIn(cval), run_time=0.4)

        self.vo("s2c")
        self.play(FadeOut(tear), run_time=0.3)
        quiz = M(r"g(1)=\,?", 64, ACC).move_to([1.4, 0.2, 0])
        self.play(ReplacementTransform(cval, quiz), run_time=0.8)
        self.sync(pad=0.1)
        for n in ("3", "2", "1"):
            num = M(n, 90, W).move_to([1.4, -1.5, 0])
            self.play(FadeIn(num, scale=1.6), run_time=0.25)
            self.play(FadeOut(num, scale=0.6), run_time=0.75)

        self.vo("s2d")
        ans = M(r"g(1)=0", 64, W).move_to(quiz)
        self.play(ReplacementTransform(quiz, ans), run_time=0.6)
        self.play(c.animate.set_value(0), run_time=3.0, rate_func=smooth)
        self.play(Flash(ax.c2p(1, 0), color=ACC, line_length=0.3), run_time=0.6)

        self.vo("s2e")
        ans2 = M(r"g(2)=0", 64, W).next_to(ans, DOWN, buff=0.35)
        self.play(FadeIn(ans2, shift=UP * 0.15), run_time=0.6)
        self.wait(1.5)
        rule = VGroup(T("뒤집히는 곳에서는", 28), T("곱해진 값 = 0", 34, ACC)).arrange(DOWN, buff=0.12)
        rule.next_to(ans2, DOWN, buff=0.45)
        frame = SurroundingRectangle(rule, color=ACC, buff=0.18, corner_radius=0.1)
        self.play(Create(frame), FadeIn(rule), run_time=1.0)
        self.sync()
        self.note("② 뒤집히는 곳: 곱해진 값 = 0", "→ g(1) = g(2) = 0", accent=1)
        self.clear_stage()

        self.vo("s2f")
        a = MathTex(r"g(x)", r"=", r"(x-1)(x-2)", r"\,h(x)", font_size=64, color=W).move_to([SX, 0.6, 0])
        self.play(Write(a), run_time=1.6)
        brace = Brace(a[2], DOWN, color=DIM)
        bf = M("f(x)", 48, DIM).next_to(brace, DOWN)
        self.play(GrowFromCenter(brace), FadeIn(bf), run_time=0.8)
        b = MathTex(r"g(x)", r"=", r"f(x)", r"\,h(x)", font_size=72, color=W).move_to([SX, 0.6, 0])
        self.play(FadeOut(brace), FadeOut(bf), TransformMatchingTex(a, b), run_time=1.2)
        hn = T("h(x): 최고차항 계수가 1인 이차함수", 26, DIM).next_to(b, DOWN, buff=0.5)
        self.play(FadeIn(hn), run_time=0.5)
        self.sync()
        self.note("③ g(x) = f(x) h(x)", "h(x): 이차, 최고차항 계수 1")
        self.clear_stage()

    # ---------- 3: 반전 — 같은 스위치 ----------
    def scene3(self):
        self.vo("s3a")
        e0 = M(r"\frac{|g(x)-f(x)|}{g(x)}", 70).move_to([SX, 1.3, 0])
        self.play(TransformFromCopy(self.strip[1], e0), run_time=1.2)

        self.vo("s3b")
        e1 = M(r"\frac{|f(x)h(x)-f(x)|}{f(x)h(x)}", 70).move_to(e0)
        self.play(TransformMatchingShapes(e0, e1), run_time=1.4)
        self.wait(1.0)
        e2 = M(r"\frac{|f(x)|\,|h(x)-1|}{f(x)\,h(x)}", 70).move_to(e0)
        self.play(TransformMatchingShapes(e1, e2), run_time=1.4)

        self.vo("s3c")
        e3 = MathTex(r"\frac{|f(x)|}{f(x)}", r"\times", r"\frac{|h(x)-1|}{h(x)}", font_size=70, color=W).move_to(e0)
        self.play(TransformMatchingShapes(e2, e3), run_time=1.2)
        mini = self.switch_mini.scale(0.35).next_to(e3[0], DOWN, buff=0.4)
        self.play(e3[0].animate.set_color(ACC), FadeIn(mini, shift=UP * 0.5), run_time=0.8)
        stamp = T("같은 스위치!", 36, ACC).next_to(mini, RIGHT, buff=0.3)
        self.play(FadeIn(stamp, scale=1.8), Flash(e3[0], color=ACC, line_length=0.3), run_time=0.8)

        self.vo("s3d")
        self.play(self.strip[0][2].animate.set_color(ACC), self.strip[1].animate.set_color(ACC), run_time=0.6)
        link = T("두 조건 = 같은 스위치", 30, ACC).next_to(self.strip, DOWN, buff=0.2)
        self.play(FadeIn(link, shift=DOWN * 0.1), run_time=0.6)
        self.sync()
        self.play(FadeOut(link), self.strip[0][2].animate.set_color(DIM),
                  self.strip[1].animate.set_color(DIM), FadeOut(mini), FadeOut(stamp), run_time=0.5)

        self.vo("s3e")
        r1 = MathTex(r"x=1,2:\ \ |h(x)-1|\to 0", r"\ \Rightarrow\ ", r"h(1)=h(2)=1", font_size=46, color=W)
        r1.next_to(e3, DOWN, buff=0.8).set_x(SX)
        self.play(Write(r1[0]), run_time=1.4)
        self.play(Write(r1[1]), Write(r1[2]), run_time=1.0)
        self.play(Create(SurroundingRectangle(r1[2], color=ACC, buff=0.1)), run_time=0.6)

        self.vo("s3f")
        den = e3[2][-4:]
        self.play(Circumscribe(den, color=ACC, shape=Circle), run_time=1.0)
        r2 = M(r"h(x)\neq 0", 50, ACC).next_to(r1, DOWN, buff=0.4).set_x(SX)
        self.play(Write(r2), run_time=0.8)
        self.sync()
        self.note("④ 두 번째 식도 같은 스위치!", "h(1) = h(2) = 1,  h(x) ≠ 0", accent=0)
        self.clear_stage()

    # ---------- 4: 포물선 들어 올리기 ----------
    def scene4(self):
        ax = self.stage_axes([-0.5, 3.5, 1], [-1, 3.4, 1], 5.6, 4.0, [SX, -1.15, 0])
        self.vo("s4a")
        self.play(Create(ax), FadeIn(self.ticks(ax, (1, 2, 3))), run_time=0.8)
        pts = VGroup(*[Dot(ax.c2p(x, 1), color=W, radius=0.1) for x in (1, 2)])
        self.play(FadeIn(pts, scale=2), run_time=0.6)
        ptl = M(r"h(1)=h(2)=1", 36).next_to(ax.c2p(1.5, 1), UP, buff=0.9)
        self.play(FadeIn(ptl), run_time=0.5)

        self.vo("s4b")
        fg = ax.plot(f, x_range=[-0.2, 3.2], color=DIM, stroke_width=4)
        flab = M("f(x)", 32, DIM).next_to(ax.c2p(3.2, f(3.2)), RIGHT, buff=0.08)
        self.play(Create(fg), FadeIn(flab), FadeOut(ptl), run_time=1.2)
        zeros = VGroup(*[Dot(ax.c2p(x, 0), color=DIM, radius=0.08) for x in (1, 2)])
        self.play(FadeIn(zeros), run_time=0.4)
        self.wait(1.0)
        arrows = VGroup(*[Arrow(ax.c2p(x, f(x)), ax.c2p(x, f(x) + 1), buff=0.04, color=ACC,
                                stroke_width=4, max_tip_length_to_length_ratio=0.3) for x in (0.3, 1, 1.5, 2, 2.7)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.0)
        hg = fg.copy()
        target = ax.plot(lambda x: f(x) + 1, x_range=[-0.2, 3.2], color=W, stroke_width=5)
        self.play(Transform(hg, target), run_time=1.8)
        hlab = M("h(x)", 32).next_to(ax.c2p(3.2, f(3.2) + 1), RIGHT, buff=0.08)
        self.play(FadeIn(hlab), FadeOut(arrows), run_time=0.5)

        self.vo("s4c")
        eq = M(r"h(x)=f(x)+1=x^2-3x+3", 46).move_to([SX, 2.55, 0])
        self.play(Write(eq), run_time=1.6)
        dd = M(r"D=9-12<0", 46, ACC).next_to(eq, DOWN, buff=0.3)
        self.play(Write(dd), run_time=1.0)
        floor = DashedLine(ax.c2p(-0.5, 0.75), ax.c2p(3.5, 0.75), color=ACC, stroke_width=3)
        fl = T("바닥 3/4 > 0", 24, ACC).next_to(floor, RIGHT, buff=0.1)
        self.play(Create(floor), FadeIn(fl), run_time=1.0)
        self.sync()
        self.note("⑤ h(x) = f(x) + 1 = x² - 3x + 3", "D < 0 → x축과 안 만남")
        self.clear_stage()

    # ---------- 5: 답 ----------
    def scene5(self):
        self.vo("s5a")
        g = M(r"g(x)=f(x)\{f(x)+1\}", 70).move_to([SX, 1.2, 0])
        self.play(Write(g), run_time=2.0)

        self.vo("s5b")
        a1 = M(r"f(-1)=(-2)(-3)=6", 52, DIM).next_to(g, DOWN, buff=0.55)
        self.play(FadeIn(a1, shift=UP * 0.1), run_time=0.7)
        a2 = MathTex(r"g(-1)=6\times7=", r"42", font_size=70, color=W).next_to(a1, DOWN, buff=0.55)
        a2[1].set_color(ACC).scale(1.5)
        self.play(Write(a2[0]), run_time=1.2)
        self.play(FadeIn(a2[1], scale=0.4), run_time=0.6)
        self.play(Flash(a2[1], color=ACC, line_length=0.4, num_lines=16), run_time=0.8)
        new_q = MathTex(r"42", font_size=30, color=ACC).move_to(self.strip[2][1])
        self.play(Transform(self.strip[2][1], new_q), run_time=0.6)
        self.sync()
        self.answer_note = self.note("답  g(-1) = 6 × 7 = 42", accent=0)
        box = SurroundingRectangle(self.answer_note, color=NOTE_ACC, buff=0.08, stroke_width=2.5)
        self.play(Create(box), run_time=0.5)
        self.notes.append(box)
        self.clear_stage()

    # ---------- 6: 출제자의 설계 ----------
    def scene6(self):
        self.vo("s6a")
        q = M(r"\frac{|g(x)-\mathbf{1}\cdot f(x)|}{g(x)}", 60).move_to([SX, 1.6, 0])
        self.play(TransformFromCopy(self.strip[1], q), run_time=1.2)
        self.play(Circumscribe(q, color=ACC), run_time=1.0)

        self.vo("s6b")
        qk = MathTex(r"\frac{|g(x)-", r"k", r"\,f(x)|}{g(x)}", font_size=50, color=W).move_to([SX + 2.6, 2.4, 0])
        qk[1].set_color(ACC)
        self.play(ReplacementTransform(q, qk), run_time=1.0)
        ax = self.stage_axes([-0.5, 3.5, 1], [-1, 3.2, 1], 5.0, 4.0, [SX - 1.3, -0.9, 0])
        fg = ax.plot(f, x_range=[-0.2, 3.2], color=DIM, stroke_width=4)
        k = ValueTracker(1.0)

        def col():
            return W if k.get_value() > 0.25 + 1e-3 else ACC

        hg = always_redraw(lambda: ax.plot(lambda x: f(x) + k.get_value(), x_range=[-0.1, 3.1],
                                           color=col(), stroke_width=5))
        kv = always_redraw(lambda: M(rf"k={k.get_value():.2f}", 52, col()).move_to([1.3, 0.2, 0]))
        hk = MathTex(r"h(x)=f(x)+", r"k", font_size=44, color=W).next_to(qk, DOWN, buff=0.35)
        hk[1].set_color(ACC)
        self.play(Create(ax), Create(fg), run_time=0.8)
        self.play(Create(hg), Write(hk), FadeIn(kv), run_time=1.2)
        self.wait(1.0)
        self.play(k.animate.set_value(0.6), run_time=1.5)

        self.vo("s6c")
        self.play(k.animate.set_value(0.25), run_time=2.2, rate_func=linear)
        self.play(Flash(ax.c2p(1.5, 0), color=ACC, line_length=0.35, num_lines=14), run_time=0.7)
        boom = T("h(x) = 0 → 극한 붕괴", 28, ACC).move_to([1.3, -0.55, 0])
        self.play(FadeIn(boom, scale=1.4), Wiggle(hg), run_time=1.2)

        self.vo("s6d")
        self.play(k.animate.set_value(1.0), FadeOut(boom), run_time=1.5)
        nl = NumberLine(x_range=[0, 1.5, 0.25], length=3.4, include_numbers=False,
                        color=DIM).move_to([1.2, -1.5, 0])
        safe = Line(nl.n2p(0.25), nl.n2p(1.5), color=W, stroke_width=8)
        hole = Circle(0.08, color=ACC, stroke_width=3).move_to(nl.n2p(0.25))
        ql = M(r"\tfrac14", 32, ACC).next_to(nl.n2p(0.25), DOWN)
        one = Dot(nl.n2p(1), color=ACC, radius=0.11)
        one_l = M("1", 34, ACC).next_to(one, UP)
        self.play(Create(nl), run_time=0.5)
        self.play(Create(safe), FadeIn(hole), FadeIn(ql), run_time=0.8)
        self.play(FadeIn(one, scale=2), FadeIn(one_l), run_time=0.6)
        res = M(r"k>\tfrac14", 52, ACC).next_to(nl, DOWN, buff=0.7)
        self.play(Write(res), run_time=0.8)
        self.sync()
        self.note("+ 1 대신 k 라면:  k > 1/4 일 때만", accent=0)
        self.clear_stage()

    # ---------- 마무리 ----------
    def outro(self):
        self.vo("out1")
        self.play(FadeOut(self.strip), FadeOut(self.src), run_time=0.6)
        whole = VGroup(self.card, *self.notes)
        self.play(whole.animate.move_to(ORIGIN), run_time=1.4)
        self.play(Indicate(self.answer_note, color=NOTE_ACC, scale_factor=1.06), run_time=1.0)
        self.sync(pad=1.5)
        self.play(FadeOut(whole), run_time=1.0)
