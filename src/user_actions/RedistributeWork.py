from typing import Dict, List, Set, Tuple, Type
from util.redis_utils import get_network
from worker_actions import WorkerAction
from user_actions import UserAction
from constants import REDIS_WORK_QUEUES_DB, REDIS_WORKER_NETWORK_DB
from uuid import getnode
from random import choice

QUEUE_OPTION = "queue"
PRE_PUSH_OPTION = "pre-push"


class RedistributeWork(UserAction):
	@classmethod
	def command(cls) -> str:
		return "redistribute"

	@classmethod
	def description(cls):
		return "Redistribute work across neighbouring worker nodes"

	def recognised_options(self):
		return set()

	def arg_options(self):
		return set()

	def obligatory_option_groups(self):
		return []

	def blocking_options(self):
		return []
	
	def execute(self) -> None:
		from redis import Redis
		worker_actions: Dict[str, Type[WorkerAction]] = {
			T.queue_name(): T
			for T in WorkerAction.__subclasses__()
		}
		mac_id = getnode()
		network_work_queues: Dict[str, Redis] = {}
		network_lock_queues: Dict[str, Redis] = {}
		the_network = get_network()
		for host in the_network:
			lock_queue = Redis(db=REDIS_WORKER_NETWORK_DB, host=host)
			if lock_queue.set("lock", mac_id, ex=300, nx=True):
				network_lock_queues[host] = lock_queue
				network_work_queues[host] = Redis(
					db=REDIS_WORK_QUEUES_DB,
					host=host,
				)
		modified: Set[str] = set()
		if len(network_work_queues) >= 2:
			total_queue_lengths: Dict[str, int] = {}
			network_queue_lengths: Dict[str, Dict[str, int]] = {}
			for work_queue, TheWorkerAction in worker_actions.items():
				network_queue_lengths[work_queue] = {}
				total_queue_lengths[work_queue] = 0
			for host, connection in network_work_queues.items():
				for work_queue, TheWorkerAction in worker_actions.items():
					if TheWorkerAction.one_at_a_time():
						worker_order_count = connection.hlen(work_queue)
						total_queue_lengths[work_queue] = (
							total_queue_lengths.get(work_queue, 0)
							+ worker_order_count
						)
						network_queue_lengths[work_queue][host] = (
							worker_order_count
						)
			for work_queue, total in total_queue_lengths.items():
				if total > 0:
					queue_lengths = network_queue_lengths[work_queue]
					hosts_with_queue = len(queue_lengths)
					min_orders_per_node = total // hosts_with_queue
					max_orders_per_node = min_orders_per_node + 1
					nodes_with_one_added_order = total % hosts_with_queue
					nodes_with_one_less_order = (
						hosts_with_queue - nodes_with_one_added_order
					)
					for relation, orders in list(queue_lengths.items()):
						if orders == min_orders_per_node:
							if nodes_with_one_less_order:
								nodes_with_one_less_order -= 1
								del queue_lengths[relation]
						elif orders == max_orders_per_node:
							if nodes_with_one_added_order:
								nodes_with_one_added_order -= 1
								del queue_lengths[relation]
					changes_needed: Dict[str, int] = {}
					order_pool: List[Tuple[str, str, str]] = []
					for host, orders in queue_lengths.items():
						if nodes_with_one_added_order:
							changes = max_orders_per_node - orders
							nodes_with_one_added_order -= 1
						elif nodes_with_one_less_order:
							changes = min_orders_per_node - orders
							nodes_with_one_less_order -= 1
						else:
							changes = 0
						if changes > 0:
							changes_needed[host] = changes
						else:
							connection = network_work_queues[host]
							for rj, rm in connection.hscan_iter(
									name=work_queue):
								job = rj.decode()
								metadata = rm.decode()
								connection.hdel(work_queue, job)
								order_pool.append((job, metadata, host))
								changes += 1
								if changes == 0:
									break
							modified.add(host)
					for host, changes in changes_needed.items():
						jobs = {}
						for _ in range(changes):
							job, payload, host = order_pool.pop()
							jobs[job] = payload
						network_work_queues[host].hmset(work_queue, jobs)
						modified.add(host)
		for connection in network_lock_queues.values():
			connection.delete("lock")
		if modified:
			host = choice(list(modified))
			RedistributeWork.run_on_host(host)
