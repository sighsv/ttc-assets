# Align to Reveal

To the best of my ability I have found no implementations or descriptions of this idea (visual encryption to hide answers or options), as it pertains to games. There are no patents, no concepts, nothing that would limit the use of this idea. Furthermore, to my knowledge, neither "Align to Reveal" nor "Transparently Trivia" are trademarked in the US (according to the USPTO Trademark Search). This document intends to serve as an "antipatent," a work of prior art which has been verifiably dated by several sources. Currently this document has been timestamped by several RFC 3161 authorities. The timestamps can be found in the companion directory `aligntoreveal.timestamp`.

This document was first drafted 8th September, 2025, which is when I first detailed the concept of using visual cryptography for games.

## Tags

Visual cryptography, visual encryption, visual decryption, trivia games, trivia card games, align to reveal, transparently trivia, transparent cipher, transparent game cipher, transparent card game key, transparent key for card games, games utilizing cryptography, cryptographic card game, cryptographic board game.

## Background

Visual encryption is a method of encrypting data where the ciphertext (cipher image) and key are both images (or may be many images), and align to reveal a secret, the plaintext (plain image, source). The concept dates to the 1960s, likely older, but provably secure methods did not arise until the 1990s. Naor and Shamir developed a method in 1994, which is a popular algorithm for this task, a simplification of their technique is used here.

The concept can be applied to real world objects, like transparencies with dot or pixel patterns, which overlay to form images. Humans are quite adept at aligning things, which makes this task quite trivial. Once aligned, if the proper key and ciphertext are paired, the source image is revealed (albeit with some minor distortion).

A general procedure for visual encryption (a la Naor, Shamir) can be given by this Python script:

```py
# load source image
plain = np.asarray(Image.open('plain.png').convert(mode='1'))
# create a random bit key
rng = np.random.default_rng(seed=1)
key = rng.integers(2, size=plain.shape)
# XOR-encrypt the plaintext with random key
encrypted = plain ^ key
# map bits to special patterns (basis matrices)
pattern = np.array([
    [ 1, -1],
    [-1,  1],
])
# encode the key and encrypted images in the patterns, and save to files
# this simply chooses the correct basis matrix for each pixel
# then constructs the image
encode = lambda a: ((np.kron(a * 2 - 1, pattern) + 1) // 2).astype(dtype=np.bool)
# the key may be inverted if a noisy background and clean image is desired
# over a noisy image with clean background
# key = key ^ 1
Image.fromarray(encode(key)).save('key.png')
Image.fromarray(encode(encrypted)).save('encrypted.png')
```

The white or black from either image can be removed, then both aligned, to achieve the visual decryption effect.

This method can be further generalized into n-party secret sharing schemes. Two-party schemes (with a ciphertext and key) are the primary focus of this document. The above algorithm can be altered to use other patterns. The only important property of the patterns is that their inclusive or (or NAND, depending on whether 1 or 0 is made transparent) produces a visually distinct (local) image from the components. The pattern listed above will produce the visually distinct combination of a fully shaded local image.

Multi party schemes have been published by various authors, but Guo et al.'s method which allows for a secret image to be split into *n* shares requiring *k* combinations by *t* essential parties, referred to as (k, n, t)-VCS is particularly notable for its practicality. Their method may be utilized instead of the Naor and Shamir method above, but particularly for the multi-party techniques touched on below.

Various other encryption algorithms may be used, including methods which optimize number of transparencies (Droste, 2001), or contrast (Blundo & Santis, 1999), steganographic methods over regular images (Attar, Taheri, Sadri, & Fattahi, 2006), methods which allow multiple secrets encoded in a single image, viewable by certain subsets (Klein, Wessler, 2007), nested progressive (region incrementing) decoding where areas of the image encode different secrets (Yang, Wu, Lin, 2019), color images (Shyu, 2006; Yang & Chen, 2008; Shyu, 2007), misalignment tolerant schemes (Yang, Peng, & Chen, 2009), schemes which do not expand the image (Shyu, 2007), and more.

There are other information hiding methods which *have* been used by games, notably color filters (red being the most common), grille ciphers, UV fluorescence, mirrors, perhaps even polarization filters, and of course simple flaps/tucks. This visual encryption method allows for more physically sturdy implementation than grille ciphers, with similar cost to color filters, while also opening the opportunity for colored secret images. Above all, this method allows for the encrypted images to be exceedingly difficult to reverse engineer, unlike color filters or mirrors, can be easier to read than grilles, and requires no electricity.

