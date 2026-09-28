# Monetization & Content Flywheel Playbook

This reference outlines the monetization mechanics, script packaging, and packaging formulas for EconLab videos.

---

## 1. The Core RPM Advantage

Economics and financial education attract high CPM/RPM advertising auctions. Advertisers include:
- Fintech platforms & brokerages (Robinhood, Interactive Brokers, M1 Finance)
- Graduate programs & business schools (MBA, Master of Finance)
- Professional exam prep (CFA, CPA, FRM, Wall Street Prep)
- Academic toolkits (Brilliant, Wolfram, Overleaf, Notion)

**Target RPM**: $12.00 – $28.00 per 1,000 long-form views.

---

## 2. The Shorts-to-Long Flywheel

Every topic must produce **both** a Short (9:16) and a Long (16:9).

```
                      [ YouTube Short / TikTok (35-50s) ]
                                      │
                     Hook: Counterintuitive paradox / viral myth
                     Action: Rapid geometric shift + visual shock
                     Pacing: 140 words, aggressive cuts
                     CTA: "Full math and welfare proof pinned below"
                                      │
                                      ▼
                      [ Long-Form Masterclass (2-4 mins) ]
                                      │
                     Depth: Rigorous derivation, clean numbers
                     Visuals: Dynamic camera pan/zoom into wedges
                     Retention: High completion rate drives algorithm
                     Monetization: Mid-rolls + Exam Prep Link
                                      │
                                      ▼
                      [ Digital Study Toolkit / Patreon ]
                     • Printable PDF Cram Sheets ($12)
                     • Downloadable 4K Clean Clips for Lecturers ($20/mo)
```

---

## 3. High-Conversion Scriptwriting Framework

### A. YouTube Shorts Script Formula (35–45 seconds / ~120–140 words)
- **0s–3s (The Pattern Interrupt Hook)**: Challenge an intuitive belief.
  - *Bad*: "Today we will study rent control in microeconomics."
  - *Good*: "Why does capping apartment rent at \$1,000 actually make housing MORE expensive for everyone?"
- **3s–20s (The Mechanical Shift)**: Show the graph immediately.
  - "Look at the market. Demand meets supply at fifty-five dollars. But when a law caps prices at forty dollars, suppliers pull back to thirty units."
- **20s–35s (The Geometric Climax)**: Show the hidden cost / deadweight loss.
  - "Meanwhile, sixty renters line up. The result isn't cheaper housing—it's a thirty-unit shortage and a deadweight loss triangle of destroyed wealth."
- **35s–42s (The Conversion CTA)**:
  - "The full mathematical proof and welfare derivation is in our pinned video. Subscribe to master economics visually."

### B. Long-Form Explainer Formula (2–4 minutes / ~350–550 words)
1. **The Core Question (0:00–0:25)**: Frame the real-world policy debate.
2. **The Unregulated Equilibrium (0:25–1:00)**: Baseline coordinates ($Q^*=45, P^*=\$55$). Introduce Consumer & Producer Surplus.
3. **The Policy Shock (1:00–1:45)**: Smooth curve transition or price boundary. Point out who wins and who loses.
4. **The Wedge & Camera Zoom (1:45–2:30)**: Zoom camera directly into the wedge (`MovingCameraScene`). Highlight Deadweight Loss triangle with `Circumscribe` or `Indicate`.
5. **Real-World Intuition & Takeaway (2:30–3:15)**: Translate the geometry back into human behavior (black markets, quality deterioration, tax incidence).
6. **Closing & Exam Prep CTA (3:15–3:30)**: "Subscribe for more animated proofs, and grab the vector cheat sheet in the description."

---

## 4. YouTube Metadata & SEO Template

For every video created, generate:
- **Title Formula A (Curiosity/Question)**: *Who Really Pays a Tax? The Hidden Math of Deadweight Loss*
- **Title Formula B (Bold/Provocative)**: *Why Price Ceilings Always Fail (Geometric Proof)*
- **Title Formula C (Curriculum/Search)**: *Deadweight Loss Explained in 2 Minutes | AP Microeconomics*
- **Description Template**:
  ```markdown
  When the government intervenes in a competitive market, where does the lost wealth go? In this animated explainer, we derive the exact deadweight loss geometry using continuous supply and demand curves.

  📌 Download the AP/College Economics Visual Cheat Sheet: [Link]
  📌 Manim Source Code & Classroom 4K Clips on Patreon: [Link]

  ⏱️ TIMESTAMPS:
  0:00 The Policy Trap
  0:32 Competitive Equilibrium Baseline
  1:15 The Tax Shock & Supply Shift
  1:52 Zooming into Deadweight Loss
  2:35 Who Actually Pays? (Tax Incidence)
  3:10 Summary & Intuition

  #Economics #Microeconomics #APMicro #Manim #Education
  ```
