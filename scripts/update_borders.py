"""
Update the 5 border SVGs for the 5 Thumper books with subtle storybook fauna & thematic motifs:
- Book 1: Storybook white rabbit silhouette nestled in the vine rinceaux + golden dewdrops
- Book 2: Clockwork gear escapement wheels & Victorian scroll medallions
- Book 3: Perched woodland songbirds on upper briar rose branches + floral tendrils
- Book 4: Gothic architectural vault rose tracery & radiating illuminated bezants
- Book 5: Imperial golden wheat sprigs & radiant star crown on Renaissance palmettes
"""

import os
import re

# -------------------------------------------------------------
# 1. BOOK 1 BORDER: Storybook Rabbit & Golden Dewdrops
# -------------------------------------------------------------
def enhance_border_1():
    filepath = 'assets/borders/border-book-1.svg'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the bunny in <defs>
    bunny_def = '''
  <!-- Storybook Young Rabbit Silhouette nestled in lower foliage -->
  <g id="storybook-bunny">
    <!-- Soft shadow ground -->
    <ellipse cx="0" cy="1" rx="13" ry="3.5" fill="#a87a3a" opacity="0.25"/>
    <!-- Hindquarters / Body -->
    <path d="M -7,0 C -11,-2 -13,-8 -10,-14 C -7,-19 0,-18 5,-13 C 8,-10 9,-4 7,0 Z" fill="#fffdfa" stroke="#7a5d28" stroke-width="0.8"/>
    <!-- Hind leg flank -->
    <path d="M -5,0 C -8,-3 -6,-9 -2,-9 C 2,-9 3,-3 1,0 Z" fill="#f5eee0" stroke="#7a5d28" stroke-width="0.5"/>
    <!-- Fluffy round tail -->
    <circle cx="-10" cy="-6" r="2.8" fill="#ffffff" stroke="#7a5d28" stroke-width="0.5"/>
    <!-- Head & Muzzle -->
    <path d="M 4,-12 C 4,-16 7,-20 12,-19 C 15,-18 16,-14 14,-11 C 12,-8 7,-8 4,-12 Z" fill="#fffdfa" stroke="#7a5d28" stroke-width="0.8"/>
    <!-- Cute snout tip -->
    <circle cx="14.2" cy="-14" r="0.9" fill="#c98a8a"/>
    <!-- Alert eye with glint -->
    <circle cx="10.2" cy="-15.5" r="1.1" fill="#3d2817"/>
    <circle cx="10.5" cy="-15.8" r="0.4" fill="#ffffff"/>
    <!-- Front paws folded gracefully -->
    <path d="M 3,-3 C 5,-2 7,0 6,0 L 2,0 Z" fill="#f5eee0" stroke="#7a5d28" stroke-width="0.5"/>
    <!-- Upright Rabbit Ears -->
    <path d="M 6,-18 C 5,-23 4,-30 8,-31 C 11,-30 9,-23 8,-17 Z" fill="#fffdfa" stroke="#7a5d28" stroke-width="0.7"/>
    <path d="M 6.8,-19 C 6,-23 5.5,-29 7.8,-30 C 9.2,-29 8.2,-23 7.8,-18 Z" fill="#ebd0d0" opacity="0.75"/>
    <path d="M 3,-17 C 1,-22 0,-28 3,-29 C 5,-28 5,-22 5,-16 Z" fill="#f3ede2" stroke="#7a5d28" stroke-width="0.6"/>
  </g>
'''

    content = content.replace('</defs>', bunny_def + '\n</defs>')

    # Place bunnies and dewdrops before closing </svg>
    bunny_instances = '''
  <!-- Book 1 Storybook Bunnies Nestled in Lower Vine Foliage -->
  <use href="#storybook-bunny" x="43" y="912"/>
  <use href="#storybook-bunny" transform="translate(757, 912) scale(-1, 1)"/>

  <!-- Golden Dewdrop Sparkles along Side Vines -->
  <circle cx="42" cy="275" r="2.2" fill="#fff8db" stroke="#a87a3a" stroke-width="0.6"/>
  <circle cx="758" cy="275" r="2.2" fill="#fff8db" stroke="#a87a3a" stroke-width="0.6"/>
  <circle cx="42" cy="725" r="2.2" fill="#fff8db" stroke="#a87a3a" stroke-width="0.6"/>
  <circle cx="758" cy="725" r="2.2" fill="#fff8db" stroke="#a87a3a" stroke-width="0.6"/>
</svg>'''

    content = content.replace('</svg>', bunny_instances)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Enhanced border-book-1.svg successfully.')


