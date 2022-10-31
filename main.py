import requests
import json, time, os


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # make data directory
    main_data_folder = os.path.join('data')
    if not os.path.exists(main_data_folder):
        os.makedirs(main_data_folder)

    # load in API key from separate key.json file
    # {"key":"YOUR_KEY_HERE"}
    key = json.load(open('key.json'))
    key = key["key"]

    # this is the max number of results per page allowed
    n_mods_per_page = 100

    # list game ids to loop through
    # (Manually get game popularity over time on Steam DB: https://steamdb.info/app/72850/graphs/)
    game_ids = [72850, 377160, 294100, 413150, 281990, 230230, 435150, 373420, 1224290, 255710, 203770, 1158310, 881100,
                211820, 105600, 246620, 333640, 200510, 268500, 223830, 8930, 289070, 271590, 220200, 322330, 244850,
                22330, 22300, 22380, 379720, 2280, 70, 220, 883710, 4000, 292030, 1091500, 1245620, 47890, 1222670,
                703080, 493340]

    # track number of api calls, can't do more than 100k in 24 hours
    api_calls = 0

    # loop over games
    for game_id in game_ids:

        print("Game ID: " + str(game_id))

        # make data directory for this game
        data_folder = os.path.join('data', str(game_id))
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # this is how you start from the first page with cursor
        cursor = '*'

        # for this game, get total number of mods
        api_call = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=' + key + '&cursor=' + cursor \
                   + '&numperpage=' + str(n_mods_per_page) + '&appid=' + str(game_id) + '&return_playtime_stats=10000000'
        api_calls += 1
        r = requests.get(api_call)
        time.sleep(1)
        data = r.json()
        total_mods = data['response']['total']

        # use total nuber of mods to see how pages we need to loop through
        n_pages = int(total_mods / n_mods_per_page) + (total_mods % n_mods_per_page > 0)

        # loop over the cursor pages
        for page in range(1, n_pages+1):

            # if it doesn't load, keep trying until it does else it will give 0 results
            got_result = False
            while got_result == False:

                api_call = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=' + key + '&cursor=' + cursor \
                           + '&numperpage=' + str(n_mods_per_page) + '&appid=' + str(game_id) + '&return_playtime_stats=10000000'

                # the thing to try, if this throws an exception then it means the result didn't load
                try:

                    api_calls += 1
                    r = requests.get(api_call)
                    data = r.json()

                    # get next cursor value if it did load
                    cursor = data['response']['next_cursor']

                    # need to replace any '+' values, else it will return an error
                    cursor = cursor.replace('+', '%2b')

                    # save page data
                    file = "page_" + str(page) + ".json"
                    with open(os.path.join(data_folder, file), "w") as outfile:
                        json.dump(data, outfile)
                    print(str(page) + '/' + str(n_pages))
                    got_result = True

                except:
                    got_result = False

            # make sure to not go over the api call limit:
            if api_calls > 100000:
                print("Continue in 24 hours")
                print("Game: " + str(game_id) + ", Page: " + str(page))
                quit()

    print('HUZZAH!')
