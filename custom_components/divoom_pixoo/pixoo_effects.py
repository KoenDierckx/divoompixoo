"""Dictionaries of Divoom Pixoo effect names to internal id's.

These were reverse engineered from the different Divoom Pixoo dials, clocks, channels ...
We keep them here to do lookups for the home assistant light effect

These are actually managed by divoom using its online system, so they might need to be updated from time to time.

You can browse these using the Divoom app, or the API (partially):
http://docin.divoom-gz.com/web/#/5/27
http://docin.divoom-gz.com/web/#/5/28
http://docin.divoom-gz.com/web/#/5/31
"""

from bidict import frozenbidict

CHANNEL_DICT: frozenbidict[str, int] = frozenbidict(
    {
        "Faces": 0,
        "Cloud": 1,
        "Visualizer": 2,
        "Custom": 3,
        "Black": 4,
    }
)

CHANNEL_INDEX_CLOUD_DICT: frozenbidict[str, int] = frozenbidict(
    {
        "Recommend gallery": 0,
        "Creation album": 1,
        "Favourite": 2,
        "Subscribe artist": 3,
    }
)

CHANNEL_INDEX_VISUALIZER_DICT: frozenbidict[str, int] = frozenbidict(
    {
        "Rainbow line": 0,
        "Worm": 1,
        "Green bottom": 2,
        "Blue bottom": 3,
        "Geen rain": 4,
        "EQ": 5,
        "Green mid": 6,
        "Rainbow bottom": 7,
        "Rainbow rain": 8,
        "Blue mirror": 9,
        "Duck": 10,
        "Dog on stage": 11,
    }
)

CHANNEL_INDEX_CUSTOM_DICT: frozenbidict[str, int] = frozenbidict(
    {
        "Custom 1": 0,
        "Custom 2": 1,
        "Custom 3": 2,
    }
)

CHANNEL_INDEX_FACES_DICT: frozenbidict[str, int] = frozenbidict(
    {
        "Custom - Clock Collections": 3,
        "Custom - DIY Analog Clock": 283,
        "Custom - DIY Digit Pic Clock": 285,
        "Custom - DIY Digital Clock": 284,
        "Custom - DIY Net Data Clock": 310,
        "financial - Bitcoin ": 64,
        "financial - Cyber Currency": 206,
        "financial - Exchange Rate": 240,
        "financial - Stock - 2": 12,
        "financial - Stock - Detail": 196,
        "Game - Fortnite": 208,
        "Game - League of Legends": 90,
        "Game - Overwatch": 92,
        "Game - PUBG": 696,
        "HOLIDAYS - Anniversary Green": 76,
        "HOLIDAYS - Anniversary Pink": 74,
        "HOLIDAYS - Christmas calendar": 214,
        "HOLIDAYS - Christmas clock1": 126,
        "HOLIDAYS - Christmas clock2": 216,
        "HOLIDAYS - Christmas girl room clock": 218,
        "HOLIDAYS - Happy New Year": 238,
        "HOLIDAYS - Shiba Inu Christmas": 212,
        "Normal - Automation clock": 128,
        "Normal - bun one clcok": 138,
        "Normal - bun two clcok": 140,
        "Normal - Classic Digital Clock": 10,
        "Normal - Digital Frame": 180,
        "Normal - Girl's room clock": 176,
        "Normal - iced lemonade clock": 144,
        "Normal - Lucky Casino Clock": 178,
        "Normal - Mondrian Pixel Art": 108,
        "Normal - Oriental zodiac": 124,
        "Normal - pixel display clock": 142,
        "Normal - Plush tiger and rainbow": 230,
        "Normal - Retrclcok": 174,
        "Normal - Shiba Inu | Tiger": 232,
        "Normal - sleeping kitty clock": 132,
        "Normal - wrist watch": 122,
        "Pixel Art - Cloud Channel": 57,
        "Pixel Art - Custom 1": 61,
        "Pixel Art - Custom 2": 63,
        "Pixel Art - Custom3": 65,
        "Pixel Art - Visualizer": 59,
        "Plan - Plan1": 201,
        "Plan - Plan2": 189,
        "Plan - Plan3": 191,
        "Plan - Plan4": 193,
        "Plan - Plan5": 195,
        "Smart hardware - Fitbit clock": 202,
        "Smart hardware - HUAWEI health": 4,
        "Smart hardware - PC Monitor": 625,
        "Smart hardware - Pulsoid Dial": 846,
        "Social - Bilibili Account": 46,
        "Social - Bilibili Concept Account": 52,
        "Social - Bilibili Concept Video": 54,
        "Social - Bilibili Stream": 116,
        "Social - Bilibili Video": 114,
        "Social - Bilibili-works": 48,
        "Social - Divoom": 160,
        "Social - DouYu Stream": 58,
        "Social - Facebook Photo": 407,
        "Social - Facebook Video": 26,
        "Social - Influencer ": 102,
        "Social - New Twitch Account": 248,
        "Social - New Twitch Stream": 252,
        "Social - Pinterest": 665,
        "Social - reddit": 664,
        "Social - TikTok User": 628,
        "Social - TikTok Video": 222,
        "Social - Tumblr": 666,
        "Social - Twitch Live List": 258,
        "Social - X- Account": 100,
        "Social - X- Post": 24,
        "Social - YouTube Account List": 55,
        "Social - YouTube Account": 38,
        "Social - YouTube Video List": 53,
        "Social - YouTube Video": 40,
        "Sport - F1\u00ae Clock": 298,
        "Sport - MLB": 5,
        "Sport - NBA\u00ae Live Clock": 304,
        "Sport - NBA\u00ae Matches Clock": 292,
        "Sport - NBA\u00ae Teams Clock": 296,
        "Sport - NHL": 602,
        "Sport - URFA\u00ae League Clock": 302,
        "TOOLS -  Message Board(English only)": 104,
        "TOOLS - Amazon music": 188,
        "TOOLS - Custom RSS": 246,
        "TOOLS - Pink Message Board": 98,
        "TOOLS - QR code": 282,
        "TOOLS - RSS Clock": 234,
        "TOOLS - Spotify Clock ": 186,
        "TOOLS - Tidal Time": 677,
        "TOOLS - Vintage Message Board": 224,
        "TOOLS - World Clocks": 72,
        "Weather - Big Time": 152,
        "Weather - Chameleon clock": 136,
        "Weather - pink design clock": 170,
        "Weather - Shiba Inu clock": 168,
        "Weather - Valoub Clock": 146,
        "Weather - Weather ONE": 182,
        "Weather - Weather TWO": 172,
    }
)