# -------------------------------------------------------------
# 2. BOOK 2 BORDER: Clockwork Escapement & Victorian Medallions
# -------------------------------------------------------------
def enhance_border_2():
    filepath = 'assets/borders/border-book-2.svg'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Enhanced fleuron-corner with miniature 8-tooth brass escapement wheel
    escapement_defs = '''
      <!-- Ornate Victorian Clockwork Escapement Medallion -->
      <g id="escapement-medallion">
        <!-- Victorian flanking scroll tendrils -->
        <path d="M -9,0 C -16,-6 -24,-4 -22,4 C -20,10 -14,8 -11,2" fill="none" stroke="url(#gold-bright)" stroke-width="0.9"/>
        <path d="M 9,0 C 16,-6 24,-4 22,4 C 20,10 14,8 11,2" fill="none" stroke="url(#gold-bright)" stroke-width="0.9"/>
        <circle cx="-22" cy="4" r="1.4" fill="url(#gold-bright)"/>
        <circle cx="22" cy="4" r="1.4" fill="url(#gold-bright)"/>
        <!-- Outer Gear Ring (12 Ratchet Teeth) -->
        <circle cx="0" cy="0" r="8.5" fill="none" stroke="url(#gold-bright)" stroke-width="1.1"/>
        <circle cx="0" cy="0" r="6.2" fill="none" stroke="url(#gold-bright)" stroke-width="0.5"/>
        <!-- 12 Clockwork Escapement Teeth -->
        <path d="M 0,-8.5 L 1.2,-10.8 L 0,-10.5 M 4.3,-7.4 L 6.2,-9.2 L 4.8,-8.4 M 7.4,-4.3 L 9.8,-5.2 L 8.6,-4.2 M 8.5,0 L 10.8,1.2 L 10.5,0 M 7.4,4.3 L 9.2,6.2 L 8.4,4.8 M 4.3,7.4 L 5.2,9.8 L 4.2,8.6 M 0,8.5 L -1.2,10.8 L 0,10.5 M -4.3,7.4 L -6.2,9.2 L -4.8,8.4 M -7.4,4.3 L -9.8,5.2 L -8.6,4.2 M -8.5,0 L -10.8,-1.2 L -10.5,-0 M -7.4,-4.3 L -9.2,-6.2 L -8.4,-4.8 M -4.3,-7.4 L -5.2,-9.8 L -4.2,-8.6" stroke="url(#gold-bright)" stroke-width="0.85" fill="none"/>
        <!-- 4 Slender Wheel Spokes -->
        <line x1="-6.2" y1="0" x2="6.2" y2="0" stroke="url(#gold-bright)" stroke-width="0.75"/>
        <line x1="0" y1="-6.2" x2="0" y2="6.2" stroke="url(#gold-bright)" stroke-width="0.75"/>
        <!-- Center Jewel Hub -->
        <circle cx="0" cy="0" r="2.8" fill="url(#gold-bright)" stroke="#543b10" stroke-width="0.4"/>
        <circle cx="0" cy="0" r="1.1" fill="#fff0bd"/>
        <circle cx="0" cy="0" r="0.5" fill="#422e0a"/>
      </g>
'''

    # Add corner escapement wheel inside fleuron-corner
    old_fleuron = '''        <circle cx="28" cy="28" r="3.5" fill="url(#gold-bright)"/>
        <path d="M 20,20 Q 35,35 55,25 Q 35,35 25,55" fill="none" stroke="url(#gold-bright)" stroke-width="1.2"/>
      </g>'''

    new_fleuron = '''        <circle cx="28" cy="28" r="3.5" fill="url(#gold-bright)"/>
        <path d="M 20,20 Q 35,35 55,25 Q 35,35 25,55" fill="none" stroke="url(#gold-bright)" stroke-width="1.2"/>
        <!-- Corner Escapement Wheel Accents -->
        <circle cx="34" cy="34" r="5.5" fill="none" stroke="url(#gold-bright)" stroke-width="0.6"/>
        <circle cx="34" cy="34" r="1.8" fill="url(#gold-bright)"/>
        <path d="M 34,28.5 L 35,27 M 39.5,34 L 41,35 M 34,39.5 L 33,41 M 28.5,34 L 27,33" stroke="url(#gold-bright)" stroke-width="0.7"/>
      </g>'''

    content = content.replace('</defs>', escapement_defs + '\n    </defs>')
    content = content.replace(old_fleuron, new_fleuron)

    # Replace center rosettes at (400, 30), (400, 970), (30, 500), (770, 500) with escapement medallions
    content = content.replace('<use href="#edge-rosette" x="400" y="30"/>', '<use href="#escapement-medallion" x="400" y="30"/>')
    content = content.replace('<use href="#edge-rosette" x="400" y="970"/>', '<use href="#escapement-medallion" x="400" y="970" transform="scale(1, -1)"/>')
    content = content.replace('<use href="#edge-rosette" x="30" y="500"/>', '<use href="#escapement-medallion" x="30" y="500" transform="rotate(90 30 500)"/>')
    content = content.replace('<use href="#edge-rosette" x="770" y="500"/>', '<use href="#escapement-medallion" x="770" y="500" transform="rotate(-90 770 500)"/>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Enhanced border-book-2.svg successfully.')


