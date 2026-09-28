# AGENT.md — EconLab Autonomous Agent Playbook
> **EconLab**: YouTube Animated Economics Channel (Manim Community + Remotion + Synthetic Voiceover)  
> **Target Audience**: AP/IB/Undergraduate Micro & Macroeconomics students, curious learners, policy wonks.  
> **Visual Identity**: 3Blue1Brown aesthetic, clean geometric intuition, dynamic camera zooms, synchronized narration.

---

## 1. Project Mission & Identity

EconLab produces high-retention, curriculum-aligned, mathematically rigorous yet visually intuitive economics explainer videos. 

### Core Tenet: "Intuition Through Geometry"
Economics textbooks drown students in static graphs and Greek letters. EconLab explains economics through **motion**:
- Curves shift smoothly across coordinates.
- Welfare areas (Consumer Surplus, Producer Surplus, Deadweight Loss, Tax Revenue) expand, shrink, and morph in real-time.
- The camera dynamically pans and zooms (`MovingCameraScene`) into critical regions (e.g., the tax wedge, the shortage gap) to explain the intuition, then pulls back to show the market overview.
- Synthetic voiceover narrates in lockstep with the visuals, with animation run-times mathematically anchored to spoken audio durations.

### Dual-Track Architecture
1. **Track 1: Manim (Python)** — **PRIMARY ENGINE** (90% of content). Ideal for continuous curves, supply/demand shifts, calculus/welfare geometry, split-screen elasticity comparisons, camera framing.
2. **Track 2: Remotion (React/TypeScript)** — **SECONDARY ENGINE** (10% of content). Ideal for discrete UI/motion-graphics layouts: Game theory payoff matrices, decision trees, auction timers, and data dashboards.

---

## 2. Environment & Execution Protocols (Windows / PowerShell)

### Conda Environment Discipline
All Python and Manim commands **must run inside the `econ` conda environment**.
```powershell
# Activate the main conda environment
conda activate econ
```

### Dependency Installation & Maintenance
If setting up or verifying the environment on Windows:

```powershell
# 1. Python dependencies (in 'econ' conda environment)
conda activate econ
pip install manim manim-voiceover piper-tts "elevenlabs<0.3,>=0.2.27"

# 2. System binaries needed on Windows:
# FFmpeg (video encoding)
winget install Gyan.FFmpeg   # or: choco install ffmpeg

# SoX (required by manim-voiceover for audio splicing/normalization)
# Without SoX, manim-voiceover throws "WARNING SoX could not be found!" and breaks.
choco install sox.portable   # or download SoX Windows binary and add to PATH

# 3. Remotion setup (Node.js track)
cd remotion-demo
npm install
npx remotion browser ensure   # Mandatory: installs headless Chromium shell
```

### Manim Render Commands Cheat-Sheet
Always test at low quality first before rendering high resolution.

| Preset | Quality Flag | Resolution & FPS | Use Case | Command Example |
| :--- | :--- | :--- | :--- | :--- |
| **Draft** | `-ql` | 480p @ 15fps | Rapid visual & timing check | `manim -ql scene.py SceneClassName` |
| **Medium** | `-qm` | 720p @ 30fps | Reviewing text readability & motion | `manim -qm scene.py SceneClassName` |
| **Master** | `-qh` | 1080p @ 60fps | Production YouTube upload | `manim -qh scene.py SceneClassName` |
| **4K** | `-qk` | 2160p @ 60fps | Archival / 4K upload | `manim -qk scene.py SceneClassName` |
| **Shorts** | `-qh` + custom | 1080x1920 (9:16) | YouTube Shorts / TikTok | `manim -qh --pixel_width=1080 --pixel_height=1920 scene.py SceneName` |

Output files land in `media/videos/<script_name>/<quality>/<SceneClassName>.mp4`, alongside auto-generated `<SceneClassName>.srt` subtitle tracks.

---

## 3. "Clean Numerics" Modeling Standard

To ensure that on-screen coordinates, axis tick marks, area polygons, and spoken narration stay perfectly clean and easy to mental-math, **every economic model must use integer or clean half-integer coordinates**. Never use messy floating-point numbers like $Q=31.42, P=68.57$.

