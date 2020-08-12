from src.random_animations import strobe
from src.star_light import sparkle
from src.trains import trains

animations = {
    fn.__name__: fn for fn in [strobe, trains, sparkle]
}