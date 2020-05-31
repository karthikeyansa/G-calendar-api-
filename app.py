from calendar_api.helper import create,events,delete,update

while True:
    ch = int(input('Enter a choice : 1-> see events, 2-> create, 3->delete: 4->update' ))
    if ch == 1:
        events()
    elif ch == 2:
        create()
    elif ch == 3:
        events()
        id = input('Enter Event Id: ')
        delete(id)
    elif ch == 4:
        events()
        id = input('Enter Event Id: ')
        update(id)
    else:
        break
