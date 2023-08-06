"""
spotilyzer create-candidates subcommand
"""

# system imports
import collections
import datetime
import math
import heapq
import sys
import textwrap

# 3rd party imports
import tabulate

# project imports
from .base import SubCommand
from .utils.cli import options, posint, csv
from .utils.paths import find_seeds_file
from .utils.stats import quality
from .json.seeds import load_seeds, SEEDS_KEY, GROUP_KEY, CANDIDATES_KEY, \
    CANDIDATE_NAME_KEY, INSTANCE_TYPES_KEY
from .json.candidates import save_candidates, REGION_KEY, GROUPS_KEY, \
    GROUP_NAME_KEY, MEM_CORE_RATIO_KEY, PRICE_KEY, RESOURCES_KEY, \
    AVG_CORES_KEY, AVG_MEMORY_KEY, MIN_CORES_KEY, MIN_MEMORY_KEY, \
    CANDIDATE_POOLS_KEY, INSTANCE_TYPE_KEY, AVAILABILITY_ZONES_KEY, \
    META_DATA_KEY, TIMESTAMP_KEY, DURATION_KEY, MINPOOL_KEY

# constants
_DESCRIPTION = "create candidate spot fleets from seeds"
_REGION_OPT = 'region'
_AVAILABILITY_ZONES_OPT = 'availability-zones'
_DURATION_OPT = 'duration'
_DURATION_DEFAULT = 90
_MINPOOL_OPT = 'minpool'
_MINPOOL_DEFAULT = 20
_SEEDS_OPT = 'seeds'
_CANDIDATES_ARG = 'candidates'
_COUNT_KEY = 'count'
_TOTAL_KEY = 'total'
_SQUARE_TOTAL_KEY = 'square-total'
_SPOT_FLEETS_KEY = 'spot-fleets'
_AVG_MEM_CORE_RATIO_KEY = 'avg-mem-core-ratio'
_FLEETS_KEY = 'fleets'
_PRICE_KEY = 'price'
_MIN_STAT_COUNT = 30
_AVG_KEY = 'avg'
_STDDEV_KEY = 'stddev'
_RESOURCES_KEY = 'resources'
_AVG_CORES_KEY = 'avg-cores'
_AVG_MEM_KEY = 'avg-mem'
_MIN_CORES_KEY = 'min-cores'
_MIN_MEM_KEY = 'min-mem'
_COV_LEVEL = 0.20
_MB_PER_GB = 1024
_TABLE_HEADER = ('Candidate', 'Price', 'Instance Type', 'Availability Zones')
_TABLE_FORMAT = 'grid'
_TABLE_FLOAT_FORMAT = '.3f'