### Canonical Benchmark Models Table

| Topic | Equation / Setup | Baseline Equilibrium | Shock / Policy Intervention | Post-Shock Outcome & Welfare |
| :--- | :--- | :--- | :--- | :--- |
| **Tax & DWL (Master Template)** | $P = 100 - Q$<br>$P = 10 + Q$ | $Q^* = 45$<br>$P^* = \$55$ | \$20 specific tax on sellers ($P = 30 + Q$) | $Q' = 35$<br>Buyers pay: \$65, Sellers receive: \$45<br>Tax Rev = \$700, DWL = \$100 |
| **Price Ceiling (Rent Control)** | $P = 100 - Q$<br>$P = 10 + Q$ | $Q^* = 45$<br>$P^* = \$55$ | Maximum price capped at $P_{cap} = \$40$ | $Q_S = 30, Q_D = 60$<br>Shortage = 30 units<br>Transferred CS, DWL triangle |
| **Price Floor (Minimum Wage)** | $P = 100 - Q$<br>$P = 10 + Q$ | $Q^* = 45$<br>$P^* = \$55$ | Minimum price set at $P_{floor} = \$70$ | $Q_D = 30, Q_S = 60$<br>Surplus = 30 units (unemployment)<br>Transferred PS, DWL triangle |
| **Production Subsidy** | $P = 100 - Q$<br>$P = 10 + Q$ | $Q^* = 45$<br>$P^* = \$55$ | \$20 specific subsidy ($P = -10 + Q$) | $Q' = 55$<br>Buyers pay: \$45, Sellers get: \$65<br>Gov Cost = \$1100, DWL = \$100 (overproduction) |
| **Negative Externality** | Demand: $P = 100 - Q$<br>$MPC = 10 + Q$<br>$MSC = 30 + Q$ | Private Market:<br>$Q_M = 45, P_M = \$55$ | Pigouvian Tax: $t = \$20$ internalizing MEC | Social Optimum: $Q_{opt} = 35, P_{opt} = \$65$<br>Eliminates DWL of \$100 |
| **Monopoly vs Perfect Comp** | Demand: $P = 100 - Q$<br>$MR = 100 - 2Q$<br>$MC = 20$ | Competitive:<br>$Q_C = 80, P_C = \$20$ | Single-price monopolist sets $MR = MC$ | $Q_M = 40, P_M = \$60$<br>Monopoly Profit = \$1,600<br>Deadweight Loss = \$400 |

---

## 4. Voiceover & Audio Pipeline Specification

### Dual-TTS Engine Strategy
We never burn paid API credits during development. The pipeline dynamically selects between Piper (offline/free) and ElevenLabs (cloud/paid):

```
Development & Iteration (Piper TTS)        Production Master (ElevenLabs TTS)
- Local, 100% offline, zero latency        - Studio broadcast voice
- Unlimited renders & script tweaks         - Activated only via TTS_SERVICE=elevenlabs
- Uses piper_service.py + ONNX voice        - Requires ELEVEN_API_KEY environment variable
```

### Voiceover Context Manager Pattern
Every visual animation must be tied directly to narration pacing using `manim-voiceover`:

```python
with self.voiceover(text="Here the government imposes a twenty dollar tax per unit.") as tracker:
    self.play(
        Transform(supply_curve, supply_tax_curve),
        Transform(supply_label, supply_tax_label),
        run_time=tracker.duration  # Synchronizes animation exactly with voice
    )
```

### Audio Cache Integrity & Cost Control
- `manim-voiceover` hashes each sentence string and caches the audio in `media/voiceovers/`.
- **Golden Rule**: If you only adjust camera coordinates, curve colors, or visual timings, **do not change the narration text strings**. The cached audio will be reused instantly with zero TTS calls and zero credit burn.
- Never hardcode API keys in code or commit them to git. Always use `$env:ELEVEN_API_KEY`.

