Vagrant.configure(2) do |config|

	config.ssh.insert_key = false

	config.vm.define "ui" do |ui|
		ui.vm.box = "ubuntu/vivid64"
	end

	config.vm.define "db" do |db|
		db.vm.box = "ubuntu/vivid64"
	end

	# log reader + varnish + example rpc-service
	config.vm.define "backend" do |backend|
		backend.vm.box = "ubuntu/vivid64"
	end

end
