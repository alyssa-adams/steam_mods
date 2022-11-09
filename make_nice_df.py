# Filter out null mods, ones without titles and descriptions
# Use the description to make keywords

import pandas as pd
import json, os, re


# put all the mod data into one giant pandas df
# each row is a single mod

game_labels = {333640: 'Caves of Qud', 292030: 'The Witcher 3: Wild Hunt', 268500: 'XCOM 2', 230230: 'Divinity: Original Sin (Classic)', 223830: 'Xenonauts', 493340: 'Planet Coaster', 435150: 'Divinity: Original Sin 2', 379720: 'DOOM', 377160: 'Fallout 4', 373420: 'Divinity: Original Sin Enhanced Edition', 883710: 'Resident Evil 2', 881100: 'Noita', 220: 'Half-Life 2', 220200: 'Kerbal Space Program', 289070: "Sid Meier's Civilization VI", 1091500: 'Cyberpunk 2077', 70: 'Half-Life', 255710: 'Cities: Skylines', 211820: 'Starbound', 203770: 'Crusader Kings II', 200510: 'XCOM: Enemy Unknown', 72850: 'The Elder Scrolls V: Skyrim', 47890: 'The Sims™ 3', 22300: 'Fallout 3', 22330: 'The Elder Scrolls IV: Oblivion ', 22380: 'Fallout: New Vegas', 8930: "Sid Meier's Civilization V", 4000: "Garry's Mod", 2280: 'DOOM (1993)', 1245620: 'ELDEN RING', 281990: 'Stellaris', 246620: 'Plague Inc: Evolved', 1158310: 'Crusader Kings III', 244850: 'Space Engineers', 703080: 'Planet Zoo', 1224290: "Horizon's Gate", 294100: 'RimWorld', 105600: 'Terraria', 1222670: 'The Sims™ 4', 322330: "Don't Starve Together", 271590: 'Grand Theft Auto V', 413150: 'Stardew Valley'}
game_ids = os.listdir(os.path.join("data"))
game_ids = list(filter(lambda x: re.search(r'[\d]+', x), game_ids))

# loop over games, add rows of mods
mods_dict = {}
for game_id in game_ids:

    print(game_id)

    files = os.listdir(os.path.join("data", str(game_id)))
    # don't include the chart file for this
    files = list(filter(lambda x: '.json' in x, files))

    for file in files:
        with open(os.path.join("data", str(game_id), file), 'r') as f:

            data = json.load(f)
            data = data['response']['publishedfiledetails']

            for mod in data:

                # filter out empty results
                if 'app_name' not in list(mod.keys()):
                    continue
                if mod['title'] == '' and mod['file_description'] == '':
                    continue

                # annoying
                if 'tags' not in list(mod.keys()):
                    mod['tags'] = None

                mods_dict[mod['publishedfileid']] = [
                    mod['app_name'],
                    mod['title'],
                    mod['file_description'],
                    mod['tags'],
                    mod['creator'],
                    mod['creator_appid'],
                    mod['consumer_appid'],
                    mod['time_created'],
                    mod['time_updated'],
                    mod['subscriptions'],
                    mod['favorited'],
                    mod['followers'],
                    mod['lifetime_subscriptions'],
                    mod['lifetime_favorited'],
                    mod['lifetime_followers'],
                    mod['views']
                ]

mods_df = pd.DataFrame.from_dict(mods_dict, orient='index', columns=['app_name', 'title', 'file_description', 'tags', 'creator', 'creator_appid', 'consumer_appid', 'time_created', 'time_updated', 'subscriptions', 'favorited', 'followers', 'lifetime_subscriptions', 'lifetime_favorited', 'lifetime_followers', 'views'])

# save to pickle
mods_df.to_pickle('mods_df.p')
