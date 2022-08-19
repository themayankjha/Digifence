FROM ubuntu:latest

RUN apt update

RUN apt install  openssh-server sudo python2 python-pip python2-dev git -y

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test 

RUN usermod -aG sudo test

RUN service ssh start

RUN git clone https://github.com/volatilityfoundation/volatility.git

RUN pip2 install pycrypto

RUN pip2 install distorm3

RUN  echo 'test:test' | chpasswd

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]