### Piper Voice Models
Piper voice models reside in `voices/`:
- Fast dev default: `en_US-lessac-medium.onnx` + `en_US-lessac-medium.onnx.json`
- High-quality offline alternative: `en_US-lessac-high` or `en_US-ryan-high` (downloadable via `python -m piper.download_voices en_US-lessac-high --download-dir voices/`).

---

## 5. Full Manim Feature Exploration Guidelines

To produce broadcast-quality animations, agents must leverage the full spectrum of Manim features:

### 1. Dynamic Camera Work (`MovingCameraScene`)
Never keep a static camera for an entire 90-second video.
- **Initialize & Save**: `self.camera.frame.save_state()` at the start of the scene.
- **Zoom into Wedge/Shortage**:
  ```python
  zoom_target = axes.c2p(35, 55) # focus on the tax wedge
  self.play(
      self.camera.frame.animate.move_to(zoom_target).set(width=8.0),
      run_time=tracker.duration
  )
  ```
- **Reset to Full Market**:
  ```python
  self.play(Restore(self.camera.frame), run_time=1.5)
  ```

### 2. Geometry, Area Shading & Riemann Regions
- Use `axes.get_area(curve, x_range=[a, b], bounded_graph=other_curve, color=..., opacity=...)` for Consumer Surplus, Producer Surplus, and Deadweight Loss triangles.
- For non-standard polygons (e.g. tax revenue rectangle): construct a `Polygon` using coordinates converted via `axes.c2p(q, p)`.
- Use `axes.get_vertical_line(axes.c2p(Q, P), line_func=DashedLine)` and `axes.get_horizontal_line(...)` for dotted equilibrium guides.

### 3. Continuous Parameter Sweeps (`ValueTracker` & `always_redraw`)
For concepts showing sensitivity (e.g., as tax rate increases from \$0 to \$40, showing the Laffer curve or DWL explosion):
```python
tax_tracker = ValueTracker(0)

supply_tax = always_redraw(lambda: 
    axes.plot(lambda q: 10 + q + tax_tracker.get_value(), x_range=[0, 70], color=RED)
)
self.play(tax_tracker.animate.set_value(20), run_time=3.0)
```

### 4. Directing Viewer Focus
- Use `Indicate(mobject, color=YELLOW, scale_factor=1.2)` to emphasize an equilibrium point.
- Use `Circumscribe(mobject, shape=Circle)` to highlight the deadweight loss triangle.
- Use `Wiggle(mobject)` or `Flash(point)` when a policy disruption hits the market.

### 5. Color Palette System (High-Contrast Academic Aesthetic)
Maintain consistent color semantics across the channel:
- **Demand Curve**: `BLUE_C` or `#58C4DD`
- **Supply Curve**: `RED_C` or `#FC6255`
- **Equilibrium Point / Guides**: `WHITE` with `DashedLine(color=GRAY)`
- **Consumer Surplus**: `GREEN_D` (`opacity=0.35`)
- **Producer Surplus**: `ORANGE` or `YELLOW_D` (`opacity=0.35`)
- **Tax Revenue Rectangle**: `PURPLE_C` or `TEAL_C` (`opacity=0.5`)
- **Deadweight Loss (DWL)**: `YELLOW_C` or `#FF5555` (`opacity=0.6`)
- **Shortage / Surplus Bar**: `RED_A` (`opacity=0.4`)

---

## 6. Known Gotchas & Troubleshooting Playbook

