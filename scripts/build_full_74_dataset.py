"""
Build complete window.THUMPER_COLLECTION with all 74 spreads:
- 100% verbatim text matching source JSON (302 stanzas, 1,196 lines)
- All 34 chapters start on a fresh spread
- Correct titles: Book 1 Ch 7 is "the Farmhouse", Book 3 Ch 5 is "Frumper's adventure", empty chapters display as "Chapter X"
- Clean speaker cues (zero "Narrator —" badges)
- Complete image mappings (53 REPLACE + 21 KEEP)
- Uniform typography metadata
"""

import json
import os
import re

with open('/tmp/thumper_source.json', 'r', encoding='utf-8') as f:
    source_books = json.load(f)

# Flatten stanzas per book
books_stanzas = []
for b_idx, b in enumerate(source_books):
    stanzas = []
    for p in b['pages']:
        for s in p['stanzas']:
            stanzas.append({
                'lines': s['lines']
            })
    books_stanzas.append(stanzas)

# Spread table:
# (id, book_num, chapter_num, chapter_title, is_chapter_start, start_s, end_s, expected_lines, image_path, title, brief, theologicalNote)
SPREADS_SPEC = [
    # Book 1: 17 spreads
    ("B01-N01", 1, 1, "A Rainy Day", True, 1, 4, 16, "assets/images/B01-S01-rainy-games.png", "Rainy Games", "Thumper watches the other rabbits playing outside his window in the rain.", "Contingent beings immersed in the immediate material world."),
    ("B01-N02", 1, 1, "A Rainy Day", False, 5, 8, 16, "assets/images/B01-S02-thumper-imagines.png", "Thumper Imagines Frumper", "Thumper at his desk imagining a winged friend who can fly anywhere.", "The intellect's capacity to conceive of transcendent realities."),
    ("B01-N03", 1, 1, "A Rainy Day", False, 9, 12, 16, "assets/images/B01-N03.png", "Longing for Miller's Farm", "Thumper looking out the rainy window imagining his winged friend flying over the fence.", "The desire for the ultimate good transcending natural limits."),
    ("B01-N04", 1, 2, "Thinking Hard", True, 13, 16, 16, "assets/images/B01-S07.png", "The Square Circle", "Thumper pondering contradictory shapes at his desk.", "The principle of non-contradiction in classical philosophy."),
    ("B01-N05", 1, 2, "Thinking Hard", False, 17, 20, 16, "assets/images/B01-S09.png", "Exhaustion Over Stew", "Thumper sitting thoughtfully over a bowl of carrot stew.", "The limits of purely self-contained causes."),
    ("B01-N06", 1, 3, "Essence and existence", True, 21, 24, 16, "assets/images/B01-N06.png", "Cutting the Butter", "Thumper slicing a block of butter at the kitchen table.", "Avicenna's distinction between what a thing is and that it is."),
    ("B01-N07", 1, 3, "Essence and existence", False, 25, 29, 20, "assets/images/B01-S11.png", "The Cut Butter on Board", "Thumper contemplating the edges of the cut butter block.", "Existence as the fundamental act of all beings."),
    ("B01-N08", 1, 4, "Which came first", True, 30, 33, 16, "assets/images/B01-S13.png", "Puzzling Over Cause", "Thumper resting his chin in his paws over the table.", "No contingent thing can be the cause of its own existence."),
    ("B01-N09", 1, 4, "Which came first", False, 34, 36, 12, "assets/images/B01-S15.png", "Light Through Clouds", "Thumper at the window as sunlight breaks through the dreary clouds.", "The realization of an uncaused First Cause."),
    ("B01-N10", 1, 5, "The Search", True, 37, 40, 16, "assets/images/B01-S17.png", "Asking the Bunnies", "Thumper questioning the group of rabbits on the woodland path.", "The philosopher seeking truth among those indifferent to metaphysics."),
    ("B01-N11", 1, 5, "The Search", False, 41, 44, 16, "assets/images/B01-S19.png", "Under the Barbed Wire", "Thumper crawling beneath the wire fence into the dangerous farm.", "The perilous pursuit of divine truth."),
    ("B01-N12", 1, 6, "The Farm", True, 45, 48, 16, "assets/images/B01-S20.png", "Traps and Berries", "Thumper cautiously navigating traps and pits toward the berries.", "The moral trials and temptations on the spiritual ascent."),
    ("B01-N13", 1, 6, "The Farm", False, 49, 52, 16, "assets/images/B01-S23.png", "Sleeping Under Berries", "Thumper asleep beneath the berry bush with guilty dreams.", "Concupiscence and the burden of guilt after falling into sin."),
    ("B01-N14", 1, 6, "The Farm", False, 53, 55, 12, "assets/images/B01-S24.png", "Awakening and Repentance", "Thumper awake under the berry branches resolved to confess.", "Metanoia: genuine repentance and the turning toward the Father."),
    ("B01-N15", 1, 7, "the Farmhouse", True, 56, 59, 16, "assets/images/B01-S26.png", "The Farm Dog Chases", "The ferocious farm dog pursuing Thumper toward the path.", "The consequences of sin overtaking creaturely strength."),
    ("B01-N16", 1, 7, "the Farmhouse", False, 60, 62, 12, "assets/images/B01-S28.png", "Airborne Rescue", "Frumper lifting Thumper into the air above the farm fence.", "The intervention of unmerited Divine Grace."),
    ("B01-N17", 1, 8, "Homecoming;", True, 63, 65, 10, "assets/images/B01-S29.png", "Peace at Home", "Thumper and Frumper resting peacefully near home at sunset.", "The peace of reconciliation and communion with God."),

    # Book 2: 14 spreads
    ("B02-N01", 2, 1, "The landing", True, 1, 4, 16, "assets/images/B02-S01-commotion-clockshop.png", "Commotion at the Clock Shop", "Gathered rabbits outside Hedgehog's clock shop after the landing.", "Initial skepticism toward claims of divine intervention."),
    ("B02-N02", 2, 1, "The landing", False, 5, 9, 20, "assets/images/B02-N02.png", "Hedgehog Addresses the Crowd", "Hedgehog rapping his staff on the shop to dismiss the miracle thesis.", "Materialism and naturalistic reductionism."),
    ("B02-N03", 2, 1, "The landing", False, 10, 13, 16, "assets/images/B02-N03.png", "Dispersing Crowd and Inquiries", "Thumper questioning Hedgehog outside the doorway as rain resumes.", "The enduring quest for deeper causal explanations."),
    ("B02-N04", 2, 2, "Lunch with frumper", True, 14, 17, 16, "assets/images/B02-S03-lunch-table.png", "Lunch in the Cottage", "Thumper and Frumper sharing stew and butter at the wooden table.", "The dialogue between faith and reason."),
    ("B02-N05", 2, 2, "Lunch with frumper", False, 18, 21, 16, "assets/images/B02-N05.png", "Encouragement to Apprentice", "Frumper encouraging Thumper to learn the art of clockmaking.", "Engaging scientific disciplines to discover higher order."),
    ("B02-N06", 2, 3, "Chapter 3", True, 22, 25, 16, "assets/images/B02-N06.png", "Retrieving the Hammer", "Thumper fetching Hedgehog's missing small hammer in the workshop.", "Beginning the discipline of philosophical inquiry."),
    ("B02-N07", 2, 3, "Chapter 3", False, 26, 29, 16, "assets/images/B02-S06-magnifying-gears.png", "Examining the Gears", "Hedgehog inspecting tiny watch escapements under magnifying loupe.", "The intricate contingent machinery of the cosmos."),
    ("B02-N08", 2, 3, "Chapter 3", False, 30, 33, 16, "assets/images/B02-N08.png", "Sound of Wings at the Window", "Hedgehog peering suspiciously at the twilight window.", "The shadowy counterfeit of the transcendent (Proditor)."),
    ("B02-N09", 2, 4, "Chapter 4", True, 34, 37, 16, "assets/images/B02-clockmaker-workshop.png", "The Clockmaker's Workshop", "Thumper questioning Hedgehog amidst clocks and brass mechanisms.", "Aquinas's First Way: the necessity of an Unmoved Mover."),
    ("B02-N10", 2, 4, "Chapter 4", False, 38, 41, 16, "assets/images/B02-N10.png", "Arranging Unpowered Gears", "Thumper laying out brass gears that cannot move on their own.", "The impossibility of an infinite regress of secondary movers."),
    ("B02-N11", 2, 4, "Chapter 4", False, 42, 45, 16, "assets/images/B02-N11.png", "Winding the Mainspring", "Close view of Hedgehog winding the spring with a brass key.", "The external source of actuality imparting motion."),
    ("B02-N12", 2, 4, "Chapter 4", False, 46, 49, 16, "assets/images/B02-N12.png", "Quarter to Nine", "Thumper pointing to the hands on the clock face in late workshop.", "The reality of time and measure in creation."),
    ("B02-N13", 2, 5, "Chapter 5", True, 50, 53, 16, "assets/images/B02-N13.png", "Frumper Enters the Workshop", "Frumper folding his wings and entering the workshop to assist.", "Grace cooperates with nature in human vocation."),
    ("B02-N14", 2, 5, "Chapter 5", False, 54, 57, 16, "assets/images/B02-N14.png", "Dawn's Plentiful Watches", "Dawn light over boxes of finished pocket watches.", "The divine bounty overflowing through faithful cooperation."),

    # Book 3: 17 spreads
    ("B03-N01", 3, 1, "Chapter 1", True, 1, 3, 12, "assets/images/B03-N01.png", "The Boiling Pot", "Sleepy Thumper upstairs in bed while pot boils on woodstove below.", "The origin of natural evil through creaturely fallibility."),
    ("B03-N02", 3, 1, "Chapter 1", False, 4, 7, 16, "assets/images/B03-N02.png", "Escape Into Thorns", "Thumper escaping burning cottage into thorns as messenger arrives.", "The sudden catastrophe of suffering and pain."),
    ("B03-N03", 3, 2, "visitors", True, 8, 11, 16, "assets/images/B03-N03.png", "Three Unhelpful Rabbits", "Injured Thumper in ashes with three critical visitor rabbits.", "Job's comforters offering shallow theodicies."),
    ("B03-N04", 3, 2, "visitors", False, 12, 16, 20, "assets/images/B03-N04.png", "Hedgehog Splints the Leg", "Hedgehog binding Thumper's broken leg with staff splint.", "True charity and practical compassion amidst suffering."),
    ("B03-N05", 3, 3, "action", True, 17, 20, 16, "assets/images/B03-N05.png", "Mole Tumbles In", "Mole tumbling from hillside burrow with cheerful encouragement.", "Resilience and the proper response to fallen nature."),
    ("B03-N06", 3, 3, "action", False, 21, 23, 12, "assets/images/B03-N06.png", "Drawing the Blueprints", "Thumper drawing house plans while Mole digs foundation trench.", "Sub-creation and rebuilding with hope and purpose."),
    ("B03-N07", 3, 4, "The remedies", True, 24, 27, 16, "assets/images/B03-N07.png", "Squirrel's Riverside Picnic", "Squirrel helping Thumper relax by mountain stream with wine.", "Aquinas's remedies for sorrow: friends, rest, and simple goods."),
    ("B03-N08", 3, 4, "The remedies", False, 28, 31, 14, "assets/images/B03-N08.png", "Songbird on the Bough", "Squirrel offering crumb of scone to songbird on the willow branch.", "The music of creation declaring providence even in trial."),
    ("B03-N09", 3, 5, "Frumper's adventure", True, 32, 35, 16, "assets/images/B03-N09.png", "Singed Frumper at Sawmill", "Frumper with singed fur carrying pine boards beside sawmill.", "The divine willingness to share in creaturely suffering."),
    ("B03-N10", 3, 5, "Frumper's adventure", False, 36, 40, 20, "assets/images/B03-N10.png", "Intercepting Lightning", "Frumper diving through storm to catch lightning above pinned fawn.", "Vicarious sacrifice and heroic intervention against death."),
    ("B03-N11", 3, 6, "thumpers question", True, 41, 44, 16, "assets/images/B03-N11.png", "The Fly on the Paw", "Singed Frumper gently blowing a live fly from his open paw.", "God's minute governance over even the smallest creature."),
    ("B03-N12", 3, 6, "thumpers question", False, 45, 47, 12, "assets/images/B03-N12.png", "The Mountain of Wisdom", "Quiet conversation on timber beam looking out toward mountains.", "The perspective of eternity resolving temporal struggles."),
    ("B03-N13", 3, 7, "the universe", True, 48, 52, 20, "assets/images/B03-N13.png", "Judging Unfinished Framing", "Frumper gesturing toward bare rafters of the incomplete cottage.", "Do not judge the finished work by the unfinished foundation."),
    ("B03-N14", 3, 7, "the universe", False, 53, 57, 20, "assets/images/B03-N14.png", "Lightning Scars and Love", "Thumper studying Frumper's scars in conversation about freedom.", "Genuine love requires genuine creaturely freedom and choice."),
    ("B03-N15", 3, 8, "Chapter 8", True, 58, 61, 16, "assets/images/B03-N15.png", "The Measuring Rod", "Frumper holding notched wooden rod against pine timber board.", "The objective standard of goodness and justice."),
    ("B03-N16", 3, 8, "Chapter 8", False, 62, 65, 16, "assets/images/B03-N16.png", "The Lesson of the Hot Handle", "Frumper drawing attention to Thumper's burned paw from the door.", "Suffering evil vs. doing evil: moral integrity."),
    ("B03-N17", 3, 8, "Chapter 8", False, 66, 68, 12, "assets/images/B03-N17.png", "Carrying Cedar Boards Healed", "Thumper walking firmly carrying heavy cedar boards uphill.", "The final restoration, healing, and resurrection of joy."),

    # Book 4: 13 spreads
    ("B04-N01", 4, 1, "The Rumbling", True, 1, 3, 12, "assets/images/B04-N01.png", "Seismometer in the Shop", "Hedgehog and Mole examining seismometer pendulum and trace.", "Discerning spiritual signs and the rumblings of judgment."),
    ("B04-N02", 4, 1, "The Rumbling", False, 4, 7, 16, "assets/images/B04-N02.png", "Mole's Cavern Fall", "Mole fallen into deep dark volcanic fissure under high ceiling.", "The descent into the underworld of spiritual peril."),
    ("B04-N03", 4, 2, "Chapter 2", True, 8, 11, 16, "assets/images/B04-N03.png", "At the Volcano Rim", "Rescue party with coiled rope peering into the smoking pit.", "The harrowing of hell: stepping into danger to save the lost."),
    ("B04-N04", 4, 2, "Chapter 2", False, 12, 16, 20, "assets/images/B04-N04.png", "Descent Into the Gloom", "Frumper leading companions with blazing torch along blood trail.", "Light penetrating into infernal darkness."),
    ("B04-N05", 4, 3, "Chapter 3", True, 17, 20, 16, "assets/images/B04-N05.png", "Glamour of the Cave Rabbits", "Thumper reaching for false honey-bread exposed as stone-chewing.", "The deceit of sin: gluttony and false sensory satisfaction."),
    ("B04-N06", 4, 3, "Chapter 3", False, 21, 23, 12, "assets/images/B04-N06.png", "Real Berries in Torchlight", "Frumper handing real berries as jagged stone falls from paw.", "True spiritual nourishment awakening the soul from delusion."),
    ("B04-N07", 4, 4, "Chapter 4", True, 24, 27, 16, "assets/images/B04-N07.png", "Temptation on the Precipice", "Sly bat coaxing weary Squirrel toward the smooth slide.", "Sloth and the seductive ease of the downward path."),
    ("B04-N08", 4, 4, "Chapter 4", False, 28, 31, 16, "assets/images/B04-N08.png", "Torch Reveals the Abyss", "Frumper's torch exposing fatal drop and open pit beneath slide.", "Truth unmasking the deadly end of temptation."),
    ("B04-N09", 4, 5, "Chapter 5", True, 32, 35, 16, "assets/images/B04-N09.png", "Proditor with the Probe", "Dog-sized Proditor sneering with red eyes tapping metal probe.", "Pride and intellectual cynicism mocking truth."),
    ("B04-N10", 4, 5, "Chapter 5", False, 36, 40, 16, "assets/images/B04-N10.png", "Puppet in the Shaft", "Hedgehog suspended by cords in mocking puppet coronation.", "Vainglory and the mockery of creaturely pride."),
    ("B04-N11", 4, 5, "Chapter 5", False, 41, 45, 20, "assets/images/B04-N11.png", "Stalactite Crushes Proditor", "Frumper dropping stalactite pinning Proditor as cords slacken.", "The sudden overthrow of demonic deception."),
    ("B04-N12", 4, 6, "Chapter 6", True, 46, 49, 16, "assets/images/B04-N12.png", "Finding Mole with Eye Flaps", "Mole found smiling with ear/eye flaps as lava approaches.", "Spiritual prudence guarding the senses from seduction."),
    ("B04-N13", 4, 6, "Chapter 6", False, 50, 54, 18, "assets/images/B04-N13.png", "Breaching the Sea Tunnel", "Frumper shattering boulder opening tunnel to daylight and ocean.", "Liberation and triumph over the infernal abyss."),

    # Book 5: 13 spreads
    ("B05-N01", 5, 1, "The Entrance", True, 1, 3, 12, "assets/images/B05-N01.png", "Weasels on Rat-Drawn Wagon", "Ragged weasels riding wooden wagon pulled by rats down forest road.", "The arrival of sophistry, greed, and moral corruption."),
    ("B05-N02", 5, 1, "The Entrance", False, 4, 6, 12, "assets/images/B05-N02.png", "Boarding Up the Shop", "Weasel hammering boards across clock shop door trapping Hedgehog.", "Silencing the voice of reason and tradition."),
    ("B05-N03", 5, 2, "Pets", True, 7, 12, 24, "assets/images/B05-weasels-cart.png", "Selling Beetles from the Cart", "Weasels peddling beetle jars as necessary pets to rabbit crowd.", "Idolatry: worshipping created things rather than the Creator."),
    ("B05-N04", 5, 3, "The light of the moon", True, 13, 17, 20, "assets/images/B05-N04.png", "Sina Under Crescent Moon", "Black snake Sina coiling around weasel by river willow tree.", "Prudence confronting deceit under the natural light of truth."),
    ("B05-N05", 5, 3, "The light of the moon", False, 18, 22, 20, "assets/images/B05-N05.png", "Tightened Coils and Logic", "Sina constricting weasel as Thumper pleads with raised paw.", "The dialectic of justice, mercy, and logical necessity."),
    ("B05-N06", 5, 3, "The light of the moon", False, 23, 27, 20, "assets/images/B05-S05-weasel-released.png", "Sina Releases the Weasel", "Weasel gasping on knees as Sina uncoils and slips away into night.", "Justice tempered with mercy; the refutation of circularity."),
    ("B05-N07", 5, 4, "the elixir", True, 28, 31, 16, "assets/images/B05-N07.png", "Selling the Elixir", "Weasels selling miracle potion as rabbit flaunts stolen vest.", "Consumerism and the illusion of instant transformation."),
    ("B05-N08", 5, 4, "the elixir", False, 32, 35, 16, "assets/images/B05-N08.png", "Riot in Looted Town", "Mole sheltering sensible rabbits while crowd fights over stolen goods.", "The social disintegration caused by unchecked covetousness."),
    ("B05-N09", 5, 5, "Swim like a fish", True, 36, 41, 22, "assets/images/B05-N09.png", "Rescuing Rabbits with Fins", "Squirrel on tree branch pulling wet rabbits with fake fins from river.", "The deadly folly of trying to transcend one's created nature."),
    ("B05-N10", 5, 6, "Hedgehog strikes back", True, 42, 46, 20, "assets/images/B05-N10.png", "Hedgehog Confronts Wagon", "Hedgehog wielding hammer atop wagon exposing the swindle.", "Righteous indignation and the defense of truth."),
    ("B05-N11", 5, 6, "Hedgehog strikes back", False, 47, 50, 16, "assets/images/B05-N11.png", "Hammer Smashes Beetle Box", "Hedgehog smashing glass display box and curling into defensive ball.", "The destruction of idols and victory of genuine substance."),
    ("B05-N12", 5, 7, "Desolation", True, 51, 54, 16, "assets/images/B05-N12.png", "Desolation in Ruined Town", "Thumper carrying empty basket toward Miller's farm gate.", "The poverty of spirit preceding entry into the Kingdom."),
    ("B05-N13", 5, 7, "Desolation", False, 55, 58, 16, "assets/images/B05-N13.png", "The Sacred Banquet Hall", "Frumper Miller welcoming Thumper into golden glowing banquet hall.", "The Beatific Vision: the eternal feast of divine communion.")
]

