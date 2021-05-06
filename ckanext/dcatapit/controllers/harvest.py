import logging

import ckan.logic as logic
import ckan.model as model
from ckan import common as _
from ckan import plugins as p
from flask.views import View
from ckan.lib.base import abort, c, render

log = logging.getLogger(__file__)

# shortcuts
get_action = logic.get_action


class HarvesterController(View):

    def get(self):
        try:
            context = {'model': model,
                       'user': c.user}
            harvest_sources = p.toolkit.get_action('harvest_source_list')(context, {'only_active': True})
            c.harvest_sources = harvest_sources

            return render('harvest/sources_list.html')

        except p.toolkit.ObjectNotFound:
            abort(404, _('Harvest source not found'))
        except p.toolkit.NotAuthorized as err:
            abort(401, self.not_auth_message)
        except Exception as err:
            msg = 'An error occurred: [%s]' % str(err)
            import traceback
            traceback.print_exc(err)

            abort(500, msg)
