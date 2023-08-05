"""
tasks
"""

import logging

from concurrent.futures import ThreadPoolExecutor, as_completed

from allianceauth.eveonline.models import EveCharacter
from fleetfinder.providers import esi
from fleetfinder.models import Fleet, FleetInformation

from esi.models import Token

from celery import shared_task

from django.utils import timezone


logger = logging.getLogger(__name__)


@shared_task
def open_fleet(character_id, motd, free_move, name, groups):
    """
    open a fleet
    :param character_id:
    :param motd:
    :param free_move:
    :param name:
    :param groups:
    :return:
    """

    required_scopes = ["esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"]

    esi_client = esi.client
    token = Token.get_token(character_id, required_scopes)

    fleet_result = esi_client.Fleets.get_characters_character_id_fleet(
        character_id=token.character_id, token=token.valid_access_token()
    ).result()
    fleet_id = fleet_result.pop("fleet_id")
    fleet_role = fleet_result.pop("role")

    if fleet_id is None or fleet_role is None or fleet_role != "fleet_commander":
        return

    fleet_commander = EveCharacter.objects.get(character_id=token.character_id)

    fleet = Fleet(
        fleet_id=fleet_id,
        created_at=timezone.now(),
        motd=motd,
        is_free_move=free_move,
        fleet_commander=fleet_commander,
        name=name,
    )
    fleet.save()
    fleet.groups.set(groups)

    esi_fleet = {"is_free_move": free_move, "motd": motd}
    esi_client.Fleets.put_fleets_fleet_id(
        fleet_id=fleet_id, token=token.valid_access_token(), new_settings=esi_fleet
    ).result()


@shared_task
def send_fleet_invitation(character_ids, fleet_id):
    """
    send a fleet invitation through the eve client
    :param character_ids:
    :param fleet_id:
    """

    required_scopes = ["esi-fleets.write_fleet.v1"]
    fleet = Fleet.objects.get(fleet_id=fleet_id)
    fleet_commander_token = Token.get_token(
        fleet.fleet_commander.character_id, required_scopes
    )
    _processes = []

    with ThreadPoolExecutor(max_workers=50) as ex:
        for _chracter_id in character_ids:
            _processes.append(
                ex.submit(
                    send_invitation,
                    character_id=_chracter_id,
                    fleet_commander_token=fleet_commander_token,
                    fleet_id=fleet_id,
                )
            )

    for item in as_completed(_processes):
        _ = item.result()


@shared_task
def send_invitation(character_id, fleet_commander_token, fleet_id):
    """
    open the fleet invite window in the eve client
    :param character_id:
    :param fleet_commander_token:
    :param fleet_id:
    """

    esi_client = esi.client
    invitation = {"character_id": character_id, "role": "squad_member"}

    esi_client.Fleets.post_fleets_fleet_id_members(
        fleet_id=fleet_id,
        token=fleet_commander_token.valid_access_token(),
        invitation=invitation,
    ).result()


@shared_task
def check_fleet_adverts():
    """
    scheduled task
    check for fleets adverts
    """

    required_scopes = ["esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"]

    esi_client = esi.client

    fleets = Fleet.objects.all()
    for fleet in fleets:
        token = Token.get_token(fleet.fleet_commander.character_id, required_scopes)

        try:
            fleet_result = esi_client.Fleets.get_characters_character_id_fleet(
                character_id=token.character_id, token=token.valid_access_token()
            ).result()

            fleet_id = fleet_result["fleet_id"]

            if fleet_id != fleet.fleet_id:
                fleet.delete()
        except Exception as e:
            if e.status_code == 404:  # 404 means the character is not in a fleet
                fleet.delete()
                logger.info("Character is not in a fleet - fleet advert removed")


@shared_task
def get_fleet_composition(fleet_id):
    """
    getting the fleet composition
    :param fleet_id:
    :return:
    """

    required_scopes = ["esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"]

    esi_client = esi.client

    fleet = Fleet.objects.get(fleet_id=fleet_id)
    token = Token.get_token(fleet.fleet_commander.character_id, required_scopes)
    fleet_infos = esi_client.Fleets.get_fleets_fleet_id_members(
        fleet_id=fleet_id, token=token.valid_access_token()
    ).result()

    characters = {}
    systems = {}
    ship_type = {}

    for member in fleet_infos:
        characters[member["character_id"]] = ""
        systems[member["solar_system_id"]] = ""
        ship_type[member["ship_type_id"]] = ""

    ids = []
    ids.extend(list(characters.keys()))
    ids.extend(list(systems.keys()))
    ids.extend(list(ship_type.keys()))

    ids_to_name = esi_client.Universe.post_universe_names(ids=ids).result()

    for member in fleet_infos:
        index = [x["id"] for x in ids_to_name].index(member["character_id"])
        member["character_name"] = ids_to_name[index]["name"]

    for member in fleet_infos:
        index = [x["id"] for x in ids_to_name].index(member["solar_system_id"])
        member["solar_system_name"] = ids_to_name[index]["name"]

    for member in fleet_infos:
        index = [x["id"] for x in ids_to_name].index(member["ship_type_id"])
        member["ship_type_name"] = ids_to_name[index]["name"]

    aggregate = get_fleet_aggregate(fleet_infos)

    differential = dict()

    for key, value in aggregate.items():
        fleet_info_agg = FleetInformation.objects.filter(
            fleet__fleet_id=fleet_id, ship_type_name=key
        )

        if fleet_info_agg.count() > 0:
            differential[key] = value - fleet_info_agg.latest("date").count
        else:
            differential[key] = value

        FleetInformation.objects.create(fleet=fleet, ship_type_name=key, count=value)

    return FleetViewAggregate(fleet_infos, aggregate, differential)


@shared_task
def get_fleet_aggregate(fleet_infos):
    """
    getting aggregate numbers for fleet composition
    :param fleet_infos:
    :return:
    """

    counts = dict()

    for member in fleet_infos:
        type_ = member.get("ship_type_name")

        if type_ in counts:
            counts[type_] += 1
        else:
            counts[type_] = 1

    return counts


class FleetViewAggregate(object):
    """
    helper class
    """

    def __init__(self, fleet, aggregate, differential):
        self.fleet = fleet
        self.aggregate = aggregate
        self.differential = differential