class CreateCandidates(SubCommand):
    """
    create-candidates subcommand
    """

    name = 'create-candidates'

    @classmethod
    def add_parser(cls, subparsers):
        """
        Add create-candidates subcommand parser.
        :param subparsers: object to attach parser
        :return: None
        """
        parser = subparsers.add_parser(cls.name, description=_DESCRIPTION,
                                       help=_DESCRIPTION)
        parser.add_argument(*options(_REGION_OPT), default=None,
                            help="AWS region to query (default is from "
                                 "configuration or AWS_DEFAULT_REGION)")
        parser.add_argument(*options(_AVAILABILITY_ZONES_OPT), type=csv,
                            default=None,
                            help="comma-separated list of availability zones "
                                 "(defaults are all availability zones in the "
                                 "target region)")
        parser.add_argument(*options(_DURATION_OPT), type=posint,
                            default=_DURATION_DEFAULT,
                            help="number of days in price history (default "
                                 f"{_DURATION_DEFAULT})")
        parser.add_argument(*options(_MINPOOL_OPT), type=posint,
                            default=_MINPOOL_DEFAULT,
                            help="minimum number of pools in spot fleet "
                                 f"(default {_MINPOOL_DEFAULT})")
        parser.add_argument(*options(_SEEDS_OPT), default=None,
                            help="JSON file with seed instance types (if not "
                                 "specified use user's copy or the package "
                                 "data)")
        parser.add_argument(_CANDIDATES_ARG,
                            help="JSON file for candidates output")

    def run(self):
        """
        Create candidates from a seed file and spot price history data.
        :return: None
        """
        self._set_region()
        seeds = self._get_seeds()
        data = self._start(seeds)
        timestamp = self._collect_data(data)
        stats = self._compute_stats(data)
        candidates = self._select_candidates(stats)
        self._price_candidates(candidates)
        self._get_candidate_resources(candidates)
        results = self._save_candidates(candidates, timestamp)
        self._display_results(results)

    def _set_region(self):
        region = self.getarg(_REGION_OPT)
        if region is not None:
            self.reconnect(region)

    def _get_seeds(self):
        seeds_file = self.getarg(_SEEDS_OPT)
        if seeds_file is None:
            seeds_file = find_seeds_file()
        return load_seeds(seeds_file)

    def _start(self, seeds):
        availability_zones = self.getarg(_AVAILABILITY_ZONES_OPT)
        if availability_zones is None:
            availability_zones = self._get_azs()
        else:
            self._validate_azs(availability_zones)
        return self._get_instance_type_offerings(seeds, availability_zones)

    def _get_azs(self):
        response = self.client.describe_availability_zones()
        return [a['ZoneName'] for a in response['AvailabilityZones']]

    def _validate_azs(self, availability_zones):
        valid_azs = set(self._get_azs())
        invalid_azs = set(availability_zones) - valid_azs
        if len(invalid_azs) > 0:
            raise ValueError("invalid availability zone(s) for region "
                             f"{self.client.meta.region_name}: "
                             f"{','.join(invalid_azs)}")

    def _get_instance_type_offerings(self, seeds, availability_zones):
        data = {}
        for seed in seeds[SEEDS_KEY]:
            group_data = data[seed[GROUP_KEY]] = {}
            instance_type_map = {}
            paginator \
                = self.client.get_paginator('describe_instance_type_offerings')
            for candidate in seed[CANDIDATES_KEY]:
                instance_type_data \
                    = group_data[candidate[CANDIDATE_NAME_KEY]] = {}
                for instance_type in candidate[INSTANCE_TYPES_KEY]:
                    instance_type_map[instance_type] \
                        = instance_type_data[instance_type] \
                        = collections.defaultdict(dict)
            for response in paginator.paginate(
                LocationType='availability-zone',
                Filters=[
                    {
                        'Name': 'location',
                        'Values': availability_zones
                    },
                    {
                        'Name': 'instance-type',
                        'Values': list(instance_type_map.keys())
                    }
                ]
            ):
                for offering in response['InstanceTypeOfferings']:
                    instance_type_map[
                        offering['InstanceType']
                    ][
                        offering['Location']
                    ] = {
                        _COUNT_KEY: 0,
                        _TOTAL_KEY: 0.0,
                        _SQUARE_TOTAL_KEY: 0.0
                    }
            del_list = [
                (c, i)
                for c, g in group_data.items()
                for i, a in g.items()
                if len(a) == 0
            ]
            if len(del_list) > 0:
                print()
                print(
                    textwrap.fill(
                        "[warning]: the following instance types are not "
                        "available in this region: "
                        f"{', '.join(d[1] for d in del_list)}"
                    ), '\n'
                )
                for del_item in del_list:
                    del group_data[del_item[0]][del_item[1]]
        return data

    def _collect_data(self, data):
        print("collecting spot price data...")
        duration = self.getarg(_DURATION_OPT)
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=duration)
        az_map = collections.defaultdict(dict)
        for group_data in data.values():
            for instance_type_data in group_data.values():
                for instance_type, az_data in instance_type_data.items():
                    for az, data_rec in az_data.items():
                        az_map[az][instance_type] = data_rec
        paginator = self.client.get_paginator('describe_spot_price_history')
        for az, az_map_data in az_map.items():
            for response in paginator.paginate(
                StartTime=start,
                EndTime=end,
                AvailabilityZone=az,
                InstanceTypes=list(az_map_data.keys()),
                ProductDescriptions=["Linux/UNIX (Amazon VPC)"]
            ):
                for history_rec in response['SpotPriceHistory']:
                    data_rec = az_map_data[
                        history_rec['InstanceType']
                    ]
                    data_rec[_COUNT_KEY] += 1
                    price = float(history_rec['SpotPrice'])
                    data_rec[_TOTAL_KEY] += price
                    data_rec[_SQUARE_TOTAL_KEY] += price * price
            record_count = sum(d[_COUNT_KEY] for d in az_map_data.values())
            print(f"  {az}: {record_count} records")
        return end

    def _compute_stats(self, data):
        stats = {}
        del_list = []
        for group, group_data in data.items():
            group_stats = stats[group] = {}
            for candidate, instance_type_data in group_data.items():
                instance_type_stats = group_stats[candidate] = {}
                del_set = set()
                for instance_type, az_data in instance_type_data.items():
                    az_stats = instance_type_stats[instance_type] = {}
                    for az, data_rec in az_data.items():
                        count = data_rec[_COUNT_KEY]
                        if count < _MIN_STAT_COUNT:
                            del_set.add(instance_type)
                            continue
                        total = data_rec[_TOTAL_KEY]
                        avg = total / count
                        variance = (data_rec[_SQUARE_TOTAL_KEY]
                                    - total * avg) / (count - 1)
                        if variance < 0.0:
                            stddev = 0.0
                        else:
                            stddev = math.sqrt(variance)
                        az_stats[az] = {
                            _AVG_KEY: avg,
                            _STDDEV_KEY: stddev
                        }
                for instance_type in del_set:
                    del instance_type_stats[instance_type]
                del_list.extend(del_set)
            self._cleanup_dict(group_stats)
        self._cleanup_dict(stats)
        if len(stats) == 0:
            raise RuntimeError("duration too short to collect any "
                               "statistically significant samples")
        if len(del_list) > 0:
            print()
            print(
                textwrap.fill(
                        "[warning]: removed the following instance types "
                        "because of insufficient data: "
                        f"{', '.join(del_list)}"
                ), '\n'
            )
        return stats

    @staticmethod
    def _cleanup_dict(stats_dict):
        del_list = [k for k,v in stats_dict.items() if len(v) == 0]
        for key in del_list:
            del stats_dict[key]

    def _select_candidates(self, stats):
        print("selecting candidates...")
        minpool = self.getarg(_MINPOOL_OPT)
        candidates = {}
        for group, group_stats in stats.items():
            spot_candidates = {}
            candidates[group] = {
                _SPOT_FLEETS_KEY: spot_candidates,
                _AVG_MEM_CORE_RATIO_KEY: None
            }
            for candidate, instance_type_stats in group_stats.items():
                fleet_candidates = {}
                spot_candidates[candidate] = {
                    _FLEETS_KEY: fleet_candidates,
                    _RESOURCES_KEY: {},
                    _PRICE_KEY: None
                }
                count = sum(len(a) for a in instance_type_stats.values())
                if count <= minpool:
                    fleet_candidates.update(instance_type_stats)
                    continue
                heap = []
                count = 0
                for instance_type, az_stats in instance_type_stats.items():
                    dyn_price = sum(
                        i[_AVG_KEY]+i[_STDDEV_KEY]
                        for i in az_stats.values()
                    ) / len(az_stats)
                    heapq.heappush(heap, (dyn_price, instance_type))
                n = minpool - count
                while n > 0:
                    item = heapq.heappop(heap)
                    pool_stat = instance_type_stats[item[1]]
                    fleet_candidates[item[1]] = pool_stat
                    n -= len(pool_stat)
        return candidates

    @staticmethod
    def _price_candidates(candidates):
        for candidate_record in candidates.values():
            for spot_candidate in candidate_record[_SPOT_FLEETS_KEY].values():
                total = sum(
                    s[_AVG_KEY]
                    for p in spot_candidate[_FLEETS_KEY].values()
                    for s in p.values()
                )
                count = sum(
                    len(p) for p in spot_candidate[_FLEETS_KEY].values()
                )
                spot_candidate[_PRICE_KEY] = total / count

    def _get_candidate_resources(self, candidates):
        print("getting candidate resources...")
        paginator = self.client.get_paginator('describe_instance_types')
        for group, candidate_record in candidates.items():
            spot_fleet_count = 0
            mem_core_ratio_total = 0.0
            mem_core_ratio_square_total = 0.0
            for candidate, spot_candidate in candidate_record[
                _SPOT_FLEETS_KEY
            ].items():
                count = 0
                core_total = 0.0
                core_square_total = 0.0
                mem_total = 0.0
                mem_square_total = 0.0
                core_min = sys.float_info.max
                mem_min = sys.float_info.max
                fleets = spot_candidate[_FLEETS_KEY]
                for response in paginator.paginate(
                    InstanceTypes=list(fleets.keys())
                ):
                    for instance_type_data in response['InstanceTypes']:
                        weight = len(
                            fleets[instance_type_data['InstanceType']]
                        )
                        count += weight
                        cores = instance_type_data['VCpuInfo']['DefaultVCpus']
                        mem = instance_type_data['MemoryInfo']['SizeInMiB']
                        core_total += weight * cores
                        core_square_total += weight * cores * cores
                        mem_total += weight * mem
                        mem_square_total += weight * mem * mem
                        core_min = min(cores, core_min)
                        mem_min = min(mem, mem_min)
                        mem_core_ratio = mem / cores
                        mem_core_ratio_total += weight * mem_core_ratio
                        mem_core_ratio_square_total \
                            += weight * mem_core_ratio * mem_core_ratio
                if not quality(count, core_total, core_square_total,
                               _COV_LEVEL):
                    print(f"[warning]: cores for {group}/{candidate} have a "
                          "large variance")
                if not quality(count, mem_total, mem_square_total, _COV_LEVEL):
                    print(f"[warning]: memories for {group}/{candidate} have "
                          "a large variance")
                spot_candidate[_RESOURCES_KEY].update(
                    {
                        _AVG_CORES_KEY: core_total / count,
                        _AVG_MEM_KEY: mem_total / count,
                        _MIN_CORES_KEY: core_min,
                        _MIN_MEM_KEY: mem_min
                    }
                )
                spot_fleet_count += count
            if not quality(spot_fleet_count, mem_core_ratio_total,
                           mem_core_ratio_square_total, _COV_LEVEL):
                print(f"[warning]: memory/core ratios for {group} have a "
                      "large variance")
            candidate_record[_AVG_MEM_CORE_RATIO_KEY] \
                = mem_core_ratio_total / spot_fleet_count

    def _save_candidates(self, candidates, timestamp):
        group_list = []
        results = {
            REGION_KEY: self.client.meta.region_name,
            META_DATA_KEY: {
                TIMESTAMP_KEY: timestamp.isoformat(),
                DURATION_KEY: self.getarg(_DURATION_OPT),
                MINPOOL_KEY: self.getarg(_MINPOOL_OPT)
            },
            GROUPS_KEY: group_list
        }
        for spot_fleet, candidate_record in candidates.items():
            candidate_list = []
            group_list.append(
                {
                    GROUP_NAME_KEY: spot_fleet,
                    MEM_CORE_RATIO_KEY: candidate_record[
                        _AVG_MEM_CORE_RATIO_KEY
                    ] / _MB_PER_GB,
                    CANDIDATES_KEY: candidate_list
                }
            )
            for candidate, fleet_candidates in candidate_record[
                _SPOT_FLEETS_KEY
            ].items():
                resources = fleet_candidates[_RESOURCES_KEY]
                pool_list = []
                candidate_list.append(
                    {
                        CANDIDATE_NAME_KEY: candidate,
                        PRICE_KEY: fleet_candidates[_PRICE_KEY],
                        RESOURCES_KEY: {
                            AVG_CORES_KEY: resources[_AVG_CORES_KEY],
                            AVG_MEMORY_KEY: resources[_AVG_MEM_KEY]
                                            / _MB_PER_GB,
                            MIN_CORES_KEY: resources[_MIN_CORES_KEY],
                            MIN_MEMORY_KEY: resources[_MIN_MEM_KEY]
                                            / _MB_PER_GB
                        },
                        CANDIDATE_POOLS_KEY: pool_list
                    }
                )
                for instance_type, instance_type_stats in fleet_candidates[
                    _FLEETS_KEY
                ].items():
                    pool_list.append(
                        {
                            INSTANCE_TYPE_KEY: instance_type,
                            AVAILABILITY_ZONES_KEY: list(
                                instance_type_stats.keys()
                            )
                        }
                    )
        save_candidates(self.getarg(_CANDIDATES_ARG), results)
        return results

    @staticmethod
    def _display_results(results):
        print()
        print(f"{REGION_KEY}: {results[REGION_KEY]}")
        print(f"{META_DATA_KEY}:")
        print(f"  {TIMESTAMP_KEY}: {results[META_DATA_KEY][TIMESTAMP_KEY]}")
        print(f"  {DURATION_KEY}: {results[META_DATA_KEY][DURATION_KEY]} days")
        print(f"  {MINPOOL_KEY}: {results[META_DATA_KEY][MINPOOL_KEY]}")
        for group in results[GROUPS_KEY]:
            print()
            print(f"group: {group[GROUP_NAME_KEY]}")
            table = [
                [
                    c[CANDIDATE_NAME_KEY],
                    c[PRICE_KEY],
                    '\n'.join(
                        p[INSTANCE_TYPE_KEY] for p in c[CANDIDATE_POOLS_KEY]
                    ),
                    '\n'.join(
                        ','.join(p[AVAILABILITY_ZONES_KEY])
                        for p in c[CANDIDATE_POOLS_KEY]
                    )
                ]
                for c in group[CANDIDATES_KEY]
            ]
            print(tabulate.tabulate(table, headers=_TABLE_HEADER,
                                    tablefmt=_TABLE_FORMAT,
                                    floatfmt=_TABLE_FLOAT_FORMAT))
