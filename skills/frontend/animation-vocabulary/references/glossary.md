# Motion glossary

Read only the section relevant to the described effect. Terms name observable
behavior unless explicitly marked as a technique; implementations vary by tool.

## Appearance

| Term | Distinguishing behavior |
| --- | --- |
| Fade | Visibility changes through opacity |
| Slide | An element moves into or out of a position |
| Scale in/out | An element changes apparent size during appearance/disappearance |
| Pop in | An entrance with a brief scale overshoot and settling |
| Reveal | Previously hidden content becomes visible, often through a moving boundary |
| Mask/clip reveal | Visibility changes within a boundary; the object itself need not move |
| Line drawing | A stroke appears to be traced over time |

## Continuity between states

| Term | Distinguishing behavior |
| --- | --- |
| Crossfade | One visual fades out while another fades in |
| Morph | The apparent shape changes continuously into another |
| Shared element transition | A perceived common object moves/resizes between views or locations |
| Layout animation | Existing elements animate from old to new layout positions |
| Origin-aware entrance | An element appears to emerge from its trigger or spatial anchor |

A shape morph is different from two images crossfading. Shared-element continuity
and layout motion may look similar; identity across views distinguishes the former.

## Scroll and gesture

| Term | Distinguishing behavior |
| --- | --- |
| Scroll reveal | Scrolling triggers an entrance that then plays |
| Scroll-linked animation | Progress continuously follows scroll position |
| Parallax | Layers move at different apparent rates |
| Rubber-banding | Movement resists displacement beyond a boundary and returns on release |
| Inertial/momentum scrolling | Movement continues after release, decaying with velocity |
| Snap points | Movement settles at defined positions |
| Drag-to-dismiss | Dragging and release determine whether an element closes |
| Magnetic effect | An object shifts toward a nearby pointer |
| Interactive transition | Progress tracks a user's gesture and can complete or cancel |

A touch gesture is not exclusive to native apps. Haptics are tactile feedback,
not a visible animation, and depend on platform capability.

## Timing and coordination

| Term | Distinguishing behavior |
| --- | --- |
| Easing | Progress changes speed over a fixed-duration transition |
| Spring | Motion follows a physical or spring-like settling model |
| Overshoot | Movement briefly passes its final target |
| Stagger | Related elements start at offset times |
| Anticipation | A preparatory movement precedes the main action |
| Velocity handoff | Subsequent motion preserves relevant velocity from a gesture or interrupted motion |

## Implementation technique

FLIP (First, Last, Invert, Play) uses measured layout states and an inverse transform
to animate a layout change. It is a technique, not a unique visible effect.
A framework's layout or shared-transition feature may use different machinery.
Describe what the user sees before prescribing an implementation.
