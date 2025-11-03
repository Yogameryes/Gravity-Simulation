# About this project
This is a 2D N-body gravity simulation using Newton's laws of Gravitation

# Screenshots
<img width="1080" height="720" alt="2025-11-02-223234_hyprshot" src="https://github.com/user-attachments/assets/230e358e-f308-4629-b2fa-758025b6b89d" />
<img width="1080" height="720" alt="2025-11-02-223218_hyprshot" src="https://github.com/user-attachments/assets/7fe4bece-89e7-4c66-9a99-924db22578d3" />



# Features
- Real Time **Gravitional Interaction** Between Objects
>Well, it's called a Gravity Simulation for a reason.
- **Collision** between the Objects.
>Collision between them adds up their masses and the radius
- **Roche Limit** 
>Objects when too close to each other can rip apart each other because of the tidal forces

# How to get started?

### Installing and setting up Python
First, Download **Python 3.13.7** or newer, then create a virtual envirment using 
`python3 -m .venv venv`. Then activate the `.venv` using `source .venv/bin/activate`. 
To deactivate the virtual environment, simply do `deactivate`.

### Installing Dependencies
To Install `pygame`, open your terminal and do `pip install pygame`.
This will install pygame inside the `.venv` file.


### Starting the simulation
To start the simulation, first you need to add an **object** and define its **properties**
currently, this is done by editing the code itself (ingame method will be added later).

```ruby
Balls = [

    Ball(width / 2 , height / 2, 10, (255, 0, 0), 10 * 1e13, 0, 0, 10, False),
    Ball(width / 2 - 248, height / 2, 5, (0, 255, 0), 2 * 1e10, 0, -2.1, 1.3, False),
    Ball(width / 2 + 260, height / 2, 5, (0, 255, 0), 2 * 1e10, 0, 3, 1.4, False),

]

```

The List called `Balls` holds all the objects currently present in the simulation. The Class `Ball` is used to define any object's properties.

The Following Properties are listed below:

```ruby
Balls = [

    Ball(pos_x , pos_y, radius, color, mass, speed_x, speed_y, density, isFragment),

]

```

`pos_x`:
Used to define the starting `x` position of the object.
>Tip: To center a object in the `x` axis, use `width/2`.

`pos_y`:
 Used to define the starting `y` position of the object.
> Tip: To center a object in the `y` axis, use `height/2`.

`radius`:
Defines the radius of the object.
>Example: `4`, `12`

`color `:
This Defines the **color** of your Object in the form of rgb values.
>Example: `(0, 255, 255)`

`mass`:
This Defines the **mass** of your Object, Greater the mass, Greater will be its **Gravitaional Pull**.
>Example: `5.34 * 1e14`

`speed_x`:
Used to define the initial **velocity** of the object in the `x` axis.
>Example: `2.23`, `-4`

`speed_y`:
Used to define the initial **velocity** of the object in the `y` axis.
>Example: `1.56`, `-3`

`density`:
This is used to define the **density** of your Object.
>Example: `1.34`, `10`

`isFragment`:
This is used to know if the Object is a **Fragment** or not preventing the fragments from dividing furthur and **slowing down** the simulation.
>Example: `False` (Default), `True` (This Makes your Object indentify as a Fragment)


### Controls

- **Right Click** + Drag: Panning the Camera
- **N**: Toggles Trails
- **Plus Key**: Increases the Trail by 0.1 Seconds
- **Minus Key**: Decreases the Trail by 0.1 Seconds
