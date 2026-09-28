import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

/**
 * Canonical Remotion Composition:
 * Topic: Prisoner's Dilemma 2x2 Payoff Matrix & Nash Equilibrium.
 * Aspect Ratio: 1920x1080 @ 30fps.
 */
export const PayoffMatrix: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animations
  const titleOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  const tableScale = spring({ frame: frame - 15, fps, config: { damping: 12 } });
  
  // Highlight Nash Equilibrium box (Defect, Defect) around frame 70
  const nashHighlight = interpolate(frame, [70, 85], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0f172a',
        fontFamily: 'Inter, system-ui, sans-serif',
        color: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {/* Title Header */}
      <div style={{ opacity: titleOpacity, textAlign: 'center', marginBottom: 40 }}>
        <h1 style={{ fontSize: 52, margin: 0, color: '#f8fafc', fontWeight: 800 }}>
          THE PRISONER'S DILEMMA
        </h1>
        <p style={{ fontSize: 24, color: '#94a3b8', margin: '8px 0 0 0' }}>
          Dominant Strategies & The Nash Equilibrium Trap
        </p>
      </div>

      {/* Payoff Matrix Table */}
      <div
        style={{
          transform: `scale(${tableScale})`,
          display: 'grid',
          gridTemplateColumns: '160px 220px 220px',
          gridTemplateRows: '70px 140px 140px',
          gap: '12px',
          alignItems: 'center',
          textAlign: 'center',
        }}
      >
        {/* Top Header Row */}
        <div />
        <div style={{ fontWeight: 700, fontSize: 26, color: '#38bdf8' }}>Silent (Cooperate)</div>
        <div style={{ fontWeight: 700, fontSize: 26, color: '#ef4444' }}>Confess (Defect)</div>

        {/* Player 1 Row 1: Silent */}
        <div style={{ fontWeight: 700, fontSize: 26, color: '#38bdf8' }}>Silent</div>
        <div style={cellStyle('#1e293b', false)}>
          <span style={{ color: '#38bdf8' }}>-1</span>, <span style={{ color: '#f43f5e' }}>-1</span>
          <div style={subLabel}>Reward (-1 yr)</div>
        </div>
        <div style={cellStyle('#1e293b', false)}>
          <span style={{ color: '#38bdf8' }}>-10</span>, <span style={{ color: '#f43f5e' }}>0</span>
          <div style={subLabel}>Sucker's Payoff</div>
        </div>

        {/* Player 1 Row 2: Confess */}
        <div style={{ fontWeight: 700, fontSize: 26, color: '#ef4444' }}>Confess</div>
        <div style={cellStyle('#1e293b', false)}>
          <span style={{ color: '#38bdf8' }}>0</span>, <span style={{ color: '#f43f5e' }}>-10</span>
          <div style={subLabel}>Temptation</div>
        </div>
        {/* Nash Equilibrium Cell */}
        <div
          style={{
            ...cellStyle(
              `rgba(239, 68, 68, ${0.15 + nashHighlight * 0.25})`,
              nashHighlight > 0.5
            ),
            border: `3px solid rgba(239, 68, 68, ${nashHighlight})`,
          }}
        >
          <span style={{ color: '#38bdf8' }}>-5</span>, <span style={{ color: '#f43f5e' }}>-5</span>
          <div style={{ ...subLabel, color: nashHighlight > 0.5 ? '#fca5a5' : '#64748b' }}>
            NASH EQUILIBRIUM
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const cellStyle = (bgColor: string, active: boolean): React.CSSProperties => ({
  backgroundColor: bgColor,
  borderRadius: 16,
  padding: '24px 16px',
  fontSize: 36,
  fontWeight: 800,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  boxShadow: active ? '0 0 30px rgba(239, 68, 68, 0.4)' : '0 4px 6px -1px rgba(0, 0, 0, 0.2)',
  transition: 'all 0.3s ease',
});

const subLabel: React.CSSProperties = {
  fontSize: 14,
  fontWeight: 600,
  color: '#64748b',
  marginTop: 6,
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
};
