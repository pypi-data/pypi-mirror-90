# django-userextensions
A user extension module for django. This includes some basic user profile settings and 
tracking of a users favorites and recently visited urls within the project. 

| | |
|--------------|------|
| Author       | David Slusser |
| Description  | A user extension module for django. This includes some basic user profile settings and tracking of a users favorites and recently visited urls within the project. |
| Requirements | `Python 3.x`<br>`Django 2.2.x` |


# Documentation
Full documentation can be found on http://django-userextensions.readthedocs.org. 
Documentation source files are available in the docs folder.


# Installation 
- pip install django-userextensions
- add userextensions to your INSTALLED_APPS
- to include recents tracking, add 'userextensions.middleware.UserRecentsMiddleware' to your middleware
- to include views to manage favorites and recents, in the project-level urls.py file add the following to your urls.py:
    from userextensions.urls import *
    path('', include('userextensions.urls'), ), 
- run migrations python ./manage.py migrate userextensions


# License
django-userextensions is licensed under the MIT license (see the LICENSE file for details).


# Features

### User Preferences
Extends the built-in User model to add theme, recents_count, page_refresh_time, and start_page fields.

### User-Defined Start Page
Users can define a specific page to be routed to after login. This is set in the UserPreference model.
To enable, add 'userextensions' to the INSTALLED_APPS and set the following in the settings.py file: 

    LOGIN_REDIRECT_URL = '/userextensions/user_login_redirect'

### User Favorites
Each user can add/delete favorites, which stores specified URL. Views are provided to add the current url as a favorite, list user favorites, and delete favorites.

### Recently viewed URLs
Each user can have recently viewed urls stored as a recent Views are provided to list and remove recents. Recents are added via middleware. 
To enable, add 'userextensions' to the INSTALLED_APPS and 'userextensions.middleware.UserRecentsMiddleware' to the MIDDLEWARE in the settings.py file. 
By default, some fixed URLs and URLs with specific prefixes are excluded from being stored in recents. These can be modified by setting the SKIP_URL_PREFIX_LIST and SKIP_FIXED_URL_LIST parameters in the settings.py file.

    INSTALLED_APPS = [
        ...
        'userextensions',
    ]

    MIDDLEWARE = [
        ...
        'userextensions.middleware.UserRecentsMiddleware',
    ]

    SKIP_URL_PREFIX_LIST = ['/admin/', '/__debug__/']
    SKIP_FIXED_URL_LIST = ['/', '/login/', '/logout/', ]


# Provided Views
Several views, with applicable templates, are provided for use. To use these, add the following to your project-level urls.py:

    from userextensions.urls import *
    
    urlpatterns = [
        ...
        path('', include('userextensions.urls'), ),
    ]


| View | Usage |
|--------------|------|
| list favorites | userextensions:list_favorites |
| list recents  | userextensions:list_recents |
| delete favorite | userextensions:delete_favorite |
| delete recent | userextensions:delete_recent |
| add favorite | userextensions:add_favorite |
| set start page | userextensions:set_start_page |
| refresh API token | userextensions:refresh_api_token |
| detail user | userextensions:detail_user |


# APIs
