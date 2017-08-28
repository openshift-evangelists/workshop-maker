from eventbrite import Eventbrite
import yaml
import datetime
import pytz

with open('input.yml', 'r') as file:
    data = yaml.load(file)

output = open('result.csv', 'w')

output.write("Date,Time,Link,Status,Presenter,Capacity,Password\n")
eventbrite = Eventbrite(data['token'])

user = eventbrite.get_user()

for e in data['events']:
    for d in e['when']:
        tz = pytz.timezone(e['tz'])
        date = tz.localize(datetime.datetime.strptime(d, '%b-%d %Y %I%p'))
        name = 'OpenShift Workshop (%s)(%s)' % (date.strftime('%b-%d;%I%p'), e['who'])

        event = eventbrite.get_user_events(user['id'], **{'name_filter': name})
        if len(event['events']) > 0:
            print('Event %s already exists' % name)
            event = event['events'][0]
        else:
            event = eventbrite.post_event({
                'event.name': {
                    'html': name
                },
                'event.start': {
                    'utc': date.astimezone(pytz.utc).replace(minute=0).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'timezone': tz.zone,
                },
                'event.end': {
                    'utc': (date + datetime.timedelta(hours=3)).astimezone(pytz.utc).replace(minute=0).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'timezone': tz.zone,
                },
                'event.organizer_id': data['organizer'],
                'event.currency': 'USD',
                'event.online_event': True,
                'event.listed': False,
                'event.password': data['password'],
                'event.capacity': data['capacity'],
            })
            print('Event %s created' % name)

        tickets = eventbrite.get_event_ticket_classes(event['id'])

        if len(tickets['ticket_classes']) == 0:
            tickets = eventbrite.post_event_ticket_class(event['id'], {
                'ticket_class.name': 'Free',
                'ticket_class.free': True,
                'ticket_class.minimum_quantity': 1,
                'ticket_class.maximum_quantity': 1,
                'ticket_class.quantity_total': data['capacity'],
            })
            print('Tickets created')
        else:
            tickets = tickets['ticket_classes'][0]
            print('Tickets exist')

        result = eventbrite.publish_event(event['id'])

        if ('published' in result and result['published']) or ('error' in result and result['error'] == 'ALREADY_PUBLISHED_OR_DELETED'):
            print('Published')
            output.write("%s,%s,%s,%s,%s,%s,%s\n" % (date.strftime('%b %d'),date.strftime('%I:%M %p %Z'),event['url'],'',e['who'],data['capacity'],data['password']))
        else:
            print(result)
