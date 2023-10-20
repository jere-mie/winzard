import coursexml, searchxml, fetchdata
import os, sys, json

search_term, session_id = None, None

for a in sys.argv[1:]:
    if 'search=' == a[:7]:
        search_term = a[7:]

session_id = os.environ.get('SESSION_ID')
if session_id is None:
    print('supply a session id by exporting `SESSION_ID`')
    exit()

if search_term is None:
    print('supply a search term with the parameter `search=$SEARCH_TERM`')
    exit()

print(f'searching for "{search_term}"')
fetched_search = fetchdata.fetch_course_search(search_term, session_id)
open(f'html/{search_term}-search.html', 'w+').write(fetched_search)

search_results = searchxml.scrape_search_list(fetched_search)
print(f'{len(search_results)} results found.')

for i in search_results:
    print(f'using {i["title"]}, {i["course_id"]}')
    fetched_course = fetchdata.fetch_course_id(i['course_id'], i['dbcsprd'], session_id)
    course_options = coursexml.scrape_course_options(fetched_course, i['course_id'])

    print(f'{len(course_options)} options found.')

    dump = json.dumps(course_options, indent=4)
    open(f'data/courses/winter2024/{i["title"].replace(" ","")}.json', 'w+').write(dump)

    # for i in course_options:
    #     days = i["times"]["lecture"]["days"]
    #     hours = i["times"]["lecture"]["hours"]
    #     instructor = i["instructor"]["lecture"]
    #     print(f'{" ".join(days)}, {" ".join(hours)}, {instructor}')