The use of transparencies with opaque markings for concealing information in games has been noted before by at least one person, "The Elder" on the BoardGameGeek forums. (The Elder, 2011) This user does not discuss the use of cryptographic methods in their post.

Several games can arise from this base concept. The above encryption scheme and other information hiding schemes in the context of games are all prior art, the following (using visual cryptography for games) is, to my knowledge, inventive.

## Transparent Trivia

The first concept outlined here is *Transparent Trivia* (or Transparently Trivia), which is a general concept for trivia games using this cryptographic align to reveal mechanic. In a Transparent Trivia game there are trivia cards (or pages, some method of physically representing the question) which have the trivia question, and an answer box. Inside the answer box is a visually encrypted image which hides the answer to the question. A transparent visual key is used to reveal the answer. To simplify gameplay, the key is shared amongst all of the cards.

An immediate advantage of this format is that answers are never spoiled at any point. The reader of the card is not aware of the answer, nor is the keeper of an answer book to future questions, unintentional viewers to the back or upside-down orientation of the card, etc. Players can freely view question cards without being made aware of the answer, which can alleviate concerns over players rewording questions, or concerns that the shuffler may be peeking. This method also allows for visual trivia, where an image on a card is the question, and the players pass the card around freely to ascertain what the answer may be. Only when they agree to reveal using the key will the answer be known.

There are three possible ways of affixing the key as a physical object.

1. Simple small transparency. This is simply a transparency with the key printed onto it, with the size and shape being just larger than the answer box. The transparency is not in the same shape as the overall card. Alignment is simple, but can be prone to rotation and flipping. To alleviate this a rectangular answer box may be used, as well as a symmetrical key. A symmetrical key can be created by generating a key that is half the width and half the height of a normal key, then flipping a copy along one axis, then flipping a copy of the half key along the other axis to produce a complete key. This key can be rotated 180° or flipped in any way while still being able to reveal the secret when visually aligned.
```py
rng = np.random.default_rng(seed=1)
key = rng.integers(2, size=(plain.width // 2, plain.height // 2))
key = np.block([key, np.fliplr(key)])
key = np.block([[key], [np.flipud(key)]])
# key is now a random 180° rotational, and fully reflective symmetrical key
# note that if the initial dimensions are not divisible by 4, there will be
# color inversion when flipping or rotating, in certain transformations
```
2. Card-sized transparency. This method would manifest as the key being in the same shape and size as the trivia cards. It is quite easy and quick to align cards using the hands or a corner, which is an advantage over the previous. Another advantage is that it is more obvious when the key is rotated improperly. Flipping along an axis may be hard to detect, e.g. if the answer box is a wide rectangle on the bottom of each card, so partially symmetric keys may be necessary for certain card designs.
3. Insert. Instead of a transparency aligned over a card, this would be a device in which cards are inserted. Once inserted fully, the card will have been automatically aligned. This method may be more viable for certain disabled players (like in the case of tremor conditions), though the use of a regular corner may be more practical. The method also simplifies presentation of the revealed secret, as a player may align it, then pass the card around while in the sleeve, allowing others to read it without having to realign the card. A downside is the insert may be more fragile and prone to wear than a simple sturdy card as in method 2.

Additionally, the answer boxes on the cards may themselves be transparent and interact with an opaque or transparent key. This is more costly to produce physically, but is cryptographically equivalent.

A general tip for answer box contents is to be unpredictably formatted, much like textual CAPTCHAs. Players may attempt to memorize patterns in the answer boxes, in the same way that players of card games may use cheat decks with minor differences between card reverses. If all of the answer boxes are the same, as in all of the true are the same within their class, with all of the false being the same within their class, or similar, then it is feasible for players to find a particular point in the answer box which reliably differentiates the categories. By having each card have a unique arrangement of its secret, it becomes infeasible to memorize the answer box, with the intended goal of memorizing the facts being more tenable.

To ensure cooperation, there may be multiple key cards which must be used together to reveal the trivia secret. This would be realized by using one of the multi-party sharing schemes.

## Augmented memory

