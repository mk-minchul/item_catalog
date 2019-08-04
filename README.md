
# Item Catalog Website

This is a restaurant menu webapp which can create edit and delete restaurants and menus.

### Prerequisites

* Python 2.7
* Vagrant

### Run
1. start the environment
```
$ vagrant up 
$ vagrant ssh
```

2. Create db and populate it with data

```
$ python database_setup.py
$ Python populate_db.py
```

3. Launch
```
$ python app.py
```
4. view at http://localhost:5000

### API
#### Returns JSON of all restaurants
```
/restaurants/JSON
```
#### Returns JSON of specific menu item
```
/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON
```
#### Returns JSON of menu
```
/restaurants/<int:restaurant_id>/menu/JSON
```