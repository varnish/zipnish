module.exports = function (grunt) {

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		clean: {
			bootstrap: ['ui/app/static/css/bootstrap.css']
		},

		sass: {
			dist: {
				options: {
					style: 'expanded'
				},
				files: {
					'ui/app/static/css/bootstrap.css': 'scss/bootstrap.scss'
				}
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');

};