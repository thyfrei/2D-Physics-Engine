# 2D Physics Engine

A small physics engine built from scratch using **Python and Pygame** to simulate and visualize the physics behind moving objects and collisions.

I started this project to understand how physics works behind the scenes in games and simulations, rather than relying on an existing physics engine. It brings together programming, classical mechanics, and a little bit of mathematics to make simple physical interactions visible on screen.

The project is still evolving as I learn more about physics and game development.

## ✨ Features

- **Gravity and motion** — Simulates the motion of balls under gravity.
- **Wall collisions** — Objects bounce off the boundaries of the screen.
- **Circle collision detection** — Detects when two circular objects come into contact or overlap.
- **Collision response** — Calculates how velocities change when two balls collide using impulse-based mechanics.
- **Coefficient of restitution** — Controls how elastic or inelastic a collision is.
- **Positional correction** — Separates overlapping balls to prevent them from remaining embedded in each other.
- **Frame-rate-aware simulation** — Uses the time elapsed between frames to update position and velocity.

## 🛠️ Built With

- **Python** — Core programming language.
- **Pygame** — Rendering, drawing, and event handling.
- **Math** — Vector operations, collision geometry, and classical mechanics.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/thyfrei/2D-Physics-Engine.git
cd 2D-Physics-Engine
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install pygame
```

### 4. Run the simulation

```bash
python main.py
```

A Pygame window will open, showing the balls moving under gravity and interacting with the screen boundaries and each other.

## 🧠 The Physics Behind the Engine

This project is not just about drawing circles on a screen. The interesting part is calculating how those circles should move and interact according to physical principles.

### 1. Motion Under Gravity

The simulation updates each ball's velocity and position over small time intervals.

For an object moving under constant gravitational acceleration:

\[
v_y^{\,new}=v_y^{\,old}+g\Delta t
\]

\[
y^{new}=y^{old}+v_y^{\,new}\Delta t
\]

Here:

- \(v_y\) is the vertical velocity.
- \(g\) is gravitational acceleration.
- \(\Delta t\) is the elapsed time between updates.
- \(y\) is the vertical position.

The engine uses \(g=981\) pixels/s² as its approximate screen-space gravitational acceleration.

This is a numerical integration method called **semi-implicit Euler integration**. It updates velocity first and then uses the new velocity to update position. This method is often useful in real-time simulations because it is simple and generally behaves better than explicit Euler integration for many mechanical systems.

### 2. Collision Detection

Before calculating a collision, the engine must determine whether two balls overlap.

Let the centers of two balls be:

\[
P_1=(x_1,y_1),\qquad P_2=(x_2,y_2)
\]

The distance between their centers is:

\[
d=\sqrt{(x_1-x_2)^2+(y_1-y_2)^2}
\]

If their radii are \(r_1\) and \(r_2\), the collision condition is:

\[
d\leq r_1+r_2
\]

If this condition is true, the circles are touching or overlapping.

The implementation uses the Pythagorean theorem to calculate the center-to-center distance. This approach is simple and efficient for circular objects.

### 3. The Collision Normal

A particularly important concept is the **collision normal**.

The normal is a unit vector pointing along the line connecting the centers of the two balls. In this implementation, it points from the second ball toward the first ball.

First, calculate the displacement:

\[
\Delta x=x_1-x_2,\qquad
\Delta y=y_1-y_2
\]

Then calculate the unit normal:

\[
\mathbf n=
\left(\frac{\Delta x}{d},
\frac{\Delta y}{d}\right)
\]

The normal tells the engine the direction in which the collision impulse should act.

Why does this matter?

During a collision, the velocity component along the normal determines whether the balls are moving toward each other or away from each other. The tangential component is not directly changed by the frictionless, normal-only collision response used here.

### 4. Relative Velocity

Two balls can have different velocities, so the engine calculates their velocity relative to one another:

\[
\mathbf v_{rel}=\mathbf v_1-\mathbf v_2
\]

The relative velocity along the collision normal is:

\[
v_{rel,n}=\mathbf v_{rel}\cdot\mathbf n
\]

Expanding the dot product:

\[
v_{rel,n}=
(v_{1x}-v_{2x})n_x+
(v_{1y}-v_{2y})n_y
\]

This scalar tells us how quickly the distance between the centers is changing along the normal direction.

- If \(v_{rel,n}<0\), the balls are approaching each other.
- If \(v_{rel,n}>0\), the balls are separating.
- If \(v_{rel,n}=0\), there is no relative velocity along the normal.

The code skips the impulse calculation when the balls are already separating. This prevents the engine from applying another collision impulse that would push them apart unnecessarily.

### 5. Impulse-Based Collision Response

Detecting a collision is only half the problem. The engine must also calculate how the balls' velocities change.

An **impulse** is a short-duration interaction that produces a change in momentum:

\[
\mathbf J=\Delta\mathbf p
\]

For a collision between two balls, the impulse magnitude is calculated using:

\[
j=
-\frac{(1+e)v_{rel,n}}
{\frac{1}{m_1}+\frac{1}{m_2}}
\]

where:

- \(j\) is the impulse magnitude.
- \(e\) is the coefficient of restitution.
- \(m_1,m_2\) are the masses of the balls.
- \(v_{rel,n}\) is their relative velocity along the collision normal.

The impulse changes the velocities along the normal direction:

\[
\mathbf v_1'=\mathbf v_1+\frac{j}{m_1}\mathbf n
\]

\[
\mathbf v_2'=\mathbf v_2-\frac{j}{m_2}\mathbf n
\]

Notice that the two balls receive impulses in opposite directions. This follows Newton's third law: the forces during the interaction are equal and opposite.

The inverse masses determine how the velocity changes are distributed. A lighter ball generally experiences a larger velocity change than a heavier ball for the same impulse.

This is the foundation of the collision response implemented in `afterCollision()`.

### 6. Coefficient of Restitution

The coefficient of restitution, represented by \(e\), describes how elastic a collision is along the collision normal.

| Value | Interpretation |
|---|---|
| \(e=1\) | Perfectly elastic collision |
| \(0<e<1\) | Partially elastic collision |
| \(e=0\) | Perfectly inelastic normal response |

The engine currently uses \(e=0.8\) for ball-to-ball and wall collisions.

This means the normal component of the relative velocity after an isolated collision is 80% of its magnitude before the collision, with the direction reversed. This interpretation assumes the collision response is applied correctly and the objects are approaching before impact.

A value below 1 represents energy loss in the normal direction. It does not necessarily mean that all kinetic energy is lost: tangential motion can remain unchanged in this frictionless collision model.

### 7. Positional Correction

Sometimes two balls overlap by the time the engine detects their collision. Changing their velocities alone does not remove this overlap.

The penetration depth is:

\[
p=r_1+r_2-d
\]

If \(p>0\), the balls overlap.

The engine distributes the correction according to their inverse masses:

\[
\Delta x_1=
\frac{p}{\frac{1}{m_1}+\frac{1}{m_2}}
\frac{1}{m_1}n_x
\]

\[
\Delta x_2=
-\frac{p}{\frac{1}{m_1}+\frac{1}{m_2}}
\frac{1}{m_2}n_x
\]

The same calculation is performed for the vertical coordinate using \(n_y\).

This moves the balls apart along the collision normal. A lighter ball receives a larger share of the positional correction, while a heavier ball receives a smaller share.

Without positional correction, small overlaps can persist and cause objects to appear stuck together or generate repeated collision responses.

### 8. Wall Collisions and Bouncing

The screen boundaries act as simple, immovable walls.

For example, when a ball reaches the bottom boundary, its position is corrected so that it remains inside the screen:

\[
y=H-r
\]

where \(H\) is the screen height and \(r\) is the ball's radius.

Its vertical velocity is then reversed and scaled by the restitution coefficient:

\[
v_y'=-e|v_y|
\]

Similar checks handle the top, left, and right boundaries.

The implementation also applies a small horizontal velocity reduction when a ball touches the floor. This is a simple damping approximation rather than a complete friction model.

## 📂 Code Structure

The main implementation is organized around a few functions and a `Ball` class.

| Component | Responsibility |
|---|---|
| `Ball` | Stores position, velocity, radius, and mass. |
| `Ball.update()` | Updates motion under gravity and handles wall collisions. |
| `checkCollision()` | Checks whether two circles touch or overlap. |
| `afterCollision()` | Calculates positional correction and impulse-based velocity changes. |
| Main game loop | Handles events, updates the simulation, draws the balls, and refreshes the display. |

This separation makes the code easier to understand and provides a foundation for adding more features later.

## ⚠️ Current Limitations

This is a learning project, so there are still areas to improve:

- **Discrete collision detection:** Very fast objects may pass through one another between frames. This is known as tunnelling.
- **Two-ball collision handling:** The current demonstration focuses on a pair of balls rather than a general multi-object collision system.
- **Simplified friction:** The floor damping is an approximation, not a physically complete friction model.
- **Numerical stability:** Large time steps can reduce accuracy and make collisions less reliable.
- **Collision edge cases:** Balls with coincident centers need special handling because the collision normal cannot be calculated from a zero distance.

These limitations are useful opportunities to explore more advanced simulation techniques.

## 🔭 Future Improvements

Some features I would like to explore as the project develops:

- Support for many balls with different masses and radii.
- Continuous collision detection to reduce tunnelling.
- More realistic friction and angular motion.
- A configurable gravity and restitution setting.
- User interaction to create, drag, and launch balls.
- Energy and momentum visualizations.
- A more robust collision solver for multiple simultaneous contacts.

## 🎯 What I'm Learning

Through this project, I'm exploring how mathematical equations become visible, interactive behaviour. It gives me a practical way to study vectors, numerical integration, momentum, impulse, restitution, and collision geometry while improving my Python programming skills.

The goal is not just to make balls bounce, but to understand the calculations that make the simulation work.

## 📄 License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.

---

*Built with Python, Pygame, curiosity, and a desire to understand physics by implementing it.*