# -------------------------------------------------------------
# 3. BOOK 3 BORDER: Perched Woodland Songbirds & Wild Briars
# -------------------------------------------------------------
def enhance_border_3():
    filepath = 'assets/borders/border-book-3.svg'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Perched songbird def
    songbird_def = '''
      <!-- Perched Woodland Songbird Silhouette (Inspired by Pater Noster / Morgan MS) -->
      <g id="perched-songbird">
        <!-- Feet clasping the golden tendril branch -->
        <path d="M -1,4 L 1,7 M 2,4 L 3,7" stroke="#704d16" stroke-width="1" stroke-linecap="round"/>
        <!-- Long Tail feathers sweeping downwards -->
        <path d="M -7,4 L -18,14 C -19,16 -17,17 -15,16 L -5,7 Z" fill="#223a19" stroke="#13240d" stroke-width="0.5"/>
        <!-- Main Body & Plumed Back -->
        <path d="M 8,-6 C 9,-3 8,2 3,5 C -2,7 -7,5 -9,3 C -9,0 -7,-3 -4,-6 C 0,-9 6,-8 8,-6 Z" fill="#35542b" stroke="#1a2e15" stroke-width="0.6"/>
        <!-- Folded Wing with fine gold feather edging -->
        <path d="M 0,-4 C -4,-2 -7,1 -9,4 C -6,3 -3,1 0,-2 Z" fill="#203617" stroke="url(#gold-leaf-5)" stroke-width="0.5"/>
        <!-- Golden-ochre breast plumage -->
        <path d="M 7,-6 C 8,-2 6,2 2,4 C 5,2 7,-1 7,-5 Z" fill="#c99130" opacity="0.85"/>
        <!-- Head & Crown -->
        <path d="M 5,-7 C 6,-11 9,-11 11,-8 C 11,-6 8,-5 5,-7 Z" fill="#35542b" stroke="#1a2e15" stroke-width="0.5"/>
        <!-- Slender Beak -->
        <path d="M 11,-8 L 15,-7.5 L 11,-6.5 Z" fill="#d4af37" stroke="#704d16" stroke-width="0.4"/>
        <!-- Alert Eye with light glint -->
        <circle cx="8.5" cy="-8" r="0.9" fill="#111111"/>
        <circle cx="8.7" cy="-8.2" r="0.3" fill="#ffffff"/>
      </g>
'''

    content = content.replace('</defs>', songbird_def + '\n    </defs>')

    # Place songbirds perched on upper branch tendrils (right side up!)
    songbird_instances = '''
  <!-- Book 3 Woodland Songbirds Perched on Upper Tendril Branches -->
  <use href="#perched-songbird" x="127" y="27"/>
  <use href="#perched-songbird" transform="translate(673, 27) scale(-1, 1)"/>
</svg>'''

    content = content.replace('</svg>', songbird_instances)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Enhanced border-book-3.svg successfully.')


