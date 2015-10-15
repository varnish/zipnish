Vagrant.configure(2) do |config|

	config.ssh.insert_key = false

	# user interface
	config.vm.define "ui" do |ui|
		ui.vm.box = "ubuntu/vivid64"
		ui.vm.network "private_network", ip: "192.168.33.11"
	end

	# mysql database
	config.vm.define "db" do |db|
		db.vm.box = "ubuntu/vivid64"
		db.vm.network "private_network", ip: "192.168.33.12"
	end

	# log reader + varnish
	config.vm.define "backend" do |backend|
		backend.vm.box = "ubuntu/vivid64"
		backend.vm.network "private_network", ip: "192.168.33.13"
	end

	# example application
	config.vm.define "exampleapp" do |app|
		app.vm.box = "ubuntu/vivid64"
		app.vm.network "private_network", ip: "192.168.33.14"
	end

end
