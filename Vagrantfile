# -*- mode: ruby -*-
# vi: set ft=ruby :

#define base_server
base_server = {
	:box => 'varnish/ubuntu-14.04-amd64',
	:box_url => 'https://images.varnish-software.com/vagrant/ubuntu-14.04-amd64.json',
}

zipnish_servers = [
	{
		:hostname => 'userinterface',
		:ip => '192.168.75.11'
	},
	{
		:hostname => 'database',
		:ip => '192.168.75.12'
	},
	{
		:hostname => 'backend',
		:ip => '192.168.75.13'
	},
	{
		:hostname => 'exampleapp',
		:ip => '192.168.75.14'
	},
	{
		:hostname => 'buildserver',
		:ip => '192.168.75.14'
	}

]

Vagrant.configure("2") do |config|
	zipnish_servers.each do |zipnish|
		config.vm.define zipnish[:hostname] do |zipnish_config|
			zipnish_config.vm.box = base_server[:box]
			zipnish_config.vm.box_url = base_server[:box_url]
			zipnish_config.vm.hostname = zipnish[:hostname]
			zipnish_config.vm.network :private_network, ip: zipnish[:ip]
		end
	end
end
