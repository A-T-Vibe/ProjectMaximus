import random

PROMPT_CATEGORIES = {
    "fruit_cutting": [
        "slow motion macro shot of a sharp knife slicing through a translucent red pomegranate, seeds glistening, cinematic lighting, satisfying ASMR",
        "close-up of a blade cutting through a ripe kiwi fruit revealing bright green flesh, slow motion, soft natural light",
        "slow motion knife slicing through a perfectly ripe mango, juice droplets in the air, warm studio lighting",
        "macro shot of slicing a translucent grape revealing the inner pulp, ultra slow motion, satisfying",
        "sharp knife cutting through a dragon fruit revealing vibrant pink flesh with black seeds, slow motion macro",
        "satisfying slow motion cut through a star fruit, perfect slices revealing star pattern, cinematic",
        "close up of slicing a blood orange revealing deep red interior, slow motion, gorgeous lighting",
        "macro shot of knife slicing through a lychee, translucent white flesh revealed, slow motion ASMR",
        "slow motion cut through a perfectly ripe papaya revealing orange flesh and black seeds, studio light",
        "ultra close-up of slicing a fig, revealing pink honeycomb interior, slow motion cinematic shot",
    ],
    "kinetic_sand": [
        "satisfying kinetic sand being sliced cleanly by a knife, smooth cut, soft purple sand, close up ASMR",
        "hands pressing into bright blue kinetic sand, slow motion, satisfying texture close up",
        "kinetic sand being poured and shaped into a perfect mound, pastel pink, ASMR close up",
        "metal comb raking through yellow kinetic sand creating perfect lines, slow motion macro shot",
        "kinetic sand being cut into cubes and stacked, satisfying crumbling texture, close up ASMR",
        "roller smoothing kinetic sand flat, leaving perfect surface, teal coloured sand, macro ASMR",
        "knife cutting through layered colourful kinetic sand revealing striped interior, slow motion",
        "hands moulding and smoothing kinetic sand into a perfect sphere, golden yellow, close up",
        "kinetic sand falling through fingers in slow motion, sparkling, warm studio lighting ASMR",
        "satisfying kinetic sand being pressed through a mould, perfect shape revealed, close up cinematic",
    ],
    "soap_cutting": [
        "close up of a knife slicing through a hard glycerin soap bar, satisfying crunch texture ASMR",
        "peeling thin curls from a hard soap bar, perfect spirals, macro close up ASMR",
        "cutting a layered colourful soap block into perfect cubes, satisfying texture, close up",
        "knife pressing into a glossy soap bar creating satisfying cracks and chips, ASMR macro",
        "soap being carved with a spatula, smooth shavings falling, close up studio lighting",
        "slicing through a transparent glycerin soap bar with glitter inside, slow motion macro ASMR",
        "cutting honeycomb textured soap revealing perfect cells inside, sharp knife, close up ASMR",
        "hard soap being scraped into fine shavings with a metal tool, satisfying texture close up",
        "knife pushing through a soft melt-and-pour soap block, clean satisfying cut, macro ASMR",
        "peeling the dry outer layer from a soap bar to reveal smooth interior, close up satisfying ASMR",
    ],
    "pressure_washing": [
        "pressure washer cleaning a dirty stone path, revealing bright surface underneath, satisfying",
        "close up of pressure washing dirt off a weathered wooden deck, satisfying transformation ASMR",
        "pressure washer cleaning a moss-covered garden statue, satisfying reveal, close up",
        "cleaning dirty garden tiles with a pressure washer, satisfying lines of clean surface revealed",
        "pressure washing a grimy driveway, revealing pristine concrete underneath, satisfying before and after",
        "close up of pressure washer removing mud from a rubber boot, satisfying cleaning ASMR",
        "pressure washing a green algae covered wall revealing clean brick, satisfying transformation",
        "pressure washer cleaning a dirty outdoor table, satisfying close up of dirt being removed",
    ],
    "liquid_pouring": [
        "slow motion pour of glossy white resin onto a dark surface, ripples and bubbles, macro cinematic",
        "paint pouring in slow motion creating fluid art, multiple colours swirling, macro satisfying",
        "honey drizzling in slow motion off a spoon, golden light catching the stream, macro ASMR",
        "slow motion pour of coloured water into a clear container, beautiful colour diffusion",
        "melted chocolate being poured over a smooth surface, slow motion close up, warm lighting",
        "thick caramel sauce pouring in slow motion, glossy and smooth, warm studio lighting macro",
        "resin art pour with glitter swirling in slow motion, metallic colours, satisfying macro",
        "slow motion milk being poured into black coffee, beautiful swirling tendrils, macro cinematic",
        "silver mercury-like liquid metal flowing in slow motion, satisfying ripples, macro close up",
    ],
    "organising": [
        "hands perfectly arranging colourful stationery items into neat rows, satisfying organisation ASMR",
        "sorting and organising a collection of smooth coloured stones by size, satisfying close up",
        "arranging perfectly matched containers and jars on a shelf, symmetrical, satisfying organisation",
        "sorting colourful Lego bricks by colour into perfect piles, close up satisfying ASMR",
        "hands arranging a colour-gradient of books on a shelf from lightest to darkest, satisfying",
        "organising a spice rack alphabetically with matching jars, satisfying transformation close up",
        "sorting coins into perfect stacks by denomination, satisfying metallic clicks, macro ASMR",
        "neatly folding and stacking matching towels into a perfect row, satisfying close up ASMR",
    ],
    "slime": [
        "glossy clear slime being stretched and folded in slow motion, satisfying texture ASMR close up",
        "butter slime being pressed and smoothed into a flat sheet, pastel yellow, macro ASMR",
        "crunchy slime being squeezed, satisfying crackling sounds texture, close up ASMR",
        "cloud slime being poked and stretched, fluffy white texture, satisfying slow motion macro",
        "jiggly slime being dropped onto a flat surface, satisfying wobble, slow motion macro",
        "holographic glitter slime being stretched, sparkles catching studio light, satisfying ASMR",
        "magnetic slime attracted to a magnet, slow motion macro, satisfying movement close up",
        "slime being twisted and braided, satisfying stretch, pastel pink, close up ASMR",
        "thick floam slime being pressed revealing bumpy texture, slow motion satisfying macro ASMR",
        "slime being poured into a container creating perfect ripples, rainbow coloured, satisfying",
    ],
}

