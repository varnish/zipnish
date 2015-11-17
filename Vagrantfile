Vagrant.configure(2) do |config|
	config.ssh.insert_key = false
	config.vm.box = 'ubuntu/vivid64'

	# user interface
	config.vm.define 'userinterface' do |userinterface|
		userinterface.vm.hostname = 'userinterface'
		userinterface.vm.network :private_network, ip: '192.168.75.11'
	end

	# database
	config.vm.define 'database' do |database|
		database.vm.hostname = 'database'
		database.vm.network :private_network, ip: '192.168.75.12'
	end

	# varnish cache, log reader
	config.vm.define 'backend' do |backend|
		backend.vm.hostname = 'backend'
		backend.vm.network :private_network, ip: '192.168.75.13'
	end

	# example application
	config.vm.define 'exampleapp' do |exampleapp|
		exampleapp.vm.hostname = 'exampleapp'
		exampleapp.vm.network :private_network, ip: '192.168.75.14'
	end

	# package building machines

	# ubuntu-vivid 64-bit (15.x)
	config.vm.define 'build-ubuntu-vivid64' do |ubuntu|
		ubuntu.vm.box = 'ubuntu/vivid64'
		ubuntu.vm.hostname = 'build-ubuntu-vivid64'
		ubuntu.vm.network :private_network, ip: '192.168.75.41'
	end
end
