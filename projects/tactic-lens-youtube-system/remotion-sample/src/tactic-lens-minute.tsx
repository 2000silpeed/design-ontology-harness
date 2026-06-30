import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const phases = [
  {label: 'Hook', start: 0, end: 240},
  {label: 'Principle', start: 240, end: 540},
  {label: 'Evidence', start: 540, end: 1050},
  {label: 'Pitch map', start: 1050, end: 1440},
  {label: 'Summary', start: 1440, end: 1800},
];

const clamp = (value: number, min: number, max: number) => Math.min(Math.max(value, min), max);

const fade = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, start + 18, end - 18, end], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

const useSceneProgress = (start: number, end: number) => {
  const frame = useCurrentFrame();
  return clamp((frame - start) / (end - start), 0, 1);
};

const TopMeta: React.FC = () => {
  const frame = useCurrentFrame();
  const active = phases.find((phase) => frame >= phase.start && frame < phase.end) ?? phases[0];

  return (
    <div className="top-meta">
      <div>
        <span className="eyebrow">TACTICLENS BREAKDOWN</span>
        <strong>FC Seoul U18 vs Suwon U18</strong>
      </div>
      <div className="phase-pill">{active.label}</div>
    </div>
  );
};

const PitchMap: React.FC<{mode?: 'normal' | 'danger'}> = ({mode = 'normal'}) => {
  const frame = useCurrentFrame();
  const lineReveal = interpolate(frame % 240, [20, 130], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div className={`pitch ${mode}`}>
      <div className="pitch-line halfway" />
      <div className="pitch-circle" />
      <div className="box left" />
      <div className="box right" />
      <svg className="pitch-svg" viewBox="0 0 760 420">
        <path
          className="route cyan"
          pathLength="1"
          strokeDasharray="1"
          strokeDashoffset={1 - lineReveal}
          d="M120 130 C205 178 286 188 404 160 C510 136 586 170 642 124"
        />
        <path
          className="route green"
          pathLength="1"
          strokeDasharray="1"
          strokeDashoffset={1 - lineReveal}
          d="M92 300 C205 220 302 306 414 250 C506 206 570 256 650 304"
        />
        <path
          className="route amber"
          pathLength="1"
          strokeDasharray="0.01 0.055"
          strokeDashoffset={1 - lineReveal}
          d="M84 240 C196 110 342 156 444 228 C515 278 572 240 662 190"
        />
        {mode === 'danger' ? <path className="route danger" d="M518 132 L646 276" /> : null}
      </svg>
      <span className="player p1">6</span>
      <span className="player p2">8</span>
      <span className="player p3">11</span>
      <span className="opponent o1" />
      <span className="opponent o2" />
      <span className="label wide">wide press</span>
    </div>
  );
};

const Timeline: React.FC = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 1800], [6, 94], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div className="timeline">
      <span className="seg cyan" style={{left: '7%', width: '18%'}} />
      <span className="seg green" style={{left: '30%', width: '16%'}} />
      <span className="seg amber" style={{left: '52%', width: '12%'}} />
      <span className="seg cyan" style={{left: '69%', width: '20%'}} />
      <i style={{left: `${x}%`}} />
    </div>
  );
};

const HookScene: React.FC = () => {
  const {fps} = useVideoConfig();
  const progress = useSceneProgress(0, 240);
  const pop = spring({frame: useCurrentFrame(), fps, config: {damping: 18, stiffness: 120}});

  return (
    <AbsoluteFill className="scene hook">
      <PitchMap mode="danger" />
      <div className="hero-copy" style={{transform: `translateY(${(1 - pop) * 28}px)`}}>
        <span className="series">TACTICAL BREAKDOWN</span>
        <h1>4-4-2 압박,<br />왜 무너졌나</h1>
        <p style={{opacity: interpolate(progress, [0.25, 0.5], [0, 1], {extrapolateRight: 'clamp'})}}>
          42:18, 측면 패스 유도는 성공했지만 커버 거리가 늦었습니다.
        </p>
      </div>
      <div className="episode-badge">EP. 04</div>
    </AbsoluteFill>
  );
};

const PrincipleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame, [260, 360], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill className="scene principle">
      <div className="chapter-number">01</div>
      <div className="chapter-copy">
        <span className="eyebrow">PRINCIPLE</span>
        <h2>압박 방향은 맞고,<br />잔류 수비가 늦다</h2>
        <p>오늘 체크할 원칙은 3가지입니다.</p>
      </div>
      <div className="principle-list" style={{opacity: reveal}}>
        <div><span>1</span><strong>측면 패스 유도</strong></div>
        <div><span>2</span><strong>8번의 2차 커버</strong></div>
        <div><span>3</span><strong>반대 풀백 rest defense</strong></div>
      </div>
    </AbsoluteFill>
  );
};

const EvidenceScene: React.FC = () => {
  return (
    <AbsoluteFill className="scene evidence">
      <div className="video-pane">
        <PitchMap mode="danger" />
        <div className="timecode">42:18</div>
        <div className="lower-third">
          <span>PRESS TRIGGER</span>
          <strong>측면 패스 유도 후 8번 커버가 늦습니다.</strong>
        </div>
        <div className="caption">압박 방향은 맞았지만, 반대 풀백의 잔류 위치가 비었습니다.</div>
      </div>
    </AbsoluteFill>
  );
};

const PitchExplanationScene: React.FC = () => {
  const frame = useCurrentFrame();
  const cardOpacity = fade(frame, 1060, 1440);

  return (
    <AbsoluteFill className="scene pitch-explain">
      <div className="map-large"><PitchMap /></div>
      <div className="analysis-card" style={{opacity: cardOpacity}}>
        <span className="eyebrow">EVIDENCE CARD</span>
        <h2>부분 성공</h2>
        <dl>
          <div><dt>Principle</dt><dd>wide press trigger</dd></div>
          <div><dt>Result</dt><dd>cover delayed by 3.4m</dd></div>
          <div><dt>Confidence</dt><dd>AI 0.82 · human review</dd></div>
        </dl>
      </div>
    </AbsoluteFill>
  );
};

const SummaryScene: React.FC = () => {
  const progress = useSceneProgress(1440, 1800);

  return (
    <AbsoluteFill className="scene summary">
      <span className="eyebrow">SUMMARY CARD</span>
      <h2>오늘의 결론</h2>
      <div className="summary-grid">
        <div style={{opacity: interpolate(progress, [0.05, 0.25], [0, 1], {extrapolateRight: 'clamp'})}}>
          <strong>압박 방향</strong><span className="green">성공</span>
        </div>
        <div style={{opacity: interpolate(progress, [0.2, 0.42], [0, 1], {extrapolateRight: 'clamp'})}}>
          <strong>8번 커버 거리</strong><span className="amber">부분 성공</span>
        </div>
        <div style={{opacity: interpolate(progress, [0.35, 0.58], [0, 1], {extrapolateRight: 'clamp'})}}>
          <strong>잔류 수비</strong><span className="danger">수정 필요</span>
        </div>
      </div>
      <p className="endline">다음 영상에서는 후방 3-2 빌드업의 첫 패스 방향을 보겠습니다.</p>
    </AbsoluteFill>
  );
};

export const TacticLensMinute: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill className="composition">
      <TopMeta />
      <Sequence from={0} durationInFrames={240}>
        <div style={{opacity: fade(frame, 0, 240)}}><HookScene /></div>
      </Sequence>
      <Sequence from={240} durationInFrames={300}>
        <div style={{opacity: fade(frame, 240, 540)}}><PrincipleScene /></div>
      </Sequence>
      <Sequence from={540} durationInFrames={510}>
        <div style={{opacity: fade(frame, 540, 1050)}}><EvidenceScene /></div>
      </Sequence>
      <Sequence from={1050} durationInFrames={390}>
        <div style={{opacity: fade(frame, 1050, 1440)}}><PitchExplanationScene /></div>
      </Sequence>
      <Sequence from={1440} durationInFrames={360}>
        <div style={{opacity: fade(frame, 1440, 1800)}}><SummaryScene /></div>
      </Sequence>
      <Timeline />
    </AbsoluteFill>
  );
};

