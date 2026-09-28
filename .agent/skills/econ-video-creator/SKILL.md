---
name: econ-video-creator
description: End-to-end skill for producing animated economics explainer videos and YouTube Shorts using Manim Community, Remotion, and synthetic voiceovers (Piper/ElevenLabs). Covers clean integer economics modeling, dynamic camera framing, audio-visual synchronization, and monetization packaging.
---

# Economics Video Creation Skill (`econ-video-creator`)

This skill provides an autonomous agent with everything required to design, script, code, animate, voice, and render curriculum-aligned economics explainer videos and YouTube Shorts.

---

## 1. Skill Folder Structure & Available Assets

Every agent working on video creation must utilize the resources packaged within this skill:

```
.agent/skills/econ-video-creator/
├── SKILL.md                          # This instruction manual
├── references/
│   ├── clean_numerics_models.json   # Exact integer equations, equilibria, and coordinate points
│   ├── color_palette.json           # Channel standard hex color codes, opacities, and roles
│   └── monetization_flywheel.md     # Shorts-to-longs flywheel, high-RPM SEO, script hooks
├── templates/
│   ├── piper_service.py             # Local Piper TTS speech service for manim-voiceover
│   ├── tax_dwl_camera_voiceover.py  # Canonical 16:9 Long-Form Manim master template
│   ├── price_ceiling_short.py       # Canonical 9:16 Shorts vertical Manim template
│   └── remotion_payoff_matrix.tsx   # Remotion Game Theory payoff matrix template
└── scripts/
    ├── render_video.py              # CLI automation to validate dependencies and render
    ├── download_piper_voice.py      # Quick downloader for Piper ONNX voice models
    └── check_audio_cache.py         # Audits cached audio to prevent ElevenLabs credit burn
```

---

## 2. Core Philosophy & Dual-Engine Architecture

EconLab teaches economics through **motion rather than static textbook diagrams**:
- Curves slide dynamically to reflect market shocks.
- The camera actively pans and zooms (`MovingCameraScene`) into deadweight loss triangles, tax wedges, and shortage gaps.
- Synthetic voiceover runs in lockstep with the visuals (`with self.voiceover(...) as tracker: self.play(..., run_time=tracker.duration)`).

### Dual-Track Selection Rule
- **Track 1: Manim (Python) — PRIMARY (90% of videos)**:
  Use for all continuous curves, welfare geometry (Consumer Surplus, Producer Surplus, Deadweight Loss), supply/demand shifts, elasticity comparisons, and externalities.
