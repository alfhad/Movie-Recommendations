import requests


def reverse(lst):
    return [ele for ele in reversed(lst)]


def get_movies_from_tastedive(word):
    baseurl = "https://tastedive.com/api/similar"
    key = '407692-Coder-20PE202B'
    param_dict = {'q': word, 'type': 'movies', 'limit': 5, 'k': key}
    resp = requests.get(baseurl, params=param_dict)
    return resp.json()


def extract_movie_titles(mov_d):
    info, info1 = [], []
    names, name1 = [], []
    for item in mov_d:
        info = mov_d[item]['Results']
    for cas in info:
        names.append(cas['Name'])
    if not names:
        for item in mov_d:
            info1 = mov_d[item]['Info']
        var = info1[0]['Name']
        name1.append(var)
        return name1
    else:
        return names


def get_related_titles(lst):
    dip = {}
    new_lst = []
    res_lst = []
    for item in lst:
        rel = get_movies_from_tastedive(item)
        mov_title = extract_movie_titles(rel)
        if len(mov_title) == 1:
            res_lst.append(mov_title)
        else:
            for t in mov_title:
                dip[t] = dip.get(t, 0) + 1
            for keys in dip:
                new_lst.append(keys)
    return res_lst, new_lst


def get_movie_data(word):
    baseurl = "http://www.omdbapi.com/"
    param_di = {'apikey': '8cec1c0d', 't': word, 'r': 'json'}
    resp = requests.get(baseurl, params=param_di)
    return resp.json()


def get_movie_rating(mov_inf):
    info = []
    d = {}
    for _ in mov_inf:
        info = mov_inf['Ratings']
    for cas in info:
        if cas['Source'] == 'Rotten Tomatoes':
            d['Value'] = cas['Value'].strip('%')
            return int(d['Value'])
    return 0


def get_sorted_recommendations(mov_lst):
    movie_recom = {}
    lst = []
    no = []
    nop, mov = get_related_titles(mov_lst)
    if nop:
        for _ in nop:
            no.append(nop)
    if mov:
        for movie in mov:
            val = get_movie_data(movie)
            pro = get_movie_rating(val)
            movie_recom[movie] = pro
        movie_recom = (sorted(movie_recom.items(), key=lambda mr: (mr[1], mr[0])))
        for val in movie_recom:
            lst.append(val[0])
    return no, reverse(lst)


print("*********************************************MOVIE RECOMMENDATION**********************************************")

movies = []
inp = '1'
while inp != '0':
    if inp == '1':
        movies.append(input('Enter a movie: '))
    print('1: Enter another movie\n0: No more movies')
    inp = input("Input = ")
    while inp != '1' and inp != '0':
        print("Type Error !!\n Try again")
        inp = input("Input = ")
print()
not_found, recommended = get_sorted_recommendations(movies)

if not_found:
    vo = not_found[0]
    print("No similar movies for :")
    for i in range(len(vo)):
        ch = vo[i][0]
        print('    {}: {}'.format(i+1, ch))
if recommended:
    print('Recommended movies are : ')
    for i in range(0, len(recommended)):
        print('     {}: {}'.format(i+1, recommended[i]))
print()
input('Press Enter to Exit !!')
