import json
import requests
import warnings

version = '0.0.1'
user_agent = 'Python/ExchangeApiClient/' + version
verticals = { 'education', 'finance', 'insurance', 'travel' }

class RequestError(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response

class Client:
    def __init__(self, vertical, api_token, base_url=None, verify=True):
        if vertical not in verticals:
            raise ValueError('invalid vertical')

        if base_url is None:
            base_url = 'https://{vertical}-api.mediaalpha.com'.format(vertical=vertical)

        self.vertical = vertical
        self.api_token = api_token
        self.base_url = base_url
        self.verify=verify

    def _handle_request(self, requests_method, url, request_body=None):
        response = requests_method(
            url,
            json=request_body,
            headers={'Content-Type': 'application/json', 'User-Agent':user_agent, 'X-API-TOKEN':self.api_token},
            verify=self.verify,
        )
        if response.status_code == 401:
            raise RequestError(response.text, response)

        elif response.status_code != 200:
            raise RequestError('invalid status code: ' + str(response.status_code), response)

        return response.json()

    def get_object(self, object_url):
        return self._handle_request(requests.get, object_url)

    def get_advertiser(self, advertiser_id):
        url = self.base_url + '/' + str(advertiser_id)
        return self.get_object(url)

    def get_campaign(self, advertiser_id, campaign_id):
        url = self.base_url + '/' + str(advertiser_id) + '/campaigns/' + str(campaign_id)
        return self.get_object(url)

    def get_ad_group(self, advertiser_id, campaign_id, ad_group_id):
        url = self.base_url + '/' + str(advertiser_id) + '/campaigns/' + str(campaign_id) + '/ad-groups/' + str(ad_group_id)
        return self.get_object(url)

    def get_campaign_channel(self, advertiser_id, campaign_id, channel_id):
        url = self.base_url + '/' + str(advertiser_id) + '/campaigns/' + str(campaign_id) + '/channels/' + str(channel_id)
        return self.get_object(url)

    def patch_object(self, url, patch):
        return self._handle_request(requests.patch, url, patch)

    def patch_campaign(self, advertiser_id, campaign_id, patch):
        url = self.base_url + '/' + str(advertiser_id) + '/campaigns/' + str(campaign_id)
        return self.patch_object(url, patch)

    def patch_ad_group(self, advertiser_id, campaign_id, ad_group_id, patch):
        url = self.base_url + '/' + str(advertiser_id) + '/campaigns/' + str(campaign_id) + '/ad-groups/' + ad_group_id
        return self.patch_object(url, patch)

    def patch_campaign_channel(self, advertiser_id, campaign_id, channel_id, patch):
        url = self.base_url + '/' + str(advertiser_id) + '/campaigns/' + str(campaign_id) + '/channels/' + channel_id
        return self.patch_object(url, patch)

    def sync_campaign(self, campaign, advertiser_id=None, campaign_id=None, campaign_url=None):
        if campaign_url is None:
            if advertiser_id is None or campaign_id is None:
                raise ValueError('advertiser_id and campaign_id must be specified when campaign_url is not specified')
            campaign_url = self.base_url + '/' + str(advertiser_id) + '/campaigns/' + str(campaign_id)

        x_campaign = self.get_object(campaign_url)

        return self._sync_campaign(campaign_url, campaign, x_campaign) + \
            self._sync_campaign_ad_groups(campaign_url, campaign, x_campaign) + \
            self._sync_campaign_channels(campaign_url, campaign, x_campaign)

    def _sync_campaign(self, campaign_url, campaign, x_campaign):
        patch = {}
        for field in ('status', 'schedule_time_zone'):
            if field in campaign and x_campaign[field] != campaign[field]:
                patch[field] = campaign[field]
        for field in ('schedule',):
            if field in campaign and json.dumps(x_campaign[field]) != json.dumps(campaign[field]):
                patch['schedule'] = campaign['schedule']
        if len(patch) == 0:
            return False

        self.patch_object(campaign_url, patch)
        return 1

    def _sync_campaign_ad_groups(self, campaign_url, campaign, x_campaign):
        if 'ad_groups' not in campaign or not(isinstance(campaign['ad_groups'], dict)):
            return 0

        x_ad_groups = {}
        for x_ad_group in x_campaign['ad_groups']:
            x_ad_groups[x_ad_group['ad_group']] = x_ad_group

        updated = 0
        for ad_group_name in campaign['ad_groups']:
            if ad_group_name not in x_ad_groups:
                warnings.warn('ad group not found: ' + str(ad_group_name))
                continue

            ad_group = campaign['ad_groups'][ad_group_name]
            x_ad_group = x_ad_groups[ad_group_name]

            patch = {}
            for field in ('bid',):
                if field in ad_group and float(x_ad_group[field]) != float(ad_group[field]):
                    patch[field] = ad_group[field]

            if len(patch) == 0:
                continue 

            self.patch_object(x_ad_group['url'], patch)
            updated += 1

        return updated

    def _sync_campaign_channels(self, campaign_url, campaign, x_campaign):
        if 'channels' not in campaign or not(isinstance(campaign['channels'], dict)):
            return 0

        x_channels = {}
        for x_channel in x_campaign['channels']:
            x_channels[x_channel['url']] = x_channel

        updated = 0
        for channel_id in campaign['channels']:
            campaign_channel_url = campaign_url + '/channels/' + str(channel_id)
            if campaign_channel_url not in x_channels:
                warnings.warn('channel not found: ' + str(channel_id))
                continue

            channel = campaign['channels'][channel_id]
            x_channel = x_channels[campaign_channel_url]

            if x_channel['status'] == 'disabled':
                x_channel['multiplier'] = 0

            patch = {}
            for field in ('status',):
                if field in channel and x_channel[field] != channel[field]:
                    patch[field] = channel[field]

            for field in ('multiplier',):
                if field in channel and float(x_channel[field]) != float(channel[field]):
                    patch[field] = channel[field]

            if len(patch) == 0:
                continue 

            self.patch_object(campaign_channel_url, patch)
            updated += 1

        return updated