- **Track 2: Remotion (React/TypeScript) — SECONDARY (10% of videos)**:
  Use for discrete UI components: Game theory payoff matrices (Prisoner's Dilemma, Cournot), decision trees, auction timers, and macroeconomic dashboards.

---

## 3. The 6-Stage End-to-End Production SOP

When asked to produce a video on any economic concept, execute these 6 stages:

```
[ Stage 1: Model Selection ] ────► Select clean integer model from clean_numerics_models.json
             │
[ Stage 2: Dual Scripting ]  ────► Write 40s Short script (hook/paradox) + 2.5m Long script
             │
[ Stage 3: Manim Coding ]    ────► Implement 16:9 (Long) & 9:16 (Short) Scene classes
             │
[ Stage 4: Local Audio & QA] ────► Render draft with Piper TTS (-ql) in conda 'econ'
             │
[ Stage 5: Frame Polish ]    ────► Verify camera zoom safety (no text clipping) & sync
             │
[ Stage 6: Master Render ]   ────► Render 1080p60 (-qh) + generate YouTube metadata
```

---

### Stage 1: Economic Model Specification ("Clean Numerics")
Never invent random equations with messy decimals. Always load or conform to [`references/clean_numerics_models.json`](file:///C:/Users/yasan/OneDrive/Desktop/EconLab/.agent/skills/econ-video-creator/references/clean_numerics_models.json):

- **Baseline Market**: Demand $P = 100 - Q$, Supply $P = 10 + Q \implies Q^* = 45, P^* = \$55$.
- **Tax (\$20)**: $S_{tax}: P = 30 + Q \implies Q' = 35, P_B = \$65, P_S = \$45, \text{Rev} = \$700, \text{DWL} = \$100$.
- **Price Ceiling (\$40)**: $Q_S = 30, Q_D = 60 \implies \text{Shortage} = 30\text{ units}$.
- **Price Floor (\$70)**: $Q_D = 30, Q_S = 60 \implies \text{Surplus} = 30\text{ units}$.
- **Subsidy (\$20)**: $S_{sub}: P = -10 + Q \implies Q' = 55, P_B = \$45, P_S = \$65, \text{DWL} = \$100$.
- **Negative Externality**: $MPC: P = 10 + Q, MSC: P = 30 + Q, t = \$20 \implies Q_{opt} = 35$.
- **Monopoly**: $P = 100 - Q, MR = 100 - 2Q, MC = 20 \implies Q_M = 40, P_M = \$60, \text{Profit} = \$1600$.

---

### Stage 2: Dual Scriptwriting (AI-Evasion Compliant)
Every topic gets two complementary scripts:

1. **Short-Form Script (35–45 seconds / ~130 words)**:
   - Starts with a 2-second pattern interrupt hook (e.g., *"Why does capping rent at \$1,000 make housing MORE expensive?"*).
   - Shows the immediate supply retraction.
   - Highlights the shortage or deadweight loss.
   - Ends with a CTA to the long-form link.
2. **Long-Form Script (2–3 minutes / ~400–500 words)**:
   - Full pedagogical progression: Real-world context $\to$ Free market baseline $\to$ Intervention shock $\to$ Camera zoom into welfare wedge $\to$ Mathematical and intuitive summary.
3. **Style Rules**:
   - Zero forbidden transitions (*Furthermore, Moreover, Notably, Additionally*).
   - High burstiness: alternate 4-word punchy declarations with 25-word analytical sentences.
   - Numbers written out phonetically for TTS clarity (*"forty-five"*, not *"45"*).

---

### Stage 3: Manim Scene Architecture

#### 16:9 Long-Form Architecture (`TaxDWLLong`)
- Extend `MovingCameraScene` and `VoiceoverScene`.
- Call `self.camera.frame.save_state()` at start.
- Wrap animations in `with self.voiceover(text=...) as trk:`.
- Zoom into critical regions:
  ```python
  self.play(
      self.camera.frame.animate.move_to(axes.c2p(35, 55)).set(width=8.0),
      run_time=trk.duration
  )
  ```
- Restore camera: `self.play(Restore(self.camera.frame))`.

#### 9:16 Shorts Vertical Architecture (`PriceCeilingShort`)
- Canvas is divided into 3 vertical zones:
  - **Zone 1 (Top third)**: Bold Hook Card (`Text(..., font_size=32).to_edge(UP, buff=0.8)`).
  - **Zone 2 (Center third)**: Rescaled coordinate axes (`Axes(x_length=5.2, y_length=4.4).move_to(ORIGIN)`).
  - **Zone 3 (Bottom third)**: Dynamic callouts, braces (`BraceBetweenPoints`), and kinetic text.

---

### Stage 4: Local Audio & QA Execution
Run renders inside the `econ` conda environment on Windows PowerShell:

```powershell
# 1. Activate conda environment
conda activate econ

# 2. Render fast draft (480p @ 15fps) using local Piper TTS
python .agent/skills/econ-video-creator/scripts/render_video.py tax_dwl.py TaxDWLCameraVoiceover -q l --aspect 16:9 --tts piper

# 3. Render Shorts draft (480x854)
python .agent/skills/econ-video-creator/scripts/render_video.py price_ceiling.py PriceCeilingShort -q l --aspect 9:16 --tts piper
```

---

### Stage 5: Frame Safety & Polish Checklist
Before triggering the master render, verify:
- [ ] **Text Width Safety**: Did you account for `Text()` being ~0.3 scene-units wide per character? Ensure labels don't clip off camera edges during zoom.
- [ ] **Color Semantics**: Verify Demand is Blue (`#58C4DD`), Supply is Red (`#FC6255`), DWL is Yellow (`#FFFF00`).
- [ ] **Run-Time Lockstep**: Are all visual transformations explicitly using `run_time=trk.duration`?
- [ ] **Audio Cache Intact**: Check `python .agent/skills/econ-video-creator/scripts/check_audio_cache.py`.

---

### Stage 6: Master Render & YouTube Packaging

```powershell
# Render 1080p60 Master Long Video
manim -qh tax_dwl.py TaxDWLCameraVoiceover

# Render 1080x1920 60fps Master Short
manim -qh --pixel_width=1080 --pixel_height=1920 price_ceiling.py PriceCeilingShort
```

Assemble YouTube metadata following [`references/monetization_flywheel.md`](file:///C:/Users/yasan/OneDrive/Desktop/EconLab/.agent/skills/econ-video-creator/references/monetization_flywheel.md):
- 3 click-worthy title options (Curiosity, Provocative, Search/AP).
- Description with exact timestamps from `manim-voiceover` audio tracks.
- Pinned comment routing traffic from Short to Long.

---

## 4. Troubleshooting & Known Gotchas

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| `WARNING SoX could not be found!` | `manim-voiceover` needs SoX CLI to splice WAVs. | Install via `choco install sox.portable` and verify `sox --version` in terminal. |
| ElevenLabs API Error | Installed latest ElevenLabs v1+ SDK instead of legacy SDK. | Run `pip install "elevenlabs<0.3,>=0.2.27"`. |
| Label clipped during camera zoom | Text is wider than estimated (~0.3 units/char). | Set camera zoom width $\ge 7.5$ units, use `font_size=18-22`, or position with `UR, buff=0.1`. |
| Remotion H.264 render fails | Odd pixel dimension in composition. | Enforce even dimensions: `1920x1080` (16:9) or `1080x1920` (9:16). |
| Remotion headless browser error | System Chrome removed old headless mode. | Run `npx remotion browser ensure` to install matching headless shell. |
| ElevenLabs credits draining rapidly | Text strings altered during visual tweaking. | Do not touch narration strings when editing visuals. Audio hashes in `media/voiceovers/` will be reused. |
