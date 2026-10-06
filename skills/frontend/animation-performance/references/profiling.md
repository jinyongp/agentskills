# Motion profiling

Read only the platform section needed. Confirm available tools and installed versions;
the user and project determine the profiler, not this reference.

## Web

Capture the affected interaction in a representative browser using supported project
tooling. A [browser performance trace](https://developer.chrome.com/docs/devtools/performance)
can connect a slow interval to scripting, layout, paint, and frame behavior. Select
the actual stall rather than attributing an entire recording's totals to motion.

For suspected render churn, correlate framework commits with the stalled interval.
For measurement costs, inspect layout reads and invalidations. For paint/composition,
inspect affected surfaces, effects, and layer changes. Transform/opacity often reduce
layout work but large surfaces, filters, and promotion can retain other costs.

Track visual values outside render-per-frame state where appropriate; semantic state
still belongs in the framework. Prefer explicit transition properties and avoid
competing transform owners. Verify any change to a library's transform representation
with installed-version behavior and traces; hardware acceleration is not guaranteed.
See [Motion values](https://motion.dev/docs/react-motion-value).

Use layer promotion only for a measured issue and consider memory/rasterization cost.
Lowering blur or adding will-change is not a universal fix. CPU throttling is a
controlled experiment, not proof of a physical mobile device's behavior. Compare
like-for-like captures and report the effect of instrumentation where relevant.

## React Native and Expo

Prefer representative release-build/device evidence for user-visible performance.
Distinguish JS-thread scheduling from UI/rendering work: the visual can remain smooth
while a JS-owned response stalls, or JS can be idle while drawing is expensive.
See [React Native performance](https://reactnative.dev/docs/performance).

Determine which driver or runtime actually owns the animated values. A supported
native driver can avoid per-frame JS updates; a worklet can run elsewhere without
eliminating UI, layout, or rendering costs. Check supported properties, event paths,
and cross-runtime scheduling for installed versions before changing execution.
See [Animated](https://reactnative.dev/docs/animations) and
[Reanimated worklets](https://docs.swmansion.com/react-native-reanimated/docs/guides/worklets/).

Capture the relevant gesture or transition under representative content and load.
Compare the same device, platform, build, refresh-rate mode, and workload. Inspect
per-frame React updates and JS/UI crossings only where their timing supports the
suspected cause. Simulator or debug evidence can guide diagnosis; label its limits.
Keep navigation, gesture arbitration, accessibility, and preference behavior intact.
