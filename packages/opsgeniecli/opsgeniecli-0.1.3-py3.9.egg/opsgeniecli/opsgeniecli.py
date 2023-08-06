#!/usr/bin/env python
# pylint: disable=too-many-lines
# -*- coding: utf-8 -*-
# File: opsgeniecli.py
#
# Copyright 2019 Yorick Hoorneman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for opsgeniecli

.. _Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

"""
from datetime import timedelta
from datetime import datetime
from operator import itemgetter
import pendulum
import urllib.parse
import urllib.request
import os
import collections
import pathlib
import random
import sys
import re
import json
import requests
from prettytable import PrettyTable
import click
import pytz
from opsgenielib import Opsgenie, InvalidApiKey

__author__ = '''Yorick Hoorneman <yhoorneman@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''26-02-2019'''
__copyright__ = '''Copyright 2019, Yorick Hoorneman'''
__credits__ = ["Yorick Hoorneman"]
__license__ = '''MIT'''
__maintainer__ = '''Yorick Hoorneman'''
__email__ = '''<yhoorneman@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class DefaultHelp(click.Command):
    """Responding with help docs when no arguments are given"""

    def __init__(self, *args, **kwargs):
        context_settings = kwargs.setdefault('context_settings', {})
        if 'help_option_names' not in context_settings:
            context_settings['help_option_names'] = ['-h', '--help']
        self.help_flag = context_settings['help_option_names'][0]
        super(DefaultHelp, self).__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        if not args:
            args = [self.help_flag]
        return super(DefaultHelp, self).parse_args(ctx, args)


class MutuallyExclusiveOption(click.Option):
    """Restricting parameters to only be usable when a defined other parameter is not used"""

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = (
                ' NOTE: This argument is mutually exclusive with '
                ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

def create_and_add_to_pretty_table(table_fields, returned_alerts):
    """
    Function to create a table for output and adding rows based on the header fields passed

    Args:
        table_fields: list of column names
        returned_alerts: list of alerts

    Returns:
        PrettyTable object
    """
    format_table = PrettyTable(table_fields)
    for item in returned_alerts:
        item_to_add = []
        for field in table_fields:
            if field == 'createdAt':
                item_to_add.append((pendulum.parse(item['createdAt'])).in_tz('Europe/Amsterdam').to_datetime_string())
            elif field == 'message':
                item_to_add.append(item['message'].replace("\n", ""))
            elif field == 'integration':
                item_to_add.append(item['integration']['name'])
            elif field == 'tags':
                item_to_add.append(' '.join(sorted(item['tags'])))
            elif field in format_table.field_names:
                item_to_add.append(item[field])
        format_table.add_row(item_to_add)
    return format_table


@click.group()
@click.pass_context
@click.option('--config-file', '--config_file', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_CONFIG',
              mutually_exclusive=["team", "apikey"])
@click.option('--team-name', 'team_name', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_TEAMNAME',
              mutually_exclusive=["config_file"])
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_TEAMID',
              mutually_exclusive=["config_file"])
@click.option('--api-key', '--api_key', cls=MutuallyExclusiveOption,
              envvar='OPSGENIE_APIKEY',
              mutually_exclusive=["config_file"])
@click.option('--profile')
def bootstrapper(context, config_file, team_name, team_id, api_key, profile):  # pylint: disable=too-many-arguments
    """
    Function to sort the authentication used in further calls

    \b
    Args:
        \b
        config_file: option to deviate from the default config location at ~/.opsgenie-cli/config.json
        team_name: teamname in Opsgenie
        team_id: teamid in Opsgenie
        api_key: API key used to authenticate. Note: some calls require an API restricted to a team, most DO NOT
        profile: option to switch between config entries in the config file

    \b
    Returns:
        This function None on success, output shows for incorrect API and misuse of parameters

    """
    if not config_file and not team_name and not api_key and not team_id:
        config_file = pathlib.PurePath(pathlib.Path.home(), ".opsgenie-cli", "config.json")
        if os.path.isfile(config_file):
            with open(config_file) as config_file_path:
                try:
                    data = json.load(config_file_path)
                except ValueError as error:
                    print("invalid json: %s" % error)
                if not profile:
                    profile = 'default'
                context.obj['teamname'] = data[0][profile]['teamname']
                context.obj['apikey'] = data[0][profile]['apikey']
                context.obj['teamid'] = data[0][profile]['teamid']
        else:
            raise click.UsageError(
                "No config was given. Do one of the following:\n"
                "\t-Create a config file at: ~/.opsgenie-cli/config.json\n"
                "\t-Specify a config file. Use --config or set the environment variable OPSGENIE_CONFIG\n"
                "\t-Specify the team & apikey. Use --team & --apikey or set the env vars OPSGENIE_TEAM & OPSGENIE_APIKEY"
            )
    elif config_file:
        with open(config_file) as config_file_path:
            data = json.load(config_file_path)
            if profile:
                context.obj['teamname'] = data[0][profile]['teamname']
                context.obj['apikey'] = data[0][profile]['apikey']
                context.obj['teamid'] = data[0][profile]['teamid']
            else:
                context.obj['teamname'] = data[0]['default']['teamname']
                context.obj['apikey'] = data[0]['default']['apikey']
                context.obj['teamid'] = data[0]['default']['teamid']
    elif team_name and api_key and team_id:
        context.obj['teamname'] = team_name
        context.obj['apikey'] = api_key
        context.obj['teamid'] = team_id
    try:
        context.obj['opsgenie'] = Opsgenie(f"{context.obj['apikey']}")
    except InvalidApiKey:
        raise SystemExit('I am sorry to say that the provided api key is invalid.')


@bootstrapper.group()
@click.pass_context
def alerts(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@alerts.command(name='query',
                help='Example: "status: closed AND teams: <opsgenie-team> AND description: *<some-hostname>*"')
@click.option('--query', required=True)
@click.option('--sort-by', "--sort_by")
@click.pass_context
def alerts_query(context, query, sort_by):
    """
    Function to query alerts

    Args:
        query: a query to filter the alerts
        sort_by: which column to filter by

    Returns:
        A table output of the alerts on success and a string otherwise

    """
    result = context.obj['opsgenie'].query_alerts(query)
    table_fields = ['message', 'tags', 'integration', 'createdAt']
    if sort_by:
        if sort_by not in table_fields:
            raise click.UsageError(
                f"No column name found named: '{sort_by}'."
            )
        result = sorted(result, key=itemgetter(sort_by))
    format_table = create_and_add_to_pretty_table(table_fields, result)

    output = format_table if len(format_table._rows) > 0 else 'No alerts found..'
    print(output)

@alerts.command(name='list')
@click.option('--active', default=False, is_flag=True)
@click.option('--more-info', default=False, is_flag=True)
@click.option('--team-name', 'team_name', default=False)
@click.option('--last', prompt=False)
@click.option('--out-of-office-hours', default=False, is_flag=True)
@click.option('--not-filtered', default=False, is_flag=True)
@click.option('--sort-by', "--sort_by", default='status')
@click.option('--limit', default=100)
@click.pass_context
def alerts_list(context, active, limit, more_info, team_name, out_of_office_hours, not_filtered, sort_by, last):  # pylint: disable=too-many-branches
    """
    Function to list alerts

    Args:
        active: filters down to alerts that are not closed and not acknowledged
        limit: amount of alerts shown in output, default is 100
        more_info: adds the column tags, source, and integration to the output
        team_name: shows the alerts for the team specified
        sort_by: which column to filter by
        last: retrieving alerts going back for x amount of time

    Returns:
        Table output of the list of alerts on success

    """
    if team_name:
        team_name = find_team_name_by_name(team_name)  # pylint: disable=no-value-for-parameter
    if {context.obj.get('teamname')} and not team_name:
        team_name = f"{context.obj.get('teamname')}"
    if not {context.obj.get('teamname')} and not team_name:
        raise click.UsageError(
            "Specify the teamname using --teamname."
        )

    if last and limit == 100:
        print(f'Note: You might need to increase limit, in order to see all alerts for the period.')

    if not_filtered:
        result = context.obj['opsgenie'].query_alerts(f"responders:{team_name} AND tag != filtered AND tag != Filtered", limit)
    else:
        result = context.obj['opsgenie'].query_alerts(f"responders:{team_name}", limit)

    if more_info:
        table_fields = ['message', 'status', 'acknowledged',
                                    'createdAt', 'tags', 'source', 'integration', 'id']
    else:
        table_fields = ['message', 'status', 'acknowledged', 'createdAt']

    if sort_by not in table_fields:
        raise click.UsageError(
            f"No column name found named: '{sort_by}'."
        )
    else:
        sortedlist = sorted(result, key=itemgetter(sort_by))

    if out_of_office_hours:
        sortedlist = [x for x in sortedlist  \
                        if (pendulum.parse(x['createdAt'])).in_tz('Europe/Amsterdam').hour >= 17 \
                        or (pendulum.parse(x['createdAt'])).in_tz('Europe/Amsterdam').hour < 8]
    if last:
        if 'm' in last:
            subtract_period = 'months'
        if 'w' in last:
            subtract_period = 'weeks'
        if 'd' in last:
            subtract_period = 'days'
        subtract_value = int(re.sub(r'[mwd]', '', last))
        args = {subtract_period: subtract_value}
        subtracted_date = (pendulum.now().in_tz('Europe/Amsterdam')).subtract(**args)
        sortedlist = [x for x in sortedlist  \
                        if (pendulum.parse(x['createdAt'])).in_tz('Europe/Amsterdam') >= subtracted_date]
    if active:
        sortedlist = [x for x in sortedlist if x['status'] == 'open' and not x['acknowledged']]

    format_table = create_and_add_to_pretty_table(table_fields, sortedlist)
    output = format_table if len(format_table._rows) > 0 else 'No alerts found..'
    print(output)


@alerts.command(cls=DefaultHelp, name='get')
@click.option('--id', 'id_')
@click.pass_context
def alerts_get(context, id_):
    """
    Function to get more information about a single alert

    Args:
        id: the id of the alert

    Returns:
        The json output of the alert on success, None otherwise

    """
    result = context.obj['opsgenie'].get_alerts(id_)
    print(json.dumps(result, indent=4, sort_keys=True))


@alerts.command(name='count')
@click.option('--team-name', 'team_name', default=False)
@click.option('--not-filtered', default=False, is_flag=True)
@click.option('--out-of-office-hours', default=False, is_flag=True)
@click.option('--last')
@click.option('--limit', default=100)
@click.pass_context
def alerts_count(context, team_name, not_filtered, out_of_office_hours, limit, last):
    """
    Function to show which alerts were noisy

    Args:
        team_name: shows the alerts for the team specified
        last: retrieving alerts going back for x amount of time

    Returns:
        Table output with alerts for an Opsgenie team and the occurrence of the alerts

    """
    if team_name:
        team_name = find_team_name_by_name(team_name)  # pylint: disable=no-value-for-parameter
    if {context.obj.get('teamname')} and not team_name:
        team_name = f"{context.obj.get('teamname')}"
    if not {context.obj.get('teamname')} and not team_name:
        raise click.UsageError(
            "Specify the teamname using --teamname."
        )

    if last and limit == 100:
        print(f'Note: You might need to increase limit, in order to see all alerts for the period.')

    if not_filtered:
        result = context.obj['opsgenie'].query_alerts(f"responders:{team_name} AND tag != filtered AND tag != Filtered", limit)
    else:
        result = context.obj['opsgenie'].query_alerts(f"responders:{team_name}", limit)

    if out_of_office_hours:
        result = [x for x in result  \
                        if (pendulum.parse(x['createdAt'])).in_tz('Europe/Amsterdam').hour >= 17 \
                        or (pendulum.parse(x['createdAt'])).in_tz('Europe/Amsterdam').hour < 8]
    if last:
        if 'm' in last:
            subtract_period = 'months'
        if 'w' in last:
            subtract_period = 'weeks'
        if 'd' in last:
            subtract_period = 'days'
        subtract_value = int(re.sub(r'[mwd]', '', last))
        args = {subtract_period:subtract_value}
        subtracted_date = (pendulum.now().in_tz('Europe/Amsterdam')).subtract(**args)
        result = [x for x in result  \
                        if (pendulum.parse(x['createdAt'])).in_tz('Europe/Amsterdam') >= subtracted_date]

    dictionary = collections.Counter((re.sub(r'(\n|\r)', '', item['message'])) for item in result)
    sorted_by_count = sorted(dictionary.items(), reverse=True, key=itemgetter(1))
    for alert in sorted_by_count:
        print(f"{alert[1]} - {alert[0]}")


@alerts.command(cls=DefaultHelp, name='acknowledge')
@click.option('--id', 'id_', prompt=False, cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', 'all_', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--team-name', 'team_name', default=False)
@click.pass_context
def alerts_acknowledge(context, id_, all_, team_name):
    """
    Function to acknowledge a single or all open alerts

    Args:
        id: the id of the alert
        all: acknowledges all open (not closed nor acknowledged) alerts

    Returns:
        The json output from the API on success, None otherwise

    """
    if {context.obj.get('teamname')} and not team_name:
        team_name = f"{context.obj.get('teamname')}"
    if id_:
        result = context.obj['opsgenie'].acknowledge_alerts(id_)
        print(json.dumps(result, indent=4, sort_keys=True))
    elif all_:
        result = context.obj['opsgenie'].query_alerts(f"responders:{team_name} \
                                                      AND NOT status: closed AND acknowledged: false")
        for item in result:
            print(f"acknowledged: {item['acknowledged']} - status: {item['status']}")
            response = context.obj['opsgenie'].acknowledge_alerts(item['id'])
            if response['result'] == 'Request will be processed':
                print(f"✓ - alert acknowledged: {item['id']} - {item['message']}")
            else:
                print(f"x - alert Not acknowledged: {item['id']} - {item['message']}")


@alerts.command(cls=DefaultHelp, name='close')
@click.option('--id', 'id_', prompt=False, cls=MutuallyExclusiveOption, mutually_exclusive=["all"])
@click.option('--all', 'all_', default=False, is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--team-name', 'team_name', default=False)
@click.pass_context
def alerts_close(context, id_, all_, team_name):
    """
    Function to close a single or all open alerts

    Args:
        id: the id of the alert
        all: close all alerts that are acknowledged but not closed

    Returns:
        The json output from the API on success, None otherwise

    """
    if {context.obj.get('teamname')} and not team_name:
        team_name = f"{context.obj.get('teamname')}"
    if id_:
        result = context.obj['opsgenie'].close_alerts(id_)
        print(json.dumps(result, indent=4, sort_keys=True))
    elif all_:
        result = context.obj['opsgenie'].query_alerts(f"teams:{team_name} and status != closed")
        print("\nThe following alerts will be closed:")
        format_table = PrettyTable(['id', 'alias', 'createdAt', 'count'])
        for item in result:
            format_table.add_row([item['id'], item['alias'], item['createdAt'], item['count']])
        print(format_table)
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in result:
                if item['acknowledged']:
                    response = context.obj['opsgenie'].close_alerts(item['id'])
                    if response['result'] == 'Request will be processed':
                        print(f"✓ - alert closed: {item['id']} - {item['message']}")
                    else:
                        print(f"x - alert Not closed: {item['id']} - {item['message']}")


@bootstrapper.group()
@click.pass_context
def policy_alerts(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@policy_alerts.command(cls=DefaultHelp, name='get')
@click.option('--id', 'id_', prompt=True)
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_alerts_get(context, id_, team_id, team_name):
    """
    Function to get more information about a single alert policy

    Args:
        id: the id of the alert policy
        team_id: the id of the team
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        The json output from the API on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "No team id was found. Use --team_id or specify the team id in the config file.\n"
        )
    result = context.obj['opsgenie'].get_notification_policy(id_, team_id)
    print(json.dumps(result, indent=4, sort_keys=True))