# Speaker cue mapping (zero Narrator badges)
SPEAKER_CUES = {
    # Book 1
    "B01-N10": {8: "Thumper —", 14: "Other bunnies —"},
    "B01-N11": {0: "Other bunnies —", 11: "Other bunnies —"},
    "B01-N15": {0: "Thumper —"},

    # Book 2
    "B02-N01": {2: "Hedgehog —", 8: "Thumper —", 15: "Other bunnies —"},
    "B02-N02": {1: "Hedgehog —"},
    "B02-N03": {2: "Thumper —", 4: "Hedgehog —", 12: "Thumper —"},
    "B02-N04": {2: "Thumper —", 4: "Thumper —", 9: "Frumper —"},
    "B02-N05": {0: "Thumper —", 4: "Frumper —"},
    "B02-N06": {3: "Hedgehog —", 4: "Thumper —", 8: "Hedgehog —", 12: "Hedgehog —"},
    "B02-N07": {0: "Thumper —", 1: "Hedgehog —", 3: "Thumper —"},
    "B02-N08": {0: "Hedgehog —", 2: "Thumper —", 4: "Hedgehog —", 8: "Thumper —", 12: "Hedgehog —"},
    "B02-N09": {0: "Thumper —", 8: "Hedgehog —", 12: "Thumper —"},
    "B02-N10": {0: "Thumper —", 4: "Hedgehog —", 8: "Thumper —"},
    "B02-N11": {0: "Hedgehog —", 4: "Thumper —"},
    "B02-N12": {0: "Hedgehog —", 4: "Thumper —", 12: "Hedgehog —"},
    "B02-N13": {0: "Thumper —", 2: "Frumper —", 8: "Hedgehog —", 10: "Frumper —"},
    "B02-N14": {10: "Frumper —"},

    # Book 3
    "B03-N03": {2: "Thumper —", 6: "First bunny —", 9: "Second bunny —", 13: "Third bunny —"},
    "B03-N04": {0: "Hedgehog —", 4: "Hedgehog —", 6: "Thumper —", 13: "Hedgehog —", 16: "Hedgehog —"},
    "B03-N05": {4: "Mole —", 6: "Thumper —", 7: "Mole —"},
    "B03-N06": {0: "Mole —"},
    "B03-N07": {0: "Squirrel —", 4: "Squirrel —"},
    "B03-N08": {4: "Songbird —", 9: "Squirrel —"},
    "B03-N09": {8: "Frumper —", 12: "Thumper —"},
    "B03-N10": {0: "Frumper —"},
    "B03-N11": {0: "Thumper —", 10: "Frumper —", 11: "Thumper —", 12: "Frumper —"},
    "B03-N12": {0: "Frumper —"},
    "B03-N13": {0: "Frumper —"},
    "B03-N14": {0: "Frumper —"},
    "B03-N15": {5: "Thumper —", 6: "Frumper —"},
    "B03-N16": {0: "Frumper —"},
    "B03-N17": {0: "Frumper —"},

    # Book 4
    "B04-N01": {2: "Mole —", 4: "Hedgehog —", 8: "Mole —"},
    "B04-N03": {3: "Raven —", 4: "Hedgehog —", 8: "Squirrel —", 10: "Hedgehog —"},
    "B04-N04": {0: "Frumper —", 4: "Squirrel —", 5: "Frumper —", 6: "Hedgehog —", 8: "Thumper —", 17: "Bat —"},
    "B04-N05": {6: "Cave bunnies —", 7: "Thumper —", 8: "Squirrel —", 12: "Frumper —"},
    "B04-N06": {8: "Frumper —"},
    "B04-N07": {10: "Bat —", 12: "Bat —", 15: "Bat —"},
    "B04-N08": {0: "Bat —", 3: "Squirrel —", 4: "Bat —", 6: "Squirrel —"},
    "B04-N09": {2: "Hedgehog —", 7: "Proditor —", 8: "Proditor —", 10: "Hedgehog —", 12: "Proditor —", 14: "Hedgehog —"},
    "B04-N10": {0: "Proditor —", 5: "Proditor —", 8: "Proditor —", 12: "Proditor —", 14: "Thumper —"},
    "B04-N11": {17: "Hedgehog —", 18: "Squirrel —"},
    "B04-N12": {0: "Mole —", 1: "Squirrel —", 5: "Mole —", 12: "Hedgehog & Mole —", 15: "Mole —"},
    "B04-N13": {0: "Mole —", 3: "Thumper —"},

    # Book 5
    "B05-N02": {5: "Hedgehog —", 11: "Hedgehog —"},
    "B05-N03": {0: "Weasel —", 4: "Weasel —", 8: "Weasel —", 13: "Weasel —"},
    "B05-N04": {2: "Sina —", 6: "Sina —", 8: "Sina —", 14: "Sina —", 16: "Weasel —", 18: "Weasel —"},
    "B05-N05": {0: "Sina —", 2: "Weasel —", 3: "Thumper —", 4: "Sina —", 8: "Sina —", 15: "Thumper —", 16: "Thumper —"},
    "B05-N06": {0: "Thumper —", 3: "Sina —", 4: "Thumper —", 7: "Sina —", 9: "Thumper —", 19: "Sina —"},
    "B05-N07": {2: "Weasels —", 6: "Weasels —", 10: "Weasels —", 13: "Weasels —"},
    "B05-N08": {0: "Weasels —", 12: "Rabbits —"},
    "B05-N09": {3: "Weasels —", 4: "Weasels —", 8: "Weasels —", 20: "Squirrel —"},
    "B05-N10": {5: "Weasels —", 7: "Hedgehog —", 8: "Hedgehog —", 10: "Rabbit —", 11: "Hedgehog —", 12: "Hedgehog —", 16: "Hedgehog —"},
    "B05-N11": {1: "Hedgehog —", 2: "Buyer —", 3: "Hedgehog —", 5: "Hedgehog —", 7: "Weasels —", 13: "Weasel —"},
    "B05-N12": {14: "Rabbits —", 15: "Thumper —"},
    "B05-N13": {11: "Frumper Miller —", 12: "Frumper Miller —"}
}

