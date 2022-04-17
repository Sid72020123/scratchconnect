"""
Main File
"""

import pyhtmlchart as chart


class Chart:
    """
    The Chart class
    """

    def __init__(self, sc):
        self.sc = sc

    def _get_user_data(self, username, keys):
        """
        Don't use this
        """
        result = []
        user = self.sc.connect_user(username)
        data = {
            'Username': username,
            'Messages Count': user.messages_count(),
            'Follower Count': user.followers_count(),
            'Following Count': user.following_count(),
            'Total Views': user.total_views(),
            'Total Loves': user.total_loves_count(),
            'Total Favourites': user.total_favourites_count(),
            'Total Projects Count': user.projects_count()
        }
        for key in keys:
            result.append(data[key])
        return result

    def user_stats_chart(self, usernames, include_data=None):
        """
        Make a comparison chart of Users Stats
        :param usernames: A list of usernames to include
        :param include_data: A list to include the user data. Choose one or more from ['Username', 'Messages Count', 'Follower Count', 'Following Count', 'Total Loves',
                            'Total Favourites', 'Total Projects Count']
        """
        if include_data is None:
            include_data = ['Username', 'Messages Count', 'Follower Count', 'Following Count', 'Total Loves',
                            'Total Favourites', 'Total Projects Count']
        if 'Username' not in include_data:
            include_data.insert(0, 'Username')
        result = []
        for username in usernames:
            data = self._get_user_data(username, include_data)
            result.append(data)
        column_chart = chart.column_chart.ColumnChart(location='user_stats_chart',
                                                      title='User Stats Comparison Chart', x_axis_title="Username(s)",
                                                      y_axis_title="Number", chart_actions=True)
        columns = include_data
        column_chart.add_data(data=result, data_titles=columns)
        return column_chart

    def user_stats_table(self, usernames, include_data=None):
        """
        Make a comparison table of Users Stats
        :param usernames: A list of usernames to include
        :param include_data: A list to include the user data. Choose one or more from ['Username', 'Messages Count', 'Follower Count', 'Following Count', 'Total Loves',
                            'Total Favourites', 'Total Projects Count']
        """
        if include_data is None:
            include_data = ['Username', 'Messages Count', 'Follower Count', 'Following Count', 'Total Loves',
                            'Total Favourites', 'Total Projects Count']
        if 'Username' not in include_data:
            include_data.insert(0, 'Username')
        result = []
        for username in usernames:
            data = self._get_user_data(username, include_data)
            result.append(data)
        table = chart.table.Table(location='user_stats_table', title='User Stats Comparison Table', font="Sans Serif",
                                  table_border=10, border_color="Black", cell_padding=5, cell_spacing=0)
        columns = include_data
        table.add_data(data=result, columns=columns)
        return table

    def _get_studio_data(self, studio_id, keys):
        """
        Don't use this
        """
        result = []
        studio = self.sc.connect_studio(studio_id)
        data = {
            'Studio ID': f"Studio {studio.id()}",
            'Comments Count': studio.stats()['comments'],
            'Followers Count': studio.stats()['followers'],
            'Managers Count': studio.stats()['managers'],
            'Projects Count': studio.stats()['projects'],
        }
        for key in keys:
            result.append(data[key])
        return result

    def studio_stats_chart(self, studio_ids, include_data=None):
        """
        Make a comparison chart of Studio Stats
        :param studio_ids: A list of studio ids to include
        :param include_data: A list to include the studio data. Choose one or more from ['Studio ID', 'Comments Count', 'Followers Count', 'Managers Count', 'Projects Count']
        """
        if include_data is None:
            include_data = ['Studio ID', 'Comments Count', 'Followers Count', 'Managers Count', 'Projects Count']
        if 'Studio ID' not in include_data:
            include_data.insert(0, 'Studio ID')
        result = []
        for studio_id in studio_ids:
            data = self._get_studio_data(studio_id, include_data)
            result.append(data)
        column_chart = chart.column_chart.ColumnChart(location='studio_stats_chart',
                                                      title='Studio Stats Comparison Chart',
                                                      x_axis_title="Studio ID(S)",
                                                      y_axis_title="Number", chart_actions=True)
        columns = include_data
        column_chart.add_data(data=result, data_titles=columns)
        return column_chart

    def studio_stats_table(self, studio_ids, include_data=None):
        """
        Make a comparison table of Studio Stats
        :param studio_ids: A list of studio ids to include
        :param include_data: A list to include the studio data. Choose one or more from ['Studio ID', 'Comments Count', 'Followers Count', 'Managers Count', 'Projects Count']
        """
        if include_data is None:
            include_data = ['Studio ID', 'Comments Count', 'Followers Count', 'Managers Count', 'Projects Count']
        if 'Studio ID' not in include_data:
            include_data.insert(0, 'Studio ID')
        result = []
        for studio_id in studio_ids:
            data = self._get_studio_data(studio_id, include_data)
            result.append(data)
        table = chart.table.Table(location='studio_stats_table', title='Studio Stats Comparison Table',
                                  font="Sans Serif", table_border=10, border_color="Black", cell_padding=5,
                                  cell_spacing=0)
        columns = include_data
        table.add_data(data=result, columns=columns)
        return table

    def _get_project_data(self, project_id, keys):
        """
        Don't use this
        """
        result = []
        project = self.sc.connect_project(project_id)
        data = {
            'Project ID': f"Project {project.id()}",
            'Views': project.stats()['views'],
            'Loves': project.stats()['loves'],
            'Favourites': project.stats()['favorites'],
            'Remixes': project.stats()['remixes'],
            'Version': project.assets_info()['version'],
            'Costumes': project.assets_info()['costumes'],
            'Blocks': project.assets_info()['blocks'],
            'Variables': project.assets_info()['variables'],
            'Assets': project.assets_info()['assets']
        }
        for key in keys:
            result.append(data[key])
        return result

    def project_stats_chart(self, project_ids, include_data=None):
        """
        Make a comparison chart of Project Stats
        :param project_ids: A list of project ids to include
        :param include_data: A list to include the project data. Choose one or more from ['Project ID', 'Views', 'Loves', 'Favourites', 'Remixes', 'Version', 'Costumes', 'Blocks',
                            'Variables', 'Assets']
        """
        if include_data is None:
            include_data = ['Project ID', 'Views', 'Loves', 'Favourites', 'Remixes', 'Version', 'Costumes', 'Blocks',
                            'Variables', 'Assets']
        if 'Project ID' not in include_data:
            include_data.insert(0, 'Project ID')
        result = []
        for project_id in project_ids:
            data = self._get_project_data(project_id, include_data)
            result.append(data)
        column_chart = chart.column_chart.ColumnChart(location='project_stats_chart',
                                                      title='Project Stats Comparison Chart',
                                                      x_axis_title="Project ID(S)", y_axis_title="Number",
                                                      chart_actions=True)
        columns = include_data
        column_chart.add_data(data=result, data_titles=columns)
        return column_chart

    def project_stats_table(self, project_ids, include_data=None):
        """
        Make a comparison table of Project Stats
        :param project_ids: A list of project ids to include
        :param include_data: A list to include the project data. Choose one or more from ['Project ID', 'Views', 'Loves', 'Favourites', 'Remixes', 'Version', 'Costumes', 'Blocks',
                            'Variables', 'Assets']
        """
        if include_data is None:
            include_data = ['Project ID', 'Views', 'Loves', 'Favourites', 'Remixes', 'Version', 'Costumes', 'Blocks',
                            'Variables', 'Assets']
        if 'Project ID' not in include_data:
            include_data.insert(0, 'Project ID')
        result = []
        for project_id in project_ids:
            data = self._get_project_data(project_id, include_data)
            result.append(data)
        table = chart.table.Table(location='project_stats_table', title='Project Stats Comparison Table',
                                  font="Sans Serif", table_border=10, border_color="Black", cell_padding=5,
                                  cell_spacing=0)
        columns = include_data
        table.add_data(data=result, columns=columns)
        return table

    def _get_user_followers_history(self, username, segment, time_range):
        """
        Don't use this
        """
        result = []
        data = self.sc.connect_user(username).user_follower_history(segment=segment, range=time_range)
        for i in range(0, len(data)):
            temp_date = str(data[i]["date"][:9]).split("-")
            temp_date.reverse()
            date = f"{temp_date[0]}/{temp_date[1]}/{temp_date[2]}"
            value = data[i]["value"]
            result.append([date, value])
        return result

    def user_followers_history_chart(self, username, segment="", time_range=365):
        """
        Make a chart of user's followers history
        """
        result = self._get_user_followers_history(username, segment, time_range)
        columns = ["Time", "Followers"]
        line_chart = chart.line_chart.LineChart(location='user_followers_history_chart',
                                                title='User Followers History Chart', x_axis_title="Date",
                                                y_axis_title="Number", chart_actions=True)
        line_chart.add_data(data=result, data_titles=columns)
        return line_chart

    def user_followers_history_table(self, username, segment="", time_range=365):
        """
        Make a table of user's followers history
        """
        result = self._get_user_followers_history(username, segment, time_range)
        columns = ["Time", "Followers"]
        table = chart.table.Table(location='user_followers_history_table', title='User Followers History Table',
                                  font="Sans Serif", table_border=10, border_color="Black", cell_padding=5,
                                  cell_spacing=0)
        table.add_data(data=result, columns=columns)
        return table
