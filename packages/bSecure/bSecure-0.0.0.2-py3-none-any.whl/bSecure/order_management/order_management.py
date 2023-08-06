from json import loads, dumps
from requests import post, get
from bSecure.helpers.constants import constants


class Order:

    def __init__(self, header=None, order_details=None):
        setattr(self, constants.get_key_header(), header)
        setattr(self, constants.get_key_order_details(), order_details)

    def set_order(self, order_details, header):
        setattr(self, constants.get_key_order_details(), order_details)
        setattr(self, constants.get_key_header(), header)
        return getattr(self, constants.get_key_order_details())

    def create_order(self):
        url = constants.get_create_order_url()
        dump_data = dumps(getattr(self, constants.get_key_order_details()))

        response = post(
            url,
            data=dump_data,
            headers=getattr(self, constants.get_key_header())
        )
        content = loads(response.content)
        return content

    def update_order(self):
        url = constants.get_update_order_url()
        print(getattr(self, constants.get_key_header()))
        response = post(
            url,
            data=getattr(self, constants.get_key_order_details()),
            headers=getattr(self, constants.get_key_header())
        )
        content = loads(response.content)
        return content

    def status_order(self, reference_id):
        url = constants.get_status_order_url()
        response = get(
            url,
            data={'code': reference_id},
            headers=getattr(self, constants.get_key_header())
        )
        return loads(response.content)
