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
- Knaves Hounds Hares: "The Game of the Modern Knaves" and sequel "Hounds or Hares" (names by sighsv) based on the board games as patented by Elizabeth Magie. Currently only has the 1904 patent board. The later 1924 patent board will be added. The retail board for the original version and the British version will be as well. No cards have been located for the original version, but cards have been located for the British versions. Approximations for the original's cards will be made.
- Kriegsspiel: components for playing the 1824 and 1828 Reisswitz rulesets of Kriegsspiel at 1:7500 (1 cm = 100 paces) scale. Currently includes dice and rulers. Will include troop pieces and maps in the future.

## Building

Requirements:

- This repository
- `inkscape` on PATH <https://inkscape.org/>
- `python3` on PATH <https://www.python.org/downloads/>
- `blender` on PATH <https://www.blender.org/>
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

Several images in Myriad Boards are under non-public-domain Creative Commons licenses.

## Contributing

If you wish to contribute you must abide by the ethos.

### Ethos

- The purpose of this project is to provide as many high quality assets for Tabletop Club as possible.
- These assets SHALL be free art, including no trademarks, no non-free copyrighted works, and no patent laden mechanics.
    - For instance, the Game of the Modern Knaves is a trademark substitution of a public domain, patent-free game. The current trademark holder would perhaps even permit usage of the trademark in this instance, but this repository is not the place for that sort of licensing.
- The generation scripts, configuration files, and other metadata SHALL be public domain under the CC0.
- The repository is divided into src and asset directories, with src being the source files which SHALL generate the final assets.
- The assets directory SHALL ONLY contain the final files ABSOLUTELY NECESSARY for the game, board, mechanic, or similar which is to be provided in the game.
- The assets directory SHALL be empty by default (other than the .gitkeep).
- Assets SHALL NOT produce errors in the current version of Tabletop Club.
- Card packs SHOULD include both the full deck (sans jokers/wildcards) and common stripped decks of the same suiting in their stacks file.
- The use of "Artificial Intelligence" tools is forbidden.
- Raster image formats SHOULD ONLY be for non-versioned files like scans of playing cards.
- Large raster images (> 500 kB or part of a set in total > 500 kB) SHOULD NOT be updated in the repository, instead scripts are to be used to automatically adjust them during the generation process. The cover image is excluded from this rule, but should still be edited only sparingly. This is to avoid using Git LFS, which greatly complicates the user experience for no benefit for this repository.
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

## Sidenotes

The cowrie die in the Bits and Pieces pack should ideally have companions which more accurately reflect the odds of cowrie throws, and other nonuniform randomization pieces. There is a dataset on Kaggle of various cowries and other shells laid out against various backgrounds (Oswald et al., 2024). It states that they depict *throws*, however, they are at least partially manually laid out. For instance, there are several cowries (but not all) in identical positions in `Brown_20.jpg`, `Brown_21.jpg`, and `Brown_22.jpg`. There are other instances of this in the dataset. It is astronomically unlikely for this to have occurred from random chance for a single shell across two images, let alone for multiple shells across multiple images. The dataset is only viable for classification, not for evaluating the probability weighting of cowrie shells.

Davoudian and Ranjitha (2013) have reportedly performed 5000 cowrie throws to result in the empirical distribution for four shells being (mouths up, probability): 0, 6.6%; 1, 24.3%; 2, 38.1%; 3: 23.6%, 4: 7.4%. This is reconstructed from Davoudian and Nagabhushan's (2020) paper on implementing a bot for Chowka Bhara, as the 2013 thesis is not published. From my own testing with roughly 200 throws of two cowrie shells (100 with 1 shell, 100 with 2, with 300 counts total) it seems the probability of mouth up is 33% to 35%. A StackExchange post states that cowrie shells have a roughly 30% chance of rolling a "0" (Malcolmson, 2016). It is unclear whether the shell up or mouth up corresponds to zero.

 We can calculate the distribution of n shells with probability m for mouth up ("inverted"), s for shell (back) up ("as is"), as such:

```
P(M=0) = (m^0 * s^n * nC0) / 2^n
P(M=1) = (m^1 * s^(n-1) * nC1) / 2^n
...
P(M=n) = (m^n * s^0 * nCn) / 2^n
```

The distribution for 50% mouth, 50% shell is 6.25%, 25%, 37.5%, 25%, 6.25%, which matches quite closely with Davoudian and Ranjitha's findings. The probabilities for 33% mouth up are 19.75%, 39.5%, 29.63%, 9.88%, 1.23%.

Black beans which have been marked on one random side by sanding against a flat rock until a roughly 2-3 mm white spot is visible have an empirical probability of landing spot up of roughly 40% to 50% (from 700 individual bean throws: 100 with a single bean, 100 with 6).

## References

- Davoudian, P., & Nagabhushan, P. (2019). Machine as One Player in Indian Cowry Board Game: Advanced Playing Strategies. International Journal of Computer Engineering and Technology, 10(2), 2019, pp. 1-13. https://doi.org/10.34218/IJCET.10.1.2019.019
- Malcolmson, J. A. (2016). *Answer to question*. Board & Card Games. StackExchange. https://boardgames.stackexchange.com/a/33500
- Oswald, C., Balaji, S., Naghul Pranav, K. S., Sridevi, M. (2024). Cowrie Shells Toss Dataset - Image Classification. Kaggle. https://www.kaggle.com/datasets/oswaldc/cowrie-shells-toss-dataset-image-classification
