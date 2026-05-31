from engine.base import Base
from animations.wave.animation import Wave
from animations.sine.animation import Sine
from animations.campfire.fire import Fire
from animations.firewall.firewall import Firewall

ANIMATIONS: dict[str, type[Base]] = {
    "wave": Wave,
    "sine": Sine,
    "campfire": Fire,
    "firewall": Firewall,
}