Typical memory has pairs of identical cards, or obviously thematically relevant ones. Pairs of differing cards which require thought to match requires a way to reveal their connection in much the same way that trivia cards need a way to reveal their answer. Of course a book may be used, but an align to reveal system can be adapted as well.

Somewhere on each card a transparent window with a printed encryption pattern can be inserted and affixed. Cards can be aligned over top a plain background. If the cards match, a sensible image is revealed, otherwise noise. This can be extended to n grouped cards using a generalized n-party visual sharing system.

## Random pairs

A party game can be realized from a simplification of the above memory concept. Instead of having an image be the main focus of the card, the transparency itself can be. In this iteration there is a deck of paired transparencies, which is then shuffled and dealt to a crowd. The players must all properly match their cards in order to collectively win.

Cards may have some imagery on them, clues which look similar between cards, but are subtly different. If given to a crowd, they may discuss with one another about who has what sorts of hints on their cards, which allows for group strategy and coordination, and invites friendly interaction.

The hidden images may be thematic or prophetic. Images may reveal to be indications of great future friendship, or perhaps even further clues. Simple clues like heart borders may pair up to reveal more obscure clues, like foxes and chickens, hidden by the encryption. Using the various multi-party schemes, like region-incrementing encryption, a card can be grouped with multiple others to have any combination reveal certain secrets. For instance, A and B may reveal a heart, B and C may reveal a dog, and A and C may reveal a bone, with all three revealing a dog, heart, and bone.

## Hidden conundrum

A roleplaying game may utilize the align to reveal concept to encode hidden scenarios which are only to be revealed after the player(s) make a decision. These scenarios may be affixed to cards in encrypted boxes which are revealed using one or more keys. Multiple keys can be created using the multi party systems referenced above in the Background section. The use of multiple keys enables the players to implement voting, whereby the secret is revealed (and thereby made effective) only when some threshold of players decide to cooperate to reveal it.

An example could be a dungeon crawler card game. In this game cards can represent locations or items. Certain item cards are key cards, which are transparent visual decryption keys as described above. Players venture through the location card deck, finding items and locked chests (visual encryption secrets). They must venture through the dungeon multiple times in order to collect specific keys to unlock specific chests to acquire further items. There may also be enemy cards, with certain ones only able to be defeated using special weapon keys which reveal the secret on the enemy card. Multiple keys may be required for a particular problem, which can be implemented using the multi-party sharing techniques referenced in the Background section.

Scenario cards may have multiple secrets contained within or on the card, which a key may reveal in sequence, or only partially. For instance, a card game wherein each card is a location with four possible objects which are hinted at by a riddle can have four separate reveal sections, all of which keyed to the same key, with the player(s) choosing to reveal only one to acquire the item.

## Board game adversary

A board game may serve as an adversary to the players, with its decisions being conveyed via align to reveal sections. A circuit board game may have an outer raceway which players roll to move along, with players landing on certain spaces which result in the board taking an action. Align to reveal cards can be drawn based on location, then aligned to certain sections on the board to reveal the board's action against or for the player.

The reveal section may in fact be composed of a great deal of hidden codes which may be revealed by sweeping keys over it, fishing for the secret. A single section may contain multiple secrets which each correspond to a different key. These combined sections may be created by generating hidden images for each of the key cards, then cropping and combining to create a complete fishing area. A single key sized area may be used to reveal multiple images using different keys, and such an area with keys can be produced by inverting the role of key and secret, with the area functioning as the key, and the transparent cards being the secrets. Multiple of these areas can be combined together in confusing ways, which requires the player(s) to carefully slide their key around in order to find the answer.

## Use in video games and virtual environments

Multiplayer tabletop games like Tabletop Club and Tabletop Simulator have implementations of hidden knowledge, where certain players are able to see more information about an object (for instance, the full face of a card) than other players. This is intended to allow players to keep their card hands or other hidden information secret.

This system works well for spoiler-type trivia games (like those where the answer is located on the card, or in a companion book) as the card front is hidden, which alleviates the concern that someone near the reader may peek. The issue of the reader being spoiled remains, making multi-reader games (like passing around an image card) still infeasible.

