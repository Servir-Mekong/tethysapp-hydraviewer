from tethys_sdk.base import TethysAppBase, url_map_maker


class Hydraviewer(TethysAppBase):
    """
    Tethys app class for HYDRA Viewer.
    """

    name = 'HYDRA Viewer'
    index = 'hydraviewer:home'
    icon = 'hydraviewer/images/icon.gif'
    package = 'hydraviewer'
    root_url = 'hydraviewer'
    color = '#34495e'
    description = 'Place a brief description of your app here.'
    tags = '&quot;Remote-Sensing&quot;,&quot;Floods&quot;'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='hydraviewer',
                controller='hydraviewer.controllers.home'
            ),
            UrlMap(
                name='precip',
                url='hydraviewer/precip',
                controller='hydraviewer.controllers.precip'
            ),
        )

        return url_maps