BOOK_META = {
    1: {
        "title": "Finding God on a Dreary Day",
        "theme": "The Existence of God, Essence vs. Existence, and Grace",
        "subtitle": "An Allegory on the Longing for the Transcendent & the Gift of Grace",
        "borderTheme": "ivy"
    },
    2: {
        "title": "Thumper and the Clock Maker",
        "theme": "The First Mover, Efficient Causality, and Teleology",
        "subtitle": "Aquinas’s First Way & the Artisan of the Cosmos",
        "borderTheme": "clockwork"
    },
    3: {
        "title": "Thumpers Bad Day",
        "theme": "The Problem of Evil, Free Will, and Suffering",
        "subtitle": "An Allegory on Evil, Goodness, and Divine Providence",
        "borderTheme": "oak"
    },
    4: {
        "title": "Thumpers Inferno",
        "theme": "Sin, Deception, Pride, and the Nature of Hell",
        "subtitle": "An Allegory on the Seven Deadly Sins & Spiritual Blindness",
        "borderTheme": "filigree"
    },
    5: {
        "title": "Necessary Beetles",
        "theme": "Justice, Mercy, Idolatry, and the Beatific Vision",
        "subtitle": "An Allegory on Idolatry, Modernity, and the Eternal Banquet",
        "borderTheme": "laurel"
    }
}

