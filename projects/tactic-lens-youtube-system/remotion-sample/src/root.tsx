import React from 'react';
import {Composition} from 'remotion';
import {TacticLensMinute} from './tactic-lens-minute';
import './style.css';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="TacticLensMinute"
      component={TacticLensMinute}
      durationInFrames={1800}
      fps={30}
      width={1280}
      height={720}
      defaultProps={{}}
    />
  );
};