# -------------------------------------------------------------
# 4. BOOK 4 BORDER: Gothic Cathedral Rose Tracery & Illuminated Bezants
# -------------------------------------------------------------
def enhance_border_4():
    filepath = 'assets/borders/border-book-4.svg'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Enhanced gothic-quadrilobe with cathedral rose tracery
    old_quadrilobe = '''      <!-- Corner Gothic Quadrilobe -->
      <g id="gothic-quadrilobe">
        <rect x="20" y="20" width="36" height="36" rx="4" fill="#8c2e2e" stroke="url(#gold-leaf)" stroke-width="1.8"/>
        <!-- 4 intersecting lobes -->
        <circle cx="38" cy="26" r="6" fill="url(#gold-leaf)"/>
        <circle cx="38" cy="50" r="6" fill="url(#gold-leaf)"/>
        <circle cx="26" cy="38" r="6" fill="url(#gold-leaf)"/>
        <circle cx="50" cy="38" r="6" fill="url(#gold-leaf)"/>
        <circle cx="38" cy="38" r="5" fill="#fcf9f2" stroke="#8c2e2e" stroke-width="0.8"/>
      </g>'''

    new_quadrilobe = '''      <!-- Corner Gothic Quadrilobe with Cathedral Rose Tracery -->
      <g id="gothic-quadrilobe">
        <rect x="20" y="20" width="36" height="36" rx="4" fill="#8c2e2e" stroke="url(#gold-leaf)" stroke-width="1.8"/>
        <!-- 4 intersecting lobes with gothic trefoil cusps -->
        <circle cx="38" cy="26" r="6" fill="url(#gold-leaf)"/>
        <circle cx="38" cy="26" r="3.2" fill="none" stroke="#8c2e2e" stroke-width="0.6"/>
        <circle cx="38" cy="50" r="6" fill="url(#gold-leaf)"/>
        <circle cx="38" cy="50" r="3.2" fill="none" stroke="#8c2e2e" stroke-width="0.6"/>
        <circle cx="26" cy="38" r="6" fill="url(#gold-leaf)"/>
        <circle cx="26" cy="38" r="3.2" fill="none" stroke="#8c2e2e" stroke-width="0.6"/>
        <circle cx="50" cy="38" r="6" fill="url(#gold-leaf)"/>
        <circle cx="50" cy="38" r="3.2" fill="none" stroke="#8c2e2e" stroke-width="0.6"/>
        <!-- Center Roundel with Gothic 4-leaf Rose Window -->
        <circle cx="38" cy="38" r="5.5" fill="#fdfbf7" stroke="#8c2e2e" stroke-width="0.8"/>
        <path d="M 38,34 C 36.5,36 36.5,40 38,42 C 39.5,40 39.5,36 38,34 Z" fill="#8c2e2e"/>
        <path d="M 34,38 C 36,36.5 40,36.5 42,38 C 40,39.5 36,39.5 34,38 Z" fill="#8c2e2e"/>
        <circle cx="38" cy="38" r="1.4" fill="url(#gold-leaf)"/>
      </g>'''

    # Enhanced rinceau-branch with illuminated radiating pen flourishes & sparks
    old_rinceau = '''        <!-- Golden Bezant (sparkling gold disc with radiating pen hair) -->
        <circle cx="10" cy="-22" r="3.2" fill="url(#gold-leaf)" stroke="#8c681b" stroke-width="0.5"/>
        <path d="M 6,-22 L 4,-24 M 14,-22 L 16,-20 M 10,-26 L 10,-28" stroke="#241e17" stroke-width="0.5"/>'''

    new_rinceau = '''        <!-- Golden Bezant with authentic Gothic manuscript illuminated radiating sparks -->
        <circle cx="10" cy="-22" r="3.2" fill="url(#gold-leaf)" stroke="#8c681b" stroke-width="0.5"/>
        <path d="M 6,-22 L 3,-23 M 14,-22 L 17,-21 M 10,-26 L 10,-29 M 10,-18 L 10,-15 M 13,-25 L 16,-28 M 7,-19 L 4,-16" stroke="#8c681b" stroke-width="0.45"/>
        <circle cx="16" cy="-28" r="0.6" fill="url(#gold-leaf)"/>
        <circle cx="4" cy="-16" r="0.6" fill="url(#gold-leaf)"/>'''

    content = content.replace(old_quadrilobe, new_quadrilobe)
    content = content.replace(old_rinceau, new_rinceau)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Enhanced border-book-4.svg successfully.')


