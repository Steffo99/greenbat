import pathlib
import royalnet.scrolls
import royalnet.lazy


lazy_config = royalnet.lazy.Lazy(
    lambda: royalnet.scrolls.Scroll.from_file("GREENBAT", pathlib.Path("greenbat.cfg.toml"))
)