| Issue / Symptom | Root Cause | Exact Solution |
| :--- | :--- | :--- |
| **Text clips off-screen during camera zoom** | Manim `Text()` is ~0.3 scene-units wide per character (much wider than 0.1). | Budget camera frame width generously (`set(width=8.0)` or higher), scale text down (`font_size=20-24`), or anchor labels with `next_to(..., buff=0.1)`. |
| **Glyphs appear as half-outlined "ghosts"** | Manim's `Write()` strokes glyph outlines before filling them. Normal behavior during animation frames. | No fix needed. If a static label is needed immediately, use `FadeIn(label)` or `Create(label)` instead of `Write()`. |
| **`pangocairo >= 1.30.0 is required`** | `manimpango` requires Pango/Cairo C development headers to build. | On Windows, ensure pre-built wheels are installed via pip (`pip install manimpango`), or install GTK/cairo runtime. |
| **`WARNING SoX could not be found!`** | `manim-voiceover` depends on SoX CLI for audio splicing. | Install SoX (`choco install sox.portable` on Windows) and confirm `sox --version` works in PowerShell. |
| **ElevenLabs SDK Error on import/generate** | `manim-voiceover`'s `ElevenLabsService` requires the legacy ElevenLabs SDK. | Pin the package: `pip install "elevenlabs<0.3,>=0.2.27"`. Do not upgrade to ElevenLabs v1+. |
| **Remotion H.264 render fails** | Remotion / H.264 encoder requires strictly even pixel dimensions. | Never use odd numbers for width/height. Use `1920x1080` (16:9) or `1080x1920` (9:16). |
| **Remotion: "Old Headless mode removed"** | Newer Chrome/Chromium versions removed legacy headless mode. | Run `npx remotion browser ensure` once per machine to download `chrome-headless-shell`. |
| **Remotion: "does not contain registerRoot"** | Missing `registerRoot(RemotionRoot)` in root file. | Always wrap exported compositions with `registerRoot` in `src/index.tsx`. Wrap multiple compositions in a `<>...</>` fragment. |

---

## 7. Canonical Code Boilerplates

### A. Custom Piper Speech Service (`piper_service.py`)
Save in `manim-demo/piper_service.py`. This provides free, local speech synthesis for `manim-voiceover`:

```python
from pathlib import Path
import subprocess
import sys
import wave
from manim_voiceover.services.base import SpeechService

class PiperService(SpeechService):
    """Local offline TTS service for manim-voiceover using Piper TTS."""

    def __init__(
        self,
        model_path: str = "voices/en-us-lessac-medium.onnx",
        config_path: str = None,
        **kwargs
    ):
        self.model_path = Path(model_path).resolve()
        self.config_path = Path(config_path or f"{model_path}.json").resolve()
        if not self.model_path.exists():
            raise FileNotFoundError(f"Piper model not found at {self.model_path}")
        super().__init__(**kwargs)

    def generate_from_text(self, text: str, cache_dir: str = None, path: str = None, **kwargs) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir
        
        audio_path = Path(path) if path else Path(cache_dir) / f"{self.get_data_hash(text)}.wav"
        
        if not audio_path.exists():
            cmd = [
                sys.executable, "-m", "piper",
                "--model", str(self.model_path),
                "--config", str(self.config_path),
                "--output_file", str(audio_path)
            ]
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            _, stderr = process.communicate(input=text)
            if process.returncode != 0:
                raise RuntimeError(f"Piper failed: {stderr}")

        with wave.open(str(audio_path), "rb") as wf:
            duration = wf.getnframes() / float(wf.getframerate())

        return {
            "final_audio": str(audio_path),
            "word_boundaries": [],
            "duration": duration
        }
```

### B. Master Template: Tax & Deadweight Loss (`tax_dwl_camera_voiceover.py`)
This script serves as the blueprint for all future microeconomics curve-shifting videos:

