## 用法示例

- 扫描单个主机的指定端口：
```bash
python portscan_v3.py -i 192.168.0.1 -p 80
```
- 扫描单个主机的端口范围：
```
```bash
python portscan_v3.py -i 192.168.0.1 -p 1-100
```
- 扫描多个主机的指定端口：
```bash
python portscan_v3.py -i hosts.txt -p 80
```
- 扫描多个主机的不同端口：
```bash
python portscan_v3.py -i hosts.txt -p 80,443,8080
```
- 保存扫描结果到自定义文件：
```bash
python portscan_v3.py -i 192.168.0.1 -p 80 -o scan_results.csv
```
- 使用多线程进行扫描（默认为200个线程）：
```bash
python portscan_v3.py -i 192.168.0.1 -p 80 -t 200
```