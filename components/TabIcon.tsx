import React from 'react';
import { View } from 'react-native';
import Svg, { Path, Circle, Rect, G } from 'react-native-svg';

interface TabIconProps {
  type: 'home' | 'calculator' | 'favorite' | 'profile';
  active: boolean;
  size?: number;
}

export function TabIcon({ type, active, size = 24 }: TabIconProps) {
  const color = active ? 'hsl(210, 75%, 45%)' : 'hsl(210, 15%, 65%)';
  const strokeWidth = active ? 2.5 : 2;

  switch (type) {
    case 'home':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Path
            d={
              "M3 12L5 10M5 10L12 3L19 10M5 10V20C5 20.5523 5.44772 21 6 21H9" +
              "M19 10L21 12M19 10V20C19 20.5523 18.5523 21 18 21H15M9 21C9.55228 21 10 20.5523 10 20" +
              "V16C10 15.4477 10.4477 15 11 15H13C13.5523 15 14 15.4477 14 16V20C14 20.5523 14.4477 21 15 21M9 21H15"
            }
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </Svg>
      );

    case 'calculator':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Rect
            x="4"
            y="2"
            width="16"
            height="20"
            rx="2"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <Rect
            x="7"
            y="5"
            width="10"
            height="3"
            rx="1"
            fill={active ? color : 'none'}
            stroke={color}
            strokeWidth={active ? 0 : strokeWidth}
          />
          <Circle cx="8" cy="13" r="1" fill={color} />
          <Circle cx="12" cy="13" r="1" fill={color} />
          <Circle cx="16" cy="13" r="1" fill={color} />
          <Circle cx="8" cy="17" r="1" fill={color} />
          <Circle cx="12" cy="17" r="1" fill={color} />
          <Circle cx="16" cy="17" r="1" fill={color} />
        </Svg>
      );

    case 'favorite':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Path
            d={
              "M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345" +
              "l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557" +
              "l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0" +
              "L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557" +
              "l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
            }
            fill={active ? color : 'none'}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </Svg>
      );

    case 'profile':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Circle
            cx="12"
            cy="8"
            r="4"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill={active ? color : 'none'}
          />
          <Path
            d="M5 20C5 17.2386 7.23858 15 10 15H14C16.7614 15 19 17.2386 19 20"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </Svg>
      );

    default:
      return null;
  }
}