```python
import os
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
from piper_service import PiperService

class TaxDWLCameraVoiceover(MovingCameraScene, VoiceoverScene):
    def construct(self):
        # 1. Initialize Speech Service (Piper by default, ElevenLabs if specified)
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

        # 2. Camera setup
        self.camera.frame.save_state()

        # 3. Setup Coordinate Axes
        axes = Axes(
            x_range=[0, 80, 10],
            y_range=[0, 110, 10],
            x_length=7,
            y_length=5.5,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=True
        ).to_corner(DL, buff=0.8)

        x_lbl = axes.get_x_axis_label(Text("Quantity (Q)", font_size=20), edge=RIGHT, direction=DOWN)
        y_lbl = axes.get_y_axis_label(Text("Price ($)", font_size=20), edge=UP, direction=LEFT)

        # 4. Define Functional Curves (Clean Numerics: P = 100 - Q, P = 10 + Q)
        demand_fn = lambda q: 100 - q
        supply_fn = lambda q: 10 + q
        supply_tax_fn = lambda q: 30 + q  # $20 tax

        d_curve = axes.plot(demand_fn, x_range=[0, 75], color=BLUE_C, stroke_width=4)
        s_curve = axes.plot(supply_fn, x_range=[0, 75], color=RED_C, stroke_width=4)
        s_tax_curve = axes.plot(supply_tax_fn, x_range=[0, 75], color=RED_A, stroke_width=4)

        d_label = Text("Demand", font_size=18, color=BLUE_C).next_to(axes.c2p(70, 30), UR, buff=0.1)
        s_label = Text("Supply", font_size=18, color=RED_C).next_to(axes.c2p(70, 80), UR, buff=0.1)
        s_tax_label = Text("Supply + Tax", font_size=18, color=RED_A).next_to(axes.c2p(65, 95), UL, buff=0.1)

        # Scene Step 1: Equilibrium
        with self.voiceover(text="Consider a competitive market with downward sloping demand and upward sloping supply.") as trk:
            self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=trk.duration * 0.5)
            self.play(Create(d_curve), Write(d_label), Create(s_curve), Write(s_label), run_time=trk.duration * 0.5)

        eq_dot = Dot(axes.c2p(45, 55), color=WHITE)
        eq_lines = axes.get_lines_to_point(axes.c2p(45, 55), color=GRAY)
        eq_label = Text("E* (Q=45, P=$55)", font_size=16).next_to(eq_dot, UR, buff=0.15)

        with self.voiceover(text="The market clears at an equilibrium quantity of forty-five units, and a price of fifty-five dollars.") as trk:
            self.play(FadeIn(eq_dot), Create(eq_lines), Write(eq_label), run_time=trk.duration)

        # Scene Step 2: Policy Shock (Tax)
        with self.voiceover(text="Now, suppose the government levies a twenty dollar tax per unit on sellers, shifting supply upward.") as trk:
            self.play(
                Transform(s_curve, s_tax_curve),
                Transform(s_label, s_tax_label),
                run_time=trk.duration
            )

        # Scene Step 3: Zoom In on Deadweight Loss & Tax Wedge
        tax_eq_dot = Dot(axes.c2p(35, 65), color=YELLOW)
        wedge_target = axes.c2p(35, 55)

        # DWL Triangle: Vertices (35, 65), (35, 45), (45, 55)
        dwl_poly = Polygon(
            axes.c2p(35, 65), axes.c2p(35, 45), axes.c2p(45, 55),
            color=YELLOW, fill_opacity=0.6, stroke_width=2
        )
        dwl_label = Text("Deadweight Loss ($100)", font_size=18, color=YELLOW).next_to(dwl_poly, RIGHT, buff=0.2)

        with self.voiceover(text="The new quantity drops to thirty-five. Buyers pay sixty-five, while sellers receive forty-five.") as trk:
            self.play(
                FadeIn(tax_eq_dot),
                self.camera.frame.animate.move_to(wedge_target).set(width=7.5),
                run_time=trk.duration
            )

        with self.voiceover(text="Because mutually beneficial trades are eliminated, this yellow triangle represents deadweight loss.") as trk:
            self.play(FadeIn(dwl_poly), Write(dwl_label), run_time=trk.duration)

        # Scene Step 4: Reset Camera Overview
        with self.voiceover(text="Total tax revenue reaches seven hundred dollars, but one hundred dollars in social welfare vanishes.") as trk:
            self.play(Restore(self.camera.frame), run_time=trk.duration)
            self.wait(1.0)
```

---

## 8. Content Production Roadmap (Micro & Macro)

When building new episodes, agents must tackle topics in this validated sequence:

