# Tabletop Club assets

This is a monorepo for various asset packs I have created for [Tabletop Club](https://github.com/drwhut/tabletop-club). Some of these are derived from existing free art, others are created whole cloth by me.

![Several screenshots of the assets laid out in game arrangements.](cover.png?raw=true)

## Overview

Game boards:
- Myriad Boards: a large collection of flat game boards generated from SVGs by a Python script that creates simple cuboid GLTF files
- Wacky Boards: non-cuboid game boards

Cards (scans rectified using a custom edge-detection based script):
- Aluette: an Aluette deck by B. P. Grimaud
- Carte Bresciane: a Bresciane-style Italian playing card deck created by ZZandro
- Smith-Waite-Rider Tarot: the legendary Rider-Waite tarot deck, illustrated by Smith

Game pieces:
- Bits and Pieces: some game pieces like pawns and checkers

Whole games:
- Knaves Hounds Hares: "The Game of the Modern Knaves" and sequel "Hounds or Hares" (names by sighsv) based on the board games as patented by Elizabeth Magie

## Building

Requirements:

- This repository
- `inkscape` on PATH <https://inkscape.org/>
- `python3` on PATH <https://www.python.org/downloads/>
- Python packages `numpy` `opencv-python` `pillow` (for card edge detection and alignment)
- ImageMagick, with `convert`, `mogrify`, `composite` on PATH
- Bash shell (for arrays)

Move into the src directory and run the generate script:

```
$ cd src
$ ./generate.sh
```

The asset packs are available in the assets directory.

## License

All works in this repository created by me (sighsv) are in the public domain, available under the CC0 license. This includes all textual files like scripts (Python and shell), configuration files (cfg), and markdown. Refer to the configuration files in the subdirectories for complete copyright information.

## Contributing

If you wish to contribute you must abide by the ethos.

### Ethos

- The purpose of this project is to provide as many high quality assets for Tabletop Club as possible.
- These assets SHALL be free art, including no trademarks, no non-free copyrighted works, and no patent laden mechanics.
- The generation scripts, configuration files, and other metadata SHALL be public domain under the CC0.
- The repository is divided into src and asset directories, with src being the source files which SHALL generate the final assets.
- The assets directory SHALL ONLY contain the final files ABSOLUTELY NECESSARY for the game, board, mechanic, or similar which is to be provided in the game.
- The assets directory SHALL be empty by default (other than the .gitkeep).
- Assets SHALL NOT produce errors in the current version of Tabletop Club.
- Card packs SHOULD include both the full deck (sans jokers/wildcards) and common stripped decks of the same suiting in their stacks file.
- The use of "Artificial Intelligence" tools is forbidden.
- Raster image formats SHOULD ONLY be for non-versioned files like scans of playing cards.
- Large raster images (> 500 kB or part of a set in total > 500 kB) SHALL NOT be updated in the repository, instead scripts are to be used to automatically adjust them during the generation process. The cover image is excluded from this rule, but should still be edited only sparingly. This is to avoid using Git LFS, which greatly complicates the user experience for no benefit for this repository.
- Vector image formats SHOULD be used in favor of raster formats.

### Tools and techniques

There are currently two tools.

- `boardgen.py` given an (ideally square, power of 2) PNG image, create a cuboid with the image on the top face
- `rectify.py` given an image with a border of some kind, find the border, crop, and rectify the subimage

Rectify is essential for converting scanned images of playing cards.

When dealing with cards they might be laid out in some kind of grid, if so, you can use `convert -crop XCOUNTxYCOUNT@ out-%04d.ext`

### Common stripped decks

French
- Black suits (26 cards)
- Red suits (26 cards)
- Face cards (12 cards)
- Pip cards (40 cards)
- Piquet (32 cards: 7 - King + Ace)
- Euchre (24 cards: 9 - King + Ace)

German
- Schnapsen
- Skat
- Doppelkopf

Latin (swords, coins, cups, clubs/batons)
- Ombre, Scopa, etc. (40 cards: Ace - 7, face cards)
