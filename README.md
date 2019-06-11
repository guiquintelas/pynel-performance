# Pynel Performance

Control panel for remote graphical resource monitoring. Created with clint-server architecture, enabling multiples clients
to connect with the same server via sockets.


Usage (Server)
---
```
git clone https://github.com/guiquintelas/pynel-performance.git
cd pynel-performance
pip install pygame
pip install py-cpuinfo
pip install psutil
python -m server.main
```

Usage (Client)
---
```
git clone https://github.com/guiquintelas/pynel-performance.git
cd pynel-performance
pip install pygame
pip install py-cpuinfo
pip install psutil
python -m client.main
```

Controls
---

- **left**: previous view
- **right**: next view
- **space**: toggle general view

Interface
---

- **General View**<br>
![Test Run](https://github.com/guiquintelas/pynel-performance/blob/master/static/geral.png)

- **CPU View**<br>
![Test Run](https://github.com/guiquintelas/pynel-performance/blob/master/static/cpu.png)

- **Hard Drive View**<br>
![Test Run](https://github.com/guiquintelas/pynel-performance/blob/master/static/disco.png)

- **Network View**<br>
![Test Run](https://github.com/guiquintelas/pynel-performance/blob/master/static/rede.png)

- **Processes View**<br>
![Test Run](https://github.com/guiquintelas/pynel-performance/blob/master/static/processos.png)