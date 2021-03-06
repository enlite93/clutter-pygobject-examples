#!/usr/bin/env python3

from gi.repository import Clutter

STAGE_WIDTH  = 1024
STAGE_HEIGHT = 768
ACTOR_WIDTH  = 128
ACTOR_HEIGHT = 128
COLS         = int(STAGE_WIDTH / ACTOR_WIDTH)
ROWS         = int(STAGE_HEIGHT / ACTOR_HEIGHT)
TOTAL        = ROWS * COLS

def press_event(actor, event, state):
    state.set_state("right")

    return True
    
def release_event(actor, event, state):
    state.set_state("active")

    return True

def enter_event(actor, event, state):
    state.set_state("hover")

    return True

def leave_event(actor, event, state):
    state.set_state("normal")

    return True

def completed(state):
    s = state.get_state()

    print("Completed transitioning to state: %s" % s);
    
    # Skip straight to left state when reaching right...
    if s == "right":
        state.warp_to_state("left")

class Group(Clutter.Group):
    def __init__(self, r, g, b, a):
        Clutter.Group.__init__(self)

        self.rectangle = Clutter.Rectangle(color=Clutter.Color(r, g, b, a))
        self.hand      = Clutter.Texture(filename="../data/redhand.png")

        for actor in self.rectangle, self.hand:
            actor.set_size(ACTOR_WIDTH, ACTOR_HEIGHT)

        self.add(self.rectangle, self.hand)

if __name__ == "__main__":
    stage        = Clutter.Stage()
    layout_state = Clutter.State()

    stage.set_color(Clutter.Color.from_string("#000000"))
    stage.set_title("State Machine")
    stage.set_size(STAGE_WIDTH, STAGE_HEIGHT)
    stage.connect("destroy", Clutter.main_quit)
    stage.connect("button-press-event", press_event, layout_state)
    stage.connect("button-release-event", release_event, layout_state)

    for i in range(TOTAL):
        row = i / COLS
        col = i % COLS

        actor = Group(
            255 * (1.0 * col / COLS),
            50,
            255 * (1.0 * row / ROWS),
            255
        )

        actor.set_position(320, 240)
        actor.set_reactive(True)

        effect = Clutter.DesaturateEffect()

        effect.set_factor(0.0)

        actor.add_effect_with_name("fade", effect)

        # "ACTIVE" state.
        layout_state.set_key(None, "active", actor, "x", Clutter.AnimationMode.LINEAR,
            ACTOR_WIDTH * int((TOTAL - 1 - i) % COLS),
            ((row * 1.0 / ROWS)) / 2,
            (1.0 - (row * 1.0 / ROWS)) / 2
        )
        
        layout_state.set_key(None, "active", actor, "y", Clutter.AnimationMode.LINEAR,
            ACTOR_HEIGHT * int((TOTAL - 1 - i) / COLS),
            ((row * 1.0 / ROWS)) / 2,
            0.0
        )
        
        layout_state.set_key(None, "active", actor, "rotation-angle-x", Clutter.AnimationMode.LINEAR, 0.0)
        layout_state.set_key(None, "active", actor, "rotation-angle-y", Clutter.AnimationMode.LINEAR, 0.0)
        
        # "RIGHT" state.
        layout_state.set_key(None, "right", actor, "x", Clutter.AnimationMode.LINEAR,
            STAGE_WIDTH,
            ((row * 1.0 / ROWS)) / 2,
            (1.0 - ( row * 1.0 / ROWS)) / 2
        )

        layout_state.set_key(None, "right", actor, "y", Clutter.AnimationMode.LINEAR,
            STAGE_HEIGHT,
            ((row * 1.0 / ROWS)) / 2,
            0.0
        )

        # "LEFT" state.
        layout_state.set_key(None, "left", actor, "rotation-angle-x", Clutter.AnimationMode.LINEAR, 45.0)
        layout_state.set_key(None, "left", actor, "rotation-angle-y", Clutter.AnimationMode.LINEAR, 5.0)
        layout_state.set_key(None, "left", actor, "x", Clutter.AnimationMode.LINEAR, -64.0)
        layout_state.set_key(None, "left", actor, "y", Clutter.AnimationMode.LINEAR, -64.0)

        # This is a state bound to only each actor; it affects the desaturate effect
        # above, the opacity, and a slight z-rotate.
        state = Clutter.State()
        
        state.set_key(None, "normal", actor, "opacity", Clutter.AnimationMode.LINEAR, 0x77)
        state.set_key(None, "normal", actor, "rotation-angle-z", Clutter.AnimationMode.LINEAR, 0.0)
        # state.set_key(None, "normal", actor, "@effects.fade.factor", Clutter.AnimationMode.LINEAR, 0.0)
        state.set_key(None, "hover", actor, "opacity", Clutter.AnimationMode.LINEAR, 0xFF)
        state.set_key(None, "hover", actor, "rotation-angle-z", Clutter.AnimationMode.LINEAR, 10.0)
        # state.set_key(None, "hover", actor, "@effects.fade.factor", Clutter.AnimationMode.LINEAR, 1.0)
        state.set_duration(None, None, 500)
        state.set_state("normal")

        actor.set_opacity(0x77)
        actor.set_data("hover-state-machine", state)
        actor.connect("enter-event", enter_event, state)
        actor.connect("leave-event", leave_event, state)

        stage.add_actor(actor)

    layout_state.set_duration(None, None, 1000)
    layout_state.set_duration("active", "left", 1400)
    layout_state.warp_to_state("left")
    layout_state.set_state("active")
    layout_state.connect("completed", completed)

    stage.show_all()

    Clutter.main()

