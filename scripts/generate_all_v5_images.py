"""
Complete automated generation script for all 53 REPLACE images for Version 5.
Uses OpenRouter API with google/gemini-3.1-flash-image and multimodal canonical reference images.
Saves directly to assets/images/<spread_id>.png.
"""

import os
import sys
import json
import time
import base64
import urllib.request
from PIL import Image

KEY = os.environ.get('OPENROUTER_API_KEY')
if not KEY:
    print("ERROR: OPENROUTER_API_KEY is not set.")
    sys.exit(1)

CANONICAL_DIR = "/Users/jacobbuscher/Documents/Thumper "
OUTPUT_DIR = "/Users/jacobbuscher/Documents/Thumper /interactive-book/assets/images"

def get_b64_image(filename, max_dim=768):
    path = os.path.join(CANONICAL_DIR, filename)
    if not os.path.exists(path):
        print(f"Warning: reference image {path} not found.")
        return None
    try:
        im = Image.open(path)
        im.thumbnail((max_dim, max_dim))
        import io
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

# Pre-cache canonical images
cached_refs = {}
ref_filenames = [
    "Thumper .png",
    "Frumper .png",
    "Frumper Flying Sky.png",
    "Hedgehog.png",
    "Mole.png",
    "Squirel .png",
    "Proditor.png",
    "bunnies book 1 .png"
]

for fname in ref_filenames:
    b64 = get_b64_image(fname)
    if b64:
        cached_refs[fname] = b64
print(f"Cached {len(cached_refs)} canonical reference images.")

