import os
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
from piper_service import PiperService

class PriceCeilingShort(MovingCameraScene, VoiceoverScene):
    """
    Canonical 9:16 Vertical YouTube Shorts Template:
    Topic: Rent Control & Shortages.
    Model: P = 100 - Q, P = 10 + Q, Ceiling = $40.
    Aspect Ratio: 1080x1920 (Render with --pixel_width=1080 --pixel_height=1920)
    """

    def construct(self):
        # 1. Voice Service Configuration
        tts_mode = os.environ.get("TTS_SERVICE", "piper").lower()
        if tts_mode == "elevenlabs":
            self.set_speech_service(ElevenLabsService(voice_name=os.environ.get("ELEVEN_VOICE_NAME", "Adam")))
        else:
            self.set_speech_service(PiperService(model_path="voices/en-us-lessac-medium.onnx"))

        # 2. ZONE 1: Mobile Hook Card (Top Screen Third)
        hook_title = Text("WHY RENT CONTROL", font_size=32, weight=BOLD, color=YELLOW)
        hook_sub = Text("MAKES HOUSING WORSE", font_size=22, color=WHITE)
        hook_group = VGroup(hook_title, hook_sub).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.8)

        # 3. ZONE 2: Rescaled Center Coordinate System
        axes = Axes(
            x_range=[0, 80, 20],
            y_range=[0, 100, 20],
            x_length=5.2,
            y_length=4.4,
            axis_config={"include_numbers": True, "font_size": 16},
            tips=False
        ).move_to(ORIGIN + UP * 0.2)

        x_lbl = axes.get_x_axis_label(Text("Q", font_size=18), edge=RIGHT, direction=DOWN)
        y_lbl = axes.get_y_axis_label(Text("P ($)", font_size=18), edge=UP, direction=LEFT)

        d_curve = axes.plot(lambda q: 100 - q, x_range=[0, 75], color=BLUE_C, stroke_width=4)
        s_curve = axes.plot(lambda q: 10 + q, x_range=[0, 75], color=RED_C, stroke_width=4)

        d_tag = Text("D", font_size=18, color=BLUE_C).next_to(axes.c2p(70, 30), RIGHT, buff=0.1)
        s_tag = Text("S", font_size=18, color=RED_C).next_to(axes.c2p(70, 80), RIGHT, buff=0.1)

        # Fast 40-second script with strong hook
        with self.voiceover(text="Rent control sounds compassionate. But geometry exposes the painful trade-off.") as trk:
            self.play(FadeIn(hook_group), Create(axes), Write(x_lbl), Write(y_lbl), run_time=trk.duration * 0.4)
            self.play(Create(d_curve), Write(d_tag), Create(s_curve), Write(s_tag), run_time=trk.duration * 0.6)

        # Equilibrium Marker
        eq_dot = Dot(axes.c2p(45, 55), color=WHITE, radius=0.08)
        eq_txt = Text("Free Market: $55", font_size=16).next_to(eq_dot, UR, buff=0.1)

        with self.voiceover(text="In a free market, rent stabilizes at fifty-five dollars for forty-five units.") as trk:
            self.play(FadeIn(eq_dot), Write(eq_txt), run_time=trk.duration)

        # Price Ceiling Imposition
        cap_line = DashedLine(axes.c2p(0, 40), axes.c2p(75, 40), color=GOLD, stroke_width=3)
        cap_label = Text("Price Cap: $40", font_size=18, color=GOLD).next_to(axes.c2p(35, 40), UP, buff=0.1)

        with self.voiceover(text="When a law caps rent at forty dollars, landlords withdraw units, dropping supply to thirty.") as trk:
            self.play(FadeOut(eq_txt), Create(cap_line), Write(cap_label), run_time=trk.duration)

        # Shortage Bracket (Zone 3 Visual Anchor)
        shortage_brace = BraceBetweenPoints(axes.c2p(30, 40), axes.c2p(60, 40), direction=DOWN, color=RED_B)
        shortage_txt = shortage_brace.get_text("Shortage: 30 Units").scale(0.65).set_color(RED_B)

        with self.voiceover(text="Meanwhile, sixty eager tenants queue up. The result isn't affordable housing—it's a thirty-unit shortage.") as trk:
            self.play(GrowFromCenter(shortage_brace), FadeIn(shortage_txt), run_time=trk.duration)

        # Final Hook to Long Form Video
        with self.voiceover(text="Watch the full proof and welfare breakdown in our pinned video below.") as trk:
            self.play(Indicate(shortage_txt, scale_factor=1.15, color=YELLOW), run_time=trk.duration)
            self.wait(0.5)
