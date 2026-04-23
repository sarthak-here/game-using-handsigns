# Game Using Hand Signs - System Design

## What It Does
A gesture-controlled Flappy Bird game where you control the bird with your hand instead
of the keyboard. A live webcam feed is processed by MediaPipe to detect 21 hand
landmarks; raising your hand flaps the bird upward.

---

## Architecture

```
Webcam (live video)
        |
        v
+--------------------------------------------------+
|        hands.py (MediaPipe Hands wrapper)        |
|  MediaPipe Hands model                           |
|  Detects 21 hand landmarks per hand             |
|  Returns: wrist, fingertips, joints (x, y, z)  |
+--------------------------------------------------+
        |
   hand_raised? (Y-coordinate comparison)
        |
        v
+--------------------------------------------------+
|        frontend.py (game loop)                   |
|  - Renders game state with OpenCV                |
|  - Bird physics: gravity + flap impulse          |
|  - Pipe generation and scroll                    |
|  - Collision detection                           |
|  - Score tracking                                |
+--------------------------------------------------+
        |
        v
  flappyBird.py (entry point)
  Initialises webcam, runs game loop:
  capture -> detect -> update physics -> render
```

---

## Data Flow

```
Frame from webcam (cv2.VideoCapture.read())
        |
  Convert BGR -> RGB (MediaPipe requires RGB)
        |
  MediaPipe Hands.process(frame)
  Returns: multi_hand_landmarks
    Landmark 0  = wrist
    Landmark 8  = index fingertip
    Landmark 12 = middle fingertip
        |
  Gesture logic:
    If fingertip_y < wrist_y by threshold -> FLAP
    (Y axis inverted: smaller Y = higher on screen)
        |
  Physics update:
    FLAP:  bird.velocity = -FLAP_STRENGTH
    Else:  bird.velocity += GRAVITY
    bird.y += bird.velocity
        |
  Pipe logic:
    Pipes scroll left at constant speed
    New pipe spawned every N frames (random gap height)
        |
  Collision: bird rect intersects pipe rect -> game over
             bird.y < 0 or > screen_height  -> game over
        |
  OpenCV render: background, pipes, bird, score
  cv2.imshow() -> loop back
```

---

## Key Design Decisions

| Decision                        | Reason                                            |
|---------------------------------|---------------------------------------------------|
| MediaPipe Hands                 | Pre-trained, runs real-time on CPU, no GPU needed |
| Y-coordinate threshold          | Simple and robust; no custom gesture classifier   |
| OpenCV for rendering            | Same library for webcam capture and game display  |
| Single-hand detection           | Game needs one binary input; detecting more wastes|

---

## Interview Conclusion

This project demonstrates real-time computer vision integration with a game loop. The
two main challenges are latency and gesture reliability. MediaPipe Hands runs at 30+ FPS
on CPU, fast enough for the game to feel responsive. The gesture detection is
intentionally kept simple: compare wrist Y to fingertip Y. A custom gesture classifier
would add latency and training complexity for no gameplay benefit, since Flappy Bird
needs only one binary input (flap or not). The main engineering challenge is the
capture-detect-render loop: if any step is slow, the game lags. OpenCV handles all
three in a single thread, keeping the loop predictable. Extension ideas: fist = pause,
left/right hand position = horizontal dodge mechanics.