Align to reveal technology can be applied to these video game environments. The use of transparency in 2D environments is often trivial. The key card or other transparent visual encryption device can simply be represented as a partially transparent image, which may or may not have "1-bit" transparency (that is, a transparency mask or a palette value which represents transparency). In 3D environments, the capabilities of the game or graphics engine may limit what sorts of transparency can be used. Typically 1-bit transparency can be utilized, as can be seen in the GLTF standard which outlines the concept of alphaMode, which can be either OPAQUE, MASK (1-bit), or BLEND. Transparent key cards can utilize the MASK or BLEND mode to achieve the effect demonstrated in real world equivalents. Other options provided by GLTF include the transmission extension, which can be used to achieve a more physically realistic transparency. Other 3D model formats may have other systems to encode transparency information.

The advantage of align to reveal is immediately obvious, even in these game environments. The same benefit of information hiding is afforded, and allows for players to deliberate over an option without concern that certain players may be aware of hidden information. Once players agree to reveal the information, the transparent key can be aligned with the encrypted content to reveal the secret which they may then act upon. As noted above, partially trusted groups may implement a system of voting by having secrets split up multiple ways, with several keys that must be combined to reveal the gameplay secret. This split approach alleviates the concern that a rogue player may reveal the secret quickly, as other players may intervene before they instance all of the copies of the keys they require to reveal the hidden information.

Game environments may allow for the mechanic to be even more useful than in real life, as game environments can allow for automatic alignment of objects like cards, as can be seen in Tabletop Club's ability to stack cards.

## References

- Attar, A. M., Taheri O., Sadri, S., & Fattahi, R. A. (2006). Data Hiding in Halftone Images using Error Diffusion Halftoning with Adaptive Thresholding. 2006 Canadian Conference on Electrical and Computer Engineering, Ottawa, ON, Canada, 2006, pp. 2029-2032. https://doi.org/10.1109/CCECE.2006.277391.
- Blundo, C., De Santis, A., & Stinson, D. (1999). On the Contrast in Visual Cryptography Schemes. J. Cryptology 12, 261–289 (1999). https://doi.org/10.1007/s001459900057
- Droste, S. (1996). New Results on Visual Cryptography. In: Koblitz, N. (eds) Advances in Cryptology — CRYPTO ’96. CRYPTO 1996. Lecture Notes in Computer Science, vol 1109. Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-68697-5_30
- The Elder. (2011). *Reply to forum question*. https://boardgamegeek.com/thread/694977/need-a-method-to-conceal-and-reveal-information-on
- Guo, T., Liu, F., Wu, C., Ren, Y., & Wang, W. (2014). On (k, n) Visual Cryptography Scheme with Essential Parties. In: Padró, C. (eds) Information Theoretic Security. ICITS 2013. Lecture Notes in Computer Science(), vol 8317. Springer, Cham. https://doi.org/10.1007/978-3-319-04268-8_4
- Klein, A., & Wessler, M. (2007). Extended visual cryptography schemes. Inf. Comput. 205, 5 (May, 2007), 716–732. https://doi.org/10.1016/j.ic.2006.12.005
- Shyu, S. J. (2006). Efficient visual secret sharing scheme for color images. Pattern Recognition. Volume 39, Issue 5, May 2006, Pages 866-880. https://doi.org/10.1016/j.patcog.2005.06.010
- Shyu, S. J. (2007). Image encryption by random grids. Pattern Recogn. 40, 3 (March, 2007), 1014–1031. https://doi.org/10.1016/j.patcog.2006.02.025
- Yang, C. -N., Wu, C. -C., & Lin, Y. -C. (2019). k Out of n Region-Based Progressive Visual Cryptography. In IEEE Transactions on Circuits and Systems for Video Technology, vol. 29, no. 1, pp. 252-262, Jan. 2019, https://doi.org/10.1109/TCSVT.2017.2771255.
- Yang, C. -N., & Chen, T. -S. (2008). Colored visual cryptography scheme based on additive color mixing. Pattern Recognition. Volume 41, Issue 10, October 2008, Pages 3114-3129. https://doi.org/10.1016/j.patcog.2008.03.031
- Yang, C. -N., Peng, A. -G., & Chen, T. -S. (2009). MTVSS: (M)isalignment (T)olerant (V)isual (S)ecret (S)haring on resolving alignment difficulty. Signal Processing. Volume 89, Issue 8, August 2009, Pages 1602-1624. https://doi.org/10.1016/j.sigpro.2009.02.014
