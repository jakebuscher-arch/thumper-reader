"""
Build complete manifest of all 74 spreads with:
- bookNumber
- spreadNumber (1 to 74)
- spreadId (B01-N01 .. B05-N13)
- chapter
- chapterTitle
- sourceStanzas (range, e.g. [1, 4])
- lineCount
- firstLine
- lastLine
- speakerDirectives (raw text from prompt)
- imageType (KEEP / REPLACE)
- imagePath (current/target path)
- legacyAssignments
- direction (scene description)
"""

import json
import re

# Read frozen source JSON
with open('/tmp/thumper_source.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

# Flatten stanzas per book
flattened_books = []
for b in books:
    flat = []
    for p in b['pages']:
        for s in p['stanzas']:
            flat.append(s['lines'])
    flattened_books.append(flat)

# Let's write out the full manifest data structure
EOF_DATA = '''
Book 1 — Finding God on a Dreary Day

B01-N01 | Chapter 1 — A Rainy Day | S001–S004 | 16 lines
Text: “Rain and damp and puddles many” → “imagine a new friend with whom to play”
Speakers: Narration only.
Image: KEEP/REASSIGN assets/images/B01-S01-rainy-games.png (use once). Legacy assignments: B01-P01 → B01-S01-rainy-games.png.
Direction: Thumper watches other rabbits splashing and playing outside his cottage window in steady rain; his solitude contrasts with their games. Retain this matching image.

B01-N02 | Chapter 1 — A Rainy Day | S005–S008 | 16 lines
Text: “Not a normal bunny will do” → “I could eat all the carrots I desire”
Speakers: S5–8 are Thumper’s imagined/self-addressed thoughts; if cued, use Thumper —, never Frumper. The tag “Thumper’s my name he opined” remains narrative attribution.
Image: KEEP/REASSIGN assets/images/B01-S02-thumper-imagines.png (use once). Legacy assignments: B01-P01 → B01-S01-rainy-games.png; B01-P02 → B01-S02-thumper-imagines.png.
Direction: Thumper at his writing desk with quill and paper imagines a winged rabbit soaring among clouds; make the imagined status clear. Retain the existing imagination image, not a literal visit from Frumper.

B01-N03 | Chapter 1 — A Rainy Day | S009–S012 | 16 lines
Text: “No fence would stop him from taking flight” → “If in only in my imagination he exists?”
Speakers: S9–11 mix imagined plans with narration; S12 is Thumper’s inward question. No Miller or Frumper speaking labels.
Image: REPLACE; create assets/images/B01-N03.png. Legacy assignments: B01-P02 → B01-S02-thumper-imagines.png; B01-P03 → B01-S06.png.
Direction: From inside Thumper’s rainy window, frame the distant fenced Miller farm, carrots and especially plump berries. Show Thumper imagining the winged friend flying over its fence at night to fetch food; an inset-like painterly reverie may distinguish this from current reality. No actual rescue or farmhouse revelation.

B01-N04 | Chapter 2 — Thinking Hard | S013–S016 | 16 lines
Text: “What is the difference between a “Frumper”” → “But never can it be square, that’s not a circle!”
Speakers: Reflective narration/Thumper’s reasoning; no spoken conversation or Frumper label.
Image: KEEP/REASSIGN assets/images/B01-S07.png (use once). Legacy assignments: B01-P03 → B01-S06.png.
Direction: Thumper studies a blue round shape and purple square on his desk while thinking about what an imagined friend could be. Reassign this existing unused illustration; keep the physical desk objects, no equations or explanatory diagram.

B01-N05 | Chapter 2 — Thinking Hard | S017–S020 | 16 lines
Text: “So to be a friend for Thumper the rabbit” → “He thinks to himself, “Well, what caused you””
Speakers: S18–19 narration. S20 has Thumper’s “There is nothing I’ve forgotten” and “Well, what caused you”; keep surrounding narration unlabeled.
Image: KEEP/REASSIGN assets/images/B01-S09.png (use once). Legacy assignments: B01-P03 → B01-S06.png; B01-P04 → B01-S10.png.
Direction: Exhausted Thumper sits over carrot stew after hours of imagining, his cheek resting on his paw. Reassign the existing stew image; Frumper must not appear physically present.

B01-N06 | Chapter 3 — Essence and existence | S021–S024 | 16 lines
Text: “Maybe Thumper has it backwards” → “Thumper has a brilliant thought”
Speakers: Narration except Thumper’s quoted request for carrots and butter in S24.
Image: REPLACE; create assets/images/B01-N06.png. Legacy assignments: B01-P04 → B01-S10.png; B01-P05 → B01-S11.png.
Direction: Thumper at the cottage table reaches for snacking carrots and butter, then begins cutting the block as an idea occurs. Include the butter block, knife and carrots; thoughtful discovery, no literal being made from butter.

B01-N07 | Chapter 3 — Essence and existence | S025–S029 | 20 lines
Text: “There is no film on the boundary” → “We must be made of existence stuff!”
Speakers: S25–27 narration/reasoning. S28’s “He is made of existance” is Thumper; S29 continues his reasoning, not Frumper speaking.
Image: KEEP/REASSIGN assets/images/B01-S11.png (use once). Legacy assignments: B01-P05 → B01-S11.png.
Direction: Close scene of Thumper contemplating precisely cut butter on a wooden board with carrots nearby. Retain the matching butter image, showing its real edges rather than a diagram of existence.

B01-N08 | Chapter 4 — Which came first | S030–S033 | 16 lines
Text: “But what is it that sticks these together” → “it seems that even thumper can’t exist, but no!”
Speakers: Thumper’s self-questioning/reasoning, with narrative tags unbadged; no second character speaking.
Image: KEEP/REASSIGN assets/images/B01-S13.png (use once). Legacy assignments: B01-P06 → B01-S14.png.
Direction: Thumper props his chin in his paws over the sliced butter, puzzled by whether he could cause himself. Reassign this quieter existing table image; do not use the picture of a jigsaw puzzle.

B01-N09 | Chapter 4 — Which came first | S034–S036 | 12 lines
Text: “Thumper now with his thoughts swirling” → “But it would have it infinity!”
Speakers: Narration; no new interlocutor.
Image: KEEP/REASSIGN assets/images/B01-S15.png (use once). Legacy assignments: B01-P06 → B01-S14.png; B01-P07 → B01-S17.png.
Direction: Thumper stands at his window as natural light breaks through clouds, his expression shifting from confusion toward understanding. Reassign the existing window-and-light image; no visible personification or diagram of God.

B01-N10 | Chapter 5 — The Search | S037–S040 | 16 lines
Text: “Wherever could a bunny find” → “no bunny would dare to enter near”
Speakers: S37–38 narration/reflection. Thumper speaks S39 and S40.1–2; Other bunnies speak S40.3–4. Delete Narrator badges.
Image: KEEP/REASSIGN assets/images/B01-S17.png (use once). Legacy assignments: B01-P07 → B01-S17.png.
Direction: Thumper addresses a group of ordinary rabbits on the rain-soaked woodland path; the others respond skeptically and point toward the farm. Retain the matching group-conversation image.

B01-N11 | Chapter 5 — The Search | S041–S044 | 16 lines
Text: “The Miller farm is close enough” → “They feared for the trouble that awaits”
Speakers: Other bunnies: S41.1–2. Narration: S41.3–4, S42 and most of S43–44. “Find him Thumper!” in S43.4 is Other bunnies.
Image: KEEP/REASSIGN assets/images/B01-S19.png (use once). Legacy assignments: B01-P07 → B01-S17.png; B01-P08 → B01-S20.png.
Direction: Thumper squeezes beneath barbed wire through the rain-washed opening; rabbits remain outside, some cheering and others worried. Reassign the existing crawling-under-the-fence picture, replacing the premature trap picture.

B01-N12 | Chapter 6 — The Farm | S045–S048 | 16 lines
Text: “Thumper hopped from place to place” → “Juicy and plump on every limb”
Speakers: Narration only.
Image: KEEP/REASSIGN assets/images/B01-S20.png (use once). Legacy assignments: B01-P08 → B01-S20.png; B01-P09 → B01-S23.png.
Direction: Thumper cautiously negotiates Miller’s farm: carrot-baited trap, exposed pit of spikes and threatening farmhand in the distance; berry bushes provide his eventual cover. Retain the trap-avoidance picture as the focal moment. Do not replace the farmhand with a weasel or remove the traps.

B01-N13 | Chapter 6 — The Farm | S049–S052 | 16 lines
Text: “Never has He ate so many” → “one that did the good by habit”
Speakers: Narration S49 and S51–52; Thumper’s prayer S50. No Narrator badge after the prayer.
Image: KEEP/REASSIGN assets/images/B01-S23.png (use once). Legacy assignments: B01-P09 → B01-S23.png.
Direction: Thumper sleeps beneath heavily laden berry branches, with a restrained dreamlike image of his selfishness/theft above him. Retain this matching dream picture; no dog attack yet.

B01-N14 | Chapter 6 — The Farm | S053–S055 | 12 lines
Text: “In every case he had something missing” → “a brand new courage he displays”
Speakers: S53–54 reflective narration, S55 action narration.
Image: KEEP/REASSIGN assets/images/B01-S24.png (use once). Legacy assignments: B01-P09 → B01-S23.png; B01-P10 → B01-S26.png.
Direction: Awake beneath the berries, Thumper looks contrite and resolved before approaching the farmhouse in new light. Reassign the existing repentance image; retain berries and the visible way toward the house.

B01-N15 | Chapter 7 — the Farmhouse | S056–S059 | 16 lines
Text: ““I stole the berries” He rehearses” → “he suddenly felt a change in his weight!”
Speakers: Only the two quoted confession lines S56.1–2 are Thumper; all chase narration remains unlabeled.
Image: KEEP/REASSIGN assets/images/B01-S26.png (use once). Legacy assignments: B01-P10 → B01-S26.png.
Direction: The large farm dog charges after frightened, tiring Thumper along the farmhouse path, berry hedges beside them. Retain the existing chase picture. No Frumper visible before the rescue reveal.

B01-N16 | Chapter 7 — the Farmhouse | S060–S062 | 12 lines
Text: “Its almost like he’s lighter now” → “Past the puddles where the bunnies friends roam”
Speakers: Narration only.
Image: KEEP/REASSIGN assets/images/B01-S28.png (use once). Legacy assignments: B01-P11 → B01-S29.png.
Direction: Frumper lifts Thumper bodily into the air just beyond the dog’s bite and carries him over the farm fence toward the puddles and home. Reassign the existing airborne rescue image; both rabbits must be visible and Frumper must be doing the lifting.

B01-N17 | Chapter 8 — Homecoming; | S063–S065 | 10 lines
Text: “Thumper and Frumper became best of friends” → “Is a God above all, a God who is listening.”
Speakers: Closing narration only, not dialogue by either rabbit.
Image: KEEP/REASSIGN assets/images/B01-S29.png (use once). Legacy assignments: B01-P11 → B01-S29.png.
Direction: Thumper and Frumper sit together peacefully near home after the rescue, wings visible, natural light and distant farm landscape. Move the existing homecoming image here, rather than using it for the airborne escape.

Book 2 — Thumper and the Clock Maker

B02-N01 | Chapter 1 — The landing | S001–S004 | 16 lines
Text: “Tick tock tick Plop!” → “How could he just “come to be” the rabbits wonder”
Speakers: Hedgehog: S1.3. Thumper: direct speech in S3. Rabbits: the question in S4.4. All narrative introductions/tags unlabeled.
Image: KEEP/REASSIGN assets/images/B02-S01-commotion-clockshop.png (use once). Legacy assignments: B02-P01 → B02-S01-commotion-clockshop.png.
Direction: Outside Hedgehog’s clock shop, townsfolk gather around Thumper and the winged Frumper after the landing; Hedgehog peers from the shop. Retain the matching crowd/clock-shop image.

B02-N02 | Chapter 1 — The landing | S005–S009 | 20 lines
Text: “The Hedgehog raps a stick against his shop” → “But that doesn’t make him a miracle that's just an illusion”
Speakers: S5.1 is narration; Hedgehog speaks S5.2 through S9. Do not assign his skeptical speech to Thumper or the crowd.
Image: REPLACE; create assets/images/B02-N02.png. Legacy assignments: B02-P01 → B02-S01-commotion-clockshop.png; B02-P02 → bunnies book 1 .png.
Direction: Hedgehog raps his wooden staff against his clock shop to quiet the celebration, addressing Thumper and the gathered rabbits with skeptical confidence. Show the staff and shop clocks; no lunch, journey or unrelated rabbits playing.

B02-N03 | Chapter 1 — The landing | S010–S013 | 16 lines
Text: “The bunnies headed back to their games” → “The clouds formed again and down the rain drops”
Speakers: S10.3 “But wait!” is Thumper; S11–12 Hedgehog, excluding attribution. S13.1 Thumper; S13.2–4 narration.
Image: REPLACE; create assets/images/B02-N03.png. Legacy assignments: B02-P02 → bunnies book 1 .png; B02-P03 → B02-S03-lunch-table.png.
Direction: The crowd disperses back to its games. Thumper remains questioning Hedgehog beside the shop doorway; Hedgehog gestures at a clock, then withdraws as rain resumes. Show these two and the clock, not Frumper at lunch.

B02-N04 | Chapter 2 — Lunch with frumper | S014–S017 | 16 lines
Text: “Back at his house he's delighted to find” → “Any reason you're asking these questions of me?”
Speakers: S14.1–2,4 narration; “Hello frumper” S14.3 Thumper. S15 Thumper. S16.1 narration; S16.2–S17 Frumper.
Image: KEEP/REASSIGN assets/images/B02-S03-lunch-table.png (use once). Legacy assignments: B02-P03 → B02-S03-lunch-table.png; B02-P04 → B02-S03-lunch-table.png.
Direction: Thumper and Frumper share carrots and butter at Thumper’s cottage table; Frumper responds with an amused, relaxed expression, wings folded beside his chair. Reassign the existing lunch image here; Hedgehog is absent.

B02-N05 | Chapter 2 — Lunch with frumper | S018–S021 | 16 lines
Text: “Hedgehog had a reason for all that transpired” → “Find out all he knows in the highest degree”
Speakers: S18 Thumper; S19–21 Frumper.
Image: REPLACE; create assets/images/B02-N05.png. Legacy assignments: B02-P04 → B02-S03-lunch-table.png.
Direction: A distinct closer view across the same lunch table: troubled Thumper explains his doubts while Frumper listens, then warmly encourages him to learn clockmaking. Preserve the same room, food and character designs; do not recycle the preceding composition or place Hedgehog at the meal.

B02-N06 | Chapter 3 | S022–S025 | 16 lines
Text: “Next morning thumper went off to the shop” → “Bouncing over to grab it with an excited hop”
Speakers: Hedgehog’s question S22.4; Thumper S23; Hedgehog S24.1,3–4 and S25.1–2. S24.2 and S25.3–4 narration.
Image: REPLACE; create assets/images/B02-N06.png. Legacy assignments: B02-P05 → B02-clockmaker-workshop.png.
Direction: Morning at the clock shop: Thumper has come to apprentice and eagerly fetches Hedgehog’s missing hammer from the far side of the workshop. Include the recognizable hammer, workbench and tool shed/storage area; establish this hammer for Book 5.

B02-N07 | Chapter 3 | S026–S029 | 16 lines
Text: “Okay what is next said thumper the rabbit” → “Then hear a sound that sounds like wings”
Speakers: Thumper S26.1; Hedgehog S26.2. S26.3 is narration. S26.4 is Thumper counting the gears he was sent to sort. S27–29 narration.
Image: KEEP/REASSIGN assets/images/B02-S06-magnifying-gears.png (use once). Legacy assignments: B02-P05 → B02-clockmaker-workshop.png; B02-P06 → B02-S06-magnifying-gears.png.
Direction: Hedgehog teaches Thumper at the cluttered bench, using a magnifying glass and forceps to assemble tiny gears, jeweled bearings and a spring before fitting the clock face. Retain the matching magnifying-glass image.

B02-N08 | Chapter 3 | S030–S033 | 16 lines
Text: “Looks like Frumper just showed up again” → “I'm quite sorry you had to hear it from me”
Speakers: Hedgehog S30.1–2; Thumper S30.3–4; Hedgehog S31; Thumper S32; Hedgehog S33.
Image: REPLACE; create assets/images/B02-N08.png. Legacy assignments: B02-P06 → B02-S06-magnifying-gears.png.
Direction: Beside the newly assembled clock, Hedgehog peers uncertainly toward the window after hearing wings while Thumper challenges the identification. Include the clock and their contrasting near/far attention. No actual Frumper outside: he is at home. If depicting the recalled shore, it must be clearly a recollection of bats at dusk, not winged rabbits.

B02-N09 | Chapter 4 | S034–S037 | 16 lines
Text: “You said that everything is like a clock” → “To make it spin and count the years”
Speakers: Thumper S34–35; Hedgehog S36; Thumper S37.
Image: KEEP/REASSIGN assets/images/B02-clockmaker-workshop.png (use once). Legacy assignments: B02-P07 → B02-clockmaker-workshop.png.
Direction: Thumper questions Hedgehog about what moves the gears while they examine the workshop clock and loose components. Reassign the existing broader workshop image here, once only; the two characters and machinery fit this conversation.

B02-N10 | Chapter 4 | S038–S041 | 16 lines
Text: “Could I build this in your shop?” → “When The other parts seem so beggarly”
Speakers: Thumper S38; Hedgehog S39; Thumper S40–41.
Image: REPLACE; create assets/images/B02-N10.png. Legacy assignments: B02-P07 → B02-clockmaker-workshop.png; B02-P08 → B02-S06-magnifying-gears.png.
Direction: Thumper lays out unpowered intermeshing gears on the workbench while Hedgehog explains that adding gears cannot supply motion. Feature loose brass gears, an unfinished mechanism and a separate spring; no magical self-moving gears, infinite-chain diagram or new speaker.

B02-N11 | Chapter 4 | S042–S045 | 16 lines
Text: “Well, in the clock It keeps everything running” → “The Cause of the motion was not the world we uncovered”
Speakers: Hedgehog S42; Thumper S43–45.
Image: REPLACE; create assets/images/B02-N11.png. Legacy assignments: B02-P08 → B02-S06-magnifying-gears.png.
Direction: Close view of Hedgehog’s paw winding a spring while Thumper watches and recognizes the need for a source of power. Show the winding key, spring and connected clock mechanism, lit warmly; keep the philosophical idea embodied in their activity.

B02-N12 | Chapter 4 | S046–S049 | 16 lines
Text: “But a gear and a spring is a thing that I see” → “Clocks to be built For everyone”
Speakers: Hedgehog S46; Thumper S47–48; Hedgehog S49.
Image: REPLACE; create assets/images/B02-N12.png. Legacy assignments: B02-P09 → Frumper .png.
Direction: Thumper points to the hands and numerals of a real clock reading quarter to nine while Hedgehog considers the question of time; unfinished customer orders surround them in the late workshop. No Frumper portrait and no floating numbers. Clock dial markings may be composited cleanly as object details rather than generated prose.

B02-N13 | Chapter 5 | S050–S053 | 16 lines
Text: “I'll get frumper he can help too” → “Said frumper as he brushed past the curtains”
Speakers: Thumper S50. S51.1–2 narration; Frumper S51.3–S52. Hedgehog S53.1–2; Frumper S53.3; S53.4 narrative attribution.
Image: REPLACE; create assets/images/B02-N13.png. Legacy assignments: B02-P09 → Frumper .png; B02-P10 → Frumper Flying Sky.png.
Direction: Frumper folds his wings and ducks through the clock-shop doorway to join Thumper and Hedgehog, then discusses the wedding order. Include pocket-watch cases and bench tools; all three are working indoors, not flying over the countryside.

B02-N14 | Chapter 5 | S054–S057 | 16 lines
Text: “As thumper worked his mind wandered” → “Then out the door Frumper leaves”
Speakers: S54 is narrated inward reflection, no speech badge. S55–56 narration. Frumper’s instruction “Go and put them where he needs” S57.3; other S57 lines narration.
Image: REPLACE; create assets/images/B02-N14.png. Legacy assignments: B02-P10 → Frumper Flying Sky.png.
Direction: At dawn, light enters the workshop as Frumper quietly adds one clock to a box and hands over an unexpectedly plentiful pile; Thumper packs the finished watches while Hedgehog hurries among outstanding orders. Show boxes, many finished watches and all three roles, without duplicated Frumpers or explanatory magic symbols.

Book 3 — Thumpers Bad Day

B03-N01 | Chapter 1 | S001–S003 | 12 lines
Text: “After a night without a wink of sleep” → “Soon thumper began to cough”
Speakers: Narration only.
Image: REPLACE; create assets/images/B03-N01.png. Legacy assignments: B03-P01 → signal-2026-08-06-12-02-24-200.png.
Direction: Sleepy Thumper in nightclothes has gone to bed after tea; downstairs the forgotten pot continues boiling over the stove. Use one coherent cottage cutaway-like viewpoint through the stair/door space or focus on the unattended pot with bedroom beyond. No Proditor or volcano; this is the accidental beginning of a domestic fire.

B03-N02 | Chapter 1 | S004–S007 | 16 lines
Text: “Smoke came up from under the door” → “His friend frumper was just hit by lightning!”
Speakers: Narration; the news of Frumper’s lightning strike is reported by a bunny, with no invented quoted speech.
Image: REPLACE; create assets/images/B03-N02.png. Legacy assignments: B03-P01 → signal-2026-08-06-12-02-24-200.png; B03-P02 → B03-cottage-ashes.png.
Direction: Thumper escapes the burning cottage through a broken upstairs window into thorn bushes; on the ground he struggles away from a wasp nest toward fallen ashes as a rabbit approaches with news. Make the broken window, burning doorway, bushes and clover/wasp area spatially consistent. Choose the ground-level aftermath with these causes visible, not a collage of repeated Thumpers.

B03-N03 | Chapter 2 — visitors | S008–S011 | 16 lines
Text: “Still in the ashes he looks at his leg” → “Maybe it's all in the perspective you've had”
Speakers: Thumper’s “How did this happen” S8.3; First bunny S9.3–4; Second bunny S10.2–4; Third bunny S11.2–4. All introductions and crying narration unlabeled.
Image: REPLACE; create assets/images/B03-N03.png. Legacy assignments: B03-P02 → B03-cottage-ashes.png; B03-P03 → Hedgehog.png.
Direction: In the cottage ashes, injured Thumper looks at his broken leg while three separate rabbits offer their unhelpful responses. Show all three visitors with differing expressions, thorns and ruin; Hedgehog has not intervened yet.

B03-N04 | Chapter 2 — visitors | S012–S016 | 20 lines
Text: “Silence! get out of here! leave him alone!” → “He says as he fixes a gash with a suture”
Speakers: Hedgehog S12.1–2 and S13.1–2; Thumper S13.3–S14; Hedgehog’s speech in S15.2–4 and S16.1,3. S12.3–4, S15.1 and S16.2,4 are narration.
Image: REPLACE; create assets/images/B03-N04.png. Legacy assignments: B03-P03 → Hedgehog.png; B03-P04 → Mole.png.
Direction: Hedgehog drives the three visitors away, breaks his wooden staff into a splint for Thumper’s leg and tends his wounds beside the ashes. Center the hands/paws securing the splint, with the broken staff and clock/watch nearby. Replace the portrait; edit the ashes image only if it can show this specific aid.

B03-N05 | Chapter 3 — action | S017–S020 | 16 lines
Text: “As thumper is laying in the ashes still” → “But not everything will roll down the landscape”
Speakers: Mole S18.1–2 excluding “he said with a smile”; Thumper S18.3; Mole S18.4 through S20. S17 narration.
Image: REPLACE; create assets/images/B03-N05.png. Legacy assignments: B03-P04 → Mole.png.
Direction: Mole tumbles out of the grassy hillside and comes to rest beside splinted Thumper and the smoldering house; he begins explaining how one responds to a fall. Show the opened burrow, sloping hill and both characters. No literal block-shaped mole or philosophical diagram.

B03-N06 | Chapter 3 — action | S021–S023 | 12 lines
Text: “You shape your thoughts through a choice of your will” → “Thumper felt proud of the progress he saw”
Speakers: Mole S21–22; S23 narration.
Image: REPLACE; create assets/images/B03-N06.png. Legacy assignments: B03-P05 → Squirel .png.
Direction: Thumper draws a house plan while Mole excavates the new foundation’s footer on the chosen hillside. Keep Thumper’s leg splinted; include the drawing, dug trench and the location that later supports the sawmill and new house. Show active rebuilding, not a Squirrel portrait.

B03-N07 | Chapter 4 — The remedies | S024–S027 | 16 lines
Text: “Hey thumper it's squirrel! how are you doing?” → “It was singing before but it's the first time he heard”
Speakers: Squirrel S24 and S25.1–2. S25.3–S27 narration.
Image: REPLACE; create assets/images/B03-N07.png. Legacy assignments: B03-P05 → Squirel .png; B03-P06 → Squirel .png.
Direction: Squirrel brings a picnic and strawberry wine and helps injured Thumper relax in the cool mountain stream; they rest by the bank and notice a songbird in the tree. Include picnic basket, bottle/cups and the bird; water continues downstream toward Miller’s farm, not away from it. Keep the leg injury visible without turning this into a medical scene.

B03-N08 | Chapter 4 — The remedies | S028–S031 | 14 lines
Text: “Squirrel tempts him nearer with a piece of a scone” → “If there's a good, all-knowing God, who also is strong”
Speakers: Songbird sings S29 only. Squirrel speaks S30.2–4. S28, S30.1 and S31 narration. Squirrel’s farewell has no invented quotation.
Image: REPLACE; create assets/images/B03-N08.png. Legacy assignments: B03-P06 → Squirel .png.
Direction: Near the picnic, Squirrel offers a piece of scone to the songbird; Thumper listens as it sings about the two narrow escapes. Emphasize bird, scone, friends and the same riverbank. No written lyrics, flashback montage or claim that the bird is Frumper.

B03-N09 | Chapter 5 — Frumper's adventure | S032–S035 | 16 lines
Text: “Back at the place where his home once stood” → “lightning burnt off most of your fur”
Speakers: Frumper S34, excluding attribution; Thumper S35. S32–33 narration.
Image: REPLACE; create assets/images/B03-N09.png. Legacy assignments: B03-P06 → Squirel .png; B03-P07 → Frumper Flying Sky.png.
Direction: Thumper returns to the building site to find his foundation, fresh-cut boards, bucket of nails and a working sawmill where Mole emerged. Frumper, visibly singed with much fur burned away, adds boards beside the plans. Include the cut-down bird tree’s stump and continuity with the earlier hill.

B03-N10 | Chapter 5 — Frumper's adventure | S036–S040 | 20 lines
Text: “You wouldn't believe the adventure I was on” → “Helped me stand up again as at last I revived”
Speakers: Frumper narrates his own rescue throughout S36–40; not Thumper or an unlabeled narrator.
Image: REPLACE; create assets/images/B03-N10.png. Legacy assignments: B03-P07 → Frumper Flying Sky.png; B03-P08 → Frumper .png.
Direction: Illustrate Frumper’s recounted adventure: the winged rabbit rises to intercept lightning above a trapped fawn under a fallen tree; the doe approaches, rain extinguishes the nearby forest fire, and the storm blows from the east. Preserve the open field with very few standing trees. A dramatic single rescue moment, not a generic flying portrait; singeing results from this strike.

B03-N11 | Chapter 6 — thumpers question | S041–S044 | 16 lines
Text: “That is an adventure that much I concede” → “That the wind that just blew it was actually me”
Speakers: Thumper S41–42. S43.1–2 narration; Frumper’s question S43.3; Thumper’s “it’s a fly that I saw” S43.4. Frumper S44. Keep “Thumper leans in” unlabeled.
Image: REPLACE; create assets/images/B03-N11.png. Legacy assignments: B03-P08 → Frumper .png.
Direction: Back at the construction site, Thumper asks his difficult question while singed Frumper opens his paw to reveal a tiny fly, then gently blows it into flight. Show the real fly, open paw and Thumper leaning close, with boards nearby. No literal visualization of God controlling insects.

B03-N12 | Chapter 6 — thumpers question | S045–S047 | 12 lines
Text: “But a fly to a bunny is just barely a hop” → “His bad day would at least reach its resolution”
Speakers: Frumper S45–46 and S47.1–2; S47.3–4 narration.
Image: REPLACE; create assets/images/B03-N12.png. Legacy assignments: B03-P09 → Frumper .png.
Direction: Frumper and Thumper continue their thoughtful conversation at the partly built house, the released fly small in the air. Use a wider, quiet view and humble attentive expressions. “Mountain of wisdom” is figurative here: do not relocate them onto a literal mountain expedition.

B03-N13 | Chapter 7 — the universe | S048–S052 | 20 lines
Text: “Everything has a nature and it imitates God” → “That’s like a baker who judges flour as if it is bread”
Speakers: Frumper speaks S48–52 continuously. The current unmarked continuation must not become narration or Thumper’s speech.
Image: REPLACE; create assets/images/B03-N13.png. Legacy assignments: B03-P09 → Frumper .png; B03-P10 → Thumper .png.
Direction: Frumper indicates the real wood and unfinished house as Thumper listens, with safe embers or the ruined stove in the background and natural sky above. Make the unfinished roof/framing visibly incomplete, as the text compares judging a house before it is built; no cosmic infographic or simultaneous giant sun and moon.

B03-N14 | Chapter 7 — the universe | S053–S057 | 20 lines
Text: “We don’t sit at the start of the world reading Gods mind” → “Your choices to love come from an actual you”
Speakers: Frumper continues S53–57. Do not relabel it as Thumper because the current image is his portrait.
Image: REPLACE; create assets/images/B03-N14.png. Legacy assignments: B03-P10 → Thumper .png; B03-P11 → Frumper .png.
Direction: Closer conversation at the unfinished house: Thumper studies Frumper’s lightning scars and singed fur as they discuss love, freedom and an unfinished story. Show stacked timber, living woodland and the two friends’ mutual attention, not a generic portrait or literal curtain hiding God.

B03-N15 | Chapter 8 | S058–S061 | 16 lines
Text: “Thumper was dazed by the flurry of replies” → “He is teaching us to live happily as our heavenly Dad”
Speakers: S58 narration. S59.1 narration; Thumper’s “Maybe 10ft” S59.2; Frumper S59.3–S61, excluding S59.4’s attribution.
Image: REPLACE; create assets/images/B03-N15.png. Legacy assignments: B03-P11 → Frumper .png.
Direction: Frumper hands Thumper a board and asks its length; Thumper guesses uncertainly while a plain measuring rod provides the concrete lesson. Include board, measuring rod, timber pile and construction work, with the splint still on Thumper’s leg.

B03-N16 | Chapter 8 | S062–S065 | 16 lines
Text: “Its better to suffer evil than ever to do it” → “But if all existed at once that would hardly be pleasant”
Speakers: Frumper S62–65.
Image: REPLACE; create assets/images/B03-N16.png. Legacy assignments: B03-P11 → Frumper .png; B03-P12 → B03-cottage-ashes.png.
Direction: While talking at the worksite, Frumper gently draws attention to Thumper’s burned paw and the remembered door-handle warning; Thumper holds a board, listening. Keep the injured paw, timber and scarred Frumper physically present. No punishment tableau, abstract souls being carved or explanatory diagrams.

B03-N17 | Chapter 8 | S066–S068 | 12 lines
Text: “But you. Thumper. Look at what has occurred.” → “Because it was hard he was proud when its done”
Speakers: Frumper S66–67; S68 narration.
Image: REPLACE; create assets/images/B03-N17.png. Legacy assignments: B03-P12 → B03-cottage-ashes.png.
Direction: Thumper and Frumper carry boards uphill and work together on the new house; Thumper discovers his leg is healed as he bears weight comfortably. Show warm, strenuous shared work and a recognizably advancing house in the field. Do not reuse the burnt-cottage picture or leave Thumper immobilized after the healing.

Book 4 — Thumpers Inferno

B04-N01 | Chapter 1 — The Rumbling | S001–S003 | 12 lines
Text: “Mole and hedgehog starred intently” → “Mole headed outside to do his part”
Speakers: Mole’s quoted warning in S1.3; Hedgehog S2; Mole S3.1–2; remainder narration.
Image: REPLACE; create assets/images/B04-N01.png. Legacy assignments: B04-P01 → Mole.png.
Direction: Hedgehog and Mole examine the seismometer’s agitated pendulum and drawn trace in the clock shop; Hedgehog consults a dusty record book while Mole prepares to inspect the buried probes. Include the actual pendulum, trace, book and probe equipment, not a standalone Mole portrait.

B04-N02 | Chapter 1 — The Rumbling | S004–S007 | 16 lines
Text: “He took a path he dug before” → “A tunnel to safety, an old lava spout”
Speakers: Narration and Mole’s inward assessment; do not invent a speech partner.
Image: REPLACE; create assets/images/B04-N02.png. Legacy assignments: B04-P01 → Mole.png; B04-P02 → Squirel .png.
Direction: Mole falls from his familiar underground passage into a much deeper volcanic cavern, then limps along the hard rock floor seeking an exit. Show the high broken tunnel opening, sulfur vents, bats, rats and lava passages; he cannot dig through these walls. No Squirrel in this scene.

B04-N03 | Chapter 2 | S008–S011 | 16 lines
Text: “Staring at the clock Hedgehog fidgeted” → “They stared down the hole and their faced grew grim”
Speakers: Raven’s quoted report S8.4; Hedgehog’s question S9.1; Squirrel S10.1–2; Hedgehog S10.3–4. Rest narration.
Image: REPLACE; create assets/images/B04-N03.png. Legacy assignments: B04-P02 → Squirel .png; B04-P03 → B04-torch-cavern.png.
Direction: At the volcano rim Hedgehog has brought rope and rescue supplies; Squirrel arrives with Thumper and Frumper, and the four look down grimly. The Raven may depart above, having delivered the warning. Mole is below, not standing with the rescue party.

B04-N04 | Chapter 2 | S012–S016 | 20 lines
Text: “I’ll fly you each to the bottom but listen to me” → “As the bats disappeared and they came to a room”
Speakers: Frumper S12; Squirrel S13.1; Frumper S13.2; Hedgehog S13.3–4; Thumper’s “Blood” S14.1. The quoted “A creature of day…” in S16 is a bat; surrounding lines narration.
Image: REPLACE; create assets/images/B04-N04.png. Legacy assignments: B04-P03 → B04-torch-cavern.png; B04-P04 → bunnies book 1 .png.
Direction: Inside the volcano, Frumper leads Thumper, Hedgehog and Squirrel along Mole’s sparse blood trail beneath wall torches; rats’ eyes glint in cracks and hanging bats flip upright and scatter before Frumper. Show all four rescuers distinctly, no recovered Mole yet; restrained blood drops, not gore.

B04-N05 | Chapter 3 | S017–S020 | 16 lines
Text: “Thumper could hardly believe what he saw” → “But the bunnies looked gentle”
Speakers: Cave bunnies’ invitation S18.3; Thumper’s question S18.4. Squirrel S19.1–2; Frumper’s warning S20.1. The rest narration.
Image: REPLACE; create assets/images/B04-N05.png. Legacy assignments: B04-P04 → bunnies book 1 .png.
Direction: Thumper reaches toward what appears to him to be honey-buttered bread among feasting cave rabbits. In the same coherent scene, Frumper’s torch begins exposing bare rock and rabbits chewing stones, while Squirrel and Hedgehog see the darkness. Clearly separate deceptive warm appearance from torchlit reality through light, not labels or explanatory panels; retain Thumper’s distorted impression of gaunt Frumper only within the illusion.

B04-N06 | Chapter 3 | S021–S023 | 12 lines
Text: “He couldn’t see it, but in the light to the flame” → “Thumper still could here the chorus just like an echo”
Speakers: Frumper’s whispered words S22 are not supplied: do not invent them. Frumper speaks S23.1–2. Everything else narration.
Image: REPLACE; create assets/images/B04-N06.png. Legacy assignments: B04-P05 → Thumper .png.
Direction: Frumper hands Thumper actual berries; a rock falls from Thumper’s paw as he recognizes suffering rabbits chewing stones on the barren cavern floor. Torchlight reveals painful faces and distended bellies. Required objects: berries, dropped rock and torch; no real bread or happy outdoor bunny picnic.

B04-N07 | Chapter 4 | S024–S027 | 16 lines
Text: “The decent was steep and they clung to the walls” → ““I thought that squirrels where the nimblest creatures around””
Speakers: Bat S26.3–4 and S27.1,4; the other lines narration.
Image: REPLACE; create assets/images/B04-N07.png. Legacy assignments: B04-P05 → Thumper .png; B04-P06 → Squirel .png.
Direction: As the group descends among stalagmites, tired Squirrel lags behind. A bat leans against the wall, coaxing her toward what looks like an easy slide. Include her companions farther along the safe path and the misleading slope at the edge; the rescue has not happened yet.

B04-N08 | Chapter 4 | S028–S031 | 16 lines
Text: “The Bat smiled, “you where lagging behind”” → “Frumper handed her her own torch he had found”
Speakers: Bat S28.1–3 and S29.1–2; Squirrel S28.4 and S29.3–4, excluding “she started to run!” narration. S30–31 narration.
Image: REPLACE; create assets/images/B04-N08.png. Legacy assignments: B04-P06 → Squirel .png.
Direction: Frumper flies high with his torch just as Squirrel stops at the cliff’s brink; its light strips away the false slide to expose a lethal drop and freshly dug grave below. Thumper and Hedgehog help her down; give her the separate torch she receives at this scene’s end. No actual slide surviving outside the illusion.

B04-N09 | Chapter 5 | S032–S035 | 16 lines
Text: “A burst of fresh air at last hit their faces” → “Your volcano could blow and destroy both our lands”
Speakers: Hedgehog S32.3–S33.2. Bat/Proditor’s “This probe…” S33.4 and questions S34.1–2; Hedgehog S34.3–4. Proditor S35.1; S35.2 attribution; Hedgehog S35.3–4. S33.3 and other action tags narration.
Image: REPLACE; create assets/images/B04-N09.png. Legacy assignments: B04-P07 → B04-proditor-giant.png.
Direction: Beside the eastern air shaft, dog-sized Proditor taunts Hedgehog with the scientific probe, tapping it against rock. Hedgehog reaches angrily for it while the others stand nearby with torches. Use Proditor’s canonical black fur, red eyes and foxlike head; he is not a giant towering across a lava chasm.

B04-N10 | Chapter 5 | S036–S040 | 16 lines
Text: “What? Said the bat with a look of surprise” → “Hedgehog was strung up like a puppet up by the rafters”
Speakers: Proditor speaks S36’s quoted/direct words, S37.2, S38–39 and S40.1–2. S36.2 and S37.1 narration. Thumper’s “What’s that sound” S40.3; action/tag and S40.4 narration.
Image: REPLACE; create assets/images/B04-N10.png. Legacy assignments: B04-P07 → B04-proditor-giant.png; B04-P08 → B04-proditor-giant.png.
Direction: Bats use a throne, hoist and cords on Hedgehog’s hands, feet and head to lift him in the shaft while pretending to make him their commander. Show the mechanism and Hedgehog becoming a puppet, with Proditor directing the deception and the three friends below. No giant monarch portrait substituting for the rope trick.

B04-N11 | Chapter 5 | S041–S045 | 20 lines
Text: “The bats were moving his limbs with strings And mocking” → “I can’t imagine, Thumper can you?”
Speakers: Narration S41–44, including the reported request to drop the cords; no invented quotation. Hedgehog S45.2; Squirrel’s whispered question S45.3–4, not Mole.
Image: REPLACE; create assets/images/B04-N11.png. Legacy assignments: B04-P08 → B04-proditor-giant.png; B04-P09 → Mole.png.
Direction: Frumper breaks a stalactite from the cave roof to pin charging Proditor to the floor; bats retreat, their puppet cords slacken and Hedgehog frees his own limbs. Show Frumper above, dog-sized black Proditor below and Hedgehog’s falling ropes. Keep the peril faithful but non-graphic; do not substitute lava, a sword or a gigantic demon.

B04-N12 | Chapter 6 | S046–S049 | 16 lines
Text: “Its then that squirrel heard it, “Why how do you do”” → ““I crawled down here to find a tunnel to the bay””
Speakers: Mole’s greeting S46.1; Squirrel S46.2. S46.3–4 are untagged rescue-party reassurance: leave the speaker name absent, or use a neutral Rescuer cue; do not invent a named or choral attribution. S47.1 is likewise an unnamed rescuer’s question; Mole S47.2–S48.2. Hedgehog and Mole jointly cry “eruption!” S49.1; Mole S49.4. Other lines narration.
Image: REPLACE; create assets/images/B04-N12.png. Legacy assignments: B04-P09 → Mole.png; B04-P10 → B04-torch-cavern.png.
Direction: The rescuers finally find limping Mole, who indicates the flaps over his eyes and how he shut out the deceivers. Thumper lifts him onto his back; Hedgehog and Mole spot the oncoming red magma that blocks their route. Show all five friends, eye coverings and the blocked exit; Mole is not the speaker asking how he survived.

B04-N13 | Chapter 6 | S050–S054 | 18 lines
Text: “Maybe we can find it and escape towards the sea” → “They talked and they laughed as they finished the dish”
Speakers: Mole continues S50.1. Thumper’s call S50.4. Other lines narration; no invented dialogue over the final meal.
Image: REPLACE; create assets/images/B04-N13.png. Legacy assignments: B04-P10 → B04-torch-cavern.png.
Direction: Frumper rams the boulder sealing the escape tunnel as magma approaches; the rock bursts into gravel and Thumper carries Mole through with Hedgehog and Squirrel. Smoke draws toward the opening and daylight/shore lies beyond. Make the headfirst impact and opening the focal action; the following fish meal can remain unpictured rather than forcing a second time into the same image.

Book 5 — Necessary Beetles

B05-N01 | Chapter 1 — The Entrance | S001–S003 | 12 lines
Text: “Its not a pleasant sound to hear a weasel sing” → “They seem like the type of thing you want as your neighbor”
Speakers: Narration only.
Image: REPLACE; create assets/images/B05-N01.png. Legacy assignments: B05-P01 → B05-weasels-cart.png.
Direction: Show several weasels actually RIDING ON a substantial wooden wagon down the forest road, not standing next to a market handcart. A harnessed RAT TEAM pulls it while a weasel cracks a whip; stolen crops fill the wagon and the riders carry beer flagons, shouting and swaggering. Include wheels, shafts/harnesses, riders, rats and raided fields. No pet-selling display yet.

B05-N02 | Chapter 1 — The Entrance | S004–S006 | 12 lines
Text: “In fact, they come with a solution for all that you need” → “Turn around now they won’t buy what you’re selling!”
Speakers: Hedgehog’s “stop right there, no!” S5.2 and warning S6.4; the rest narration.
Image: REPLACE; create assets/images/B05-N02.png. Legacy assignments: B05-P01 → B05-weasels-cart.png; B05-P02 → B05-weasels-cart.png.
Direction: At Hedgehog’s clock shop, weasels imprison him and nail boards across the door, then depart toward town with the same rat-drawn wagon. Show a weasel hammering the final board, Hedgehog visible behind the obstruction and the waiting wagon/rat team. His own recognizable hammer remains inside for his later escape.

B05-N03 | Chapter 2 — Pets | S007–S012 | 24 lines
Text: “Get your beetles! Come buy a pet!” → “He had not changed their minds no, not in the least.”
Speakers: Weasel: S7.1–2,4; S8–9 excluding “he calls”; S10.2–4 excluding narration. S7.3, S10.1 and S11–12 narration. Thumper’s objection in S12 is reported, not supplied dialogue: do not invent his words.
Image: KEEP/REASSIGN assets/images/B05-weasels-cart.png (use once). Legacy assignments: B05-P02 → B05-weasels-cart.png; B05-P03 → B05-sina-black-snake.png.
Direction: Retain and reassign the existing beetle-market image here, where it actually fits: weasels offer beetles in glass containers from a wooden sales cart to rabbits. Its displayed beetle and crowd belong to this sales pitch, not the wagon journey or elixir. Use only once. This 24-line chapter is the sole 24-line exception under my later 16–24-line allowance; do not compress its font.

B05-N04 | Chapter 3 — The light of the moon | S013–S017 | 20 lines
Text: “Thats when he heard it, a sound from a bush” → “Sina wound up so close that he slid on his shoe”
Speakers: Sina S13.3–4, S14.3–4 and S15.1–2; S16.3–4 Sina. Weasel S17.1,3. Other lines are narration.
Image: REPLACE; create assets/images/B05-N04.png. Legacy assignments: B05-P03 → B05-sina-black-snake.png; B05-P04 → B05-sina-black-snake.png.
Direction: At a riverside tree under a CRESCENT moon, black Sina addresses Thumper, summons a weasel and coils around that weasel as beetles are set at the tree’s base. One crushed beetle disproves the sales claim; the weasel offers the replacement. Show all three characters and the beetles. Replace both the full-moon black-snake portrait and the green-snake variant; no gruesome insect detail.

B05-N05 | Chapter 3 — The light of the moon | S018–S022 | 20 lines
Text: ““So slick weasels but that’s proof you aren’t truthful” → “But how can a part cause the whole that itself it is in?”
Speakers: Sina S18.1–2; Weasel’s “I need air” S18.3; Thumper S18.4. Sina S19–20; Thumper begins his answer S21.4 and continues S22, with narrative tags unbadged.
Image: REPLACE; create assets/images/B05-N05.png. Legacy assignments: B05-P04 → B05-sina-black-snake.png.
Direction: Sina’s black coils tighten around the frightened weasel beside the same tree while Thumper urgently reasons with him, one paw raised in appeal. Include the live weasel’s face and constricting coils, Thumper, crescent moon and river. A distinct closer composition; no already-released weasel, chains diagram or snake eating its tail.

B05-N06 | Chapter 3 — The light of the moon | S023–S027 | 20 lines
Text: “Maybe the causes make a circle this is how it prevails” → “So long thumper, Sina said as he uncoiled and left”
Speakers: Thumper S23.1–2; Sina S23.4; Thumper S24.1–3; Sina S24.4; Thumper S25.2–S27.2. Sina’s farewell S27.4, excluding attribution; remaining action lines narration.
Image: KEEP/REASSIGN assets/images/B05-S05-weasel-released.png (use once). Legacy assignments: B05-P05 → B05-S05-weasel-released.png.
Direction: Retain the release image: the weasel is down on his knees struggling for breath while Sina uncoils and leaves, and Thumper stands nearby after answering. Keep the black snake, crescent moon and matching riverside tree; do not reuse this image during the earlier tightening-coils scene.

B05-N07 | Chapter 4 — the elixir | S028–S031 | 16 lines
Text: “Mole met the weasels as they sold an elixir” → “He had a ring on his finger and his clothes where all new”
Speakers: Weasels S28.3–S30.2 and S31.2. All other lines narration.
Image: REPLACE; create assets/images/B05-N07.png. Legacy assignments: B05-P05 → B05-S05-weasel-released.png; B05-P06 → B05-weasels-cart.png.
Direction: The weasels stand on their recognizable wagon selling an ELIXIR to a rabbit crowd while Mole watches skeptically. Show an actual flask being offered/drunk and a newly dressed rabbit returning with a ring; remove beetle jars as the focal merchandise. No magic gold emerging from the bottle: the apparent wealth is stolen, not conjured.

B05-N08 | Chapter 4 — the elixir | S032–S035 | 16 lines
Text: “Behold! Gentile rabbits, the elixir’s effective” → “The ones that didn’t drink hid with mole in the ground”
Speakers: Weasels S32.1–2. S33–34 narrated discovery. Quarreling rabbits S35.1–2, not weasels or Mole; S35.3–4 narration.
Image: REPLACE; create assets/images/B05-N08.png. Legacy assignments: B05-P06 → B05-weasels-cart.png; B05-P07 → Squirel .png.
Direction: Mole points out that one rabbit wears another’s clothes and ring; rabbits argue and grab stolen food and possessions in the looted town. In the foreground Mole shelters the rabbits who refused the elixir in an underground refuge. Include stolen garments/ring and visible damage; no prosperous market, Squirrel portrait or generic wagon shot.

B05-N09 | Chapter 5 — Swim like a fish | S036–S041 | 22 lines
Text: “Squirrel wasn’t in town when the weasels arrived” → “He must come to save us. Or the evil will spread”
Speakers: S36.1–3 narration framing the reconstructed pitch; Weasels S36.4–S38.2. S38.3 narration; S38.4 reports the weasels’ pressure. S39–40 narration; Squirrel S41.1–2 excluding the attribution.
Image: REPLACE; create assets/images/B05-N09.png. Legacy assignments: B05-P07 → Squirel .png; B05-P08 → Hedgehog.png.
Direction: Squirrel stretches from a sturdy branch over the river and pulls drowning young rabbits with pasted-on fake fins out of the current. Show multiple endangered rabbits, visible artificial fins, her actual grip/paws and rescued rabbits crying on the bank. Water carries them downstream toward the ocean. The sales pitch is reconstructed because Squirrel missed it; depict the actual rescue, not her attending the earlier sale. Keep this complete rescue chapter at 22 lines.

B05-N10 | Chapter 6 — Hedgehog strikes back | S042–S046 | 20 lines
Text: “Hedgehog’s hammer burst through the door” → “Rivers don’t care about the things that you wish”
Speakers: Weasels’ calls S43.2; Hedgehog S43.4, S44.1–2,4 and S45–46. Rabbit’s protest S44.3. Opening/action lines narration.
Image: REPLACE; create assets/images/B05-N10.png. Legacy assignments: B05-P08 → Hedgehog.png.
Direction: Hedgehog, carrying the same hammer retrieved inside his shop, stands on the weasels’ wagon confronting them and the deceived rabbits. Include broken shop-door boards visible behind him, a rabbit clutching money and another wearing pasted fins; Hedgehog points out the fraud. No portrait or snake-only picture.

B05-N11 | Chapter 6 — Hedgehog strikes back | S047–S050 | 16 lines
Text: “With a twirl of his hammer he narrowed his gaze” → “Hedgehog scolded them all that they were ever allowed”
Speakers: Hedgehog S47.2,4 and S48.2. An unidentified buyer/townscreature S47.3: label Buyer, not a named character or confirmed weasel. Weasels S48.4; the recognizing Weasel shouts “Escape!” S50.2. Action narration elsewhere.
Image: REPLACE; create assets/images/B05-N11.png. Legacy assignments: B05-P09 → B05-sina-black-snake.png.
Direction: Hedgehog smashes the beetles’ GLASS BOX with his hammer, then curls into a spiny ball as attacking weasels fall from the wagon; black Sina emerges from the nearby river and the townsfolk rally. Choose the immediate fight as the focal instant, with smashed glass box and dropped hammer visible, not Hedgehog simultaneously upright and rolled up. No duplicate hedgehogs.

B05-N12 | Chapter 7 — Desolation | S051–S054 | 16 lines
Text: “The town was in ruins and there was nothing to eat” → ““Its the one place with food” solemnly spoke Thumper”
Speakers: Narration through S53. Two rabbits’ warnings S54.3; Thumper’s reply S54.4. No Sina dialogue.
Image: REPLACE; create assets/images/B05-N12.png. Legacy assignments: B05-P09 → B05-sina-black-snake.png; B05-P10 → B05-frumper-banquet.png.
Direction: In the rain-struck, hungry town, Squirrel reunites rescued young rabbits with weeping parents while Thumper carries an empty food basket toward Miller’s farm gate. Make ruined stores, scant roots/nuts and desolate rabbits visible; retain the emotional move from failed sharing toward the one remaining food source. No banquet yet.

B05-N13 | Chapter 7 — Desolation | S055–S058 | 16 lines
Text: “The Gate was already open when he went towards the house.” → “They are invited to the table at my sacred banquet hall”
Speakers: S55–S57.3 narration. Frumper Miller speaks S57.4 through S58. Do not label the revelation as Thumper, ordinary Miller or Narrator.
Image: REPLACE; create assets/images/B05-N13.png. Legacy assignments: B05-P10 → B05-frumper-banquet.png.
Direction: Thumper stands alone at the farmhouse doorway as it opens to reveal the canonical Frumper Miller welcoming him, with abundant food and the banquet hall beyond. The open gate and protective farm landscape must match Book 1; a discreet trapped rat/pit and distant dog may establish the approach without gore. Preserve the mysterious “figure one and three” through subtle threefold natural illumination around one Frumper, not three duplicated rabbits or an explanatory Trinity diagram. Other invited friends have not arrived yet: replace/edit the existing banquet image that already gathers them at the door.
'''

print("Manifest block loaded successfully")
