=============================
Django Bloxby
=============================

.. image:: https://badge.fury.io/py/django-bloxby.svg
    :target: https://badge.fury.io/py/django-bloxby

A django application for bridging bloxby and your django software supporting User creation, package creation and autologin
and also publishing sites from the bloxby application to your django application.


Quickstart
----------

Install Django Bloxby::

    pip install django-bloxby

Add it to your `INSTALLED_APPS`:

App name you add to INSTALLED_APPS used to be :code:`bloxby` you add to :code:`INSTALLED_APPS` in versions :code:`0.0.19` downwards, but
it has changed in version :code:`0.0.20` since the ftp part has been integrated into the library.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bloxby',

        # optional, if you are running the FTP server
        'bloxby.ftp'
        ...
    )


The following settings are available to you (in :code:`settings.py`):

.. code-block:: python

    BLOXBY_BUILDER = {
        'url': 'http://clouddigitalmarketing.com',
        'custom_api_url': 'http://159.65.79.47:3000', # optional, needed only if the node api is deployed
        'username': 'hello@linkfusions.com',
        'password': 'accountpassword',
        'package_prefix': 'LF-', # optional, but you may want to provide this to ensure uniqueness
        'account_email_prefix': 'LF', # optional, but you may want to provide this to ensure uniqueness
        'public_key': 'Yourpublickeyasstatedinthebloxbyapplicationsettings',
        'autologin_hash': 'Yourautologinhash',
        'default_package_id': 1
    }



- :code:`url`: This is the base url of the server that hosts the bloxby builder.
- :code:`custom_api_url`: This is the base URL of the node server that interfaces the bloxby database to provide data not provided by the default bloxby builder API.
- :code:`username`: Admin user email
- :code:`password`: Password of the admin user specified
- :code:`package_prefix`: This could be empty, but it is used to distinguish packages in case of your builder being accessed by more than one application.
- :code:`account_prefix`: Same explanation goes here, in case you have some users shared across your applications.
- :code:`public_key`: API key you generated and saved in the admin settings on your bloxby dashboard.
- :code:`autologin_hash`: The auto login hash which you as well got from the dashboard.
- :code:`default_package_id`: Default package to add for new users being created if none is provided at the point of calling the create function.


Then run migrate command. :code:`python manage.py migrate`.


Usage (Accessing Default Bloxby APIs)
-------------------------------------

Once the settings are configured you could run requests to access the default endpoints provided by bloxby here this way:

.. code-block:: python

    from djbloxby.bloxby.functions import Bloxby
    b = Bloxby()
    # Retrieve User with id of 4
    b.Users.retrieve(4)
    # Delete User with id of 4
    b.Users.delete(4)
    # Update user with id of 4
    b.Users.update(4, last_name='New')
    # Create new user
    b.Users.create(first_name='John', last_name='Felix', email='jfelix@localhost.com', password=generate_password(), type='User', package_id=5)

    # Working with Packages
    b.Packages.create(name='New Free Package', sites_number=10,
                      disk_space=100,
                      export_site=True,
                      ftp_publish=True, price=4.00, currency='USD')

    b.Packages.delete(3)
    # Delete packages with id of 3

    # .....
    # Could also do .update, .retrieve, .delete with this.


More information on integrating with the default APIs of :code:`Users` and :code:`Packages` can be `found here <https://support.bloxby.com/knowledge-base/restful-api-end-point-api-users/>`_ and
`here <https://support.bloxby.com/knowledge-base/restful-api-end-point-api-packages/>`_ respectively.


Template
--------

You could autologin user in html by getting the autologin URL for the current user, this process also creates a new account on the
the bloxby instance for the current logged in if they do not already have one.

.. code-block:: html

    {% load bloxby %}

    <h1>Click <a href="{% user_builder_dashboard %}">here</a> to login to your builder dashboard.


Setup Extra API server
----------------------

This extra server helps to provide extra functionalities not provided by the default API service such as export and pulling of templates.
In the repo, there is a folder named :code:`node_api` that contains Node.js server code that accesses the database of the Bloxby server directly.
To configure this, open the file at :code:`node_api/index.js` and set the parameters of the database connection pool function like this:

.. code-block:: javascript

    let pool = mysql.createPool({
        host: 'database host',
        user: 'root',
        password: 'password',
        database: 'bloxby'
    });


Additionally, you need the credentials of an admin user from the builder site passed in the :code:`signIn` function called at line 91 of the :code:`index.js`
file.
To setup this node server on a fresh server *(could as well run in the same server the bloxby instance runs in)*, you just need to clone this
repo :code:`git clone https://github.com/damey2011/django-bloxby.git` and then navigate into the :code:`node_api` folder.

Next, run :code:`./setup_node_api.sh`. This installs all the dependencies needed to run the node_js application including npm and the Node V8 runtime itself.