```
[Phase 1: Core Price Controls & Fiscal Policy]
├── Ep 1: Tax & Deadweight Loss (Template Completed)
├── Ep 2: Price Ceilings & Rent Control (Shortage gap, non-price rationing)
├── Ep 3: Price Floors & Minimum Wage (Surplus gap, unemployment, lost surplus)
└── Ep 4: Subsidies & Overproduction (Deadweight loss beyond equilibrium)

[Phase 2: Market Failures & Market Power]
├── Ep 5: Negative Externalities & Pigouvian Taxes (MPC vs MSC, social optimum)
├── Ep 6: Positive Externalities & Subsidies (MPB vs MSB, underproduction)
├── Ep 7: Elasticity & Tax Incidence (Split-screen comparison: steep vs flat curves)
└── Ep 8: Monopoly vs Perfect Competition (MR=MC, consumer surplus extraction, DWL)

[Phase 3: Strategic Behavior & Remotion UI Track]
├── Ep R1: Prisoner's Dilemma & Payoff Matrix (Remotion animated matrix & dominant strategies)
└── Ep R2: Cournot vs Bertrand Duopoly (Reaction curves & price wars)

[Phase 4: Macroeconomic Fundamentals (Deferred until Micro is complete)]
├── Ep M1: The AD-AS Framework (Short-run vs long-run macroeconomic equilibrium)
├── Ep M2: The Phillips Curve & Inflation Expectations
└── Ep M3: The IS-LM Model (Monetary vs Fiscal policy transmission)
```

---

## 9. Academic Narration & Scriptwriting Rules (AI Evasion Compliant)

All narration scripts must strictly adhere to the project's writing standards:

1. **Burstiness & Sentence Length Variation**:
   - Never write uniform 15-word sentences. Alternate between sharp punchy statements (3–6 words) and compound analytical observations (25+ words).
   - *Example*: "Prices freeze at forty dollars. But demand surges to sixty units while suppliers withdraw, opening a thirty-unit shortage that price signals can no longer resolve."
2. **Forbidden AI Vocabulary**:
   - **Transitions to Avoid**: "Furthermore", "Moreover", "Notably", "Additionally", "Consequently", "It is important to note that".
   - **Adjectives/Verbs to Avoid**: "Pivotal", "Crucial", "Delve into", "Underscore", "Tapestry", "Nuanced", "In conclusion".
   - **Human Alternatives**: "The market responds immediately:", "Notice what happens at the margin:", "Here the welfare arithmetic breaks down:", "Look closely at the wedge:".
3. **Conversational Academic Cadence**:
   - Write for spoken delivery. Numbers should be spelled phonetically where clarity requires ("forty-five", not "45") so the TTS engine pronounces them naturally.
   - Use active voice ($>70\%$).

---

## 10. Agent Standard Operating Procedure (SOP)

When an agent is tasked with creating a new video episode (e.g., "Build the Price Ceiling episode"):

### Step 1: Numerics & Script Specification
1. Select clean integer parameters from Section 3.
2. Draft the script with 4 to 6 discrete narration blocks.
3. Verify that the script contains no forbidden AI transitions and has natural rhythmic burstiness.

### Step 2: Manim Code Assembly
1. Clone the canonical structure from `tax_dwl_camera_voiceover.py`.
2. Define the new curve functions, equilibrium points, and welfare polygons.
3. Configure camera pan/zoom targets to focus on the key economic tension (e.g. the shortage gap).
4. Wrap every visual transition inside `with self.voiceover(text=...) as tracker:`.

### Step 3: Fast Local Draft Verification
1. Run low-quality render with Piper TTS in the `econ` environment:
   ```powershell
   conda activate econ
   manim -ql price_ceiling.py PriceCeilingVoiceover
   ```
2. Check for text clipping, label overlap, or camera frame overflow.

### Step 4: Visual Polish & Production Render
1. Adjust label positions with `buff` or `next_to` anchors.
2. Render master 1080p60:
   ```powershell
   manim -qh price_ceiling.py PriceCeilingVoiceover
   ```
3. (Optional final pass) If authorized by user, render with ElevenLabs:
   ```powershell
   $env:TTS_SERVICE="elevenlabs"
   $env:ELEVEN_API_KEY="<user_key>"
   manim -qh price_ceiling.py PriceCeilingVoiceover
   ```

### Step 5: Deliverables Checklist
Before reporting completion, verify:
- [ ] Rendered MP4 exists and plays smoothly.
- [ ] Auto-generated `.srt` subtitle file matches narration.
- [ ] No labels clipped during zoom frames.
- [ ] Clean integer economics verified.
- [ ] Narration passes AI evasion check (zero forbidden transition words).