@policy_alerts.command(cls=DefaultHelp, name='enable')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"],
              help='Specify the team id for team-based alert policies instead of global policies.')
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Specify the name of the alert policy you want to enable.')
@click.option('--id', 'id_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["filter"],
              help='The id of the alert policy you want to enable.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_alerts_enable(context, team_id, filter_, id_, team_name):  # pylint: disable=too-many-branches
    """
    Function to enable alert policies

    Args:
        team_id: the id of the team, to enable an alert policy connected to that team
        filter: a string to search on through existing alert policies. Can't be used together with --id
        id: the id of the alert policy. Can't be used together with --filter
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        String output specifying which alert policy was enabled on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team id using --team_id."
        )
    if not any([filter, id_]):
        raise click.UsageError("--id or --filter is required")
    if id_:
        result = context.obj['opsgenie'].enable_policy(id_, team_id)
        if result['result'] == 'Enabled':
            print(f"✓ - alert policy {id_} enabled for team: {context.obj.get('teamname')}")
    if filter_:
        id_ = []
        filters_enabled = []
        alert_policies = context.invoke(policy_alerts_list, team_id=team_id, print_output=False)
        for filt_ in filter_:
            filtered_results = [x for x in alert_policies['data'] if (filt_).lower() in (x['name']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_enabled.append(filtered_results[0]['name'])
            else:
                print(f"\nMultiple alert policies found for: '{filt_}'")
                filtered_format_table = PrettyTable(['id', 'name', 'type', 'enabled'])
                for result in filtered_results:
                    filtered_format_table.add_row([result['id'], result['name'], result['type'], result['enabled']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the alert policy you want to enable', type=str)
                id_.append(temp_id)
                filters_enabled.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
        result = context.obj['opsgenie'].enable_policy(id_, team_id)
        if result['result'] == 'Enabled':
            print(f"✓ - Alert policies enabled: {filters_enabled} for team: '{context.obj.get('teamname')}'")


@policy_alerts.command(cls=DefaultHelp, name='disable')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"],
              help='Specify the team id for team-based alert policies instead of global policies.')
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Specify the name of the alert policy you want to disable.')
@click.option('--id', 'id_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["filter"],
              help='The id of the alert policy you want to disable.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_alerts_disable(context, team_id, filter_, id_, team_name):  # pylint: disable=too-many-branches
    """
    Function to disable alert policies

    Args:
        team_id: the id of the team, to disable an alert policy connected to that team
        filter: a string to search on through existing alert policies. Can't be used together with --id
        id: the id of the alert policy. Can't be used together with --filter
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        String output specifying which alert policy was disabled on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team id using --team_id."
        )
    if not any([filter_, id_]):
        raise click.UsageError("--id or --filter is required")
    if id_:
        result = context.obj['opsgenie'].disable_policy(id_, team_id)
        if result['result'] == 'Disabled':
            print(f"✓ - alert policy {id_} disabled for team: '{context.obj.get('teamname')}'")
    if filter_:
        id_ = []
        filters_disabled = []
        alert_policies = context.invoke(policy_alerts_list, team_id=team_id, print_output=False)
        for filt_ in filter_:
            filtered_results = [x for x in alert_policies['data'] if (filt_).lower() in (x['name']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_disabled.append(filtered_results[0]['name'])
            else:
                print(f"\nMultiple alert policies found for: '{filt_}'")
                filtered_format_table = PrettyTable(['id', 'name', 'type', 'disabled'])
                for result in filtered_results:
                    filtered_format_table.add_row([result['id'], result['name'], result['type'], result['enabled']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the alert policy you want to disable', type=str)
                id_.append(temp_id)
                filters_disabled.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
        result = context.obj['opsgenie'].disable_policy(id_, team_id)
        if result['result'] == 'Disabled':
            print(f"✓ - Alert policies disabled: {filters_disabled} for team: '{context.obj.get('teamname')}'")


@policy_alerts.command(name='list')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"],
              help='Specify the team id for team-based alert policies instead of global policies.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.option('--active', 'enabled', default=False, is_flag=True)
@click.pass_context
def policy_alerts_list(context, team_id, team_name, enabled, print_output=True):
    """
    Function to list alert policies

    Args:
        team_id: the id of the team to list alert policies for
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        Table output listing alert policies in the format of three columns: ID, Name, and Enabled (boolean)

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team id using --team_id."
        )
    result = context.obj['opsgenie'].list_alert_policy(team_id)
    format_table = PrettyTable(['teamid', 'name', 'enabled'])
    sortedlist = sorted(result['data'], key=itemgetter('name'))
    for item in sortedlist:
        if enabled:
            if item['enabled']:
                format_table.add_row([item['id'], item['name'], item['enabled']])
        else:
            format_table.add_row([item['id'], item['name'], item['enabled']])
    if print_output:
        print(format_table)
        return None
    return result


@policy_alerts.command(cls=DefaultHelp, name='set')
@click.option('--name', 'alert_name', help='Specify the name for the alert policy.', required=True)
@click.option('--filter', 'filter_', help='Specify what you want to filter on, it uses regex.', required=True)
@click.option('--description', 'description', help='Specify the description for the alert policy.', required=True)
@click.option('--enabled', is_flag=True, default=False, help='Specify if the alert policy should be enabled when created.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_alerts_set(context, alert_name, filter_, description, enabled, team_name):  # pylint: disable=too-many-branches
    """
    Function to create an alert policies

    Args:
        team_id: the id of the team, to disable an alert policy connected to that team
        filter: a string to search on through existing alert policies. Can't be used together with --id
        id: the id of the alert policy. Can't be used together with --filter
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        String output specifying which alert policy was disabled on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and 'team_id' not in locals():
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name using --team-name."
        )
    result = context.obj['opsgenie'].create_alert_policy(alert_name, filter_, description, team_id, enabled)
    if result:
        print(f"✓ - Alert policy created.\n\t"
              f"Enabled: {result['data']['enabled']}\n\t"
              f"Name: {alert_name}\n\t"
              f"Filter: {filter_}\n\t"
              f"Team: {context.obj.get('teamname')}")

@policy_alerts.command(cls=DefaultHelp, name='delete')
@click.option('--id', 'id_', help='The id of the alerts policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["filter"])
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Filter based on the name of the maintenance policy.')
@click.option('--all', 'all_', default=False, is_flag=True, help='Will remove all alerts policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_alerts_delete(context, id_, all_, team_id, filter_, team_name):  # pylint: disable=too-many-locals, too-many-branches, too-many-arguments
    """
    Function to delete a single or multiple alerts

    Args:
        id: the id of the alert policy
        all: shows all alert policies that will be deleted, deletion follows after a prompts
        team_id: the id of the team to remove alert policies for
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        String output specifying which alert policy id was removed and for which team on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    if id_:
        response = context.obj['opsgenie'].delete_alert_policy(id_, team_id)
        if response['result'] == 'Deleted':
            print(f"✓ - alert policy {id_} deleted for team: {context.obj.get('teamname')}")
    elif all_:
        reponse = context.obj['opsgenie'].list_alert_policy(team_id)
        print("The following alerts policies will be deleted:")
        for item in reponse['data']:
            print(f"{item['id']} - {item['name']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in reponse['data']:
                response = context.obj['opsgenie'].delete_alert_policy(f"{item['id']}", team_id)
                if response['result'] == 'Deleted':
                    print(f"✓ - alert policy {item['id']} deleted for team: {context.obj.get('teamname')}")
    elif filter_:
        id_ = []
        filters_deleted = []
        alert_policies = context.obj['opsgenie'].list_alert_policy(team_id)
        for filt_ in filter_:
            filtered_results = [x for x in alert_policies['data'] if (filt_).lower() in (x['name']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_deleted.append(filtered_results[0]['name'])
            else:
                print(f"\nMultiple alert filters found for: '{filt_}'.")
                filtered_format_table = PrettyTable(['teamid', 'name', 'enabled'])
                for f_result in filtered_results:
                    filtered_format_table.add_row([f_result['id'],
                                                   f_result['name'],
                                                   f_result['enabled']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the policy you want to delete', type=str)
                id_.append(temp_id)
                filters_deleted.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
        del_result = context.obj['opsgenie'].delete_alert_policy(id_, team_id)
        if del_result['result'] == 'Deleted':
            print(f"✓ - Alert policies deleted: {filters_deleted}")
    else:
        raise click.UsageError(
            "Use --id, --all or --filter to delete one or multiple alert policies"
        )


@bootstrapper.group()
@click.pass_context
def users(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@users.command(name='list')
@click.option('--limit', default=100)
@click.pass_context
def users_list(context, limit):
    """
    Function to list users

    Args:
        limit: the amount of users returned

    Returns:
        The json output from the API on success, None otherwise

    """
    result = context.obj['opsgenie'].list_users(limit)
    print(json.dumps(result, indent=4, sort_keys=True))


@bootstrapper.group()
@click.pass_context
def integrations(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@integrations.command(cls=DefaultHelp, name='list')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def integrations_list(context, team_id, team_name):
    """
    Function to list integrations

    Args:
        team_id: the id of the team to list integrations for
        team_name: the teamname of the team to list integrations for

    Returns:
        Table output listing integrations in the format of five columns: type, id, name, teamId, enabled (boolean)

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    result = context.obj['opsgenie'].list_integrations_by_team_id(team_id)
    format_table = PrettyTable(['type', 'id', 'name', 'teamId', 'enabled'])
    for item in result['data']:
        format_table.add_row([item['type'], item['id'], item['name'], item['teamId'], item['enabled']])
    print(format_table)


@integrations.command(cls=DefaultHelp, name='get')
@click.option('--id', 'id_', required=True)
@click.pass_context
def integrations_get(context, id_):
    """
    Function to get more information about a single integrations

    Args:
        id: the id of the integration

    Returns:
        The json output from the API on success, None otherwise

    """
    try:
        result = context.obj['opsgenie'].get_integration_by_id(id_)
        print(json.dumps(result, indent=4, sort_keys=True))
    except requests.exceptions.HTTPError:
        print(f'The API called failed. Make sure that the api key used has the permissions.\n'
              f'Use --profile <name> to specify a different entry in the config.'
              f'Use <opsgeniecli config list> to see the config entries')


@bootstrapper.group()
@click.pass_context
def config(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@config.command(name='list')
@click.option('--config', default="~/.opsgenie-cli/config.json", envvar='OPSGENIE_CONFIG')
def config_list(config):  # pylint: disable=redefined-outer-name
    """Function that shows the entries in the config file"""
    if "~" in config:
        config = os.path.expanduser(config)
    with open(config) as config_file:
        data = json.load(config_file)
        for i in data[0]:
            print(json.dumps(i, indent=4, sort_keys=True))


@bootstrapper.group()
@click.pass_context
def policy_maintenance(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@policy_maintenance.command(cls=DefaultHelp, name='get')
@click.option('--id', 'id_', prompt=True)
@click.pass_context
def policy_maintenance_get(context, id_):
    """
    Function to get more information about a single maintenance policy

    Args:
        id: the id of the maintenance policy

    Returns:
        The json output from the API on success, None otherwise

    """
    result = context.obj['opsgenie'].get_maintenance(id_)
    print(json.dumps(result, indent=4, sort_keys=True))


@policy_maintenance.command(cls=DefaultHelp, name='set')
@click.option('--description', prompt=True)
@click.option('--start-date', 'start_date', help='Example: 2019-03-15T14:34:09')
@click.option('--end-date', 'end_date', help='Example: 2019-03-15T15:34:09')
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Filter down based on the name of the alert policy.')
@click.option('--state', type=click.Choice(['enabled', 'disabled']), default='enabled', help='State of rule that \
    will be defined in maintenance and can take \
    either enabled or disabled for policy type rules. This field has to be disabled for integration type entity rules')
@click.option('--entity', type=click.Choice(['integration', 'policy']), default='policy', help='The type of the entity \
    that maintenance will be applied. It can be either integration or policy')
@click.option('--hours', type=int, help='Filter duration is hours.')
@click.option('--id', 'id_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["filter"],
              help='The id of the entity that maintenance will be applied.')
@click.pass_context
def policy_maintenance_set(context,  # pylint: disable=too-many-branches, too-many-arguments, too-many-locals
                           description,
                           id_,
                           state,
                           entity,
                           hours,
                           filter_,
                           start_date,
                           end_date):
    """
    Function to create a maintenance policy

    Args:
        description: the name of the maintenance policy
        id: the id of the entity (integration or alert- or notification policies) used in the maintenance policy
        state: the state of the maintenance rule, enabled or disabled
        entity: the entity allows filtering using policies or a whole integrations
        hours: setting a maintenance policy from now plus the specified amount of hours
        filter: instead of specifying the id, using the name of the policy. Returns list that matches the filter
        start_date: a date and time on which the maintenance policy should start
        end_date: a date and time on which the maintenance policy should end

    Returns:
        String output names the title and the start- and end date of the maintenance policy on success, None otherwise

    """
    if not any([filter_, id_]):
        raise click.UsageError("--id or --filter is required")
    if filter_:
        id_ = []
        filters_enabled = []
        result = context.obj['opsgenie'].list_alert_policy(context.obj.get('teamid'))
        for filt_ in filter_:
            filtered_results = [x for x in result['data'] if (filt_).lower() in (x['name']).lower()]
            if len(filtered_results) == 0:
                raise click.UsageError(
                    f"\nNo alert filters found for {filt_}."
                )
            elif len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_enabled.append(filtered_results[0]['name'])
            else:
                print(f"\nMultiple alert filters found for {filt_}.")
                filtered_format_table = PrettyTable(['id', 'name', 'type', 'enabled'])
                for result in filtered_results:
                    filtered_format_table.add_row([result['id'], result['name'], result['type'], result['enabled']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the filter you want to use', type=str)
                id_.append(temp_id)
                filters_enabled.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
    if all([start_date, end_date]):
        start_dt = pendulum.parse(start_date, tz='Europe/Amsterdam')
        end_dt = pendulum.parse(end_date, tz='Europe/Amsterdam')
    else:
        start_dt = pendulum.now(tz='Europe/Amsterdam')
        end_dt = start_dt.add(hours=hours)
    if hours:
        result = context.obj['opsgenie'].set_maintenance_hours(context.obj.get('teamid'),
                                                               hours,
                                                               entity,
                                                               description,
                                                               state,
                                                               id_)
    if all([start_date, end_date]):
        result = context.obj['opsgenie'].set_maintenance_schedule(context.obj.get('teamid'),
                                                                  start_dt.isoformat(),
                                                                  end_dt.isoformat(),
                                                                  entity,
                                                                  description,
                                                                  state,
                                                                  id_)
    if result.status_code == 201:
        if hours:
            print(f"✓ - Maintenance policy created.\n\t"
                  f"Description: {description}\n\t"
                  f"Time: {hours}hours\n\t"
                  f"Policies enabled: {filters_enabled}")
        if start_date and end_date:
            print(f"✓ - Maintenance policy created.\n\t"
                  f"Description: {description}\n\t"
                  f"Start: {start_dt.to_datetime_string()}\n\t"
                  f"End: {end_dt.to_datetime_string()}\n\t"
                  f"Policies enabled: {filters_enabled}")


@policy_maintenance.command(cls=DefaultHelp, name='cancel')
@click.option('--id', 'id_', multiple=True, cls=MutuallyExclusiveOption,
              mutually_exclusive=["filter"])
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Filter based on the name of the maintenance policy.')
@click.pass_context
def policy_maintenance_cancel(context, id_, filter_):
    """
    Function to cancel a single maintenance policy

    Args:
        id: the id of the maintenance policy
        filter: the name or a part of a maintenance policy. In the case of multiple results,
        the results are displayed with a choice to select one.

    Returns:
        String output specifying which maintenance policy id was canceled and for which team on success, None otherwise

    """
    if id_:
        result = context.obj['opsgenie'].cancel_maintenance(id_)
        if result['result'] == 'Cancelled':
            print(f"✓ - Maintenance policies canceled: {id_}")
    if filter_:
        id_ = []
        filters_canceled = []
        maintenance_policies = context.obj['opsgenie'].list_maintenance(
            non_expired=True)
        for filt_ in filter_:
            filtered_results = [x for x in maintenance_policies['data'] if (filt_).lower() in (x['description']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_canceled.append(filtered_results[0]['description'])
            else:
                print(f"\nMultiple maintenance filters found for: '{filt_}'.")
                filtered_format_table = PrettyTable(['id', 'description', 'status', 'type'])
                for f_result in filtered_results:
                    filtered_format_table.add_row([f_result['id'],
                                                   f_result['description'],
                                                   f_result['status'],
                                                   f_result['time']['type']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the policy you want to cancel', type=str)
                id_.append(temp_id)
                filters_canceled.append([item['description'] for item in filtered_results
                                         if item.get('id') == temp_id][0])
        result = context.obj['opsgenie'].cancel_maintenance(id_)
        if result['result'] == 'Cancelled':
            print(f"✓ - Maintenance policies canceled: {filters_canceled}")
    else:
        raise click.UsageError(
            "Use --id or --filter to cancel one or multiple maintenance policies"
        )


@policy_maintenance.command(cls=DefaultHelp, name='delete')
@click.option('--id', 'id_', multiple=True, cls=MutuallyExclusiveOption,
              mutually_exclusive=["filter"])
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Filter based on the name of the maintenance policy.')
@click.option('--all', 'all_', default=False, is_flag=True, help='Will remove all maintenance policies for the team.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"],
              help='Specify the team id. The team id of the config file is used when no --team_id is given.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_maintenance_delete(context, id_, all_, team_id, team_name, filter_):  # pylint: disable=too-many-locals, too-many-branches, too-many-arguments
    """
    Function to delete a single or all maintenance policies

    Args:
        id: the id of the maintenance policy
        filter: the name or a part of a maintenance policy. In the case of multiple results,
        the results are displayed with a choice to select one.
        all: shows all maintenance policies that will be deleted, deletion follows after a prompts
        team_id: the id of the team
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        String output specifying which maintenance policy id was removed and for which team on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    if id_:
        result = result = context.obj['opsgenie'].delete_maintenance(id_)
        if result.status_code == 200:
            print(f"✓ - Maintenance policies deleted: {id_}")
    elif all_:
        result = context.obj['opsgenie'].list_maintenance()
        print("The following maintenance policies will be deleted:")
        for item in result['data']:
            print(f"{item['id']} - {item['description']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in result['data']:
                result = context.obj['opsgenie'].delete_maintenance(item['id'])
                if result.status_code == 200:
                    print(f"✓ - maintenance policy {item['id']} deleted for team: {context.obj.get('teamname')}")
    elif filter_:
        id_ = []
        filters_deleted = []
        maintenance_policies = context.obj['opsgenie'].list_maintenance(
            non_expired=True)
        for filt_ in filter_:
            filtered_results = [x for x in maintenance_policies['data'] if (filt_).lower() in (x['description']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_deleted.append(filtered_results[0]['description'])
            else:
                print(f"\nMultiple maintenance filters found for: '{filt_}'.")
                filtered_format_table = PrettyTable(['id', 'description', 'status', 'type'])
                for f_result in filtered_results:
                    filtered_format_table.add_row([f_result['id'],
                                                   f_result['description'],
                                                   f_result['status'],
                                                   f_result['time']['type']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the policy you want to delete', type=str)
                id_.append(temp_id)
                filters_deleted.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
        del_result = context.obj['opsgenie'].delete_maintenance(id_)
        if del_result.status_code == 200:
            print(f"✓ - Maintenance policies deleted: {filters_deleted}")
    else:
        raise click.UsageError(
            "Use --id, --all or --filter to delete one or multiple maintenance policies"
        )


@policy_maintenance.command(name='list')
@click.option('--nonexpired', '--active', default=False,
              is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["past"])
@click.option('--past', default=False, is_flag=True,
              cls=MutuallyExclusiveOption, mutually_exclusive=["non-expired"])
@click.pass_context
def policy_maintenance_list(context, nonexpired, past):
    """
    Function to list a maintenance policies

    Args:
        nonexpired: lists only maintenance policies that are active or scheduled
        past: lists expired maintenance policies

    Returns:
        Table output listing maintenance policies in the format of five columns:
        id, status, description, type and startdate

    Note:
        Using an API key that is not team scoped/restricted will output all maintenance policies.
        To only show maintenance policies for a team, use --profile or --api-key.

    Examples:
        opsgeniecli policy-maintenance list
        opsgeniecli --profile 'saas' policy-maintenance list

    """
    if nonexpired:
        result = context.obj['opsgenie'].list_maintenance(non_expired=True)
    elif past:
        result = context.obj['opsgenie'].list_maintenance(past=True)
    else:
        result = context.obj['opsgenie'].list_maintenance()
    format_table = PrettyTable(['id', 'status', 'description', 'type', 'startdate', 'enddate'])
    for item in result['data']:
        if 'endDate' in item['time']:
            end_date = ((pendulum.parse(item['time']['endDate'])).in_tz('Europe/Amsterdam')).to_datetime_string()
        else:
            end_date = None
        start_date = ((pendulum.parse(item['time']['startDate'])).in_tz('Europe/Amsterdam')).to_datetime_string()
        format_table.add_row([item['id'], item['status'], item['description'],
                              item['time']['type'], start_date, end_date])
    print(format_table)


@bootstrapper.group()
@click.pass_context
def heartbeat(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@heartbeat.command(cls=DefaultHelp, name='ping')
@click.option('--heartbeat-name', '--heartbeat_name', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_ping(context, heartbeat_name):
    """
    Function to ping a heartbeat

    Args:
        heartbeat_name: the name of the heartbeat

    Returns:
        The json output from the API on success, None otherwise

    """
    result = context.obj['opsgenie'].ping_heartbeat(heartbeat_name)
    print(json.dumps(result, indent=4, sort_keys=True))


@heartbeat.command(cls=DefaultHelp, name='get')
@click.option('--heartbeat-name', '--heartbeat_name', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_get(context, heartbeat_name):
    """
    Function to get more information about a single heartbeat

    Args:
        heartbeat_name: the name of the heartbeat

    Returns:
        The json output from the API on success, None otherwise

    """
    result = context.obj['opsgenie'].get_heartbeat(heartbeat_name)
    print(json.dumps(result, indent=4, sort_keys=True))


@heartbeat.command(name='list')
@click.pass_context
def heartbeat_list(context):
    """
    Function to get more information about a single heartbeat

    Returns:
        The json output from the API on success, None otherwise

    """
    result = context.obj['opsgenie'].list_heartbeats()
    print(json.dumps(result, indent=4, sort_keys=True))


@heartbeat.command(cls=DefaultHelp, name='enable')
@click.option('--heartbeat-name', '--heartbeat_name', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_enable(context, heartbeat_name):
    """
    Function to enable a single heartbeat

    Args:
        heartbeat_name: the name of the heartbeat

    Returns:
        The json output from the API on success, None otherwise

    """
    result = context.obj['opsgenie'].enable_heartbeat(heartbeat_name)
    print(json.dumps(result, indent=4, sort_keys=True))


@heartbeat.command(cls=DefaultHelp, name='disable')
@click.option('--heartbeat-name', '--heartbeat_name', help='The name of the heartbeat.')
@click.pass_context
def heartbeat_disable(context, heartbeat_name):
    """
    Function to enable a disable heartbeat

    Args:
        heartbeat_name: the name of the heartbeat

    Returns:
        The json output from the API on success, None otherwise

    """
    result = context.obj['opsgenie'].disable_heartbeat(heartbeat_name)
    print(json.dumps(result, indent=4, sort_keys=True))


@bootstrapper.group()
def teams():
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@teams.command(cls=DefaultHelp, name='get')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def teams_get(context, team_id, team_name):
    """
    Function to get more information about a team

    Args:
        team_id: the id of the team
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        Table output listing the team members of a team in the format of two columns: id's and usernames

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    result = context.obj['opsgenie'].get_team_by_id(team_id)
    format_table = PrettyTable([result['data']['name'] + ' ids', result['data']['name'] + ' usernames'])
    for item in result['data']['members']:
        format_table.add_row([item['user']['id'], item['user']['username']])
    print(format_table)


@teams.command(cls=DefaultHelp, name='logs')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def teams_logs(context, team_id, team_name):
    """
    Function to get the team logs

    Args:
        team_id: the id of the team
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        The json output from the API on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    result = context.obj['opsgenie'].get_team_logs_by_id(team_id)
    print(json.dumps(result, indent=4, sort_keys=True))


@teams.command(name='list')
@click.pass_context
def teams_list(context):
    """
    Function to list all the teams

    Returns:
        Table output listing the teams in the format of two columns: team id's and team names

    """
    result = context.obj['opsgenie'].list_teams()
    format_table = PrettyTable(['id', 'name', 'description'])
    for item in result['data']:
        format_table.add_row([item['id'], item['name'], item['description']])
    print(format_table)


@click.pass_context
def find_team_id_by_name(context, team_name):
    """Function to find a team_id, based on a search string that matches against a name and description."""
    teams_found = context.obj['opsgenie'].list_teams()
    filtered_teams = [x for x in teams_found['data'] if re.findall(rf"\b{team_name}\b", x['name'], re.IGNORECASE)
                      or re.findall(rf"\b{team_name}\b", x['description'], re.IGNORECASE)]
    if len(filtered_teams) == 1:
        return filtered_teams[0]['id']
    if len(filtered_teams) > 1:
        format_table = PrettyTable(['id', 'name', 'description'])
        for item in filtered_teams:
            format_table.add_row([item['id'], item['name'], item['description']])
        print(f'Multiple teams found for {team_name}: \n{format_table}')
        team_id = ""
        while len(team_id) < 30:
            team_id = click.prompt('Enter the id of the team you want', type=str)
        return team_id
    print(f'No teams found for {team_name}')
    return None


@click.pass_context
def find_team_name_by_name(context, team_name):
    """Function to find a team name, based on a search string that matches against name and description."""
    teams_found = context.obj['opsgenie'].list_teams()
    filtered_teams = [x for x in teams_found['data'] if re.findall(rf"\b{team_name}\b", x['name'], re.IGNORECASE)
                      or re.findall(rf"\b{team_name}\b", x['description'], re.IGNORECASE)]
    if len(filtered_teams) == 1:
        return filtered_teams[0]['name']
    if len(filtered_teams) > 1:
        format_table = PrettyTable(['id', 'name', 'description'])
        for item in filtered_teams:
            format_table.add_row([item['id'], item['name'], item['description']])
        print(f'Multiple teams found for {team_name}: \n{format_table}')
        team_name = ""
        while len(team_name) < 3:
            team_name = click.prompt('Enter the name of the team you want', type=str)
        return team_name
    print(f'No teams found for {team_name}')
    return None


@click.pass_context
def find_team_schedule_name_by_name(context, team_name):
    """Function to find a team schedule name, based on a search string that matches against team name."""
    schedules_found = context.obj['opsgenie'].list_schedules()
    teams_with_ownerteam_key = [x for x in schedules_found['data'] if 'ownerTeam' in x]
    filtered_schedules = [x for x in teams_with_ownerteam_key
                          if re.findall(rf"\b{team_name}\b", x['name'], re.IGNORECASE)
                          or re.findall(rf"\b{team_name}\b", x['ownerTeam']['name'], re.IGNORECASE)]
    if len(filtered_schedules) == 1:
        return filtered_schedules[0]['name']
    if len(filtered_schedules) > 1:
        format_table = PrettyTable(['schedule name', 'team name'])
        for item in filtered_schedules:
            format_table.add_row([item['name'], item['ownerTeam']['name']])
        print(f'Multiple teams found for {team_name}: \n{format_table}')
        team_schedule = ""
        while len(team_schedule) < 3:
            team_schedule = click.prompt('Enter the schedule name that you want', type=str)
        return team_schedule
    print(f'No teams found for {team_name}')
    return None


@bootstrapper.group()
def teams_routing_rules():
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@teams_routing_rules.command(cls=DefaultHelp, name='list')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def teams_routing_list(context, team_id, team_name):
    """
    Function to list all the information about the routing of alerts for a team

    Args:
        team_id: the id of the team
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        The json output from the API on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    result = context.obj['opsgenie'].get_routing_rules_by_id(team_id)
    print(json.dumps(result, indent=4, sort_keys=True))


@bootstrapper.group()
def escalations():
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@escalations.command(cls=DefaultHelp, name='get')
@click.option('--id', 'id_', cls=MutuallyExclusiveOption, mutually_exclusive=["escalation_name"])
@click.option('--escalation-name', '--escalation_name', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def escalations_get(context, id_, escalation_name):
    """
    Function to list to get more information about a single escalation

    Args:
        id: the id of the escalation
        escalation_name: the name of the escalation

    Returns:
        The json output from the API on success, None otherwise

    """
    if id_:
        result = context.obj['opsgenie'].get_escalations_by_id(id_)
    elif escalation_name:
        result = context.obj['opsgenie'].get_escalations_by_name(escalation_name)
    else:
        raise click.UsageError(
            "No escalation id or escalation name was specified. Use --id or --escalation_name.\n"
        )
    print(json.dumps(result, indent=4, sort_keys=True))


@escalations.command(name='list')
@click.pass_context
def escalations_list(context):
    """
    Function to list the escalation for each team

    Returns:
        Table output listing the teams in the format of three columns: id's, escalation name, and ownerTeam

    """
    result = context.obj['opsgenie'].list_escalations()
    format_table = PrettyTable(['id', 'name', 'ownerTeam'])
    for item in result['data']:
        format_table.add_row([item['id'], item['name'], item['ownerTeam']['name']])
    print(format_table)


@bootstrapper.group()
@click.pass_context
def schedules(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@schedules.command(cls=DefaultHelp, name='get')
@click.option('--id', 'id_', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.pass_context
def schedules_get(context, id_, team_name):
    """
    Function to get more information about a single schedule

    Args:
        id: the id of the escalation
        team_name: the name of the team, uses a regex to find the schedule name of the team

    Returns:
        The json output from the API on success, None otherwise

    """
    if not any([id_, team_name]):
        raise click.UsageError(
            "No schedule id or team name was specified. Use --id or --team-name.\n"
        )
    if id_:
        result = context.obj['opsgenie'].get_schedules_by_id(id_)
    if team_name:
        team_schedule_name = find_team_schedule_name_by_name(team_name)  # pylint: disable=no-value-for-parameter
        result = context.obj['opsgenie'].get_schedules_by_name(team_schedule_name)
    print(json.dumps(result, indent=4, sort_keys=True))


@schedules.command(name='timeline')
@click.option('--team-name', 'team_name', required=True)
@click.option('--expand', type=click.Choice(['base', 'forwarding', 'override'], case_sensitive=False))
@click.option('--interval', default=2)
@click.option('--intervalunit', default='months')
@click.option('--history', is_flag=True)
@click.pass_context
def schedules_timeline(context, team_name, history, expand, interval, intervalunit):  # pylint: disable=too-many-locals, too-many-arguments
    """
    Function to list the schedules for all teams

    Returns:
        Table output listing the schedules for all teams in the format of two columns: id and name

    """
    team_schedule_name = find_team_schedule_name_by_name(team_name)  # pylint: disable=no-value-for-parameter
    result = context.obj['opsgenie'].list_schedule_timeline_by_team_name(team_schedule_name, expand, interval, intervalunit)

    rotation = 'finalTimeline'
    if expand:
        rotation = f'{expand}Timeline'

    if not result['data'][f'{rotation}']['rotations']:
        print('No schedules were found, exiting..')
        return

    format_table = PrettyTable(['user', 'startdate', 'enddate'])
    print(f'\n On-call schedules - {rotation.lower()}')

    for item in result['data'][f'{rotation}']['rotations'][0]['periods']:
        if not history and pendulum.now().in_tz('UTC') > pendulum.parse(item['startDate']):
            continue
        else:
            start_dt = pendulum.parse(item['startDate']).in_tz('Europe/Amsterdam')
            end_dt = pendulum.parse(item['endDate']).in_tz('Europe/Amsterdam')
            format_table.add_row([item['recipient']['name'], f'{start_dt.format("ddd")} {start_dt.to_datetime_string()}', f'{end_dt.format("ddd")} {end_dt.to_datetime_string()}'])
    print(format_table)


@schedules.command(name='reshuffle')
@click.option('--team-name', 'team_name', required=True)
@click.option('--start-date', 'start_date', help='Example: 2020-03-20', required=True)
@click.option('--end-date', 'end_date', help='Example: 2020-06-27', required=True)
@click.option('--exclude-engineer', 'exclude_engineer')
@click.pass_context
def reshuffle_timeline(context, team_name, start_date, end_date, exclude_engineer):  # pylint: disable=too-many-locals, too-many-arguments
    """
    Function to reshuffle the schedules for all teams

    Returns:
        Table output listing the schedules for all teams in the format of two columns: id and name

    """
    ## get current schedule
    team_schedule_name = find_team_schedule_name_by_name(team_name)  # pylint: disable=no-value-for-parameter
    result = context.obj['opsgenie'].list_schedule_timeline_by_team_name(team_schedule_name, 'base', 2, 'months')

    ### get all engineers that will be on call
    unique_engineers = list(set([x['recipient']['name'] for x in result['data']['finalTimeline']['rotations'][0]['periods']]))
    if exclude_engineer:
        engineer_to_remove = [x for x in unique_engineers if re.findall(rf"\b{exclude_engineer}\b", x, re.IGNORECASE)]
        unique_engineers.remove(engineer_to_remove[0])

    #### STILL TO DO: what if more than 1 engineer to exclude?

    ## show old schedule, filtered down in time:
    format_table = PrettyTable(['user', 'startdate', 'enddate'])
    print(f'\n Current On-call schedule')
    start_date = pendulum.parse(start_date)
    end_date = pendulum.parse(end_date)
    all_start_dates = []
    for item in result['data'][f'finalTimeline']['rotations'][0]['periods']:
        item_date_value = pendulum.parse(item['startDate'])
        if start_date <= item_date_value and item_date_value < end_date:
            all_start_dates += [item_date_value]

            start_dt = pendulum.parse(item['startDate']).in_tz('Europe/Amsterdam')
            end_dt = pendulum.parse(item['endDate']).in_tz('Europe/Amsterdam')
            format_table.add_row([item['recipient']['name'], start_dt.to_datetime_string(), end_dt.to_datetime_string()])
    print(format_table)

    ## get all the days for that period
    format_table = PrettyTable(['user', 'startdate', 'enddate'])
    print(f'\n Proposed On-call schedule')
    copy_list_unique_engineers = list(unique_engineers)
    last_engineer = ""
    for date in all_start_dates:
        while True:
            randomNumber = random.randint(0, (len(copy_list_unique_engineers) - 1))
            engineer = copy_list_unique_engineers[randomNumber]
            if engineer != last_engineer:
                break

        start_ams_dt = date.in_tz('Europe/Amsterdam')
        stop_ams_dt = start_ams_dt.add(days=1)
        format_table.add_row([engineer, start_ams_dt.to_datetime_string(), stop_ams_dt.to_datetime_string()])

        last_engineer = format_table._rows[-1][0]
        del copy_list_unique_engineers[randomNumber]
        if not copy_list_unique_engineers:
            copy_list_unique_engineers = list(unique_engineers)
    print(format_table)

    answer = input("\nDo you want to override the old schedule with the proposed schedule? [y/n]: ").lower().strip()


@schedules.command(name='list')
@click.pass_context
def schedules_list(context):
    """
    Function to list the schedules for all teams

    Returns:
        Table output listing the schedules for all teams in the format of two columns: id and name

    """
    result = context.obj['opsgenie'].list_schedules()
    sortedlist = sorted(result['data'], key=itemgetter('name'))
    format_table = PrettyTable(['id', 'name'])
    for item in sortedlist:
        format_table.add_row([item['id'], item['name']])
    print(format_table)


@bootstrapper.group()
@click.pass_context
def logs(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@logs.command(cls=DefaultHelp, name='download')
@click.option('--marker', required=True)
@click.option('--download-path', '--download_path', required=True)
@click.option('--limit')
@click.pass_context
def logs_download(context, marker, limit, download_path):
    """
    Function to download logs

    Args:
        marker: download logs since a certain date, called the marker
        limit: maximum amount of files that are downloaded
        download_path: local location to store the log files

    Returns:
        String output on the progress and the log files at the specified download location

    """
    if limit and marker:
        result = context.obj['opsgenie'].get_logs_filenames(marker, limit)
    if marker and not limit:
        result = context.obj['opsgenie'].get_logs_filenames(marker)
    result = context.obj['opsgenie'].get_logs_filenames(id)
    total_count = len(result['data'])
    current_count = 1
    for file in result['data']:
        print(f"{current_count} - {total_count} - downloading {file['filename']}")
        download_url = context.obj['opsgenie'].get_logs_download_link(file['filename'])
        urllib.request.urlretrieve(download_url.text, f"{download_path}/{file['filename']}")
        current_count = current_count + 1


@bootstrapper.group()
@click.pass_context
def policy_notifications(context):  # pylint: disable=unused-argument
    """Sub-command for Opsgeniecli. This function is a placeholder to maintain the correct hierarchy for the cli"""
    pass


@policy_notifications.command(cls=DefaultHelp, name='enable')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"],
              help='Specify the team id for team-based notification policies instead of global policies.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Specify the name of the notification policy you want to enable.')
@click.option('--id', 'id_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["filter"],
              help='The id of the notification policy you want to enable.')
@click.pass_context
def policy_notifications_enable(context, team_id, team_name, filter_, id_):  # pylint: disable=too-many-branches
    """
    Function to enable notification policies

    Args:
        team_id: the id of the team, to enable a notification policy connected to that team
        team_name: alternative to team_id, uses regex to search for the team_id
        filter: a string to search on through existing notification policies. Can't be used together with --id.
        id: the id of the notification policy. Can't be used together with --filter.

    Returns:
        String output specifying which notification policy was enabled on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    if not any([filter_, id_]):
        raise click.UsageError("--id or --filter is required")
    if id_:
        result = context.obj['opsgenie'].enable_policy(id_, team_id)
        if result['result'] == 'Enabled':
            print(f"✓ - Notification policy {id_} enabled for team: '{context.obj.get('teamname')}'")
    if filter_:
        id_ = []
        filters_enabled = []
        notifications_policies = context.invoke(policy_notifications_list, team_id=team_id, print_output=False)
        for filt_ in filter_:
            filtered_results = [x for x in notifications_policies['data'] if (filt_).lower() in (x['name']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_enabled.append(filtered_results[0]['name'])
            else:
                print(f"\nMultiple notifications policies found for: '{filt_}'")
                filtered_format_table = PrettyTable(['id', 'name', 'type', 'enabled'])
                for result in filtered_results:
                    filtered_format_table.add_row([result['id'], result['name'], result['type'], result['enabled']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the notifications policy you want to enable', type=str)
                id_.append(temp_id)
                filters_enabled.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
        result = context.obj['opsgenie'].enable_policy(id_, team_id)
        if result['result'] == 'Enabled':
            print(f"✓ - Notifications policies enabled: {filters_enabled} for team: '{context.obj.get('teamname')}'")


@policy_notifications.command(cls=DefaultHelp, name='disable')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"],
              help='Specify the team id for team-based notification policies instead of global policies.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Specify the name of the notification policy you want to disable.')
@click.option('--id', 'id_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["filter"],
              help='The id of the notification policy you want to disable.')
@click.pass_context
def policy_notifications_disable(context, team_id, team_name, filter_, id_):  # pylint: disable=too-many-branches
    """
    Function to disable notification policies

    Args:
        team_id: the id of the team, to disable a notification policy connected to that team
        team_name: alternative to team_id, uses regex to search for the team_id
        filter: a string to search on through existing notification policies. Can't be used together with --id.
        id: the id of the notification policy. Can't be used together with --filter.

    Returns:
        String output specifying which notification policy was disabled on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    if not any([filter, id_]):
        raise click.UsageError("--id or --filter is required")
    if id_:
        result = context.obj['opsgenie'].disable_policy(id_, team_id)
        if result['result'] == 'Disabled':
            print(f"✓ - Notification policy {id_} disabled for team: '{context.obj.get('teamname')}'")
    if filter_:
        id_ = []
        filters_disabled = []
        notifications_policies = context.invoke(policy_notifications_list, team_id=team_id, print_output=False)
        for filt_ in filter_:
            filtered_results = [x for x in notifications_policies['data'] if (filt_).lower() in (x['name']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_disabled.append(filtered_results[0]['name'])
            else:
                print(f"\nMultiple notifications policies found for: '{filt_}'")
                filtered_format_table = PrettyTable(['id', 'name', 'type', 'enabled'])
                for result in filtered_results:
                    filtered_format_table.add_row([result['id'], result['name'], result['type'], result['enabled']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the notifications policy you want to disable', type=str)
                id_.append(temp_id)
                filters_disabled.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
        result = context.obj['opsgenie'].disable_policy(id_, team_id)
        if result['result'] == 'Disabled':
            print(f"✓ - Notifications policies disabled: {filters_disabled} for team: '{context.obj.get('teamname')}'")


@policy_notifications.command(cls=DefaultHelp, name='get')
@click.option('--id', 'id_', prompt=True)
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_notifications_get(context, id_, team_id, team_name):
    """
    Function to get more information about a single notification policy

    Args:
        id: the id of the notification policy
        team_id: the id of the team
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        The json output from the API on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    result = context.obj['opsgenie'].get_notification_policy(id_, team_id)
    print(json.dumps(result, indent=4, sort_keys=True))


@policy_notifications.command(cls=DefaultHelp, name='delete')
@click.option('--id', 'id_', multiple=True, help='The id of the notifications policy that will be deleted.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["filter"])
@click.option('--filter', 'filter_', multiple=True, cls=MutuallyExclusiveOption, mutually_exclusive=["id"],
              help='Filter based on the name of the notifications policy.')
@click.option('--all', 'all_', default=False, is_flag=True, help='Will remove all team notifications policies.',
              cls=MutuallyExclusiveOption, mutually_exclusive=["id"])
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"])
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.pass_context
def policy_notifications_delete(context, id_, team_id, team_name, all_, filter_):  # pylint: disable=too-many-branches, too-many-locals, too-many-arguments
    """
    Function to delete a single or all notifications policies

    Args:
        id: the id of the notification policies
        all: shows all notification policies that will be deleted, deletion follows after a prompts
        filter: a string to search on through existing notifications policies. Can't be used together with --id
        team_id: the id of the team to remove notifications policies for
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        String output specifying which notification policy id was removed and for which team on success, None otherwise

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    if id_:
        result = context.obj['opsgenie'].get_notification_policy(id_, team_id)
        if result.status_code == 200:
            print(f"✓ - notification policy {id_} deleted for team: {context.obj.get('teamname')}")
        else:
            print(result.text)
            sys.exit(1)
    elif all_:
        result = context.obj['opsgenie'].list_notification_policy(team_id)
        print("The following notifications policies will be deleted:")
        for item in result['data']:
            print(f"{item['id']} - {item['name']}")
        value = click.confirm('\nDo you want to continue?', abort=True)
        if value:
            for item in result['data']:
                result = context.obj['opsgenie'].delete_notification_policy(item['id'], team_id)
                if result.status_code == 200:
                    print(f"notifications policy {item['id']} deleted for team: {context.obj.get('teamname')}")
                else:
                    print(result.text)
                    sys.exit(1)
    elif filter_:
        id_ = []
        filters_deleted = []
        notifications_policies = context.obj['opsgenie'].list_notification_policy(team_id)
        for filt_ in filter_:
            filtered_results = [x for x in notifications_policies['data'] if (filt_).lower() in (x['name']).lower()]
            if len(filtered_results) == 1:
                id_.append(filtered_results[0]['id'])
                filters_deleted.append(filtered_results[0]['name'])
            else:
                print(f"\nMultiple notifications filters found for: '{filt_}'.")
                filtered_format_table = PrettyTable(['teamid', 'name', 'enabled'])
                for f_result in filtered_results:
                    filtered_format_table.add_row([f_result['id'],
                                                   f_result['name'],
                                                   f_result['enabled']])
                print(filtered_format_table)
                temp_id = ""
                while len(temp_id) < 30:
                    temp_id = click.prompt('Enter the id of the policy you want to delete', type=str)
                id_.append(temp_id)
                filters_deleted.append([item['name'] for item in filtered_results if item.get('id') == temp_id][0])
        del_result = context.obj['opsgenie'].delete_notification_policy(id_, team_id)
        if del_result.status_code == 200:
            print(f"✓ - Notifications policies deleted: {filters_deleted}")
    else:
        raise click.UsageError(
            "Use --id, --all or --filter to delete one or multiple notifications policies"
        )


@policy_notifications.command(cls=DefaultHelp, name='list')
@click.option('--team-id', 'team_id', cls=MutuallyExclusiveOption, mutually_exclusive=["team_name"],
              help='Specify the id of the team. The teamid from the config is used when no --team_id argument is given.')
@click.option('--team-name', 'team_name', default=False, cls=MutuallyExclusiveOption, mutually_exclusive=["team_id"])
@click.option('--non_expired', '--active', default=False, is_flag=True)
@click.pass_context
def policy_notifications_list(context, team_id, team_name, non_expired, print_output=True):
    """
    Function to list notifications policies

    Args:
        team_id: the id of the team
        non_expired: filters down notifications policies that are not closed and not acknowledged
        team_name: alternative to team_id, uses regex to search for the team_id

    Returns:
        Table output listing the notifications policies for a team in the format of two columns: id, name, and enabled

    """
    if team_name:
        team_id = find_team_id_by_name(team_name)  # pylint: disable=no-value-for-parameter
    elif {context.obj.get('teamid')} and not team_id:
        team_id = f"{context.obj.get('teamid')}"
    if not {context.obj.get('teamid')} and not team_id:
        raise click.UsageError(
            "Specify the team name or team id using --team_name or --team_id."
        )
    result = context.obj['opsgenie'].list_notification_policy(team_id)
    sortedlist = sorted(result['data'], key=itemgetter('name'))
    format_table = PrettyTable(['id', 'name', 'enabled'])
    for item in sortedlist:
        if non_expired:
            if item['enabled']:
                format_table.add_row([item['id'], item['name'], item['enabled']])
        else:
            format_table.add_row([item['id'], item['name'], item['enabled']])
    if print_output:
        print(format_table)
        return None
    return result


@bootstrapper.command()
@click.pass_context
def on_call(context):
    """
    Function to list the user on-call per team

    Returns:
        Table output listing the user on-call per team in the format of two columns: team, and EOD

    """
    result = context.obj['opsgenie'].get_users_on_call()
    table_eod = PrettyTable(['Team', 'EOD'])
    table_no_eod = PrettyTable(['Opsgenie teams without an EOD'])
    for item in result['data']:
        if item['onCallParticipants']:
            table_eod.add_row([item['_parent']['name'], item['onCallParticipants'][0]['name']])
        else:
            table_no_eod.add_row([item['_parent']['name']])
    print(table_no_eod)
    print(table_eod)


@bootstrapper.command(cls=DefaultHelp, name='override')
@click.option('--start-date', 'start_date', cls=MutuallyExclusiveOption, mutually_exclusive=["hours"],
              help='Example: 2019-03-15T14:34:09.')
@click.option('--end-date', 'end_date', cls=MutuallyExclusiveOption, mutually_exclusive=["hours"],
              help='Example: 2019-03-15T15:34:09')
@click.option('--team-name', 'team_name')
@click.option('--engineer', help='Name the username of the engineer who will be on call.')
@click.option('--hours', type=int, help='Amount of hours to set the override for.')
@click.pass_context
def override(context, team_name, engineer, hours, start_date, end_date):  # pylint: disable=too-many-arguments
    """
    Function to override the on-call schedule with another user

    Args:
        team_name: the name of the team
        engineer: the user who take the on-call duty
        hours: sets the start date to now and the end date to now + the amount of hours specified
        start_date: start date of the override
        end_date: end date of the override

    Returns:
        String output specifying which users will be on-call and the start- and end date on success, None otherwise

    Examples:
    $ opsgeniecli.py override --team_name <TEAMSCHEDULE> --engineer <ENGINEER> --hours <INTEGER>
    $ opsgeniecli.py override --team_name <TEAMSCHEDULE> --engineer <ENGINEER>
    --start-date 2019-03-15T14:34:09 --end-date 2019-03-15T15:34:09

    """
    if team_name:
        team_name = find_team_schedule_name_by_name(team_name)  # pylint: disable=no-value-for-parameter
    if hours:
        result = context.obj['opsgenie'].set_override_for_hours(team_name, engineer, hours)
        start_dt = pendulum.now(tz='Europe/Amsterdam')
        end_dt = start_dt.add(hours=hours)
    elif start_date and end_date:
        start_dt = pendulum.parse(start_date, tz='Europe/Amsterdam').in_tz('UTC')
        end_dt = pendulum.parse(end_date, tz='Europe/Amsterdam').in_tz('UTC')
        result = context.obj['opsgenie'].set_override_scheduled(team_name, start_dt.format('YYYY-MM-DDTHH:mm:ss\Z'), end_dt.format('YYYY-MM-DDTHH:mm:ss\Z'), engineer)
    else:
        raise click.UsageError(
            "Specify the amount of hours you want to override the schedule (using --hours), \
            or specify a schedule (using --start_date and --end_date)."
        )
    if result.status_code == 201:
        start = start_dt.to_datetime_string()
        end = end_dt.to_datetime_string()
        print(f"✓ - override set to {engineer} between {start} and {end}")
    else:
        print(result.text)


def main():
    """Main entry point of tool"""
    bootstrapper(obj={})  # pylint: disable=no-value-for-parameter, unexpected-keyword-arg


if __name__ == '__main__':
    main()
