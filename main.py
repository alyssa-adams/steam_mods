# This is a sample Python script.

# A83D7C58F30EA64909BAE418EBBCE771
# Use this query to get all the different file ids in the workshop: https://steamapi.xpaw.me/#IPublishedFileService/QueryFiles
# https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=A83D7C58F30EA64909BAE418EBBCE771&page=1&numperpage=100
# Then loop through the IDs to get the file details: https://steamapi.xpaw.me/#IPublishedFileService/GetDetails
# https://api.steampowered.com/IPublishedFileService/GetDetails/v1/?key=A83D7C58F30EA64909BAE418EBBCE771&publishedfileids%5B0%5D=2872975601

# Estimated time to collect data: 14,150,465 files
# 100,000 requests per day
# 2 days to get the file IDs (100 IDs per query)
# Another 2 days to get the file details if we did 100 IDs per query

# Or, can just use this query
# https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=A83D7C58F30EA64909BAE418EBBCE771&page=1&numperpage=100&search_text=mod&return_playtime_stats=1000000
# This filters all files by files that have the word "mod" in the description or title
# total files: 734,777

import requests
import json, time, re


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # make directory
    measures = os.path.join('data', 'measures')
    if not os.path.exists(measures):
        os.makedirs(measures)

    n_mods_per_page = 100

    # for this game, get total number of mods
    game_id = 72850
    api_call = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=A83D7C58F30EA64909BAE418EBBCE771&cursor=' + cursor + '&numperpage=' + str(
        n_mods_per_page) + '&appid=' + str(game_id) + '&return_playtime_stats=10000000'
    r = requests.get(api_call)
    data = r.json()
    total_mods =

    n_mods_per_page = 100
    n_pages = int(total_mods / n_mods_per_page) + (total_mods % n_mods_per_page > 0)
    cursor = '*'

    for page in range(4758, n_pages):

        got_result = False

        while got_result == False:

            #api_call = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v2/?key=A83D7C58F30EA64909BAE418EBBCE771&page=' + str(page) + '&numperpage=100&search_text=mod&return_playtime_stats=1000000'
            #api_call = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=A83D7C58F30EA64909BAE418EBBCE771&cursor=' + cursor + '&numperpage=100&search_text=mod'
            api_call = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/?key=A83D7C58F30EA64909BAE418EBBCE771&cursor=' + cursor + '&numperpage=' + str(n_mods_per_page) + '&appid=72850&return_playtime_stats=10000000'

            r = requests.get(api_call)
            #time.sleep(1)
            data = r.json()

            try:
                cursor = data['response']['next_cursor']
                cursor = cursor.replace('+', '%2b')
                got_result = True
            except:
                got_result = False

        with open("mod_json_data/" + str(page) + ".json", "w") as outfile:
            json.dump(data, outfile)

        print(page)
        print(cursor)
