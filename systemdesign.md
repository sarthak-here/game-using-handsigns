# Game Using Hand Signs — System Design

## What It Does
A gesture-controlled Flappy Bird game where you control the bird with your hand instead of the keyboard. A live webcam feed is processed by MediaPipe to detect hand landmarks; a raised hand flaps the bird upward. Built in Python with OpenCV for display.

---

## Architecture

```
Webcam (live video)
        |
        v
+--------------------------------------------------+
|            hands.py  (MediaPipe wrapper)         |
|  MediaPipe Hands model                           |
|  - Detects 21 hand landmarks per hand            |
|  - Returns: wrist, finger tips, joints (x,y,z)  |
+--------------------------------------------------+
        |
   hand_raised? (landmark logic)
        |
        v
+--------------------------------------------------+
|           frontend.py  (game loop)               |
|  - Renders game state with OpenCV                |
|  - Bird physics: gravity + flap impulse          |
|  - Pipe generation and scroll                    |
|  - Collision detection                           |
|  - Score tracking                                |
+--------------------------------------------------+
        |
        v
  flappyBird.py  (entry point / orchestrator)
  - Initialises webcam (cv2.VideoCapture)
  - Runs game loop: capture -> detect -> update -> render
```

---

## Input

| Input | Detail |
|---|---|
| Webcam frames | 30fps, RGB, any resolution |
| Hand gesture | Raised / lowered hand (Y-coordinate of wrist vs fingertips) |

---

## Data Flow

```
Frame from webcam (cv2.VideoCapture.read())
        |
  Convert BGR -> RGB
        |
  MediaPipe Hands.process(frame)
        |
  Returns: multi_hand_landmarks
    Landmark 0  = wrist
    Landmark 8  = index finger tip
    Landmark 12 = middle finger tip
        |
  Gesture logic:
    If fingertip_y < wrist_y by threshold -> hand raised -> FLAP
    (Y axis is inverted: smaller Y = higher on screen)
        |
  Game physics update:
    If FLAP: bird.velocity = -FLAP_STRENGTH
    Else:    bird.velocity += GRAVITY
    bird.y  += bird.velocity
        |
  Pipe logic:
    Pipes scroll left at constant speed
    New pipe spawned every N frames at random gap height
        |
  Collision check:
    bird.rect intersects pipe.rect -> game over
    bird.y < 0 or > screen_height   -> game over
        |
  OpenCV render:
    Draw background, pipes, bird, score
    Overlay webcam feed (small corner thumbnail)
        |
  cv2.imshow() -> display frame
  Loop back to capture
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| MediaPipe Hands | Pre-trained, runs real-time on CPU without GPU |
| Y-coordinate threshold for gesture | Simple and robust; no complex gesture classifier needed |
| OpenCV for rendering | Unified library for both webcam capture and game display |
| Single-hand detection | Reduces latency; game only needs one binary input (flap/no-flap) |

---

## Interview Conclusion

This project demonstrates real-time computer vision integration with a game loop — the two main challenges being latency and gesture reliability. MediaPipe Hands runs at 30+ FPS on CPU, which is fast enough for the game to feel responsive. The gesture detection is intentionally kept simple: compare wrist Y-coordinate to fingertip Y-coordinate. A more complex approach (training a custom gesture classifier) would add latency and training complexity for no gameplay benefit, since Flappy Bird only needs one binary input. The main engineering challenge is synchronizing the capture-detect-render loop: if any step is slow, the game feels laggy. OpenCV handles all three in a single thread, which keeps the loop predictable. If I were extending this, I would add a second gesture (fist = pause) and map left/right hand movement to horizontal dodge mechanics.
