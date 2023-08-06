import os
import requests
from OAuth2 import OAuth2
from destiny_enums import MembershipType

API_ROOT_PATH = "https://www.bungie.net/Platform"


class BungieAPI:
    def __init__(self, api_key: str):
        self.__HEADERS = {"X-API-Key": api_key, "Authorization": "Bearer "}
        os.environ["X-API-KEY"] = api_key

    @staticmethod
    def start_oauth2(client_id, client_secret):
        OAuth2(client_id, client_secret)

    def __renew_headers(self):
        self.__HEADERS["Authorization"] = "Bearer " + os.getenv("ACCESS_TOKEN")

    def get_bungie_user_by_id(self, membership_id: str) -> dict:
        api_call = requests.get(API_ROOT_PATH + "/User/GetBungieNetUserById/" + membership_id + "/",
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def search_users(self, query_string: str) -> dict:
        api_call = requests.get(API_ROOT_PATH + "/User/SearchUsers/?q=" + query_string, headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_profile(self, membership_type: MembershipType, destiny_membership_id: str) -> dict:
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/" + str(membership_type.value) + "/Profile/"
                                + destiny_membership_id + "/?components=100", headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_clan_weekly_reward_state(self, group_id: str) -> dict:
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/Clan/" + group_id + "/WeeklyRewardState/",
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_collectible_node_details(self, membership_type: MembershipType, destiny_membership_id: str,
                                     character_id: int,
                                     collectible_presentation_node_hash: int, components: str) -> dict:
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/" + str(membership_type.value) + "/Profile/"
                                + destiny_membership_id + "/Character/" + str(character_id)
                                + "/Collectibles/" + str(
            collectible_presentation_node_hash) + "/?components=" + components,
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_linked_profiles(self, membership_type: MembershipType, membership_id: str):
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/" + str(membership_type.value) + "/Profile/"
                                + membership_id + "/LinkedProfiles/", headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_character(self, membership_type: MembershipType, destiny_membership_id: str, character_id: int) -> dict:
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/" + str(membership_type.value) + "/Profile/"
                                + destiny_membership_id + "/Character/" + str(character_id) + "/?components=200",
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_vendor(self, membership_type: MembershipType, destiny_membership_id: str, character_id: int,
                   vendor_hash: str,
                   components: str):
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/" + str(membership_type.value) + "/Profile/"
                                + destiny_membership_id + "/Character/" + str(character_id)
                                + "/Vendors/" + vendor_hash + "/?components=" + components, headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_vendors(self, membership_type: MembershipType, destiny_membership_id: str, character_id: int,
                    components: str):
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/" + str(membership_type.value) + "/Profile/"
                                + destiny_membership_id + "/Character/" + str(character_id)
                                + "/Vendors/?components=" + components, headers=self.__HEADERS)
        return (api_call.json())['Response']

    def manifest(self, entity_type: str, hash_identifier: str) -> dict:
        """ Manifests the specified entity. Returns general information about the entity, see API documentation for more details:
            https://bungie-net.github.io/#Destiny2.GetDestinyEntityDefinition

        :param entity_type: The type of entity for whom you would like results. These correspond to the entity's
            definition contract name. See api.ini/Definitions
        :param hash_identifier: The hash identifier for the specific Entity you want returned.
        :return: dict
        """
        api_call = requests.get(API_ROOT_PATH + "/Destiny2/Manifest/" + entity_type + "/" + hash_identifier,
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def get_public_vendors(self, components: str) -> dict:
        """Returns information on the requested vendor, see API documentation for more details:
            https://bungie-net.github.io/#Destiny2.GetPublicVendors

        :param vendor_hash: The hash identifier for the specific Vendor you want returned.
        :param components: See api.ini/Components
        :return: dict
        """
        api_call = requests.get(API_ROOT_PATH + '/Destiny2//Vendors/?components=' + components,
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def search_entities(self, entity_type: str, search_term: str) -> dict:
        """Searches for the specified entity in the API, see API documentation for more details:
            https://bungie-net.github.io/#Destiny2.SearchDestinyEntities

        :param entity_type: The type of entity for whom you would like results. These correspond to the entity's
            definition contract name. See api.ini/Definitions
        :param search_term: The string to use when searching for Destiny entities.
        :return: dict
        """
        api_call = requests.get(API_ROOT_PATH + '/Destiny2/Armory/Search/' + entity_type + "/" + search_term + "/",
                                headers=self.__HEADERS)
        return (api_call.json())['Response']

    def search_destiny_player(self, membership_type: MembershipType, display_name: str):
        api_call = requests.get(
            API_ROOT_PATH + '/Destiny2/SearchDestinyPlayer/' + str(membership_type.value) + "/" + display_name + "/",
            headers=self.__HEADERS)
        return (api_call.json())['Response']
