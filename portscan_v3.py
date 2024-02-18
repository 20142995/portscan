#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import csv
import argparse
import socket
import ipaddress
import asyncio

socket.setdefaulttimeout(15)


def gen_port(port_range):
    ports = []
    for port in port_range.split(','):
        if '-' in port:
            a, b = port.split('-')
            for i in range(int(a), int(b)+1):
                ports.append(str(i))
        else:
            ports.append(port)
    return ports


def gen_ip(ip_range):
    def num2ip(num):
        return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))

    def ip2num(ip):
        ips = [int(x) for x in ip.split('.')]
        return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]

    start, end = [ip2num(x) for x in ip_range.split('-')]
    return [num2ip(num) for num in range(start, end+1) if num & 0xff]


async def scan_port(host_port):
    host, port = host_port.split(':')
    try:
        reader, writer = await asyncio.open_connection(host, int(port))
        writer.write(b'GET / HTTP/1.1\r\n\r\n')
        await writer.drain()
        data = await reader.read(1024)
        writer.close()
        if len(data) > 2:
            return host_port, 'open', str(data)
        else:
            return host_port, 'open', ''
    except:
        return host_port, 'close', ''


async def worker(queue, results):
    while not queue.empty():
        host_port = await queue.get()
        try:
            host_port, state, recv = await scan_port(host_port)
            results.append([host_port, state, recv])
            sys.stdout.write('{}[{}] {}\t{}\t{}\n'.format(
                '\r' if state == 'close' else '', '+' if state == 'open' else '-', host_port, state, recv))
        except:
            pass


async def main():
    parser = argparse.ArgumentParser(description=u'socket tcp portscan')
    parser.add_argument('-i', "--input", dest='hosts',
                        help='targets, IP (192.168.1.1), IP range(192.18.1.1-192.168.1.3), IP/mask(192.18.1.1/24), txt file(xxx.txt), ip:port(192.168.1.1:80)')
    parser.add_argument('-p', "--port", dest='ports', default='21-23,80,443,445,1433,1521,3306,3389,6379,7001,8080,8443',
                        help='ports, default \'21-23,80,443,445,1433,1521,3306,3389,6379,7001,8080,8443\'')
    parser.add_argument('-t', "--thread", dest='threadnum',
                        type=int, default=200, help='threadnum, default 200')
    parser.add_argument('-o', "--output", dest='output',
                        default='results.csv', help='output file, default \'results.csv\'')
    args = parser.parse_args()
    if not args.hosts:
        parser.print_help()
        sys.exit("[*] need -i")
    else:
        if os.path.isfile(args.hosts):
            hosts = [_.strip()
                     for _ in open(args.hosts, 'r', encoding='utf8').readlines()]
        else:
            hosts = [args.hosts]
        queue = asyncio.Queue()
        results = []
        for host in hosts:
            if ':' in host:
                queue.put_nowait(host)
            else:
                if '-' in host:
                    for ip in gen_ip(host):
                        for port in gen_port(args.ports):
                            queue.put_nowait('{}:{}'.format(ip, port))
                elif '/' in host:
                    try:
                        for ip in ipaddress.ip_network(host, strict=False).hosts():
                            for port in gen_port(args.ports):
                                queue.put_nowait('{}:{}'.format(ip, port))
                    except:
                        sys.stdout.write('[*] {}\terror\n'.format(host))
                else:
                    for port in gen_port(args.ports):
                        queue.put_nowait('{}:{}'.format(host, port))
        tasks = [worker(queue, results) for _ in range(args.threadnum)]
        await asyncio.gather(*tasks)

        with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Host:Port', 'State', 'Data'])
            writer.writerows(results)
if __name__ == '__main__':
    asyncio.run(main())