Then, install the project dependencies by running :code:`npm install`. Once all these are done, you can start the server by running
:code:`./start_node_api.sh`. All together, after configuring the :code:`index.js` with the correct database details. The lines of code below would setup and get the
node server running on port 3000.

.. code-block:: bash

    $ git clone https://github.com/damey2011/django-bloxby.git
    $ cd node_api
    $ ./setup_node_api.sh
    $ npm install
    $ ./start_node_api.sh
    $ sudo ufw allow 3000

The last line is to enable port 3000 which the server runs on accessible from outside the server.


End points provided by the node server
######################################

- :code:`/<autologin_token>/templates`: This endpoint would return the templates of the user whose autologin token is passed.
- :code:`/<site_id>/export/`: This returns a zip file of the exported site whose site_id is passed.

Both endpoints take only :code:`GET` requests. You don't need to consume these endpoints raw by the way, just for documentation purpose.
The next section provides information on how to consume these endpoints within the library in an abstract manner.


Django User Support
###################

You are able to tie the bloxby instance users to a Django user through a model object provided in this
repo, :code:`bloxby.models.UserBridge`.

The :code:`UserBridge` object provides a couple of attributes and methods.

- :code:`create` *classmethod*: This can be used to create a bloxby account for a user. Takes in parameters:
    - :code:`user`: User object of the user you want to create the bloxby account for.
    - :code:`package_id`: Bloxby Builder Package ID of the package you want to assign to user being created. Falls back to the :code:`settings.BLOXBY_BUILDER['default_package_id']` if no parameter is provided in this position.

    Returns the new :code:`UserBridge` instance.


.. code-block:: python

    user = request.user
    UserBridge.create(user, 4)


- :code:`dashboard_url` *property*: This returns the URL the current instance of UserBridge can use to auto login into the bloxby instance

.. code-block:: python

    try:
        login_url = request.user.userbridge.dashboard_url
        # OR login_url = UserBridge.objects.get(user=request.user).dashboard_url
    except UserBridge.DoesNotExist:
        login_url = UserBridge.create(request.user).dashboard_url

    # Do whatever you want with the login url maybe pass it to HTML


- :code:`user_templates` *method*: This returns the templates the current user has. Assumed you have done the initial setup in :code:`settings.py`, and most importantly added the :code:`BLOXBY_BUILDER['custom_api_url']` setting.

.. code-block:: python

    try:
        templates = request.user.userbridge.user_templates()
    except UserBridge.DoesNotExist:
        templates = UserBridge.create(request.user).user_templates()

    # You can also access the template data by doing

    for template in templates:
        print(template.sites_id)
        print(template.users_id)
        print(template.sites_name)
        print(template.sitethumb)
        print(template.sites_lastupdate_on)


    # To get your data in JSON in an API view

    json_templates = UserTemplateSerializer(templates, many=True).data


If you want it in json, you can do a simple serializer in django rest framework like this:

.. code-block:: python

    class UserTemplateSerializer(serializers.Serializer):
        sites_id = serializers.IntegerField()
        sites_name = serializers.CharField()
        sitethumb = serializers.CharField()
        edit_url = serializers.SerializerMethodField()
        sites_lastupdate_on = serializers.CharField()

        def get_edit_url(self, obj):
            return f"{settings.BLOXBY_BUILDER['url']}/sites/{obj.sites_id}"

        def to_representation(self, instance):
            data = super(UserTemplateSerializer, self).to_representation(instance)
            try:
                last_updated = datetime.fromtimestamp(int(data.get('sites_lastupdate_on', 0)))
                data['sites_lastupdate_on'] = last_updated.strftime('%d %B %Y, %H:%m')
            except TypeError:
                data['sites_lastupdate_on'] = 'Never'
            return data


Note that the :code:`to_representation` method was overridden to format the datetime to our own taste, it is not
necessary to do so. If you are satisfied with the format of the default :code:`sites_lastupdate_on`, you might want to
leave overriding to_representation out of your code.

- :code:`save_site_from_remote` *method*: This method does not return anything, just downloads the site from the node server you setup earlier, takes parameters:

    - :code:`site_id`: This is the unique ID of the site which you want to download from the user's builder account into your django application, how to render the site will be in the next section.
    - :code:`target`: This could be any string, something that differentiates objects using the sites. e.g. I could pass in 'event' as this parameter for me to know how to retrieve this particular template to render.
    - :code:`obj_id` *optional*: Should you want to attach this site you are downloading to another model instance in your application, you can pass in their unique key (preferably primary key) here. Note that the :code:`target` and :code:`obj_id` need to be unique together.


Use in Django Application
#########################

Assuming that I intend to use a template for an event home page.

In the view that lets us tie the event to a template:

.. code-block:: python

    from bloxby.models import Template

    class AssignSiteToEvent (View):
        def post(self, request, *args, **kwargs):
            # Assuming you hit this endpoint with a post request with data {"site_id": 100, "event_id": 4}
            site_id = self.request.data.get('site_id')
            event_id = self.request.data.get('event_id')
            if event_id:
                self.request.user.userbridge.save_site_from_remote(site_id=site_id, target='event', obj_id=tenant_id)
            else:
                Template.objects.filter(remote_id=site_id, target='home', owner=self.request.user).delete()
            return HttpResponseRedirect('/success')



To render it:

.. code-block:: python

    from bloxby.models import Template

    class EventLandingPageView(View):
        def get(self, request, *args, **kwargs):
            page = request.GET.get('page')
            # The page parameter helps to handle the other page when the template attached has multiple pages,
            # and they are linked. e.g. http://site.com/<event_id>/?page=contact.html
            event_id = kwargs.get('event_id')
            template = Template.objects.filter(target='event', obj_id=event_id)
            # retrieve the template that got saved from the 'save_site_from_remote' method called in the 'AssignSiteToEvent' part.
            if template.exists():
                template = template.first()
                if page:
                    try:
                        page = template.page_set.filter(name__iexact=page.lower()).first()
                        return HttpResponse(page.render())
                    except Page.DoesNotExist:
                        raise Http404('Page does not exist.')
                index_page = template.index_page
                if index_page:
                    return HttpResponse(index_page.render())
            # Handle situation where no template is attached to the event
            return HttpResponse('No template to render')


Setup FTP Server (Alternative, not recommended)
-----------------------------------------------

**In Production Environment**

This part assumes you have python, pip and virtualenv installed globally on your server.

Make :code:`setup_ftp_server.sh` and :code:`start_ftp_server.sh` executable if they are not already
executable. :code:`chmod u+x setup_ftp_server.sh` and :code:`chmod u+x start_ftp_server.sh`.

Run:

.. code-block:: bash

    ./setup_ftp_server.sh


This installs certain dependencies needed.

** To start the servers **

Run

.. code-block:: bash

    ./start_ftp_server.sh


This starts the FTP server on port 21 and the django server on port 8000. The servers work together, the django server started on port 8000
provides the admin dashboard to manage the external applications that want to receive files through FTP.

So rather than running an FTP server on each and every one of those applications, we'd register them here
and also have this library running on them to allow authentication of users, receipt and processing of files.


These processes are managed by `PM2 <https://pm2.keymetrics.io/docs/usage/quick-start/>`_. So this allows you to use some of the
PM2 commands if you are familiar with them.

For example, you just did a git pull and you want to restart, you could just do:

.. code-block:: bash

    pm2 restart all


This restarts the django server and the ftp server.


Why the Django Server inside of the library
###########################################

The Django server provides admin interface to manage external applications.
You just need to add a model object named :code:`Application` that takes in the auth URL and file receiving URL of the 
external application (these are automatically also provided by this library), this where the FTP server performs 
authentication for users that want to publish pages.

e.g. I have an external application at https://dev.linkfusions.com , and in this external application, I have
:code:`django-bloxby` installed already with the URLs set. I can just add an Application model instance through the FTP server 
instance admin, name it 'dev-fusions', provide the auth url as installed in my external application (How to do this in 
the next section), provide the auth and receiving url and that's all.


**How to add the URLs to your external application**

In your :code:`urls.py`, you can add these:

.. code-block:: python

    urlpatterns = [
        ...

        path('bloxby/', include('djbloxby.bloxby.urls')),
        ...
    ]


If I setup this way, my auth URL is going to be :code:`http://<mydomain>/bloxby/ftp/auth/` and my
receiving URL is going to be :code:`http://<mydomain>/bloxby/ftp/receive/`. (These are the URLs you
register in the :code:`Application` model with the FTP server).


How to access the pages published to your external application
--------------------------------------------------------------


A couple of models are made available for this :code:`Template`, :code:`Page`,
:code:`TemplateAsset`. The :code:`Template` is just a sugar-coated name for Website.
It encapsulates the assets and the HTML pages. The :code:`Page` represents the HTML files and they
have two major attributes (functions) which are :code:`render` and :code:`process`.

The :code:`render` function returns HTML string of a page. :code:`process`, swaps all the URLs with
the django application compatible URLs depending on your default file storage, it's only called once
for every page (at initial page request, the very first time the page is being accessed).It parses all the
CSS files also and makes sure their URLs are valid.


Possible Issues
----------------

Make sure to set the correct address to the :code:`Site` in admin.

FTP Client is able to connect and authenticate but unable to list directory. Enable passive ports
on your server (where the FTP server runs). In this, passive ports run in the range 60000-65535.
You can enable this by running:


.. code-block:: bash

    sudo ufw allow from ip_address to any port 60000:65535 proto tcp


Where :code:`ip_address` is whatever (domain or IP address) you configure in the :code:`Site`
in admin.


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