output_books = []
for b_num in range(1, 6):
    b_meta = BOOK_META[b_num]
    book_obj = {
        "bookNumber": b_num,
        "title": b_meta["title"],
        "theme": b_meta["theme"],
        "subtitle": b_meta["subtitle"],
        "borderTheme": b_meta["borderTheme"],
        "pages": []
    }
    output_books.append(book_obj)

global_spread_num = 0
all_assembled_lines = []

for spec in SPREADS_SPEC:
    (spread_id, book_num, chapter_num, chapter_title, is_chapter_start,
     start_s, end_s, expected_lines, image_path, ill_title, ill_brief, ill_theological) = spec

    global_spread_num += 1
    book_stanzas_source = books_stanzas[book_num - 1]

    # Slice stanzas
    spread_stanzas = []
    spread_lines = []
    for s_idx in range(start_s - 1, end_s):
        stz = book_stanzas_source[s_idx]
        spread_stanzas.append({
            "chapter": chapter_num,
            "chapterTitle": chapter_title,
            "lines": list(stz['lines'])
        })
        spread_lines.extend(stz['lines'])
        all_assembled_lines.extend(stz['lines'])

    if len(spread_lines) != expected_lines:
        raise ValueError(f"Line count mismatch on {spread_id}: expected {expected_lines}, got {len(spread_lines)}")

    # Speaker cues
    raw_cues = SPEAKER_CUES.get(spread_id, {})
    speaker_before = {str(k): v for k, v in raw_cues.items()}

    # Check first line formatting
    first_line = spread_lines[0]
    initial_prefix = ""
    initial_letter = ""
    first_line_rest = first_line
    is_dialogue_opening = False

    if is_chapter_start:
        # Check if line 0 is dialogue or narrative
        starts_with_quote = first_line.startswith('“') or first_line.startswith('"')
        has_speaker_at_0 = "0" in speaker_before

        if starts_with_quote or has_speaker_at_0:
            is_dialogue_opening = True
            initial_letter = ""
            first_line_rest = first_line
        else:
            first_char = first_line[0] if first_line else ""
            if first_char in ('"', '“', "'", '‘'):
                initial_prefix = first_char
                if len(first_line) > 1:
                    initial_letter = first_line[1]
                    first_line_rest = first_line[2:]
                else:
                    initial_letter = ""
                    first_line_rest = ""
            elif first_char.isalpha():
                initial_letter = first_char
                first_line_rest = first_line[1:]
            else:
                initial_letter = ""
                first_line_rest = first_line

    page_obj = {
        "id": spread_id,
        "spreadNumber": global_spread_num,
        "bookNumber": book_num,
        "bookTitle": BOOK_META[book_num]["title"],
        "chapter": chapter_num,
        "chapterTitle": chapter_title,
        "isChapterStart": is_chapter_start,
        "isDialogueOpening": is_dialogue_opening,
        "initialPrefix": initial_prefix,
        "initialLetter": initial_letter,
        "firstLineRest": first_line_rest,
        "speakerBefore": speaker_before,
        "stanzas": spread_stanzas,
        "illustration": {
            "title": ill_title,
            "brief": ill_brief,
            "image": image_path,
            "theologicalNote": ill_theological
        }
    }

    output_books[book_num - 1]["pages"].append(page_obj)

# Verification against source
source_all_lines = []
for b in source_books:
    for p in b['pages']:
        for s in p['stanzas']:
            source_all_lines.extend(s['lines'])

print(f"Total source lines: {len(source_all_lines)}")
print(f"Total assembled lines: {len(all_assembled_lines)}")
if source_all_lines != all_assembled_lines:
    for i in range(min(len(source_all_lines), len(all_assembled_lines))):
        if source_all_lines[i] != all_assembled_lines[i]:
            print(f"Mismatch at line {i}:")
            print(f"  Source:    '{source_all_lines[i]}'")
            print(f"  Assembled: '{all_assembled_lines[i]}'")
            break
    raise SystemExit("Source verification FAILED!")

print("VERIFICATION SUCCESS: 100% string equality with source manuscript across all 74 spreads!")

# Write to js/book-data.js
js_content = "/**\n * Complete 5-Book Thumper Series Reader Data (74 Spreads)\n * Faithfully transcribed verbatim from source manuscripts\n */\nwindow.THUMPER_COLLECTION = " + json.dumps(output_books, indent=2, ensure_ascii=False) + ";\n"

with open('js/book-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated js/book-data.js with {global_spread_num} spreads across 5 books!")
