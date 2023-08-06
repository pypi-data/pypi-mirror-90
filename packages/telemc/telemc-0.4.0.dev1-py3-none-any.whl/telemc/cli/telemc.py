import argparse
import os

import redis

from telemc import TelemetryController
from telemc.telemc import NodeInfo, TelemetrySubscriber


class CLI:
    ctrl: TelemetryController

    def __init__(self, ctrl) -> None:
        super().__init__()
        self.ctrl = ctrl

    def list(self, args):
        for node in self.ctrl.get_nodes():
            print(node)

    def info(self, args):
        if args.node_id:
            info = self.ctrl.get_node_info(args.node_id)
            if not info:
                print("no such node '%s'" % args.node_id)
            else:
                self._print_info(info)
        else:
            for info in self.ctrl.get_node_infos():
                self._print_info(info)

    @staticmethod
    def _print_info(node_info: NodeInfo):
        print(node_info.node)
        for k, v in node_info.data.items():
            print('%-10s %s' % (k, v))

    def pause(self, args):
        if args.node_id:
            self.ctrl.pause(args.node_id)
        else:
            self.ctrl.pause_all()

    def unpause(self, args):
        if args.node_id:
            self.ctrl.unpause(args.node_id)
        else:
            self.ctrl.unpause_all()

    def follow(self, args):
        try:
            with TelemetrySubscriber(self.ctrl.rds) as sub:
                for t in sub:
                    print(t)
        except KeyboardInterrupt:
            return


def main():
    parser = argparse.ArgumentParser(prog='telemc')
    parser.add_argument('--redis-host', help='redis host', type=str,
                        default=os.getenv('telemc_redis_host', 'localhost'))
    parser.add_argument('--redis-port', help='redis port', type=int,
                        default=int(os.getenv('telemc_redis_port', 6379)))

    subparsers = parser.add_subparsers(dest='command', help='telemc command')
    subparsers.required = True

    # commands
    subparsers.add_parser('list', help='list nodes')

    cmd_info = subparsers.add_parser('info', help='show node info')
    cmd_info.add_argument('--node-id', help='the id of the node to look up')

    cmd_pause = subparsers.add_parser('pause', help='pause telemetry reporting')
    cmd_pause.add_argument('--node-id', help='the id of the node to pause')

    cmd_unpause = subparsers.add_parser('unpause', help='start telemetry reporting')
    cmd_unpause.add_argument('--node-id', help='the id of the node to unpause')

    subparsers.add_parser('follow', help='subscribe to the telemetry data')

    # parse
    args = parser.parse_args()

    # app context
    rds = redis.Redis(host=args.redis_host, port=args.redis_port, decode_responses=True)
    cli = CLI(TelemetryController(rds))

    # dispatch
    getattr(cli, args.command)(args)


if __name__ == '__main__':
    main()