# -------------------------------------------------------------
# 5. BOOK 5 BORDER: Imperial Wheat Sprigs & Radiant Star Finials
# -------------------------------------------------------------
def enhance_border_5():
    filepath = 'assets/borders/border-book-5.svg'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Enhanced center-palmette with golden wheat sprigs & star crown finial
    old_palmette = '''      <!-- Center Crown / Palmette -->
      <g id="center-palmette">
        <path d="M 0,-10 C -8,-2 -15,4 0,10 C 15,4 8,-2 0,-10 Z" fill="#425c38" stroke="url(#sepia-gold)" stroke-width="0.8"/>
        <circle cx="0" cy="0" r="3.5" fill="url(#sepia-gold)"/>
        <path d="M -25,0 Q -10,-8 0,0 Q 10,-8 25,0" fill="none" stroke="url(#sepia-gold)" stroke-width="1.2"/>
      </g>'''

    new_palmette = '''      <!-- Center Crown / Palmette with Imperial Wheat & Radiant Star -->
      <g id="center-palmette">
        <!-- Golden Wheat Sprigs of Harvest & Wisdom arching outward -->
        <g stroke="url(#sepia-gold)" fill="url(#sepia-gold)">
          <path d="M -4,-5 C -10,-10 -18,-11 -25,-10" fill="none" stroke-width="0.7"/>
          <ellipse cx="-13" cy="-9" rx="2.2" ry="1.1" transform="rotate(25 -13 -9)"/>
          <ellipse cx="-18" cy="-10.5" rx="2.2" ry="1.1" transform="rotate(15 -18 -10.5)"/>
          <ellipse cx="-23" cy="-10.5" rx="1.8" ry="0.9" transform="rotate(5 -23 -10.5)"/>
          
          <path d="M 4,-5 C 10,-10 18,-11 25,-10" fill="none" stroke-width="0.7"/>
          <ellipse cx="13" cy="-9" rx="2.2" ry="1.1" transform="rotate(-25 13 -9)"/>
          <ellipse cx="18" cy="-10.5" rx="2.2" ry="1.1" transform="rotate(-15 18 -10.5)"/>
          <ellipse cx="23" cy="-10.5" rx="1.8" ry="0.9" transform="rotate(-5 23 -10.5)"/>
        </g>
        <!-- Radiant Crown Finial -->
        <polygon points="0,-16 1.8,-11.5 5.5,-11.5 2.5,-9 3.5,-5 0,-7.5 -3.5,-5 -2.5,-9 -5.5,-11.5 -1.8,-11.5" fill="url(#sepia-gold)"/>
        <!-- Central Palmette Leaf -->
        <path d="M 0,-10 C -8,-2 -15,4 0,10 C 15,4 8,-2 0,-10 Z" fill="#385430" stroke="url(#sepia-gold)" stroke-width="0.8"/>
        <circle cx="0" cy="0" r="3.5" fill="url(#sepia-gold)"/>
        <path d="M -25,0 Q -10,-8 0,0 Q 10,-8 25,0" fill="none" stroke="url(#sepia-gold)" stroke-width="1.2"/>
      </g>'''

    # Enhanced corner-renaissance with laurel berry accents
    old_corner = '''        <!-- Central Corner Laurel Leaf -->
        <path d="M 38,38 C 45,30 54,32 50,42 C 42,50 30,45 38,38 Z" fill="#425c38" stroke="url(#sepia-gold)" stroke-width="0.6"/>
        <circle cx="38" cy="38" r="3" fill="url(#sepia-gold)"/>
      </g>'''

    new_corner = '''        <!-- Central Corner Laurel Leaf & Classical Berries -->
        <path d="M 38,38 C 45,30 54,32 50,42 C 42,50 30,45 38,38 Z" fill="#385430" stroke="url(#sepia-gold)" stroke-width="0.6"/>
        <circle cx="38" cy="38" r="3" fill="url(#sepia-gold)"/>
        <circle cx="32" cy="46" r="1.6" fill="url(#sepia-gold)"/>
        <circle cx="46" cy="32" r="1.6" fill="url(#sepia-gold)"/>
      </g>'''

    content = content.replace(old_palmette, new_palmette)
    content = content.replace(old_corner, new_corner)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Enhanced border-book-5.svg successfully.')


if __name__ == '__main__':
    enhance_border_1()
    enhance_border_2()
    enhance_border_3()
    enhance_border_4()
    enhance_border_5()
    print('All 5 border SVGs enhanced successfully!')
