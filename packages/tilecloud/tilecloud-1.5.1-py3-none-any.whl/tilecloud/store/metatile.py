from io import BytesIO

from PIL import Image

from tilecloud import Tile, TileStore
from tilecloud.lib.PIL_ import FORMAT_BY_CONTENT_TYPE


class MetaTileSplitterTileStore(TileStore):
    def __init__(self, format, tile_size=256, border=0, **kwargs):
        self.format = format
        self.tile_size = tile_size
        self.border = border
        TileStore.__init__(self, **kwargs)

    def get(self, tiles):
        for metatile in tiles:
            metaimage = None if metatile.data is None else Image.open(BytesIO(metatile.data))
            for tilecoord in metatile.tilecoord:
                if metatile.error:
                    yield Tile(tilecoord, metadata=metatile.metadata, error=metatile.error, metatile=metatile)
                    continue
                if metatile.data is None:
                    yield Tile(
                        tilecoord,
                        metadata=metatile.metadata,
                        error="Metatile data is None",
                        metatile=metatile,
                    )
                    continue

                x = self.border + (tilecoord.x - metatile.tilecoord.x) * self.tile_size
                y = self.border + (tilecoord.y - metatile.tilecoord.y) * self.tile_size
                image = metaimage.crop((x, y, x + self.tile_size, y + self.tile_size))
                string_io = BytesIO()
                image.save(string_io, FORMAT_BY_CONTENT_TYPE[self.format])
                yield Tile(
                    tilecoord,
                    data=string_io.getvalue(),
                    content_type=self.format,
                    metadata=metatile.metadata,
                    metatile=metatile,
                )
