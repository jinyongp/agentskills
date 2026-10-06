# Native motion runtime decisions

Read only the section matching the implementation question. Consult documentation
for installed versions; APIs and architecture requirements vary.

## Driver and worklets

React Native [Animated](https://reactnative.dev/docs/animations) and existing
animation systems may already meet the task. A native driver can avoid per-frame JS
updates for supported properties; verify the actual driver and event path.

For an installed worklet engine, confirm compatible React Native/Expo versions,
architecture, native build, and setup before proposing changes.
[Reanimated worklets](https://docs.swmansion.com/react-native-reanimated/docs/guides/worklets/)
can run animation/gesture work on the UI runtime. Keep per-frame values in the
appropriate runtime and send meaningful semantic updates across boundaries rather
than using React state each frame. Use the installed version's scheduling APIs;
thread-crossing functions and setup instructions are version-specific.

UI-runtime work is not free: heavy computations, layout, and drawing can still miss
frame deadlines. Validate suspected bottlenecks with relevant build/device traces.

## Gestures, navigation, and keyboard

Reuse project gesture, sheet, and navigation primitives. Identify which gesture
owns the interaction and how it yields to nested scroll or system navigation.
Carry current position and appropriate velocity into release/settling; handle
cancellation and restoration without stale callbacks. Respect platform back actions
and interactive navigation. Keep explicit alternate controls and accessible focus.

Keyboard-following UI must coordinate with existing avoidance, insets, and navigation.
Check focused fields and actions on relevant iOS/Android devices. If a helper library
is necessary, match the project's SDK/build requirements; avoid layering a second
compensation over a working platform handler.

## Reduced motion and haptics

Read the system preference through the existing library or React Native
[AccessibilityInfo](https://reactnative.dev/docs/accessibilityinfo) and handle changes
where supported. Preserve the outcome with less movement or instant feedback.

When haptics are requested, choose meaningful events such as a completed selection
rather than continuous drag frames. The installed native API or
[Expo Haptics](https://docs.expo.dev/versions/latest/sdk/haptics/) may provide feedback.
Hardware, settings, and platform conditions can suppress it; a successful call is
not proof that the user felt a vibration. Check relevant physical-device behavior,
keep visual/semantic feedback, and report unsupported or untested conditions.
