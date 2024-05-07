from django_cron import CronJobBase, Schedule
import docker
from cabinet.models import ContainerStats, Container
from datetime import datetime
from django.utils import timezone


class StatsCronJob(CronJobBase):
    RUN_EVERY_MINS = 5  # каждый час - 60 !!!!!

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cabinet.get_stats'  # уникальный код для вашей задачи

    def do(self):
        try:
            # функция записи статистики, которую нужно вызывать каждый час
            client = docker.from_env()
            containers = Container.objects.all()
            # для всех запущенных контейнеров собираем статистику
            for db_container in containers:
                container = client.containers.get(db_container.id)

                if container.status == 'exited':
                    new_record = ContainerStats.objects.create(
                        container=db_container,
                        time=timezone.now(),
                        cpu=0,
                        ram=0,
                        disk=0,
                    )
                    new_record.save()
                    continue

                # stats
                stats = container.stats(stream=False)
                name = stats['name']  # 'name': '/UbuntuContainer',
                cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
                system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
                number_of_cores = stats['cpu_stats']['online_cpus']
                cpu_percent = (cpu_delta / system_delta) * number_of_cores * 100.0
                time = stats['read']  # 'read': '2024-05-06T10:12:00.461046383Z'
                date_string, microseconds_string = time.split('.')
                # Only keep the first 6 digits of the microseconds
                microseconds_string = microseconds_string[:6]
                # Combine them back
                adjusted_date_string = f"{date_string}.{microseconds_string}Z"
                # Now parse the string with the adjusted format
                your_datetime = datetime.strptime(adjusted_date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
                # your_datetime = timezone.make_aware(your_datetime, timezone.utc)
                memory_usage = stats['memory_stats']['usage']  # 'usage': 897024
                # storage_stats = stats['storage_stats']['']  # legacy
                # create a new record to bd
                new_record = ContainerStats.objects.create(
                    container=db_container,
                    time=your_datetime,
                    cpu=cpu_percent,
                    ram=memory_usage/1024/1024,
                    disk=0,
                    # disk=storage_stats
                )
                # Ssave the object
                new_record.save()
        except Exception as e:
            print(e)

# stats
# {'read': '2024-05-06T10:12:00.461046383Z',
# 'preread': '2024-05-06T10:11:59.444891153Z',
# 'pids_stats': {'current': 1},
# 'blkio_stats': {'io_service_bytes_recursive': [],
#    'io_serviced_recursive': [],
#    'io_queue_recursive': [],
#    'io_service_time_recursive': [],
#    'io_wait_time_recursive': [],
#    'io_merged_recursive': [],
#    'io_time_recursive': [],
#   'sectors_recursive': []},
# 'num_procs': 0,
# 'storage_stats': {},
# 'cpu_stats':
#    {'cpu_usage':
#          {'total_usage': 243855100,
#           'percpu_usage': [2406400, 5288400, 21822800, 2022600, 390800, 0, 168033900, 43890200],
#           'usage_in_kernelmode': 60000000, 'usage_in_usermode': 50000000},
#      'system_cpu_usage': 138865330000000,
#      'online_cpus': 8,
#      'throttling_data': {'periods': 0, 'throttled_periods': 0, 'throttled_time': 0}
#      },
# 'precpu_stats':
#     {'cpu_usage':
#          {'total_usage': 243855100,
#           'percpu_usage': [2406400, 5288400, 21822800, 2022600, 390800, 0, 168033900, 43890200],
#           'usage_in_kernelmode': 60000000,
#           'usage_in_usermode': 50000000},
#      'system_cpu_usage': 138857210000000,
#      'online_cpus': 8,
#      'throttling_data': {'periods': 0, 'throttled_periods': 0, 'throttled_time': 0}
#    },
# 'memory_stats':
#     {'usage': 897024,
#      'max_usage': 6537216,
#      'stats':
#          {'active_anon': 4096,
#           'active_file': 0,
#           'cache': 0,
#           'dirty': 0,
#           'hierarchical_memory_limit': 9223372036854771712,
#           'hierarchical_memsw_limit': 9223372036854771712,
#           'inactive_anon': 593920,
#           'inactive_file': 0,
#           'mapped_file': 0,
#           'pgfault': 1309,
#           'pgmajfault': 0,
#           'pgpgin': 847,
#           'pgpgout': 701,
#           'rss': 598016,
#           'rss_huge': 0,
#           'total_active_anon': 4096,
#           'total_active_file': 0,
#           'total_cache': 0,
#           'total_dirty': 0,
#           'total_inactive_anon': 593920,
#           'total_inactive_file': 0,
#           'total_mapped_file': 0,
#           'total_pgfault': 1309,
#           'total_pgmajfault': 0,
#           'total_pgpgin': 847,
#           'total_pgpgout': 701,
#           'total_rss': 598016,
#           'total_rss_huge': 0,
#           'total_unevictable': 0,
#           'total_writeback': 0,
#           'unevictable': 0,
#           'writeback': 0
#          },
#          'limit': 3593285632
#      },
#      'name': '/UbubtuContainer',
#      'id': '0407e65c2ea1a2d5dff1f14d5bb08b868c178e88cb8de912b5ce65bcb35a2342',
#      'networks':
#            {'eth0':
#                 {'rx_bytes': 2092,
#                  'rx_packets': 26,
#                  'rx_errors': 0,
#                  'rx_dropped': 0,
#                  'tx_bytes': 936,
#                  'tx_packets': 12,
#                  'tx_errors': 0,
#                  'tx_dropped': 0
#               }
#             }
# }
