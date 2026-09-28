import os
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
from piper_service import PiperService

class TaxDWLCameraVoiceover(MovingCameraScene, VoiceoverScene):
    """
    Canonical 16:9 Long-Form Explainer Video:
    Topic: Commodity Tax, Incidence, and Deadweight Loss.
    Model: Demand P = 100 - Q, Supply P = 10 + Q, Specific Tax = $20.
    """

    def construct(self):
        # 1. Dual-TTS Engine Selection
        tts_mode = os.environ.get("TTS_SERVICE", "piper").lower()
        if tts_mode == "elevenlabs":
            self.set_speech_service(
                ElevenLabsService(
                    voice_name=os.environ.get("ELEVEN_VOICE_NAME", "Adam")
                )
            )
        else:
            self.set_speech_service(
                PiperService(model_path="voices/en-us-lessac-medium.onnx")
            )

        # 2. Camera State Initialization
        self.camera.frame.save_state()

        # 3. Setup Coordinate Axes
        axes = Axes(
            x_range=[0, 80, 10],
            y_range=[0, 110, 10],
            x_length=7.5,
            y_length=5.6,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=True
        ).to_corner(DL, buff=0.8)

        x_lbl = axes.get_x_axis_label(Text("Quantity (Q)", font_size=20), edge=RIGHT, direction=DOWN)
        y_lbl = axes.get_y_axis_label(Text("Price ($)", font_size=20), edge=UP, direction=LEFT)

        # 4. Functional Curves (Clean Numerics: P = 100 - Q, P = 10 + Q)
        d_curve = axes.plot(lambda q: 100 - q, x_range=[0, 75], color=BLUE_C, stroke_width=4)
        s_curve = axes.plot(lambda q: 10 + q, x_range=[0, 75], color=RED_C, stroke_width=4)
        s_tax_curve = axes.plot(lambda q: 30 + q, x_range=[0, 75], color=RED_A, stroke_width=4)

        d_label = Text("Demand", font_size=18, color=BLUE_C).next_to(axes.c2p(70, 30), UR, buff=0.1)
        s_label = Text("Supply", font_size=18, color=RED_C).next_to(axes.c2p(70, 80), UR, buff=0.1)
        s_tax_label = Text("Supply + Tax", font_size=18, color=RED_A).next_to(axes.c2p(65, 95), UL, buff=0.1)

        # --- SECTION 1: Market Baseline ---
        with self.voiceover(text="Consider a competitive market with downward sloping demand and upward sloping supply.") as trk:
            self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=trk.duration * 0.45)
            self.play(Create(d_curve), Write(d_label), Create(s_curve), Write(s_label), run_time=trk.duration * 0.55)

        eq_dot = Dot(axes.c2p(45, 55), color=WHITE)
        eq_lines = axes.get_lines_to_point(axes.c2p(45, 55), color=GRAY)
        eq_label = Text("E* (45 units, $55)", font_size=16).next_to(eq_dot, UR, buff=0.15)

        with self.voiceover(text="The market clears at forty-five units, establishing an equilibrium price of fifty-five dollars.") as trk:
            self.play(FadeIn(eq_dot), Create(eq_lines), Write(eq_label), run_time=trk.duration)

        # --- SECTION 2: Policy Intervention ---
        with self.voiceover(text="Now suppose lawmakers impose a twenty dollar per unit tax on sellers, driving a wedge into production costs.") as trk:
            self.play(
                Transform(s_curve, s_tax_curve),
                Transform(s_label, s_tax_label),
                run_time=trk.duration
            )

        # --- SECTION 3: Zooming into Deadweight Loss & Tax Wedge ---
        tax_eq_dot = Dot(axes.c2p(35, 65), color=YELLOW)
        wedge_target = axes.c2p(35, 55)

        # DWL Triangle: (35, 65) -> (35, 45) -> (45, 55)
        dwl_poly = Polygon(
            axes.c2p(35, 65), axes.c2p(35, 45), axes.c2p(45, 55),
            color=YELLOW, fill_opacity=0.6, stroke_width=2
        )
        dwl_label = Text("Deadweight Loss ($100)", font_size=18, color=YELLOW).next_to(dwl_poly, RIGHT, buff=0.2)

        # Tax Revenue Rectangle: (0, 45) to (35, 65)
        tax_rect = Polygon(
            axes.c2p(0, 45), axes.c2p(35, 45), axes.c2p(35, 65), axes.c2p(0, 65),
            color=PURPLE_C, fill_opacity=0.4, stroke_width=1.5
        )

        with self.voiceover(text="Output contracts to thirty-five units. Buyers pay sixty-five dollars, while sellers take home forty-five.") as trk:
            self.play(
                FadeIn(tax_eq_dot),
                self.camera.frame.animate.move_to(wedge_target).set(width=8.0),
                run_time=trk.duration
            )

        with self.voiceover(text="The government collects seven hundred dollars in revenue, but trades that should have happened are extinguished.") as trk:
            self.play(FadeIn(tax_rect), run_time=trk.duration)

        with self.voiceover(text="This yellow triangle isolates the deadweight loss: one hundred dollars of social surplus that simply ceases to exist.") as trk:
            self.play(FadeIn(dwl_poly), Write(dwl_label), Circumscribe(dwl_poly, shape=Rectangle), run_time=trk.duration)

        # --- SECTION 4: Camera Pullback & Conclusion ---
        with self.voiceover(text="When trade is taxed, the burden falls on both sides—and efficiency inevitably pays the price.") as trk:
            self.play(Restore(self.camera.frame), run_time=trk.duration)
            self.wait(1.0)