HASHTAGS = {
    "fruit_cutting": "#satisfying #asmr #oddlysatisfying #fruitcutting #slowmotion #relaxing #satisfyingvideo",
    "kinetic_sand": "#kineticsand #satisfying #asmr #oddlysatisfying #sand #relaxing #satisfyingvideo",
    "soap_cutting": "#soapcutting #asmr #satisfying #oddlysatisfying #soap #relaxing #satisfyingvideo",
    "pressure_washing": "#pressurewashing #satisfying #cleaning #oddlysatisfying #asmr #relaxing",
    "liquid_pouring": "#satisfying #pouring #asmr #oddlysatisfying #resin #relaxing #satisfyingvideo",
    "organising": "#organising #satisfying #asmr #oddlysatisfying #organized #relaxing",
    "slime": "#slime #asmr #satisfying #oddlysatisfying #slimevideo #relaxing #satisfyingvideo",
}

AUDIO_MAP = {
    "fruit_cutting": "knife_cutting.mp3",
    "kinetic_sand": "sand_texture.mp3",
    "soap_cutting": "soap_crunch.mp3",
    "pressure_washing": "water_spray.mp3",
    "liquid_pouring": "liquid_pour.mp3",
    "organising": "soft_ambient.mp3",
    "slime": "slime_texture.mp3",
}


def get_random_prompt():
    category = random.choice(list(PROMPT_CATEGORIES.keys()))
    prompt = random.choice(PROMPT_CATEGORIES[category])
    return {
        "prompt": prompt,
        "category": category,
        "hashtags": HASHTAGS[category],
        "audio_file": AUDIO_MAP[category],
    }


def get_prompt_by_category(category):
    if category not in PROMPT_CATEGORIES:
        raise ValueError(f"Unknown category: {category}")
    prompt = random.choice(PROMPT_CATEGORIES[category])
    return {
        "prompt": prompt,
        "category": category,
        "hashtags": HASHTAGS[category],
        "audio_file": AUDIO_MAP[category],
    }


def get_all_categories():
    return list(PROMPT_CATEGORIES.keys())
