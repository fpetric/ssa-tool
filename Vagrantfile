# This Vagrantfile produces a working environment based on Python 3.6.

Vagrant::DEFAULT_SERVER_URL.replace('https://vagrantcloud.com')

$script = <<-SCRIPT
apt update && apt install python3-pip -y

git clone https://github.com/networkx/networkx.git
pushd .
cd networkx/ && git checkout networkx-2.2 && pip3 install -e .
popd

pushd .
git clone https://github.com/vermiculus/ssa-tool.git
cd ssa-tool/ && chown -R vagrant .
popd
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell", inline: $script
end
