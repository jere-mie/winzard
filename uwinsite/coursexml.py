import bs4, sys, json, re

def scrape_course_options(xml, course_code='NULL0001'):
    xml = xml.replace('\u00a0', ' ') # non-breaking space

    soup = bs4.BeautifulSoup(xml, 'lxml')

    # course_code = re.findall(r'([A-Z]{4} [0-9]{4})', str(soup))
    field_classes = ['cmpnt_class_nbr', 'dates', 'days_times', 'room', 'instructor', 'seats']
    field_objects = [ soup.select(f'td.{c.upper()}') for c in field_classes ]
    
    options = []
    for i in range(len(field_objects[0])):
        try:
            for j in range(len(field_objects)):
                field_objects[j][i] = field_objects[j][i].text.strip().replace('\u00a0', ' ').replace('\r', '\n').replace('\n\n', '\n')

            dates = field_objects[1][i]
            times = field_objects[2][i].split('\n')
            room = field_objects[3][i].split('\n')
            instructor = field_objects[4][i].split('\n')
            seats = field_objects[5][i].split('\n')
            code = course_code
            days = []
            hours = []
            if times[0] != 'Not Applicable':
                days = times[0].split(' ')
                hours = times[1].split(' to ')
            opt = {
                'dates': dates.split('\u00a0- '),
                'code': course_code,
                'lab_exists': False,
                'times': {
                    'lecture': {
                        'days': days,
                        'hours': hours,
                    }
                },
                'room': {
                    'lecture': room[0]
                },
                'instructor': {
                    'lecture': instructor[0]
                },
                'seats': {
                    'lecture': seats[0]
                }
            }
            if len(times) == 4:
                opt['times']['lab'] = {
                    'days': times[2].split(' '),
                    'hours': times[3].split(' to '),
                }
                opt['room']['lab'] = room[1]
                opt['instructor']['lab'] = instructor[1]
                opt['seats']['lab'] = seats[1]
                opt['lab_exists'] = True

            options += [opt]
        except IndexError:
            print(f'failed to parse {i} of {course}')
            pass
    return options

if __name__ == '__main__':
    file_path = sys.argv[1] if 1 in sys.argv else 'math1730'
    file_text = open(f'html/{file_path}.html').read()
    opt = scrape_course_options(file_text)
    print(json.dumps(opt, indent=4))