# 53 Image Specifications
SPECS = [
    # Book 1 (2 images)
    {
        "id": "B01-N03",
        "refs": ["Thumper .png", "Frumper Flying Sky.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B01-N03. Depict this focal action: From inside Thumper's rainy window, frame the distant fenced Miller farm, carrots and especially plump berries. Show Thumper imagining the winged friend flying over its fence at night to fetch food; an inset-like painterly reverie may distinguish this from current reality. Required visible characters/objects: Thumper the young rounded brown rabbit looking out rainy window, distant fenced Miller farm, plump berries, imagined winged rabbit soaring over fence. Preserve painterly depth, warm natural woodland palette, fine textured fur. Exclude modern streetwear, cartoon faces, actual rescue or farmhouse revelation. Show one coherent place and moment; no text. Match the established painterly series."
    },
    {
        "id": "B01-N06",
        "refs": ["Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B01-N06. Depict this focal action: Thumper at the cottage table reaches for snacking carrots and butter, then begins cutting the block as an idea occurs. Required visible characters/objects: Thumper the young rounded brown rabbit seated at wooden cottage table, butter block on board, knife in paw, carrots nearby, thoughtful expression of sudden discovery. Preserve painterly depth, warm natural woodland palette, fine textured fur. Exclude literal being made from butter, modern clothing, cartoon faces, text. Match the established painterly series."
    },

    # Book 2 (10 images)
    {
        "id": "B02-N02",
        "refs": ["Hedgehog.png", "Thumper .png", "bunnies book 1 .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N02. Depict this focal action: Hedgehog raps his wooden staff against his clock shop to quiet the celebration, addressing Thumper and the gathered rabbits with skeptical confidence. Required visible characters/objects: Hedgehog the clockmaker in waistcoat and glasses holding wooden staff, clock shop exterior with antique clocks visible, listening Thumper and gathered ordinary rabbits. Preserve Hedgehog and Thumper canonical scale and maturity. Exclude lunch table, journey, unrelated playing, text. Match the established painterly series."
    },
    {
        "id": "B02-N03",
        "refs": ["Thumper .png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N03. Depict this focal action: The crowd disperses back to its games. Thumper remains questioning Hedgehog beside the clock shop doorway; Hedgehog gestures at an antique clock, then withdraws as rain resumes. Required visible characters/objects: Thumper looking inquisitive, Hedgehog gesturing toward shop clock, rainy cobblestones, dispersing crowd in far distance. Preserve canonical designs and adult/young-rabbit proportions. Exclude Frumper at lunch, modern elements, text. Match the established painterly series."
    },
    {
        "id": "B02-N05",
        "refs": ["Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N05. Depict this focal action: A distinct closer view across the same lunch table: troubled Thumper explains his doubts while Frumper listens attentively, then warmly encourages him to learn clockmaking. Required visible characters/objects: Thumper and winged Frumper across cottage wooden table, bowls of carrot stew and butter, Frumper's folded feathered wings, warm encouraging expressions between adult friends. Preserve canonical designs. Exclude Hedgehog, duplicate Frumpers, text. Match the established painterly series."
    },
    {
        "id": "B02-N06",
        "refs": ["Thumper .png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N06. Depict this focal action: Morning at the clock shop: Thumper has come to apprentice and eagerly fetches Hedgehog's missing wooden-handled hammer from the far side of the workshop. Required visible characters/objects: Thumper carrying the distinctive small craftsman hammer, Hedgehog working at cluttered clockmaker workbench, clock parts, tool shed/storage shelves. Establish this hammer clearly. Exclude Frumper, giant scales, text. Match the established painterly series."
    },
    {
        "id": "B02-N08",
        "refs": ["Hedgehog.png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N08. Depict this focal action: Beside the newly assembled clock, Hedgehog peers uncertainly toward the workshop window after hearing a sound like wings, while Thumper challenges the identification. Required visible characters/objects: Hedgehog looking startled toward window, Thumper beside bench with finished clock mechanism, contrast in attention. Distant twilight outside window may hint at bats at dusk, not winged rabbits. Exclude actual Frumper outside, text. Match the established painterly series."
    },
    {
        "id": "B02-N10",
        "refs": ["Thumper .png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N10. Depict this focal action: Thumper lays out unpowered intermeshing brass gears on the workbench while Hedgehog explains that adding gears cannot supply motion. Required visible characters/objects: Thumper arranging loose brass cogs and gears on wooden table, Hedgehog lecturing beside him, an unfinished clock frame and a separate unattached coil spring. Exclude self-moving magical gears, infinite-chain diagrams, text. Match the established painterly series."
    },
    {
        "id": "B02-N11",
        "refs": ["Hedgehog.png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N11. Depict this focal action: Close view of Hedgehog's paws winding a mainspring with a brass winding key while Thumper watches intently and recognizes the need for an external source of power. Required visible characters/objects: Hedgehog's focused face and paws turning the winding key, coiled clockwork spring under tension, connected brass gears, Thumper's enlightened face nearby, warm oil lamp illumination. Exclude magical glows, floating symbols, text. Match the established painterly series."
    },
    {
        "id": "B02-N12",
        "refs": ["Thumper .png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N12. Depict this focal action: Thumper points to the hands and Roman numerals of a real clock face reading quarter to nine (8:45) while Hedgehog considers the question of time; unfinished customer orders surround them in the late workshop. Required visible characters/objects: Thumper pointing to antique clock dial showing 8:45, thoughtful Hedgehog in spectacles, workbench surrounded by clock cases and tools. Exclude Frumper, floating numbers, text outside dial. Match the established painterly series."
    },
    {
        "id": "B02-N13",
        "refs": ["Frumper .png", "Hedgehog.png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N13. Depict this focal action: Frumper folds his pale feathered wings and ducks through the clock-shop doorway to join Thumper and Hedgehog, then discusses the urgent wedding order. Required visible characters/objects: Frumper entering through wooden doorway with folded wings, Thumper and Hedgehog looking up from workbench, pocket-watch cases, evening workshop setting. All three characters working indoors. Exclude flying outside, maternal pose, text. Match the established painterly series."
    },
    {
        "id": "B02-N14",
        "refs": ["Frumper .png", "Hedgehog.png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B02-N14. Depict this focal action: At dawn, light enters the workshop as Frumper quietly adds one clock to a box and hands over an unexpectedly plentiful pile of finished timepieces; Thumper packs the finished watches while Hedgehog hurries among orders. Required visible characters/objects: Morning golden dawn through workshop window, Frumper, Thumper packing boxes, Hedgehog with inspection loupe, plentiful finished brass pocket watches in boxes. Exclude duplicate Frumpers, magical sparkles, text. Match the established painterly series."
    },

    # Book 3 (17 images)
    {
        "id": "B03-N01",
        "refs": ["Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N01. Depict this focal action: Sleepy Thumper in nightclothes has gone upstairs to bed after tea; downstairs in the cottage the forgotten kettle/pot continues boiling furiously over the hot woodstove. Required visible characters/objects: Coherent cottage cutaway or view through stairway showing Thumper asleep in bedroom upstairs in nightshirt, and boiling smoking pot unattended on iron woodstove downstairs. Exclude Proditor, volcano, explosion, text. Match the established painterly series."
    },
    {
        "id": "B03-N02",
        "refs": ["Thumper .png", "bunnies book 1 .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N02. Depict this focal action: Thumper escapes his burning cottage through a broken upstairs window into thorn bushes; on the ground he struggles away from a wasp nest toward fallen ashes as an ordinary rabbit approaches with news. Required visible characters/objects: Smoldering burning cottage with broken window, thorn bushes, disturbed wasp nest, Thumper on ground in soot-stained fur clutching injured leg, arriving rabbit messenger. Exclude repeated Thumpers, gore, text. Match the established painterly series."
    },
    {
        "id": "B03-N03",
        "refs": ["Thumper .png", "bunnies book 1 .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N03. Depict this focal action: In the cottage ashes, injured Thumper sits looking at his painful broken leg while three separate visiting rabbits offer unhelpful explanations with varying facial expressions. Required visible characters/objects: Thumper in soot and ashes clutching swollen hind leg, smoldering ruins, three visiting rabbits standing nearby (one critical, one philosophical, one superstitious). Exclude Hedgehog (not arrived yet), exposed bone, text. Match the established painterly series."
    },
    {
        "id": "B03-N04",
        "refs": ["Hedgehog.png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N04. Depict this focal action: Hedgehog drives the three unhelpful visitors away, breaks his wooden staff into a splint for Thumper's leg and tends his wounds beside the ashes. Required visible characters/objects: Hedgehog kneeling beside injured Thumper, carefully binding a wooden staff splint with cloth strips to Thumper's hind leg, broken staff pieces on ground, three rabbits retreating in background. Exclude gore, modern medical items, text. Match the established painterly series."
    },
    {
        "id": "B03-N05",
        "refs": ["Mole.png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N05. Depict this focal action: Mole tumbles out of the grassy hillside burrow and comes to rest beside splinted Thumper and the smoldering cottage; he begins explaining with good humor how one responds to a fall. Required visible characters/objects: Mole in work overalls dusting off dirt beside freshly opened burrow entrance on hillside, Thumper with splinted leg resting on grass, ruined cottage in background. Exclude block-shaped mole, diagrams, text. Match the established painterly series."
    },
    {
        "id": "B03-N06",
        "refs": ["Thumper .png", "Mole.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N06. Depict this focal action: Thumper draws a house blueprint on parchment while Mole energetically excavates the new foundation's trench on the chosen hillside. Required visible characters/objects: Thumper with splinted leg propped up, holding charcoal and drawing floor plans on wooden board, Mole digging foundation trench with shovel, dirt piles, hillside view. Exclude Squirrel (not arrived yet), text on blueprint. Match the established painterly series."
    },
    {
        "id": "B03-N07",
        "refs": ["Squirel .png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N07. Depict this focal action: Squirrel brings a picnic basket and strawberry wine and helps injured Thumper relax in the cool mountain stream; they rest by the grassy bank and notice a songbird in the tree above. Required visible characters/objects: Squirrel with bushy russet tail, Thumper dipping paws in clear stream, wooden picnic basket, stone bottle and ceramic cups, woodland songbird perched on branch overhead. Water flows naturally downstream. Exclude Frumper, modern picnic items, text. Match the established painterly series."
    },
    {
        "id": "B03-N08",
        "refs": ["Squirel .png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N08. Depict this focal action: Near the river picnic, Squirrel offers a crumb of scone to the small songbird; Thumper listens as the bird sings about narrow escapes. Required visible characters/objects: Squirrel gently holding out a piece of golden scone toward a charming woodland songbird, Thumper listening attentively on mossy riverbank, stream and picnic basket. Exclude written musical notes, flashback bubbles, text. Match the established painterly series."
    },
    {
        "id": "B03-N09",
        "refs": ["Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N09. Depict this focal action: Thumper returns to the building site to find his stone foundation, fresh-cut pine boards, bucket of nails, and a working watermill/sawmill. Frumper, visibly singed with patches of scorched fur from lightning, stacks boards beside the plans. Required visible characters/objects: Thumper hobbling up on splint, Frumper with large feathered wings and scorched/singed patches of fur carrying timber boards, freshly dug foundation, nail bucket, tree stump. Exclude gore, text. Match the established painterly series."
    },
    {
        "id": "B03-N10",
        "refs": ["Frumper Flying Sky.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N10. Depict this focal action: Illustrate Frumper's recounted adventure: the majestic winged rabbit rises through a stormy sky to intercept a jagged lightning bolt above a trapped fawn pinned under a fallen tree; the doe watches anxiously, rain extinguishes a forest fire, storm blowing from the east. Required visible characters/objects: Winged rabbit Frumper diving through dark storm clouds amidst brilliant lightning strike, mother doe and small fawn beneath fallen oak trunk, rain quenching embers. Dramatic hero moment. Exclude baby-like characters, text. Match the established painterly series."
    },
    {
        "id": "B03-N11",
        "refs": ["Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N11. Depict this focal action: Back at the construction site, Thumper asks his difficult question about suffering while singed Frumper opens his large paw to reveal a tiny live fly, then gently blows it into flight. Required visible characters/objects: Close view of singed Frumper's open paw with tiny black fly about to take flight, Thumper leaning close with curious earnest face, construction timbers and sawdust in background. Exclude magical halos, text. Match the established painterly series."
    },
    {
        "id": "B03-N12",
        "refs": ["Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N12. Depict this focal action: Frumper and Thumper continue their thoughtful conversation beside the partly built cottage, the released fly hovering small in the golden air. Required visible characters/objects: Wide, quiet view of the two adult friends seated on a timber beam, peaceful expressions, partly framed cottage walls, mountain backdrop, tiny fly in distance. Exclude literal mountain climbing equipment, text. Match the established painterly series."
    },
    {
        "id": "B03-N13",
        "refs": ["Frumper .png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N13. Depict this focal action: Frumper indicates the raw wood framing and unfinished house as Thumper listens; safe embers or ruined chimney in distance under natural sky. Required visible characters/objects: Frumper with feathered wings gesturing toward unfinished roof rafters and wall studs, Thumper listening intently with splinted leg, wood shavings, carpenter tools. Structure is visibly incomplete. Exclude cosmic diagrams, sun/moon collision, text. Match the established painterly series."
    },
    {
        "id": "B03-N14",
        "refs": ["Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N14. Depict this focal action: Closer conversation at the unfinished house: Thumper studies Frumper's lightning scars and scorched fur as they discuss love, freedom and an unfinished story. Required visible characters/objects: Intimate close view of Thumper looking with deep respect and empathy at the scorched lightning patterns across Frumper's shoulder and wing feathers, Frumper's warm noble expression, timber framing around them. Exclude literal curtains, text. Match the established painterly series."
    },
    {
        "id": "B03-N15",
        "refs": ["Frumper .png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N15. Depict this focal action: Frumper hands Thumper a wooden board and asks its length; Thumper guesses uncertainly while Frumper holds a plain notched wooden measuring rod to teach the concrete lesson. Required visible characters/objects: Frumper holding long notched measuring stick against pine plank, Thumper holding the other end thoughtfully with leg splint visible, timber stack, construction setting. Exclude written numbers, text. Match the established painterly series."
    },
    {
        "id": "B03-N16",
        "refs": ["Frumper .png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N16. Depict this focal action: While talking at the worksite, Frumper gently draws attention to Thumper's slightly burned paw and the remembered door-handle warning; Thumper holds a board, listening with realization. Required visible characters/objects: Frumper gently touching Thumper's wrapped/sooted paw, Thumper reflecting with board in lap, construction timbers, late afternoon woodland light. Exclude hellish flames, abstract souls, text. Match the established painterly series."
    },
    {
        "id": "B03-N17",
        "refs": ["Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B03-N17. Depict this focal action: Thumper and Frumper carry heavy cedar boards uphill and work together on the newly completed house; Thumper discovers his leg is fully healed as he bears weight comfortably and joyfully. Required visible characters/objects: Thumper standing firmly on both legs without splint carrying a board alongside Frumper, their handsome newly built cottage nearly finished on the green hill, golden sunset light. Exclude ruins, text. Match the established painterly series."
    },

    # Book 4 (13 images)
    {
        "id": "B04-N01",
        "refs": ["Hedgehog.png", "Mole.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N01. Depict this focal action: Hedgehog and Mole examine the seismometer's agitated swinging pendulum and drawn paper trace in the clock shop; Hedgehog consults a dusty leather record book while Mole prepares to inspect buried probes. Required visible characters/objects: Workshop table with mechanical brass seismometer, swinging pendulum recording zigzag line on paper drum, Hedgehog holding open dusty book, Mole with digging trowel and probe rods, alarm on their faces. Exclude standalone portraits, modern digital screens, text. Match the established painterly series."
    },
    {
        "id": "B04-N02",
        "refs": ["Mole.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N02. Depict this focal action: Mole falls from his familiar underground dirt tunnel through a collapsed ceiling into a much deeper volcanic cavern, then limps along the jagged black rock floor seeking an exit. Required visible characters/objects: Mole in overalls holding head after fall, high broken tunnel opening far above, dark volcanic basalt chamber, glowing red lava veins in cracks, sulfur steam vents, shadows of distant bats. Exclude Squirrel, modern gear, text. Match the established painterly series."
    },
    {
        "id": "B04-N03",
        "refs": ["Hedgehog.png", "Squirel .png", "Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N03. Depict this focal action: At the dark rocky volcano rim, Hedgehog has brought coiled rope and rescue gear; Squirrel arrives with Thumper and winged Frumper, and all four peer down grimly into the smoking pit. Required visible characters/objects: Volcano crater rim, coil of sturdy rope, Hedgehog, Squirrel, Thumper, Frumper with large wings, rising volcanic smoke, black raven flying away into stormy sky. Exclude Mole (trapped below), text. Match the established painterly series."
    },
    {
        "id": "B04-N04",
        "refs": ["Frumper .png", "Thumper .png", "Hedgehog.png", "Squirel .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N04. Depict this focal action: Inside the volcano cavern, Frumper holds a blazing torch leading Thumper, Hedgehog and Squirrel along Mole's sparse blood trail; glowing eyes of rats peer from rock crevices and hanging bats scatter before the firelight. Required visible characters/objects: Frumper holding high wooden torch, Thumper, Hedgehog, Squirrel following close together on narrow ledge, subtle drops of blood on stone, scattering bats, glowing rat eyes. Exclude gore, recovered Mole, text. Match the established painterly series."
    },
    {
        "id": "B04-N05",
        "refs": ["Thumper .png", "Frumper .png", "Hedgehog.png", "Squirel .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N05. Depict this focal action: Thumper reaches toward what appears to him as honey-buttered bread among feasting cave rabbits; in the same coherent scene, Frumper's torchlight exposes the illusion, revealing bare rock and starving rabbits gnawing on stones. Required visible characters/objects: Thumper reaching out mesmerized, Frumper holding torch whose yellow flame cuts through the glamour to show grey cavern and gaunt rabbits chewing pebbles, Squirrel and Hedgehog looking horrified behind. Exclude split screen panels, text. Match the established painterly series."
    },
    {
        "id": "B04-N06",
        "refs": ["Frumper .png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N06. Depict this focal action: Frumper hands Thumper real woodland berries; a jagged stone falls from Thumper's paw as he awakens from the illusion and recognizes the suffering rabbits chewing rocks on the barren floor. Required visible characters/objects: Close emotional view of Frumper pressing red berries into Thumper's paw, small stone falling to the cavern floor from Thumper's hand, torchlight revealing sad cave rabbits with swollen bellies. Exclude happy picnic, outdoor trees, text. Match the established painterly series."
    },
    {
        "id": "B04-N07",
        "refs": ["Squirel .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N07. Depict this focal action: As the group descends among volcanic stalagmites, exhausted Squirrel lags behind; a cunning bat leaning against the dark rock wall smoothly coaxes her toward what appears to be a gentle slide. Required visible characters/objects: Tired Squirrel pausing on steep path, a dark bat with clawed wings gesturing toward an apparently smooth deceptive slide, distant silhouettes of Thumper and Frumper ahead on safe trail. Exclude giant bat monster, rescue already done, text. Match the established painterly series."
    },
    {
        "id": "B04-N08",
        "refs": ["Frumper Flying Sky.png", "Squirel .png", "Thumper .png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N08. Depict this focal action: Frumper swoops in high with his blazing torch just as Squirrel halts at the brink; the torchlight strips away the false slide to expose a sheer fatal drop and freshly dug grave below; Thumper and Hedgehog help pull her back. Required visible characters/objects: Frumper flying with torch overhead, light illuminating jagged cliff edge and deep pit, terrified Squirrel recoiling into the arms of Thumper and Hedgehog, fleeing bat in shadows. Exclude surviving slide, text. Match the established painterly series."
    },
    {
        "id": "B04-N09",
        "refs": ["Proditor.png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N09. Depict this focal action: Beside the eastern air shaft, dog-sized Proditor with black fur, red eyes and foxlike head taunts Hedgehog with the brass seismometer probe, tapping it against stone; Hedgehog reaches angrily for it. Required visible characters/objects: Dog-sized black bat Proditor (matching canonical reference) sneering with glowing red eyes holding metal probe, angry Hedgehog confronting him, friends with torches behind in cavern shaft. Exclude giant mountain-sized monster, lava chasm, text. Match the established painterly series."
    },
    {
        "id": "B04-N10",
        "refs": ["Hedgehog.png", "Proditor.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N10. Depict this focal action: Subservient bats use an ornate throne, pulley hoist and cords on Hedgehog's hands, feet and head to suspend him like a puppet in the shaft while mockingly pretending to make him their commander; Proditor directs from below. Required visible characters/objects: Hedgehog suspended mid-air by puppet cords tied to limbs and head, bats pulling ropes through cavern rafters, smirking Proditor below, horrified friends watching. Exclude giant monarch, severed limbs, text. Match the established painterly series."
    },
    {
        "id": "B04-N11",
        "refs": ["Frumper Flying Sky.png", "Proditor.png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N11. Depict this focal action: Frumper breaks a heavy stalactite from the cavern ceiling to pin charging Proditor to the stone floor; bats flee, the puppet hoist cords go slack and Hedgehog frees his own limbs. Required visible characters/objects: Frumper landing from above having dropped stone stalactite pinning dog-sized black Proditor by his cloak/wings to floor, slackened cords falling away as Hedgehog stands free. Exclude swords, gore, giant demon, text. Match the established painterly series."
    },
    {
        "id": "B04-N12",
        "refs": ["Mole.png", "Thumper .png", "Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N12. Depict this focal action: The rescuers finally discover limping Mole in a side tunnel; Mole points to flaps of cloth covering his eyes and ears that shut out the deceivers; Thumper lifts Mole onto his back as Hedgehog spots red magma approaching. Required visible characters/objects: Reunited friends, Mole with cloth flaps over eyes smiling proudly, Thumper kneeling to carry Mole piggyback, Hedgehog pointing at glowing red lava seepage blocking path. Exclude gore, text. Match the established painterly series."
    },
    {
        "id": "B04-N13",
        "refs": ["Frumper Flying Sky.png", "Thumper .png", "Mole.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B04-N13. Depict this focal action: Frumper with outstretched wings rams his horns/shoulders into the giant boulder blocking the escape tunnel as fiery magma approaches; the boulder shatters into gravel, opening a path to daylight and ocean air for Thumper carrying Mole, Hedgehog and Squirrel. Required visible characters/objects: Dramatic impact of Frumper shattering stone boulder with white feathered wings flared, burst of light and rubble, Thumper carrying Mole through opening, cool sea breeze and daylight beyond. Exclude fish dinner, text. Match the established painterly series."
    },

    # Book 5 (11 images)
    {
        "id": "B05-N01",
        "refs": ["Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N01. Depict this focal action: Several sneaky weasels in ragged clothes actually RIDING ON a substantial wooden wagon down the forest road; a team of harnessed large rats pulls the wagon while a driver weasel cracks a whip; stolen grain and vegetables fill the wagon and the riders brandish beer flagons swaggering. Required visible characters/objects: Heavy wooden farm wagon, team of harnessed grey rats pulling wagon, multiple weasels riding on top with stolen crops and drinking flagons, whip cracking, dusty road. Exclude market stalls, beetle jars yet, text. Match the established painterly series."
    },
    {
        "id": "B05-N02",
        "refs": ["Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N02. Depict this focal action: At Hedgehog's clock shop, weasels trap him inside and nail wooden boards crisscross across his front door; Hedgehog glares furiously from behind the barred window; the rat-drawn wagon waits in the street. Required visible characters/objects: Sneering weasel hammering heavy timber plank across shop door, nail flying, Hedgehog's angry face behind shop window, waiting rat-drawn wagon in street. His clockmaker hammer remains safely inside. Exclude gore, text. Match the established painterly series."
    },
    {
        "id": "B05-N04",
        "refs": ["Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N04. Depict this focal action: At a riverside willow tree under a silvery CRESCENT moon, Sina, a magnificent long BLACK-scaled snake, addresses Thumper, summons a weasel and coils around the frightened weasel as beetle jars sit at the tree's roots; one crushed beetle lies on stone. Required visible characters/objects: Sina as an elegant long glossy BLACK snake coiling around a nervous weasel, Thumper watching from riverbank, jars with beetles, crescent moon reflecting in river. Exclude green snake, full moon, gruesome gore, text. Match the established painterly series."
    },
    {
        "id": "B05-N05",
        "refs": ["Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N05. Depict this focal action: Black Sina's powerful coils tighten firmly around the gasping weasel beside the riverside tree while Thumper urgently reasons with Sina, raising one paw in philosophical appeal. Required visible characters/objects: Closer composition of Sina's glossy black coils constricting the panicked weasel, Thumper pleading passionately with raised paw, crescent moon in sky, riverside reeds. Exclude already released weasel, ouroboros diagram, text. Match the established painterly series."
    },
    {
        "id": "B05-N07",
        "refs": ["Mole.png", "bunnies book 1 .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N07. Depict this focal action: The weasels stand atop their wooden wagon selling a miracle ELIXIR in glass flasks to an eager crowd of ordinary rabbits while Mole in overalls watches skeptically from the edge; one rabbit drinks and returns proudly in a fine stolen vest and ring. Required visible characters/objects: Weasel on wagon holding up amber elixir flask, crowd of rabbits buying bottles with coins, one rabbit showing off newly acquired waistcoat and ring, suspicious Mole watching from foreground. Exclude beetle jars as main merchandise, magic gold smoke, text. Match the established painterly series."
    },
    {
        "id": "B05-N08",
        "refs": ["Mole.png", "bunnies book 1 .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N08. Depict this focal action: Mole points out to the rabbits that they are wearing each other's stolen clothes and jewelry; fighting and chaos break out in the looted village street as rabbits quarrel over stolen goods; in the foreground Mole ushers sensible rabbits who refused the elixir into an underground burrow shelter. Required visible characters/objects: Mole ushering terrified innocent rabbits into wooden trapdoor underground shelter, background street brawl with rabbits fighting over garments and stolen loaves, looted market carts. Exclude Squirrel portrait, text. Match the established painterly series."
    },
    {
        "id": "B05-N09",
        "refs": ["Squirel .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N09. Depict this focal action: Squirrel leans out from a sturdy overhanging willow branch over the rushing river and rescues drowning young rabbits who have fake pasted-on paper fins; several wet rescued rabbits huddle shivering on the riverbank. Required visible characters/objects: Agile Squirrel hanging from tree bough grabbing a young rabbit from swirling river, crude artificial fins peeling off in the water, wet shivering rabbits huddled safely on grassy shore, water flowing swiftly downstream. Exclude sales wagon, text. Match the established painterly series."
    },
    {
        "id": "B05-N10",
        "refs": ["Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N10. Depict this focal action: Hedgehog, having broken free and wielding his workshop hammer, stands boldly atop the weasels' wagon confronting the swindlers; broken boards from his shop door behind him, a rabbit clutching coins and another with pasted fins look on as Hedgehog exposes the scam. Required visible characters/objects: Hedgehog standing resolute on wagon holding his distinctive wooden-handled hammer, surprised weasels backing away, crowd of rabbits listening, broken door planks in distance. Exclude snake alone, portrait, text. Match the established painterly series."
    },
    {
        "id": "B05-N11",
        "refs": ["Hedgehog.png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N11. Depict this focal action: Hedgehog smashes the beetles' large glass display box with his hammer, sending shards and beetles flying, then curls into a tight spiny ball as attacking weasels fall off the wagon; black Sina rises up from the nearby river in support. Required visible characters/objects: Dramatic instant of hammer smashing glass box with beetles scattering, Hedgehog curled in defensive spiny ball, weasels stumbling off wagon, head of black snake Sina emerging from water. Exclude two simultaneous hedgehogs, text. Match the established painterly series."
    },
    {
        "id": "B05-N12",
        "refs": ["Squirel .png", "Thumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N12. Depict this focal action: In the rain-soaked, devastated village after the riot, Squirrel reunites shivering young rabbits with weeping parents; Thumper carries an empty woven food basket solemnly toward Miller's distant farm gate through the puddles. Required visible characters/objects: Somber muddy village scene, Squirrel comforting rabbit families, Thumper carrying empty basket walking toward distant white farmhouse fence in misty rain, empty food stalls. Exclude banquet, text. Match the established painterly series."
    },
    {
        "id": "B05-N13",
        "refs": ["Thumper .png", "Frumper .png"],
        "prompt": "Use the attached canonical character and style references. Create ONE distinct portrait illustration for B05-N13. Depict this focal action: Thumper stands alone at the farmhouse porch as the heavy wooden door swings wide to reveal Frumper Miller himself, majestic with large pale feathered wings and gentle smile, welcoming Thumper into a warm hall filled with an abundant banquet table and golden light. Required visible characters/objects: Thumper with empty basket at stone threshold, adult winged Frumper in warm linen tunic with magnificent wings opening door, glowing banquet hall with tables overflowing with fresh bread, fruits and harvest, threefold divine light emanating warmly. Exclude other guests (not arrived yet), Trinity diagram, multiple Frumpers, text. Match the established painterly series."
    }
]

print(f"Total specs to generate: {len(SPECS)}")

def generate_spec(spec):
    out_path = os.path.join(OUTPUT_DIR, f"{spec['id']}.png")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"Skipping {spec['id']}: already exists ({os.path.getsize(out_path)} bytes).")
        return True

    print(f"\nGenerating {spec['id']}...")
    content_parts = [{'type': 'text', 'text': spec['prompt']}]
    for r in spec['refs']:
        if r in cached_refs:
            content_parts.append({
                'type': 'image_url',
                'image_url': {'url': f"data:image/png;base64,{cached_refs[r]}"}
            })

    req_data = {
        'model': 'google/gemini-3.1-flash-image',
        'messages': [{'role': 'user', 'content': content_parts}]
    }

    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        },
        data=json.dumps(req_data).encode()
    )

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                res = json.loads(resp.read().decode())
                images = res['choices'][0]['message'].get('images', [])
                if images:
                    url = images[0].get('image_url', {}).get('url', '')
                    if url.startswith('data:image'):
                        _, b64 = url.split(',', 1)
                        raw = base64.b64decode(b64)
                        with open(out_path, 'wb') as f:
                            f.write(raw)
                        print(f"SUCCESS: Saved {out_path} ({len(raw)} bytes)")
                        return True
                print(f"Attempt {attempt+1}: No image in response: {res}")
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(3)

    return False

if __name__ == '__main__':
    successes = 0
    failures = []
    for spec in SPECS:
        ok = generate_spec(spec)
        if ok:
            successes += 1
        else:
            failures.append(spec['id'])
        # Small delay between API calls to avoid rate limits
        time.sleep(1.5)

    print(f"\nFINISHED: {successes}/{len(SPECS)} images generated successfully.")
    if failures:
        print(f"Failed spreads: {failures}")
    else:
        print("ALL 53 IMAGES GENERATED SUCCESSFULLY!")
